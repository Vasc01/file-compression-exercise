""" Demonstration of the backend capabilities.

Makes use of fire CLI library
"""

from core.compression import LZWCompression, HuffmanCompression
import fire

from data.file_handler import FileHandler


class Application(object):

    def encode(self, path: str, algorithm: str, new_name=None):
        file_handler = FileHandler()
        file_handler.initiate_encode(path, algorithm, new_name)

    def decode(self, file_to_decode: str, new_file_name: str):
        print('application starts the decompress function')


def run():
    fire.Fire(Application)
