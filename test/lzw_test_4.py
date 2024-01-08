import os

from sandbox.lzw_encode_byte_no_restart import LZWCompressionBytesNoRestart



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
in_file.close()




# input_data = b"AAA BBB AB  CDDDD CCAA CCAAAAAAAXRRPPLLL  OO" * 88
print()
# print("Input data:", type(input_data), input_data)

lzw_compression = LZWCompressionBytesNoRestart()
compressed_data = lzw_compression.encode(input_data)
print("Compressed data:", compressed_data)
print("Codebook size:", len(lzw_compression.codebook))
print()
print(lzw_compression.codebook)
print()

decompressed_data = lzw_compression.decode(compressed_data)
# print("Decompressed data:", decompressed_data)
print("Codebook size:", len(lzw_compression.codebook))

print("Len input:", len(input_data))
print("Len decompressed:", len(decompressed_data))
print()
# print(lzw_compression.codebook)
print()

print(input_data == decompressed_data)
