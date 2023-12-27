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
