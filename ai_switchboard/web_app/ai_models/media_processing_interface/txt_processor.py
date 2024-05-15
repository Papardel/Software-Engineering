from abc import ABC, abstractmethod

from media_processor import MediaProcessor


class TXTProcessor(MediaProcessor, ABC):
    @abstractmethod
    def run_model(self, video):
        pass

    @abstractmethod
    def get_directory(self):
        pass
