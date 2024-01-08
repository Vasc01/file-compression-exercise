"""LZW and Huffman compression algorithms.

This module contains the classes of LZW and Huffman compression and the helper classes BinaryTree and Node.
"""

import heapq
from abc import ABC, abstractmethod


class CompressionABC(ABC):
    """A template for creation of compression algorithm.

    The encode and decode methods are required for the interface with the compression algorithms.
    In the implemented LZW and Huffman algorithms they receive bytes-data and return bytes-data.
    """

    @abstractmethod
    def encode(self, data):
        raise NotImplemented

    @abstractmethod
    def decode(self, data):
        raise NotImplemented


class LZWCompression(CompressionABC):
    """LZW compression algorithm.

    This class performs encoding and decoding using LZW algorithm. It is a simplified version without dynamic
    adaptation of the codebook and without its restarting.
    Input and output for the encoding and decoding are bytes.

    Attributes:
        INITIAL_CODEBOOK_SIZE (int): The initial codebook covers all 8-bit possibilities.
        MAXIMUM_CODEBOOK_SIZE (int): The codebook grows until it exhausts all 12-bit possibilities.
        codebook_size (None/int): Tracks the current codebook size.
        codebook (None/dict): Contains the codebook used by the algorithm.
        bit_size (None/int): Contains the maximum needed bits amount for bit-packing of the code array.
    """

    INITIAL_CODEBOOK_SIZE = 256
    MAXIMUM_CODEBOOK_SIZE = 4096

    def __init__(self):
        """Initiates an instance of the LZW algorithm."""

        self.codebook_size = None
        self.codebook = None
        self.bit_size = None

    def encode(self, uncompressed_data: bytes):
        """Will compress bytes input to bytes output.

        Encode and decode are the main methods of the compression algorithm. They make use of the other methods
        in the class to perform their function step by step.

        Args:
            uncompressed_data (bytes): Data to be compressed.

        Returns:
            compressed_code (bytes): Compressed data.
        """

        # Builds the initial codebook.
        self.create_codebook()

        # A list of integers(codes) is created. The integers are references to content in the codebook.
        code_array = self.create_code(uncompressed_data=uncompressed_data)

        # Bit-packing on the code array reduces its size.
        self.calculate_max_bit_size(code_array=code_array)
        compressed_code = self.compress_code(code_array=code_array, bit_size=self.bit_size)

        return compressed_code

    def create_codebook(self):
        """Initiation of the base codebook.

        A codebook with all 8-bit possibilities is created and saved in the instance attribute self.codebook.
        The codebook is used and potentially extended in the method self.create_code().
        """

        self.codebook_size = self.INITIAL_CODEBOOK_SIZE
        # k:v str:int
        self.codebook = {chr(i): i for i in range(self.codebook_size)}

    def create_code(self, uncompressed_data: bytes):
        """Main encoding algorithm.

        This method navigates through the initial data, develops further the initial codebook and
        generates an array of codes referring to the codebook.

        Args:
            uncompressed_data (bytes): Data to encode. It will be compared with existing codebook entries.

        Returns:
            code_array (list): Codes pointing to original uncompressed data in the codebook.
        """

        # Stores sequences of one or more symbols for entry in the codebook.
        string = ""

        # Encoded output in codepoints - integer array of codes.
        code_array = []

        # Start of LZW compression algorithm.
        for symbol in uncompressed_data:                # Symbol is still a byte here.
            string_and_symbol = string + chr(symbol)    # Here byte data turns into str.

            if string_and_symbol in self.codebook:
                string = string_and_symbol

            else:
                # Output the stored sequence to the codes array.
                code_array.append(self.codebook[string])

                # Adds string_and_symbol to the codebook.
                if len(self.codebook) < self.MAXIMUM_CODEBOOK_SIZE:
                    self.codebook[string_and_symbol] = self.codebook_size
                    self.codebook_size += 1

                # Stores sequences of one or more symbols for entry in the codebook.
                string = chr(symbol)

        # Output the code for string.
        if string:
            code_array.append(self.codebook[string])

        return code_array

    def calculate_max_bit_size(self, code_array: list):
        """Calculates the maximum bit size for the largest number in the code array.

        The bit size is used from self.compress_code() and self.decompress_code() for bit-packing and unpacking
        of the code array.

        Args:
            code_array (list): Codes pointing to original uncompressed data in the codebook.
        """
        self.bit_size = max(code_array).bit_length()

    @staticmethod
    def compress_code(code_array: list, bit_size: int):
        """Uses bit-packing to reduce the size of the code array.

        Args:
            code_array (list): Codes pointing to original uncompressed data in the codebook.
            bit_size (int): Maximum bit size for the largest number in the code array.

            Returns:
                compressed_code (bytes): The integer code array in bit-packed form.
        """
        # Number of bytes needed for each integer.
        byte_size = (bit_size + 7) // 8

        compressed_code = bytearray()

        # Each integer from the code array is represented as array of bytes and added to a single variable.
        for i in code_array:
            i_bytes = int(i).to_bytes(byte_size, 'little', signed=True)
            compressed_code.extend(i_bytes)

        return bytes(compressed_code)

    def decode(self, compressed_data: bytes):
        """Will decompress bytes input to bytes output.

        Decode and encode are the main methods of the compression algorithm. They make use of the other methods
        in the class to perform their function step by step.

        Args:
            compressed_data (bytes): The integer code array in bit-packed form.

        Returns:
            decompressed_data (bytes): Data identical to the original before compression.
        """

        # Compressed data in form of bytes is turned into code array.
        code_array = self.decompress_code(compressed_code=compressed_data, bit_size=self.bit_size)

        # Builds the initial codebook for decoding.
        self.create_reversed_codebook()

        # A list of integers(codes) is used to retrieve the original information from the codebook.
        decompressed_data = self.recover_data(code_array=code_array)

        return decompressed_data

    @staticmethod
    def decompress_code(compressed_code: bytes, bit_size: int):
        """Uses bit-unpacking to recreate the original code array from bytes.

        Args:
            compressed_code (bytes): The integer code array in bit-packed form.
            bit_size (int): Maximum bit size for the largest number in the code array.

        Returns:
            code_array (list): Codes pointing to original uncompressed data in the codebook.
        """
        # Number of bytes used for each integer
        byte_size = (bit_size + 7) // 8

        code_array = []

        # An integer is created from bytes and added to a recreated code array.
        for i in range(0, len(compressed_code), byte_size):
            i_bytes = compressed_code[i:i + byte_size]
            code_array.append(int.from_bytes(i_bytes, 'little', signed=True))

        return code_array

    def create_reversed_codebook(self):
        """Initiation of the base codebook for decompression.

        A codebook with all 8-bit possibilities is created and saved in the instance attribute self.codebook.
        The codebook is used and potentially extended in the method self.recover_data().
        """

        self.codebook_size = self.INITIAL_CODEBOOK_SIZE
        # k:v int:str
        self.codebook = {i: chr(i) for i in range(self.codebook_size)}

    def recover_data(self, code_array: list):
        """Main decoding algorithm.

        Obtains the data identical to the original before compression using the codebook.
        This method navigates through the encoded data, develops further the initial decompression codebook and
        generates the original data from it.

        Args:
            code_array (list): Codes pointing to original uncompressed data in the codebook.

        Returns:
            decompressed_data (bytes): Data identical to the original before compression.
        """

        # Start of LZW decoding algorithm.
        w = result = chr(code_array.pop(0))

        for code in code_array:

            if code in self.codebook:
                # entry becomes the stored str in this int-code
                entry = self.codebook[code]
            elif code == self.codebook_size:
                entry = w + w[0]
            else:
                raise ValueError(f'Poorly compressed code: {code}')

            result += entry

            if self.codebook_size < self.MAXIMUM_CODEBOOK_SIZE:

                # Add w+entry[0] to the codebook.
                self.codebook[self.codebook_size] = w + entry[0]
                self.codebook_size += 1

            w = entry

        # Turns string into bytes before return.
        decompressed_data = bytes(result, 'utf-8')

        return decompressed_data


