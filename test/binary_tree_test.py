"""Test for the BinaryTree class.
Test the creation of the binary tree and codebook separately from the encoding and decoding of the Huffman algorithm.
"""

from core.compression import BinaryTree

binary_tree = BinaryTree()

input_data = b"AAA BBB AB  CDDDD CCAA CCAAAAAAAXRRPPLLL  OO"
print()
print("Input data  :", type(input_data), input_data)
print()

frequency_dict = binary_tree.create_frequency_dict(input_data)
print("Frequency dictionary k:v byte:occurrence")
print("Note: byte is transformed automatically to int when becoming key in the dictionary")
print(frequency_dict)
print()

binary_tree.create_heap(frequency_dict)
print("Node objects in heap:")
print(binary_tree.heap)
print("Most left Node contains the element with the least occurrence:")
print(binary_tree.heap[0].byte)
print()

binary_tree.create_tree()
print("Node objects in heap reduced to one with highest occurrence:")
print(binary_tree.heap)
print("Occurrence for the root node:")
print(binary_tree.heap[0].occurrence)
print()

binary_tree.initiate_create_codes()
print("Codebook:")
print(binary_tree.codebook)
