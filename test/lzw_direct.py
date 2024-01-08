"""Tests the LZW compression with different input options.

The methods are addressed directly without the use of data handler.
For simplicity only the main methods (encode and decode) of the algorithm are tested here.
The goal is to try testdata with different amount of repetition.
"""
import sys

from core.compression import LZWCompression

data_0 = b"ABCDEFGHIJKLMNOPQRSTUVWXYZ"
data_1 = b"AAA BBB CCC DDD EEE FFF GGG HHH III JJJ KKK LLL MMM NNN OOO PPP QQQ RRR SSS TTT UUU VVV WWW XXX YYY ZZZ"
data_2 = b"AAAAAAAAAAAAAAAAAAAAAAAAAA"
data_3 = b"AAA BBB AB  CDDDD CCAA CCAAAAAAAXRRPPLLL  OO"
data_4 = b"AAA BBB AB  CDDDD CCAA CCAAAAAAAXRRPPLLL  OO" * 100
data_5 = b"Python is a programming language that lets you work quickly and integrate systems more effectively."
data_6 = b"Python is a programming language that lets you work quickly and integrate systems more effectively." * 6
data_7 = b"Python is a programming language that lets you work quickly and integrate systems more effectively." * 16

input_options = [data_0, data_1, data_2, data_3, data_4, data_5, data_6, data_7]


def encode_and_decode(input_data):
    """Tests encoding and decoding and creates printout of essential data.

    Args:
        input_data (bytes): Data to be encoded.
    """

    print("Input data size: ", sys.getsizeof(input_data), "bytes")
    print("Input data type: ", type(input_data))

    lzw_compression = LZWCompression()
    compressed_data = lzw_compression.encode(uncompressed_data=input_data)

    print("Compressed data size: ", sys.getsizeof(compressed_data), "bytes")
    print("Compressed data type: ", type(compressed_data))

    decoded_data = lzw_compression.decode(compressed_data=compressed_data)

    print("Decompressed data size: ", sys.getsizeof(decoded_data), "bytes")
    print("Decompressed data type: ", type(decoded_data))

    print("Decompressed data = Input data:", decoded_data == input_data)

    compression_rate = sys.getsizeof(input_data) / sys.getsizeof(compressed_data)
    print(f"Compression rate: {compression_rate:.2f}")


# Executes all testcases and names them for the output.
n = 0
for data in input_options:
    print()
    print(f'data_{n}')
    n += 1
    encode_and_decode(data)