class HuffmanCompression(CompressionABC):
    """Huffman compression algorithms.

    This class performs encoding and decoding using Huffman algorithm.
    Input and output for the encoding and decoding are bytes.
    This class relies on codebook generated from the BinaryTree class.

    Attributes:
        codebook (dict): Contains the codebook used by the algorithm.
    """

    def __init__(self):
        """Initiates an instance of the Huffman algorithm."""

        # k:v data(int):code(str)
        self.codebook = None

    def set_codebook(self, uncompressed_data: bytes):
        """Calls the codebook creation.

        The algorithm relies on an initial pass through the uncompressed data to generate an optimal codebook.

        Args:
            uncompressed_data (bytes): Data to be compressed.
        """

        binary_tree = BinaryTree()
        self.codebook = binary_tree.create_codebook(uncompressed_data=uncompressed_data)

    def encode(self, uncompressed_data: bytes, codebook=None):
        """Will compress bytes input to bytes output.

        Encode and decode are the main methods of the compression algorithm. They make use of the other methods
        in the class to perform their function step by step.

        Args:
            uncompressed_data (bytes): Data to be compressed.
            codebook (None/dict): An option to add custom codebook instead of generating one automatically.

        Returns:
            encoded_data (bytes): Compressed data.
        """

        # If no specific codebook is passed, standard codebook will be created.
        if codebook:
            self.codebook = codebook
        else:
            self.set_codebook(uncompressed_data=uncompressed_data)

        # Replaces data entries with code from the codebook.
        converted_data = self.convert_to_code(uncompressed_data=uncompressed_data)

        # Adds bits to the encoded data to keep it in 8-bit byte format.
        padded_converted_data = self.pad_converted_data(converted_data=converted_data)

        # Data is converted from string to bytes.
        encoded_data = self.encode_to_bytes(padded_converted_data=padded_converted_data)

        return encoded_data

    def decode(self, compressed_data: bytes, codebook=None):
        """Will decompress bytes input to bytes output.

        Decide and encode are the main methods of the compression algorithm. They make use of the other methods
        in the class to perform their function step by step.

        Args:
            compressed_data (bytes): Data to be decoded.
            codebook (None/dict): An option to add custom codebook instead of using the saved one.

        Returns:
            decompressed_data (bytes): Data identical to the original before compression.
        """
        # If no specific codebook is passed, created codebook will be used.
        if codebook:
            self.codebook = codebook

        # Data is converted from bytes to string of bits.
        bit_string = self.decode_to_string(compressed_data=compressed_data)

        # Removes leading and trailing padding bits.
        unpadded_bit_string = self.remove_padding(bit_string=bit_string)

        # Decoding using the reversed_codebook.
        decompressed_data = self.convert_to_original(unpadded_bit_string=unpadded_bit_string)

        return decompressed_data

    def convert_to_code(self, uncompressed_data: bytes):
        """Replaces data entries with code from the codebook

        Args:
            uncompressed_data (bytes): Data to be converted to code.

        Returns:
            converted_data (str): String of codes(bits).
        """

        converted_data = ""

        for entry in uncompressed_data:
            converted_data += self.codebook[entry]

        return converted_data

    def convert_to_original(self, unpadded_bit_string: str):
        """Converts encoded data to the original using the reversed codebook.

        Args:
            unpadded_bit_string (str): String of codes(bits).

        Returns:
            decompressed_data (bytes): Data identical to the original before compression.
        """
        current_code = ""
        decoded_bytes = bytearray()
        reversed_codebook = {v: k for k, v in self.codebook.items()}

        # Reads bits from the encoded data, when match with the codebook is found the original data is recovered.
        for bit in unpadded_bit_string:
            current_code += bit
            if current_code in reversed_codebook:
                data = reversed_codebook[current_code]
                decoded_bytes.append(data)
                current_code = ""

        decompressed_data = bytes(decoded_bytes)

        return decompressed_data

    @staticmethod
    def pad_converted_data(converted_data: str):
        """Adds padding to converted data to keep it multiple of 8.

        Args:
            converted_data (str): String of codes(bits).

        Returns:
            padded_converted_data (str): String of codes(bits) with padding on both ends.
        """
        # Finds the amount of missing bits and adds them at the end as trailing zero.
        extra_padding = 8 - len(converted_data) % 8
        converted_data += "0" * extra_padding

        # Puts information about the padding in form of a full byte in the front of the converted data.
        padding_info = f"{extra_padding:08b}"
        converted_data = padding_info + converted_data

        return converted_data

    @staticmethod
    def remove_padding(bit_string: str):
        """Removes trailing and leading bits that don't belong to the encoded information.

        Args:
            bit_string (str): String of codes(bits) with padding on both ends.

        Returns:
            unpadded_bit_string (str): String of codes(bits).
        """
        # The leading byte contains information about the trailing padding.
        padding_info = bit_string[:8]

        # Amount of trailing padding bits.
        extra_padding = int(padding_info, 2)

        # Removes leading and trailing padding bits.
        bit_string = bit_string[8:]
        unpadded_bit_string = bit_string[:-1 * extra_padding]

        return unpadded_bit_string

    @staticmethod
    def encode_to_bytes(padded_converted_data: str):
        """Converts string of bits to bytes.

        Args:
            padded_converted_data (str): String of codes(bits) with padding on both ends.

        Returns:
            encoded_data (bytes): Compressed data, output of the encoding.
        """
        if len(padded_converted_data) % 8 != 0:
            print("Encoded text not padded properly")
            exit(0)

        # Creates mutable bytes array with 8-bit bytes from the string.
        bytes_data = bytearray()
        for i in range(0, len(padded_converted_data), 8):
            byte = padded_converted_data[i:i + 8]
            bytes_data.append(int(byte, 2))

        encoded_data = bytes(bytes_data)

        return encoded_data

    @staticmethod
    def decode_to_string(compressed_data: bytes):
        """Converts bytes to string of bits.

        Args:
            compressed_data (bytes): Compressed data, output of the encoding.

        Returns:
            bit_string (str): String of codes(bits) with padding on both ends.
        """

        bit_string = ""

        # Extracts the bits from the bytes and combines them to a string in bit_string.
        for b in compressed_data:

            # bin(int) is used to convert and obtain an integer value's binary string equivalent.
            # Slice operator omits the prefix "0b" in the string.
            # rjust() does right alignment of the string,
            # while filling the left empty spaces with "0" until total length of 8 is reached.
            bits = bin(b)[2:].rjust(8, '0')
            bit_string += bits

        return bit_string


