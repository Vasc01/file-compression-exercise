""" To be able to get data from files and after processing it to save it in another file, a file handler is used."""

import os.path
import pickle
from abc import ABC, abstractmethod

# FIXME: It is OK to work with file handler classes but please provide some context, e.g we need
#   structures that have a specific attribute for the data and the meta-information, and then we can
#   use the file handler to read/write the data and meta-information from/to the file.


class FileHandlerABC(ABC):
    # FIXME: Naming too generic, not descriptive enough. As a suggestion, I would use something like CompressedFileAbc.

    """Defines file and path handling methods needed for the frontend to operate."""

    @staticmethod
    @abstractmethod
    def get_path_info(*args):
        # FIXME: Add docsting for people using the abstract class.
        raise NotImplemented

    @staticmethod
    @abstractmethod
    def get_file_bytes(*args):
        # FIXME: Add docsting for people using the abstract class.
        raise NotImplemented

    @staticmethod
    @abstractmethod
    def write_in_file(*args):
        # FIXME: Add docsting for people using the abstract class.
        raise NotImplemented

    @staticmethod
    @abstractmethod
    def read_from_file(*args):
        # FIXME: Add docsting for people using the abstract class.
        raise NotImplemented

    @staticmethod
    @abstractmethod
    def recreate_file(*args):
        # FIXME: Add docsting for people using the abstract class.
        raise NotImplemented

    @staticmethod
    @abstractmethod
    def rebuild_file_path(*args):
        # FIXME: Add docsting for people using the abstract class.
        raise NotImplemented


class FileHandler(FileHandlerABC):
    # FIXME: Naming too generic, not descriptive enough. As a suggestion, I would use something like CompressedFile.

    """Deals wit file paths, reading data from files and writing information to newly created files."""

    # FIXME: Missing constructor, please avoid using static methods, we use objects instead with a constructor.
    #   and then we can use the object to call the methods.

    @staticmethod
    def get_path_info(complete_path: str):
        # FIXME: Not good, file_path, file_name, file_extension are a state of the compressed file
        # FIXME: It is not only the path info we get

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
        # FIXME: Better name for this method, e.g. read()

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
        # FIXME: Better name for this method, e.g. write()

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
        # FIXME: Better name for this method, e.g. deserialize

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
        # FIXME: Description is not clear, what is the purpose of this method?

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
        # FIXME: Avoid using one-line methods, they are spamming the code and make it hard to read.

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
