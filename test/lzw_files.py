import os
import sys

from core.compression import LZWCompression

folder_path = r"C:\Files X\14_Workspace\1_Projects\file-compression-exercise\test\example_files"
file_name = r"pure_text.txt"
in_file_path = folder_path + "\\" + file_name

out_file_name = file_name.split(".")[0] + "_encoded"
out_file_path = folder_path + "\\" + out_file_name

in_file_size = os.stat(in_file_path).st_size
print()
print("Input file size:", in_file_size, "bytes")

in_file = open(in_file_path, 'rb')
input_data = in_file.read()
print("Input data type:", type(input_data))
print("Input data size: ", sys.getsizeof(input_data), "bytes")
in_file.close()

print()
# print("Input data:", type(input_data), input_data)

lzw_compression = LZWCompression()
compressed_data = lzw_compression.encode(input_data)
# print("Compressed data:", compressed_data)
print("Compressed data size: ", sys.getsizeof(compressed_data), "bytes")
print("Compressed data type: ", type(compressed_data))

decoded_data = lzw_compression.decode(compressed_data)

print("Decompressed data size: ", sys.getsizeof(decoded_data), "bytes")
print("Decompressed data type: ", type(decoded_data))

print("Decompressed data = Initial data:", decoded_data == input_data)
