import struct
import heapq
import os
from abc import ABC, abstractmethod


class CompressionABC(ABC):

    @abstractmethod
    def encode(self, data):
        raise NotImplemented

    @abstractmethod
    def decode(self, data):
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

        # reserve 256 for end of code
        dictionary_size += 1

        # stores sequences for entry in the dictionary
        string = ""

        # encoded output in codepoints
        temporary_data_output = []

        # start LZW compression algorithm
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

                else:
                    temporary_data_output.append(256)

                    # Rebuild the dictionary.
                    dictionary_size = 256
                    dictionary = {chr(i): i for i in range(dictionary_size)}
                    # reserve 256 for end of code
                    dictionary_size += 1

                # stores sequences for entry in the dictionary
                string = chr(symbol)

        # Output the code for string.
        if string:
            temporary_data_output.append(dictionary[string])
        # end LZW compression algorithm

        # output for inspection
        print(dictionary)
        print(dictionary_size)
        print(temporary_data_output)

        # integer array to binary
        # compressed_data = struct.pack('>' + 'i' * len(temporary_data_output), *temporary_data_output)
        compressed_data = self.pack(temporary_data_output)

        return compressed_data

    def pack(self, codepoints):
        """Variable bit lengths"""
        tailbits = []
        codesize = 4096

        minwidth = 8
        while (1 << minwidth) < codesize:
            minwidth = minwidth + 1

        nextwidth = minwidth

        for pt in codepoints:

            newbits = self.inttobits(pt, nextwidth)
            tailbits = tailbits + newbits

            codesize = codesize + 1

            if codesize >= (2 ** nextwidth):
                nextwidth = nextwidth + 1

            while len(tailbits) > 8:
                nextbits = tailbits[:8]
                nextbytes = self.bitstobytes(nextbits)
                for bt in nextbytes:
                    yield struct.pack("B", bt)

                tailbits = tailbits[8:]

        if tailbits:
            tail = self.bitstobytes(tailbits)
            for bt in tail:
                yield struct.pack("B", bt)

    def inttobits(self, anint, width=None):

        remains = anint
        retreverse = []
        while remains:
            retreverse.append(remains & 1)
            remains = remains >> 1

        retreverse.reverse()

        ret = retreverse
        if None != width:
            ret_head = [0] * (width - len(ret))
            ret = ret_head + ret

        return ret

    def bitstobytes(self, bits):

        ret = []
        nextbyte = 0
        nextbit = 7
        for bit in bits:
            if bit:
                nextbyte = nextbyte | (1 << nextbit)

            if nextbit:
                nextbit = nextbit - 1
            else:
                ret.append(nextbyte)
                nextbit = 7
                nextbyte = 0

        if nextbit < 7: ret.append(nextbyte)
        return ret

    def decode(self):
        raise NotImplemented


