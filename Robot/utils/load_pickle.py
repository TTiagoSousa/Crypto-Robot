# load_pickle.py
import os
import pandas as pd
import logging

def load_pickle_file(start_date, end_date, time_frame, pair_1, folder="Currencies_History"):
    pkl_filename = f"df_{start_date}_{end_date}_{time_frame}_{pair_1}.pkl"
    pkl_path = os.path.join(folder, pkl_filename)
    
    try:
        df = pd.read_pickle(pkl_path)
        return df
    except FileNotFoundError:
        logging.error(f"File {pkl_filename} not found in {folder}")
        return None
    except Exception as e:
        logging.error(f"Error loading file: {str(e)}")
        return None