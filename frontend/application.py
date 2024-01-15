""" Handles the backend capabilities for demonstration of the functionalities.

Makes use of fire CLI library for input and rich library for output.
"""
import os
from pathlib import Path
import time
import fire
from core.compression import LZWCompression, HuffmanCompression
from data.file_handler import FileHandler
from frontend.rich_output import RichOutput


class Application(object):
    """Creates input-output interface for a human operator.

    Using structured commands the user is able to access encoding and decoding for
    LZW compression and Huffman compression algorithms.
    A new file is created after encoding or decoding and some information about the process is displayed in
    the terminal.

    Attributes:
        file_handler (FileHandler): Handles paths, file names and writing and reading to/from files.
        lzw_compression (LZWCompression): LZW encoding and decoding algorithm.
        huffman_compression (HuffmanCompression): Huffman encoding and decoding algorithm.
        rich_output (RichOutput): Handles structured output to the terminal.
    """

    def __init__(self, file_handler, lzw_compression, huffman_compression, rich_output):
        """Initiates an instance of the Application.

        As the Application class handles the communication with the backend, it works with objects of the
        backend classes.

        Args:
            file_handler (FileHandler): Handles paths, file names and writing and reading to/from files.
            lzw_compression (LZWCompression): LZW encoding and decoding algorithm.
            huffman_compression (HuffmanCompression): Huffman encoding and decoding algorithm.
            rich_output (RichOutput): Handles structured output to the terminal.
        """

        self.file_handler = file_handler
        self.lzw_compression = lzw_compression
        self.huffman_compression = huffman_compression
        self.rich_output = rich_output

    def encode(self, complete_path: str, algorithm: str, new_name=None):
        """Will take file and create encoded version of it.

        Method addressable by the user. It reads from file,
        performs data encoding and writes the result in newly created file.

        Args:
            complete_path (str): Complete path can be absolute path to file or just the file name.
            Files without extension are accepted as well.
            algorithm (str): Used to determine which compression algorithm to use. Choices are "lzw"/"huf"
            new_name (str): Optional new file name for the generated file. File extension is generated automatically
            for the new file. If no new file name is given the original file name is used with new file extension.
        """

        # The given path is split in path to containing folder, file name, file extension.
        path_info = self.file_handler.get_path_info(complete_path)

        file_path = path_info[0]
        file_name = new_name if new_name else path_info[1]
        file_extension = path_info[2]
        file_extension_compressed = "." + algorithm

        # Input file represented as bytes.
        data_for_compression = self.file_handler.get_file_bytes(complete_path)

        # Timestamp for beginning of encoding.
        start = time.time()

        # Holds compressed data and metadata.
        # During execution of the encoding a loading animation is played.
        compressed_data = self.rich_output.execute_with_spinner(self._execute_encoding_algorithm,
                                                                algorithm, data_for_compression, file_extension)
        # Timestamp for end of encoding.
        end = time.time()

        # Creates new file.
        self.file_handler.write_in_file(compressed_data,
                                        file_path,
                                        file_name,
                                        file_extension_compressed)

        # Data for output creation.

        output_header = "LZW" if algorithm == "lzw" else "Huffman"

        # Related to original file.
        original_filename = path_info[1] + file_extension
        original_size = os.stat(complete_path).st_size
        path = file_path if len(file_path) else Path.cwd()

        # Related to new file.
        converted_filename = file_name + file_extension_compressed
        new_file_path = self.file_handler.rebuild_file_path(file_path, file_name, file_extension_compressed)
        new_file_size = os.stat(new_file_path).st_size

        # Statistical calculations.
        compression_rate = original_size / new_file_size
        time_elapsed = end - start

        # Output block as feedback after file creation.
        print()
        self.rich_output.add_rule(f"{output_header} Encoding")

        self.rich_output.add_path(path)
        print()

        self.rich_output.display_output(original_filename,
                                        converted_filename,
                                        f"{original_size:,} Bytes",
                                        f"{new_file_size:,} Bytes",
                                        compression_rate,
                                        f"{time_elapsed:,.2f} s")

        self.rich_output.add_rule()
        print()

    def _execute_encoding_algorithm(self, algorithm: str, data_for_compression: bytes, file_extension: str):
        """Decides which algorithm to use and applies it.

        This is a helper method for the encode-method.

        Args:
            algorithm (str): Compression algorithm to use.
            data_for_compression (bytes): Bytes data from the original file.
            file_extension (str): The file extension is saved with the compressed data for use on the recreated
            decoded file later.

        Returns:
            compressed_data (tuple): Contains the compressed data from the original file, the original file extension
            and additional data needed for decoding.
        """

        if algorithm == "lzw":

            encoded_data = self.lzw_compression.encode(data_for_compression)

            # Needed for decoding.
            bit_size = self.lzw_compression.bit_size

            return bit_size, encoded_data, file_extension

        elif algorithm == "huf":

            encoded_data = self.huffman_compression.encode(data_for_compression)

            # Needed for decoding.
            codebook = self.huffman_compression.codebook

            return codebook, encoded_data, file_extension

    def decode(self, complete_path: str, new_name=None):
        """Will take compressed file and recreate the original version.

        Method addressable by the user. It reads from file,
        performs data decoding and writes the result in newly created file.

        Args:
            complete_path (str): Complete path can be absolute path to file or just the file name.
            new_name (str): Optional new file name for the generated file. File extension is generated automatically
            for the new file. If no new file name is given the original file name is used with new file extension.
        """

        # The given path is split in path to containing folder, file name, file extension.
        path_info = self.file_handler.get_path_info(complete_path)

        file_path = path_info[0]

        # If no name is given by the user the present name is used.
        file_name = new_name if new_name else path_info[1]

        file_extension = path_info[2]

        # Contains decoding information, compressed data, original file extension.
        retrieved_data = self.file_handler.read_from_file(complete_path)

        # The file extension of the original file is red from the compressed data where it was saved.
        file_extension_original = retrieved_data[2]

        # Timestamp for beginning of decoding.
        start = time.time()

        # During execution of the decoding a loading animation is played.
        decompressed_data = self.rich_output.execute_with_spinner(self._execute_decoding_algorithm,
                                                                  retrieved_data,
                                                                  file_extension)

        # Timestamp for end of decoding.
        end = time.time()

        # Recreates original file.
        self.file_handler.recreate_file(decompressed_data,
                                        file_path,
                                        file_name,
                                        file_extension_original)

        # Data for output creation.

        output_header = "LZW" if file_extension == ".lzw" else "Huffman"

        # Related to original file.
        path = file_path if len(file_path) else Path.cwd()
        original_filename = path_info[1] + file_extension
        original_size = os.stat(complete_path).st_size

        # Related to new file.
        converted_filename = file_name + file_extension_original
        new_file_path = self.file_handler.rebuild_file_path(file_path, file_name, file_extension_original)
        new_file_size = os.stat(new_file_path).st_size

        # Statistical calculations.
        compression_rate = 0  # For decoding no data on compression is displayed.
        time_elapsed = end - start

        # Output block as feedback after file creation.
        print()
        self.rich_output.add_rule(f"{output_header} Decoding")

        self.rich_output.add_path(path)
        print()

        self.rich_output.display_output(original_filename,
                                        converted_filename,
                                        f"{original_size:,} Bytes",
                                        f"{new_file_size:,} Bytes",
                                        compression_rate,
                                        f"{time_elapsed:,.2f} s")

        self.rich_output.add_rule()
        print()

    def _execute_decoding_algorithm(self, retrieved_data: tuple, file_extension: str):
        """Decides which algorithm to use and applies it.

        This is a helper method for the decode-method.

        Args:
            retrieved_data (tuple): Contains decoding information, compressed data, original file extension.
            file_extension (str): The file extension of the compressed file points to the algorithm
            to use when decoding it.

        Returns:
            decoded_data (bytes): Contains the decoded data ready to be written in a new file.
        """

        if file_extension == ".lzw":

            self.lzw_compression.bit_size = retrieved_data[0]
            decoded_data = self.lzw_compression.decode(retrieved_data[1])

            return decoded_data

        elif file_extension == ".huf":

            self.huffman_compression.codebook = retrieved_data[0]
            decoded_data = self.huffman_compression.decode(retrieved_data[1])

            return decoded_data

    def print_info(self):
        """Pints an information block about available functionalities.

        A text block with helpful information about the operation of the program will be printed.
        """

        print()
        self.rich_output.add_rule("Info")
        self.rich_output.display_info()
        self.rich_output.add_rule()
        print()


def run():
    """Activation of the frontend.

    All necessary backend objects are created and loaded in the frontend class.
    The frontend methods are mapped to shortcuts and passed to the fire library which makes them directly accessible
    from the terminal.
    """

    # Backend objects.
    file_handler = FileHandler()
    lzw_compression = LZWCompression()
    huffman_compression = HuffmanCompression()
    rich_output = RichOutput()

    # Frontend.
    application = Application(file_handler=file_handler,
                              lzw_compression=lzw_compression,
                              huffman_compression=huffman_compression,
                              rich_output=rich_output)

    # Mapping of methods to commands for their execution in CLI.
    # -h and --help are already taken as part of fire library. Instead -i and -info are used.
    commands = {"-e": application.encode, "--encode": application.encode,
                "-d": application.decode, "--decode": application.decode,
                "-i": application.print_info, "--info": application.print_info}

    # Loads the commands in fire for use in the console.
    fire.Fire(commands)
