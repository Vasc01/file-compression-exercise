""" To be able to get data from files and after processing it to save it in another file a file handler is used."""

import os.path
import pickle
from abc import ABC, abstractmethod


class FileHandlerABC(ABC):

    @staticmethod
    @abstractmethod
    def get_path_info(path):
        raise NotImplemented


class FileHandler(FileHandlerABC):
    """Deals wit file paths, reading data from files and writing information to newly created files."""

    @staticmethod
    def get_path_info(complete_path: str):
        """Gets file location, file name and extension from path.

        Args:
            complete_path (str): Expected to have path to file including file name and extension.

        Returns:
            path_info (tuple): Contains separately path to containing folder, file name and file extension.
        """
        file_path = os.path.split(complete_path)[0]
        file_name = os.path.splitext(os.path.basename(complete_path))[0]
        file_extension = os.path.splitext(complete_path)[1]

        return file_path, file_name, file_extension

    @staticmethod
    def get_file_bytes(complete_path: str):
        """ Reads a file as bytes.

        This allows the compression algorithms to work on any type of file.

        Args:
            complete_path (str): Expected to have path to file including file name and extension.

        Returns:
            data (bytes): The file represented as bytes.
        """

        with open(complete_path, 'rb') as f:
            data = f.read()

        return data

    @staticmethod
    def write_in_file(data: tuple, file_path: str, file_name: str, file_extension: str):
        """Makes use of pickle to serialize a python object and write it to file.

        Args:
            data (tuple): Compressed data.
            file_path (str): Path to containing folder.
            file_name (str): File name without extension.
            file_extension (str): File extension.
        """

        # Creates the complete path from parts for the new file.
        new_path = os.path.join(file_path, (file_name + file_extension))

        with open(new_path, 'wb') as f:
            pickle.dump(data, f)

    @staticmethod
    def read_from_file(file_path: str):
        """Makes use of pickle to recover a python object serialized in a file.

        Args:
            file_path: Complete path to file including file name and extension.

        Returns:
            stored_data (tuple): Recovered tuple.
        """

        with open(file_path, 'rb') as f:
            stored_data = pickle.load(f)

        return stored_data

    @staticmethod
    def recreate_file(data: bytes, file_path: str, file_name: str, file_extension: str):
        """Creates a new fie and fills it with the passed bytes-data.

        Args:
            data (bytes): Decoded data.
            file_path (str): Path to containing folder.
            file_name (str): File name without extension.
            file_extension (str): File extension.
        """

        # Creates the complete path from parts for the new file.
        new_path = os.path.join(file_path, (file_name + file_extension))

        with open(new_path, 'wb') as f:
            f.write(data)

    @staticmethod
    def rebuild_file_path(file_path: str, file_name: str, file_extension: str):
        """Creates a complete file path from separate parts.

        Args:
            file_path (str): Path to containing folder.
            file_name (str): File name without extension.
            file_extension (str): File extension.

        Returns:
            path (str): Path to file including file name and extension.
        """
        path = os.path.join(file_path, (file_name + file_extension))

        return path
