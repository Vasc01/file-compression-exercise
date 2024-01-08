"""Tests the BinaryTree class.
Tests the creation of the binary tree and the codebook separately
from the encoding and decoding of the Huffman algorithm.
"""

from core.compression import BinaryTree

data = b"AAA BBB AB  CDDDD CCAA CCAAAAAAAXRRPPLLL  OO"


def create_codebook_step_by_step(input_data: bytes):
    """Tests codebook creation for the Huffman algorithm.

    The end goal of the class BinaryTree is to generate a codebook for the Huffman algorithm.
    Here the steps of the codebook creation are tested one by one.
    Goal is to ensure that the methods perform as expected.

    Args:
        input_data (bytes): Data to create the codebook from.
    """

    binary_tree = BinaryTree()

    print()
    print("Input data  :", type(input_data), input_data)
    print()

    frequency_dict = binary_tree.create_frequency_dict(input_data=input_data)
    print("Frequency dictionary k:v byte:occurrence.")
    print("Note: byte is transformed automatically to int when becoming key in the dictionary.")
    print(frequency_dict)
    print()

    binary_tree.create_heap(frequency=frequency_dict)
    print("Node objects in heap:")
    print(binary_tree.heap)
    print("Most left Node contains the element with the least occurrence:")
    print(binary_tree.heap[0].byte)
    print()

    binary_tree.create_tree()
    print("Node objects in heap reduced to one with highest occurrence:")
    print(binary_tree.heap)
    print("Occurrence for the root node:")
    print(binary_tree.heap[0].occurrence)
    print()

    binary_tree.initiate_create_codes()
    print("Codebook:")
    print(binary_tree.codebook)


def create_codebook(input_data: bytes):
    """Tests codebook creation for the Huffman algorithm.

    Here the codebook is created at once.

    Args:
        input_data (bytes): Data to create the codebook from.
    """
    binary_tree = BinaryTree()
    print("Codebook:")
    print(binary_tree.create_codebook(uncompressed_data=input_data))


# Initiation of the tests.
create_codebook_step_by_step(input_data=data)
create_codebook(input_data=data)
