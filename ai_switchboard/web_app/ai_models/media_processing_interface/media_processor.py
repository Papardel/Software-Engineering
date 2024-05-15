from abc import ABC, abstractmethod


class MediaProcessor(ABC):

    @abstractmethod
    def run_model(self, video):
        pass

    @abstractmethod
    def get_directory(self):
        pass
