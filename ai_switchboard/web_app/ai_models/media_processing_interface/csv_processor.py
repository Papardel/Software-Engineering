from abc import ABC, abstractmethod

from media_processor import MediaProcessor

"""
Interface for CSV file processing classes classes. 
Get Directory method is used to get the directory of the CSV file to be processed, which should be the same as the 
processing class. Run model method is used to run the model on the CSV file, where the output should be the name 
of the output file saved in the db.
"""


class CSVProcessor(MediaProcessor, ABC):
    @abstractmethod
    def run_model(self, media):
        pass

    @abstractmethod
    def get_directory(self):
        pass
