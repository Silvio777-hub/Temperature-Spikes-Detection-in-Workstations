import pandas as pd
import os

def read_csv_robust(file_path, **kwargs):
    """
    Robustly reads a CSV file using pandas, automatically trying different encodings
    (utf-8, utf-8-sig, cp1252, latin-1) to handle legacy logs and platform-specific symbols.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"CSV file not found: {file_path}")
        
    encodings = ['utf-8', 'utf-8-sig', 'cp1252', 'latin-1']
    last_err = None
    
    for encoding in encodings:
        try:
            return pd.read_csv(file_path, encoding=encoding, **kwargs)
        except (UnicodeDecodeError, LookupError) as e:
            last_err = e
            continue
            
    raise last_err
