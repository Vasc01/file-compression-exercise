from core_test.compression import HuffmanCompression, BinaryTree

tree = BinaryTree()
tree.create()
tree.insert()
tree.export()

huffman_algorithm = HuffmanCompression()
huffman_algorithm.set_binary_tree(tree)
huffman_algorithm.encode("path")
