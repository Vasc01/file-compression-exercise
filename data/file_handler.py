from abc import ABC, abstractmethod


class FileHandlerABC(ABC):

    @abstractmethod
    def create_file(self, path, data):
        raise NotImplemented


class FileHandler(FileHandlerABC):

    def create_file(self, path, data):
        print("File handler creates a file from the data")
        with open(r'C:\users\vesel\desktop\compressed_data.txt', 'x') as f:
            pass

    def get_file_size(self, path):
        pass
