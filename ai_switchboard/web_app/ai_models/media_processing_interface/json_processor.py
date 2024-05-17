from abc import ABC, abstractmethod

from media_processor import MediaProcessor


"""
Interface for JSON file processing classes classes. 
Get Directory method is used to get the directory of the JSON file to be processed, which should be the same as the 
processing class. Run model method is used to run the model on the JSON file, where the output should be the name 
of the output file saved in the db.
"""


class JSONProcessor(MediaProcessor, ABC):
    @abstractmethod
    def run_model(self, json_file):
        pass

    @abstractmethod
    def get_directory(self):
        pass
