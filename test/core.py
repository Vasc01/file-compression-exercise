from core.algorihm import HuffmanAlgorithm, BinaryTree

tree = BinaryTree()
tree.create()
tree.insert()
tree.export()

huffman_algorithm = HuffmanAlgorithm()
huffman_algorithm.set_binary_tree(tree)
huffman_algorithm.encode("path")
