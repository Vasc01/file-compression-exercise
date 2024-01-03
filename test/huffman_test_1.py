"""Test of Huffman encoding step by step
"""

from core.compression import HuffmanCompression

input_data = b"AAA BBB AB  CDDDD CCAA CCAAAAAAAXRRPPLLL  OO"
print()
print("Input data:", type(input_data), input_data)
print()

huffman_compression = HuffmanCompression()

# Encoding:

huffman_compression.set_codebook(input_data)

print("Unpadded and padded code in comparison with byte lengths:")
converted_data = huffman_compression.convert_to_code(input_data)
print(converted_data)
padded_converted_data = huffman_compression.pad_converted_data(converted_data)
print("| 1byte|" * 18)
print(padded_converted_data)
print()

bytes_data = huffman_compression.encode_to_bytes(padded_converted_data)
print("Encoded data:", type(bytes_data), bytes_data)
print()

# Decoding:

bit_string = huffman_compression.decode_to_string(bytes_data)
print(bit_string)

unpadded_bit_string = huffman_compression.remove_padding(bit_string)
print(unpadded_bit_string)

decompressed_data = huffman_compression.convert_to_original(unpadded_bit_string)
print("Decoded data:", type(decompressed_data), decompressed_data)
