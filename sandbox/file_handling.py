"""Test of Huffman encoding with text file
"""
import os
from core.compression import HuffmanCompression

folder_path = r"/test/example_files"
file_name = r"treasure_island_ch1.txt"
in_file_path = folder_path + "\\" + file_name

out_file_name = file_name.split(".")[0] + "_encoded.bin"
out_file_path = folder_path + "\\" + out_file_name

decompressed_file_name = file_name.split(".")[0] + "_decoded.txt"
decompressed_file_path = folder_path + "\\" + decompressed_file_name

in_file_size = os.stat(in_file_path).st_size
print("Input file size:", in_file_size, "bytes")

in_file = open(in_file_path, 'rb')
uncompressed_data = in_file.read()
print("Input data type:", type(uncompressed_data))
in_file.close()

huffman_compression = HuffmanCompression()

encoded_data = huffman_compression.encode(uncompressed_data)
print(encoded_data)

out_file = open(out_file_path, "wb")
out_file.write(encoded_data)
out_file.close()

out_file_size = os.stat(out_file_path).st_size
print("Output file size:", out_file_size, "bytes")

encoded_file = open(out_file_path, "rb")
compressed_data = encoded_file.read()
print(type(compressed_data))
print(compressed_data)
encoded_file.close()

decompressed_data = huffman_compression.decode(compressed_data)
print(decompressed_data)

decompressed_file = open(decompressed_file_path, "wb")
decompressed_file.write(decompressed_data)
decompressed_file.close()
