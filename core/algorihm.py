from abc import ABC, abstractmethod


class AlgorithmABC(ABC):

    @abstractmethod
    def encode(self):
        raise NotImplemented

    @abstractmethod
    def decode(self):
        raise NotImplemented


class LZWAlgorithm(AlgorithmABC):

    def encode(self):
        raise NotImplemented

    def decode(self):
        raise NotImplemented


class HuffmanAlgorithm(AlgorithmABC):

    def encode(self):
        raise NotImplemented

    def decode(self):
        raise NotImplemented
