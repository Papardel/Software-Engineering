from abc import ABC, abstractmethod


class MediaProcessor(ABC):
    @abstractmethod
    def run_model(self, video, request=None):  # missing arguments which will be passed in from the queue
        pass