class BinaryTree(object):
    """Creates a Huffman tree and a codebook out of it.

    It is used in the HuffmanCompression class.

    Attributes:
        heap (list): Contains priority queue of nodes with the lowest occurrence values in the front. Managed by heapq.
        codebook (dict): Codebook with codes generated from the Huffman tree.
    """
    def __init__(self):
        """Initiates an instance of the binary tree."""

        self.heap = []
        # k:v data(int):code(str) used for compression.
        self.codebook = {}

    def create_codebook(self, uncompressed_data: bytes):
        """Based on frequency of occurrence a code is assigned to the original data points.

        This is the first of two passes of the Huffman algorithm over the data.
        This method makes use of the other methods in the class to perform its function step by step.

        Args:
            uncompressed_data (bytes): Data to be converted to code.

        Returns:
            codebook (dict): Codebook with codes generated from the Huffman tree.
        """

        frequency = self.create_frequency_dict(input_data=uncompressed_data)
        self.create_heap(frequency=frequency)
        self.create_tree()
        self.initiate_create_codes()

        return self.codebook

    @staticmethod
    def create_frequency_dict(input_data: bytes):
        """Determines how many times each element from the input data occurred.

        This is the first pass over the complete data. The occurrence determines how far in the front
        of the priority que a node is stored.

        Args:
            input_data (bytes): Data to be converted to code.

        Returns:
            frequency (dict): Contains frequency of occurrence for individual input data points.
        """
        # frequency dict k:v data:occurrence
        # Note: byte is transformed automatically to int when becoming key in the dictionary.

        frequency = {}

        for byte in input_data:
            if byte not in frequency:
                frequency[byte] = 0
            frequency[byte] += 1

        return frequency

    def create_heap(self, frequency: dict):
        """Fills the priority queue with elements.

        Nodes are stored in the priority queue as preparation for the tree creation.

        Args:
            frequency (dict): Contains frequency of occurrence for individual input data points.
        """

        for key in frequency:
            node = Node(key, frequency[key])

            # Push the value item onto the heap, maintaining the heap invariant.
            heapq.heappush(self.heap, node)

    def create_tree(self):
        """Connects individual nodes.

        For two nodes with the lowest occurrence one parent is created with the sum of their occurrences.
        The process is repeated until one parent/root node is left.
        """

        # In the last loop only two nodes will be left, so all nodes are regarded.
        while len(self.heap) > 1:

            # Takes out of the heap the two nodes with the least occurrence, maintaining the heap invariant.
            node_1 = heapq.heappop(self.heap)
            node_2 = heapq.heappop(self.heap)

            # Creates a new node in the tree with occurrence level the sum of its child nodes.
            # This node doesn't have any character info.
            merged = Node(None, node_1.occurrence + node_2.occurrence)
            merged.left_child = node_1
            merged.right_child = node_2

            # Returns the new node in the priority que for further use.
            heapq.heappush(self.heap, merged)
            # The root node:
            # At the end the priority que will have only one node with the largest number of occurrence.

    def initiate_create_codes(self):
        """Starts the recursion for creation of codes."""

        # Creates initial parameters for the recursion.
        root = heapq.heappop(self.heap)
        current_code = ""

        # Calls the recursion.
        self.create_codes(root, current_code)

    def create_codes(self, root, current_code: str):
        """Generates codes by traversing the entire tree.

        Args:
            root (Node): Building block for the Huffman tree.
            current_code (str): Contains the code for individual occurrences/datapoints.
        """
        # Recursion end condition:
        # When bottom of the tree is reached - data containing nodes don't have children.
        if root is None:
            return None

        # Activates only if the node is data containing, not only holding occurrence amount.
        if root.byte:
            # Used for encoding k:v character:code.
            self.codebook[root.byte] = current_code
            return

        # Navigation adds to the code 0 for going to the left child and 1 for going to the right child.
        self.create_codes(root.left_child, current_code + "0")
        self.create_codes(root.right_child, current_code + "1")


class Node(object):
    """Nodes are building blocks of the Huffman tree.

    Node is used in the BinaryTree.

    Attributes:
        byte (None, bytes): Datapoint from the original data.
        occurrence (int): How many times the datapoint appears in the uncompressed data.
        left_child (Node, None): Node lower in the tree structure if any.
        right_child (Node, None): Node lower in the tree structure if any.
    """

    def __init__(self, byte: [None, bytes], occurrence: int):
        """Initiates an instance of the Node."""

        # Note: self.create_frequency_dict changed the byte to an int.
        self.byte = byte
        self.occurrence = occurrence
        self.left_child = None
        self.right_child = None

    # Comparison base is defined for use by the heapq module in the BinaryTree class.
    def __lt__(self, other):
        return self.occurrence < other.occurrence

    def __eq__(self, other):
        if other is None:
            return False
        if not isinstance(other, Node):
            return False
        return self.occurrence == other.occurrence
