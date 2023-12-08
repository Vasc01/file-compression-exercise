""" Demonstration of the backend capabilities.
"""
from core.algorihm import LZWAlgorithm, HuffmanAlgorithm
from core.stream_encoder import StreamEncoder
from core.performance_calculator import PerformanceCalculator


class Application(object):

    def __init__(self):
        self.lzw_algorithm = LZWAlgorithm()
        self.huffman_algorithm = HuffmanAlgorithm()
        self.stream_encoder = StreamEncoder()
        self.performance_calculator = PerformanceCalculator

    def run(self):
        # eventloop
        pass
