from abc import ABC, abstractmethod


class StreamProcessor(ABC):
    @abstractmethod
    def run_model(self, video): # missing arguments which will be passed in from the queue
        pass
