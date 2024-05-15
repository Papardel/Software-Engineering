from abc import ABC, abstractmethod

from .media_processor import MediaProcessor


class VideoProcessor(MediaProcessor, ABC):
    @abstractmethod
    def run_model(self, video):
        pass

    @abstractmethod
    def get_directory(self):
        pass
