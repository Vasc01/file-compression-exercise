from abc import ABC, abstractmethod

from data.file_handler import FileHandler


class AlgorithmABC(ABC):

    @abstractmethod
    def encode(self, path):
        raise NotImplemented

    @abstractmethod
    def decode(self):
        raise NotImplemented


class LZWAlgorithm(AlgorithmABC):

    def __init__(self):
        self.file_handler = FileHandler()

    def encode(self, path):
        print("LZW algorithm starts the encode function")

        # compression data is saved here
        data = None

        self.file_handler.create_file(path, data)

    def decode(self):
        raise NotImplemented


class HuffmanAlgorithm(AlgorithmABC):

    def __init__(self):
        self.binary_tree = None

    def set_binary_tree(self, binary_tree):
        self.binary_tree = binary_tree

    def encode(self, path):
        pass

    def decode(self):
        pass


class BinaryTree(object):

    def create(self):
        pass

    def export(self):
        pass

    def insert(self):
        pass

