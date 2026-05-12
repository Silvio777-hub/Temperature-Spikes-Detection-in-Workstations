import csv
import os

class CSVHandler:
    """Handles writing metrics to CSV files."""
    def __init__(self, file_path):
        self.file_path = file_path
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

    def write_row(self, data_dict):
        file_exists = os.path.isfile(self.file_path)
        with open(self.file_path, 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=data_dict.keys())
            if not file_exists:
                writer.writeheader()
            writer.writerow(data_dict)
