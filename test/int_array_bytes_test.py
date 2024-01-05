import sys

from sandbox.int_array_to_bytes import *

input_int_array = [1, 32, 66, 260, 3332, 6, 4566, 32, 32, 67, 68, 268, 68, 266, 67, 258, 67, 272,
                   257, 276, 65, 88, 82, 82, 80, 80, 76, 284, 265, 79, 79]

print(input_int_array)
print("Input Array size:", sys.getsizeof(input_int_array))

# compressed_data = int_array_to_bytes(input_int_array)
# print("Compressed data:", compressed_data)
# print(sys.getsizeof(compressed_data))
#
# output_int_array = bytes_to_int_array(compressed_data)
# print("Decompressed data:", output_int_array)
#
# print("Is output array = input array", input_int_array == output_int_array)
