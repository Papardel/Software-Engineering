from abc import ABC, abstractmethod

"""Interface for media processing in general."""


class MediaProcessor(ABC):

    @abstractmethod
    def run_model(self, media):
        pass

    @abstractmethod
    def get_directory(self):
        pass
