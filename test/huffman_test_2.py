"""Test of Huffman encoding with text file
"""
import os
from core.compression import BinaryTree, HuffmanCompression

folder_path = r"C:\Files X\14_Workspace\1_Projects\file-compression-exercise\test\example_files"
file_name = r"treasure_island_ch1.txt"
in_file_path = folder_path + "\\" + file_name

out_file_name = file_name.split(".")[0] + "_encoded.bin"
out_file_path = folder_path + "\\" + out_file_name

in_file_size = os.stat(in_file_path).st_size
print("Input file size:", in_file_size, "bytes")

in_file = open(in_file_path, 'r+')
uncompressed_data = in_file.read()
print("Input data type:", type(uncompressed_data))
in_file.close()

binary_tree = BinaryTree()
frequency_dict = binary_tree.create_frequency_dict(uncompressed_data)
binary_tree.create_heap(frequency_dict)
binary_tree.create_tree()
binary_tree.initiate_create_codes()
print(binary_tree.codebook)

huffman_compression = HuffmanCompression()
huffman_compression.set_codebook(binary_tree.codebook, binary_tree.reversed_codebook)

encoded_data = huffman_compression.encode(uncompressed_data)
print(encoded_data)

out_file = (open(out_file_path, "wb"))
out_file.write(encoded_data)
out_file.close()

out_file_size = os.stat(out_file_path).st_size
print("Output file size:", out_file_size, "bytes")
