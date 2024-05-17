from abc import ABC, abstractmethod

from .media_processor import MediaProcessor


"""
Interface for Video file processing classes, which process the live stream.
The run_model method is used to run the model on the live stream, 
where the output should be a boolean value which is used to evaluate whether db should save that live stream segment.
"""


class LiveStreamProcessor(MediaProcessor, ABC):
    @abstractmethod
    def run_model(self, stream_segment):
        pass

    @abstractmethod
    def get_directory(self):
        pass
