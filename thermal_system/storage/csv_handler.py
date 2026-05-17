import csv
import os
import shutil

class CSVHandler:
    """
    Handles robust, atomic writing of metrics to CSV files.
    Implements NFR 05: Atomic writes to prevent log corruption.
    """
    def __init__(self, file_path):
        self.file_path = file_path
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

    def write_row(self, data_dict):
        file_exists = os.path.isfile(self.file_path)
        temp_path = self.file_path + ".tmp"
        
        # If file exists, copy it to temp then append
        # If not, create new temp
        if file_exists:
            shutil.copy2(self.file_path, temp_path)
        
        with open(temp_path, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=data_dict.keys())
            if not file_exists:
                writer.writeheader()
            writer.writerow(data_dict)
            
        # Atomic rename
        os.replace(temp_path, self.file_path)
