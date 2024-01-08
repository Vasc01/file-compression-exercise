""" Demonstration of the backend capabilities.
Makes use of fire CLI library
"""

from core.compression import LZWCompression, HuffmanCompression
from core.performance_calculator import PerformanceCalculator
import fire


class Application(object):

    def __init__(self):
        self.lzw_algorithm = LZWCompression()
        self.huffman_algorithm = HuffmanCompression()
        self.performance_calculator = PerformanceCalculator()

    def compress(self, algorithm, path):
        print('application starts the compress function')

        self.performance_calculator.set_start_time()

        if algorithm == "lzw":
            self.lzw_algorithm.encode(path)
        elif algorithm == "huffman":
            pass

        self.performance_calculator.set_end_time()
        print("Compression took XX seconds. Compression ratio XX%")

    def decompress(self):
        print('application starts the decompress function')

    def stream(self):
        # stream encoding
        pass


def run():
    fire.Fire(Application)
