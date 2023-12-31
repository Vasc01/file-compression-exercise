"""Test of Huffman encoding step by step
"""

from core.compression import BinaryTree, HuffmanCompression

input_data = "AAA BBB AB  CDDDD CCAA CCAAAAAAAXRRPPLLL  OO"

binary_tree = BinaryTree()
frequency_dict = binary_tree.create_frequency_dict(input_data)
binary_tree.create_heap(frequency_dict)
binary_tree.create_tree()
binary_tree.initiate_create_codes()
print(binary_tree.codebook)
print(binary_tree.reversed_codebook)

huffman_compression = HuffmanCompression()
huffman_compression.set_codebook(binary_tree.codebook, binary_tree.reversed_codebook)

converted_data = huffman_compression.convert_to_code(input_data)
print(converted_data)

padded_converted_data = huffman_compression.pad_converted_data(converted_data)
print("| 1byte|" * 18)
print(padded_converted_data)

mutable_bytes_data = huffman_compression.create_byte_array(padded_converted_data)
print(mutable_bytes_data)
encoded_data = bytes(mutable_bytes_data)
print(encoded_data)

encoded_data_2 = huffman_compression.encode(input_data)
print(encoded_data_2)
