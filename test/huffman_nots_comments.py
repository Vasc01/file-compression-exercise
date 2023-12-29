# Explanation of algorithm https://www.youtube.com/watch?v=_Kl3TtBXxq8
# Explanation of code https://www.youtube.com/watch?v=JCOph23TQTY
# Code https://github.com/bhrigu123/huffman-coding/blob/master/huffman.py
"""
A heap is a binary tree in which each node has a smaller key than its children;
this property is called the heap property or heap invariant.

Huffman tree is used to determine the code for each datapoint
priority queue - leas repeated datapoint first
0 for left and 1 for right paths
no ambiguity in code as no part of encoded information represents other shorter code


COMPRESSION
1 create frequency dictionary
2 create priority que with ?MinHeap?
3 build huffman tree
4 assign codes to characters

5 encode input replacing characters with code
6 add padding when storing if code not multiple of 8
7 8 bit stored padding at the beginning of the bit stream
8 output result to output binary file

DECOMPRESSION
1 read the binary file
2 read padding and remove padding
3 decode the bits - read code and replace with values (mapping must be available)
4 save the decoded data in output file
5 maybe compare with the original data
"""


import heapq
import os


class HuffmanCoding:
    def __init__(self, path):
        self.path = path                                                        # path to file
        self.heap = []
        self.codes = {}
        self.reverse_mapping = {}

    class HeapNode:                                                             # heap is a data structure
        def __init__(self, char, freq):
            self.char = char
            self.freq = freq
            self.left = None                                                    # left child or path
            self.right = None                                                   # right child or path

        # defining comparators less_than and equals
        def __lt__(self, other):
            return self.freq < other.freq

        def __eq__(self, other):
            if other is None:
                return False
            if not isinstance(other, HeapNode):
                return False
            return self.freq == other.freq

    # functions for compression ====================================================================================

    def make_frequency_dict(self, text):                                      # step c1
        frequency = {}                                                        # frequency dict k:v character:occurrence
        for character in text:
            if not character in frequency:
                frequency[character] = 0
            frequency[character] += 1
        return frequency

    def make_heap(self, frequency):                                             # step c2 create priority que
        for key in frequency:
            node = self.HeapNode(key, frequency[key])
            heapq.heappush(self.heap, node)

    def merge_nodes(self):                                                      # step c3 create tree
        while len(self.heap) > 1:
            node1 = heapq.heappop(self.heap)
            node2 = heapq.heappop(self.heap)

            merged = self.HeapNode(None, node1.freq + node2.freq)
            merged.left = node1
            merged.right = node2

            heapq.heappush(self.heap, merged)

    def make_codes_helper(self, root, current_code):
        if root is None:
            return

        if (root.char != None):
            self.codes[root.char] = current_code
            self.reverse_mapping[current_code] = root.char
            return

        self.make_codes_helper(root.left, current_code + "0")
        self.make_codes_helper(root.right, current_code + "1")

    def make_codes(self):                                                   # step c4 assign codes to characters
        root = heapq.heappop(self.heap)
        current_code = ""
        self.make_codes_helper(root, current_code)

    def get_encoded_text(self, text):                             # step c5 encode input replacing characters with code
        encoded_text = ""
        for character in text:
            encoded_text += self.codes[character]
        return encoded_text

    def pad_encoded_text(self, encoded_text):              # step c6 add padding when storing if code not multiple of 8
        extra_padding = 8 - len(encoded_text) % 8
        for i in range(extra_padding):
            encoded_text += "0"

        padded_info = "{0:08b}".format(extra_padding)  # step c7 8 bit stored padding at the beginning of the bit stream
        encoded_text = padded_info + encoded_text
        return encoded_text

    def get_byte_array(self, padded_encoded_text):                          # 8 output result to output binary file
        if (len(padded_encoded_text) % 8 != 0):
            print("Encoded text not padded properly")
            exit(0)

        b = bytearray()
        for i in range(0, len(padded_encoded_text), 8):
            byte = padded_encoded_text[i:i + 8]
            b.append(int(byte, 2))
        return b

    def compress(self):
        filename, file_extension = os.path.splitext(self.path)          # split path for saving result in same location
        output_path = filename + ".bin"                                 # save result as binary file

        with open(self.path, 'r+') as file, open(output_path, 'wb') as output:
            text = file.read()                                          # rad text
            text = text.rstrip()                                        # remove whitespaces

            frequency = self.make_frequency_dict(text)                  # frequency dict k:v character:occurrence
            self.make_heap(frequency)
            self.merge_nodes()
            self.make_codes()

            encoded_text = self.get_encoded_text(text)
            padded_encoded_text = self.pad_encoded_text(encoded_text)

            b = self.get_byte_array(padded_encoded_text)
            output.write(bytes(b))

        print("Compressed")
        return output_path

    # functions for decompression ====================================================================================

    def remove_padding(self, padded_encoded_text):
        padded_info = padded_encoded_text[:8]
        extra_padding = int(padded_info, 2)

        padded_encoded_text = padded_encoded_text[8:]
        encoded_text = padded_encoded_text[:-1 * extra_padding]

        return encoded_text

    def decode_text(self, encoded_text):
        current_code = ""
        decoded_text = ""

        for bit in encoded_text:
            current_code += bit
            if (current_code in self.reverse_mapping):
                character = self.reverse_mapping[current_code]
                decoded_text += character
                current_code = ""

        return decoded_text

    def decompress(self, input_path):
        filename, file_extension = os.path.splitext(self.path)
        output_path = filename + "_decompressed" + ".txt"

        with open(input_path, 'rb') as file, open(output_path, 'w') as output:
            bit_string = ""

            byte = file.read(1)
            while (len(byte) > 0):
                byte = ord(byte)
                bits = bin(byte)[2:].rjust(8, '0')
                bit_string += bits
                byte = file.read(1)

            encoded_text = self.remove_padding(bit_string)

            decompressed_text = self.decode_text(encoded_text)

            output.write(decompressed_text)

        print("Decompressed")
        return output_path