from core.compression import HuffmanCompression

input_data = b"AAA BBB AB  CDDDD CCAA CCAAAAAAAXRRPPLLL  OO"
print()
print("Input data  :", type(input_data), input_data)
print()

huffman_algorithm = HuffmanCompression()
encoded_data = huffman_algorithm.encode(input_data)
print("Encoded data:", type(encoded_data), encoded_data)
print()

decoded_data = huffman_algorithm.decode(encoded_data)
print("Decoded data:", type(decoded_data), decoded_data)
