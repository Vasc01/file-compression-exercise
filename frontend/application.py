""" Demonstration of the backend capabilities.

Makes use of fire CLI library for input
and rich library for output.
"""
import os
from pathlib import Path

import fire

from core.compression import LZWCompression, HuffmanCompression
from data.file_handler import FileHandler
from frontend.rich_output import RichOutput


class Application(object):

    def __init__(self, file_handler, lzw_compression, huffman_compression, rich_output):
        self.file_handler = file_handler
        self.lzw_compression = lzw_compression
        self.huffman_compression = huffman_compression
        self.rich_output = rich_output

    def encode(self, complete_path: str, algorithm: str, new_name=None):
        # complete path can be absolute path to file or just the file name
        # files without extension are accepted as well

        # path to file, file name, file extension
        path_info = self.file_handler.get_path_info(complete_path)

        file_path = path_info[0]
        file_name = new_name if new_name else path_info[1]
        file_extension = path_info[2]
        file_extension_compressed = "." + algorithm

        # file represented as bytes
        data_for_compression = self.file_handler.get_file_bytes(complete_path)

        # Holds compressed data and metadata.
        compressed_data = self._execute_encoding_algorithm(algorithm, data_for_compression, file_extension)

        # creates new file
        self.file_handler.write_in_file(compressed_data,
                                        file_path,
                                        file_name,
                                        file_extension_compressed)

        # Data for output creation.
        header = "LZW" if algorithm == "lzw" else "Huffman"
        original_filename = path_info[1] + file_extension
        converted_filename = file_name + file_extension_compressed
        original_size = os.stat(complete_path).st_size
        new_file_path = self.file_handler.rebuild_file_path(file_path, file_name, file_extension_compressed)
        new_file_size = os.stat(new_file_path).st_size
        compression_rate = original_size/new_file_size
        path = file_path if len(file_path) else Path.cwd()

        # Output as feedback after file creation.
        print()
        self.rich_output.add_rule(f"{header} Encoding")

        self.rich_output.add_path(path)
        print()

        self.rich_output.add_table(original_filename,
                                   converted_filename,
                                   f"{original_size} Bytes",
                                   f"{new_file_size} Bytes",
                                   compression_rate)

        self.rich_output.add_rule()
        print()

    def _execute_encoding_algorithm(self, algorithm, data_for_compression, file_extension):

        if algorithm == "lzw":

            encoded_data = self.lzw_compression.encode(data_for_compression)
            bit_size = self.lzw_compression.bit_size

            return bit_size, encoded_data, file_extension

        elif algorithm == "huf":

            encoded_data = self.huffman_compression.encode(data_for_compression)
            codebook = self.huffman_compression.codebook

            return codebook, encoded_data, file_extension

    def decode(self, complete_path: str, new_name=None):

        path_info = self.file_handler.get_path_info(complete_path)

        file_path = path_info[0]
        file_name = new_name if new_name else path_info[1]
        file_extension = path_info[2]

        retrieved_data = self.file_handler.read_from_file(complete_path)

        file_extension_original = retrieved_data[2]

        decompressed_data = self._execute_decoding_algorithm(retrieved_data, file_extension)

        # recreates original file
        self.file_handler.recreate_file(decompressed_data,
                                        file_path,
                                        file_name,
                                        file_extension_original)

    def _execute_decoding_algorithm(self, retrieved_data, file_extension):

        if file_extension == ".lzw":

            self.lzw_compression.bit_size = retrieved_data[0]
            decoded_data = self.lzw_compression.decode(retrieved_data[1])

            return decoded_data

        elif file_extension == ".huf":

            self.huffman_compression.codebook = retrieved_data[0]
            decoded_data = self.huffman_compression.decode(retrieved_data[1])

            return decoded_data

    def help(self):
        print()
        self.rich_output.add_rule(f"Help")

        self.rich_output.display_help()
        self.rich_output.add_rule()
        print()


def run():

    file_handler = FileHandler()
    lzw_compression = LZWCompression()
    huffman_compression = HuffmanCompression()
    rich_output = RichOutput()

    fire.Fire(Application(file_handler=file_handler,
                          lzw_compression=lzw_compression,
                          huffman_compression=huffman_compression,
                          rich_output=rich_output))
