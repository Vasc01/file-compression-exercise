# For the Huffman algorithm the codebook can be saved within the compressed file.

import pickle
from sys import getsizeof

codebook = {1: "a", 2: "b", 3: "c"}
compressed_data = b"ABCDE_abcde"

print(getsizeof(codebook))
print(getsizeof(compressed_data))
print(type(compressed_data))

file_content = (codebook, compressed_data)

with open('data_encoded.sco', 'wb') as f:
    pickle.dump(file_content, f)

with open('data_encoded.sco', 'rb') as f:
    new_data = pickle.load(f)

print(new_data)
