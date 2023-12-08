from abc import ABC, abstractmethod


class FileHandlerABC(ABC):

    @abstractmethod
    def some_function(self):
        raise NotImplemented


class FileHandler(FileHandlerABC):

    def some_function(self):
        pass
