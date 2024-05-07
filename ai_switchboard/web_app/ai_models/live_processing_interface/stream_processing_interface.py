from abc import ABC, abstractmethod


class stream_processor(ABC):
    @abstractmethod
    def run_model(self, video): # missing arguments which will be passed in from the queue
        pass
