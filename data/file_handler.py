import os.path
import pickle
from abc import ABC, abstractmethod


class FileHandlerABC(ABC):

    @abstractmethod
    def create_file(self, path, data):
        raise NotImplemented


class FileHandler(FileHandlerABC):

    @staticmethod
    def get_path_info(complete_path):
        """Gets file location file name and extension from path.

        Args:
            complete_path (str): Expected to have path to file including file name and extension.
        """
        file_path = os.path.split(complete_path)[0]
        file_name = os.path.splitext(os.path.basename(complete_path))[0]
        file_extension = os.path.splitext(complete_path)[1]

        return file_path, file_name, file_extension

    @staticmethod
    def get_file_bytes(complete_path):

        with open(complete_path, 'rb') as f:
            data = f.read()

        return data

    @staticmethod
    def write_in_file(data, file_path, file_name, file_extension):

        # Names and locates the new file
        new_path = os.path.join(file_path, (file_name + file_extension))

        with open(new_path, 'wb') as f:
            pickle.dump(data, f)

    @staticmethod
    def read_from_file(file_path):

        with open(file_path, 'rb') as f:
            stored_data = pickle.load(f)

        return stored_data

    @staticmethod
    def recreate_file(data, file_path, file_name, file_extension):

        new_path = os.path.join(file_path, (file_name + file_extension))

        with open(new_path, 'wb') as f:
            f.write(data)

    @staticmethod
    def rebuild_file_path(file_path, file_name, file_extension):

        path = os.path.join(file_path, (file_name + file_extension))

        return path

    def get_file_size(self, path):
        pass

    def create_file(self, path, data):
        pass
