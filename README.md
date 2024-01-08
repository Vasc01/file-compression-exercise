# Info
File compression program for exercise purpose.

For more information on the project and contribution guidelines see the project Wiki.

Note: This project is under development. Technical requirements and use may change in near future.

# How to Run

- Technical requirements:
  - python 3
  - at this stage there are no further requirements
 
# How to Use

The program is operated from the terminal or the IDE.

Two comprssion algorithms are available:

- LZW compression in the class LZWCompression
- Huffman compression in the class HuffmanCompression

Both compression algorithms have methods encode(data: bytes) and decode(data: bytes). The methods receive and return bytes data. These are the main methods of the compression algorithms. The rest of the metods and the attributes are public and can be addressed separately as well to inspect particular operations within the compression algorithms.

The test files in the test folder are an example of use:

- binary_tree_test.py
- huffman_test.py
- lzw_test.py
