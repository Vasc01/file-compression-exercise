import struct
from abc import ABC, abstractmethod


class CompressionABC(ABC):

    @abstractmethod
    def encode(self, path):
        raise NotImplemented

    @abstractmethod
    def decode(self):
        raise NotImplemented


class LZWCompression(CompressionABC):

    def __init__(self):
        pass

    def encode(self, uncompressed_data: bytes):
        """Compress bytes data"""

        print("LZWCompression starts the encode method")

        # Build the dictionary.
        # Starts with the amount of entries for the identical code
        dictionary_size = 256
        maximum_dictionary_size = 4096
        dictionary = {chr(i): i for i in range(dictionary_size)}

        # stores sequences for entry in the dictionary
        string = ""

        # encoded output
        temporary_data_output = []

        for symbol in uncompressed_data:
            string_and_symbol = string + chr(symbol)

            if string_and_symbol in dictionary:
                string = string_and_symbol

            else:
                # output the stored sequence
                temporary_data_output.append(dictionary[string])

                # Add string_and_symbol to the dictionary.
                if len(dictionary) < maximum_dictionary_size:
                    dictionary[string_and_symbol] = dictionary_size
                    dictionary_size += 1

                # stores sequences for entry in the dictionary
                string = chr(symbol)

        # Output the code for string.
        if string:
            temporary_data_output.append(dictionary[string])

        # output for inspection
        print(dictionary)
        print(dictionary_size)
        print(temporary_data_output)

        # integer array to binary
        compressed_data = struct.pack('>' + 'i' * len(temporary_data_output), *temporary_data_output)

        return compressed_data

    def decode(self):
        raise NotImplemented


class HuffmanCompression(CompressionABC):

    def __init__(self):
        self.binary_tree = None

    def set_binary_tree(self, binary_tree):
        self.binary_tree = binary_tree

    def encode(self, path):
        pass

    def decode(self):
        pass


class BinaryTree(object):

    def create(self):
        pass

    def export(self):
        pass

    def insert(self):
        pass
