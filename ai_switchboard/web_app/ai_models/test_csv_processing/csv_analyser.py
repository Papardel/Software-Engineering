from ..media_processing_interface.csv_processor import CSVProcessor

class CSVAnalyser(CSVProcessor):
    def run_model(self, csv_file):
        csv_file_path = os.path.join(os.path.dirname(__file__), csv_file)
        print("Testing running different processing mehtods and formats...")
        os.remove(csv_file_path)

        return "test was succesful"
        


    def get_directory(self):
        return os.path.dirname(__file__)
