from sandbox.lzw_encode_bytes import LZWCompressionBytes

lzw_compression = LZWCompressionBytes()

lzw_compression.create_codebook()
codebook = lzw_compression.codebook
print(lzw_compression.codebook)

lzw_compression.create_reversed_codebook()
print(lzw_compression.codebook)
reversed_codebook = lzw_compression.codebook
reversed_reversed_codebook = {v: k for k, v in reversed_codebook.items()}

print(codebook == reversed_reversed_codebook)