class HuffmanCompression(CompressionABC):
    """Huffman compression and decompression algorithms.

    This class relies on codebook generated from the BinaryTree class.
    It receives input data and a codebook.

    """

    def __init__(self):
        self.codebook = None
        self.reversed_codebook = None

    def set_codebook(self, codebook, reversed_codebook):
        self.codebook = codebook
        self.reversed_codebook = reversed_codebook

    def encode(self, uncompressed_data):
        """Executes sequence of steps/functions for the encoding process
        """
        converted_data = self.convert_to_code(uncompressed_data)
        padded_converted_data = self.pad_converted_data(converted_data)
        mutable_bytes_data = self.create_byte_array(padded_converted_data)
        encoded_data = bytes(mutable_bytes_data)

        return encoded_data

    def decode(self, compressed_data):
        """
        Receives the compressed data (bytes)
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

        # Removes leading and trailing padding bits.
        unpadded_bit_string = self.remove_padding(bit_string)

        # Decoding using the reversed_codebook.
        decompressed_data = self.convert_to_original(unpadded_bit_string)

        return decompressed_data

    def convert_to_code(self, uncompressed_data):
        """Replaces data entries with code from the codebook and returns the converted data
        """
        converted_data = ""
        for entry in uncompressed_data:
            converted_data += self.codebook[entry]
        return converted_data

    def convert_to_original(self, unpadded_bit_string):
        """Converts encoded data to the original using the reversed codebook
        """
        current_code = ""
        decompressed_data = ""

        # Reads bits from the encoded data, when match with the codebook is found the original data is recovered.
        for bit in unpadded_bit_string:
            current_code += bit
            if current_code in self.reversed_codebook:
                data = self.reversed_codebook[current_code]
                decompressed_data += data
                current_code = ""

        return decompressed_data

    @staticmethod
    def pad_converted_data(converted_data):
        """Adds padding to converted data to keep it multiple of 8.
        """
        # Finds the amount of missing bits and adds them at the end as trailing zero.
        extra_padding = 8 - len(converted_data) % 8
        converted_data += "0" * extra_padding

        # Puts information about the padding in form of a full byte in the front of the converted data.
        padding_info = f"{extra_padding:08b}"
        converted_data = padding_info + converted_data

        return converted_data

    @staticmethod
    def remove_padding(bit_string):
        """Removes trailing and leading bits that don't belong to the encoded information.
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
    def create_byte_array(padded_converted_data):
        """String to bytearray
        """
        if len(padded_converted_data) % 8 != 0:
            print("Encoded text not padded properly")
            exit(0)

        # Creates mutable bytes array with 8-bit bytes from the string.
        bytes_data = bytearray()
        for i in range(0, len(padded_converted_data), 8):
            byte = padded_converted_data[i:i + 8]
            bytes_data.append(int(byte, 2))

        return bytes_data


class BinaryTree(object):
    """Creates a Huffman tree and a codebook out of it.

    Used in the HuffmanCompression class.

    """
    def __init__(self):

        # Contains priority queue of nodes with the lowest occurrence values in the front. Managed by heapq.
        self.heap = []
        # k:v characters:code used for compression.
        self.codebook = {}
        # k:v code:characters used for decompression.
        self.reversed_codebook = {}

    @staticmethod
    def create_frequency_dict(input_data):
        """Determines how many times each element from the input data occurred.

        This is the first pass over the complete data. The occurrence determines how far in the front
        of the priority que a node is stored.
        """
        # frequency dict k:v character:occurrence
        frequency = {}
        for character in input_data:
            if character not in frequency:
                frequency[character] = 0
            frequency[character] += 1
        return frequency

    def create_heap(self, frequency):
        """Fills the priority queue with elements.
        Nodes are stored in the priority queue as preparation for the tree creation.
        """
        for key in frequency:
            node = Node(key, frequency[key])

            # Push the value item onto the heap, maintaining the heap invariant.
            heapq.heappush(self.heap, node)

    def create_tree(self):
        """Connect individual nodes.

        For two nodes with the lowest occurrence one parent is created with the sum of their occurrences.
        The process is repeated until one parent/root node is left.
        """

        # In the last loop only two nodes will be left, so all nodes are regarded.
        while len(self.heap) > 1:

            # Takes out of the heap the two nodes with the least occurrence, maintaining the heap invariant..
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
        """Starts the recursion for creation of codes.

        """
        # Creates initial parameters for the recursion.
        root = heapq.heappop(self.heap)
        current_code = ""

        # Calls the recursion.
        self.create_codes(root, current_code)

    def create_codes(self, root, current_code):
        """Generates codes by traversing the entire tree.
        """
        # Recursion end condition:
        # When bottom of the tree is reached - data containing nodes don't have children.
        if root is None:
            return None

        # Activates only if the node is data containing, not only holding occurrence amount.
        if root.character:
            # Used for encoding k:v character:code.
            self.codebook[root.character] = current_code
            # Used for decoding k:v code:character.
            self.reversed_codebook[current_code] = root.character
            return

        # Navigation adds to the code 0 for going to the left child and 1 for going to the right child.
        self.create_codes(root.left_child, current_code + "0")
        self.create_codes(root.right_child, current_code + "1")

    def export(self):
        pass

    def insert(self):
        pass


class Node:
    """Describes nodes used in the BinaryTree.

    Part of the Huffman tree.

    Attributes:

    """
    def __init__(self, character, occurrence):
        self.character = character
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
