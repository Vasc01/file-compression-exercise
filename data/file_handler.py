import os.path
import pickle
from abc import ABC, abstractmethod

from core.compression import LZWCompression, HuffmanCompression


class FileHandlerABC(ABC):

    @abstractmethod
    def create_file(self, path, data):
        raise NotImplemented


class FileHandler(FileHandlerABC):

    def __init__(self):
        self.algorithm = None
        self.file_path = None
        self.file_name = None
        self.file_extension = None
        self.original_data = None
        self.encoded_data = None
        self.encoded_file_extension = None

    def initiate_encode(self, complete_path, algorithm, file_name=None):

        self.get_path_info(complete_path)
        self.get_file_data(complete_path)
        data_to_write = self.encode(algorithm)

        if file_name:
            self.file_name = file_name

        self.write_in_file(data_to_write)

    def get_path_info(self, complete_path):
        """Gets file location file name and extension from path.

        Args:
            complete_path (str): Expected to have path to file including file name and extension.
        """
        self.file_path = os.path.split(complete_path)[0]
        self.file_name = os.path.splitext(os.path.basename(complete_path))[0]
        self.file_extension = os.path.splitext(complete_path)[1]

    def get_file_data(self, complete_path):

        with open(complete_path, 'rb') as f:
            data_for_compression = f.read()

        self.original_data = data_for_compression

    def encode(self, algorithm):

        if algorithm == "lzw":
            encoder = LZWCompression()

            encoded_data = encoder.encode(self.original_data)
            bit_size = encoder.bit_size

            self.encoded_file_extension = ".lzw"

            return bit_size, encoded_data, self.file_extension

        elif algorithm == "huf":
            encoder = HuffmanCompression()

            encoded_data = encoder.encode(self.original_data)
            codebook = encoder.codebook

            self.encoded_file_extension = ".huf"

            return codebook, encoded_data, self.file_extension

    def write_in_file(self, data_to_write):

        new_path = os.path.join(self.file_path, (self.file_name + self.encoded_file_extension))
        # new_path = self.file_path + self.file_name + self.encoded_file_extension

        print(new_path)

        with open(new_path, 'wb') as f:
            pickle.dump(data_to_write, f)

        print("New file created.")

    def get_file_size(self, path):
        pass

    def create_file(self, path, data):
        pass
