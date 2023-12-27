import os

from core.compression import LZWCompression

in_file_path = r"C:\Files X\14_Workspace\1_Projects\file-compression-exercise\test\example_files\bg_flag.jpg"

in_file_size = os.stat(in_file_path).st_size
print("Input file size:", in_file_size, "bytes")

in_file = open(in_file_path, 'rb')
uncompressed_data = in_file.read()
print("Input data type:", type(uncompressed_data))

lzw_compression = LZWCompression()
compressed_data = lzw_compression.encode(uncompressed_data)
print("Output data type:", type(compressed_data))

out_file = (
    open(r"C:\Files X\14_Workspace\1_Projects\file-compression-exercise\test\example_files\bg_flag_encoded",
         "wb")
)
for data in compressed_data:
    out_file.write(data)
out_file.close()

out_file_path = r"C:\Files X\14_Workspace\1_Projects\file-compression-exercise\test\example_files\bg_flag_encoded"
out_file_size = os.stat(out_file_path).st_size
print("Output file size:", out_file_size, "bytes")
