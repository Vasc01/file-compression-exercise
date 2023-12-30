"""Test for the BinaryTree class.
Test the creation of the binary tree and codebook separately from the encoding and decoding of the Huffman algorithm.
"""

from core.compression import BinaryTree

binary_tree = BinaryTree()
input_data = "AAA BBB AB  CDDDD CCAA CCAAAAAAAXRRPPLLL  OO"

frequency_dict = binary_tree.create_frequency_dict(input_data)
print("Frequency dictionary k:v character:occurrence")
print(frequency_dict)
print()

binary_tree.create_heap(frequency_dict)
print("Node objects in heap")
print(binary_tree.heap)
print("Most left Node contains element with least occurrence:")
print(binary_tree.heap[0].character)
print()

binary_tree.create_tree()
print("Node objects in heap reduced to one with highest occurrence")
print(binary_tree.heap)
print("Occurrence for the root node:")
print(binary_tree.heap[0].occurrence)
print()

binary_tree.initiate_create_codes()
print("Codebook and reversed codebook:")
print(binary_tree.codebook)
print(binary_tree.reversed_codebook)
