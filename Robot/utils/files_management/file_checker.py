import os

def check_file_exists(start_date, end_date, time_frame, pair_1):
    folder_path = "Currencies_History"
    pkl_path = os.path.join(folder_path, f"df_{start_date}_{end_date}_{time_frame}_{pair_1}.pkl")
    return os.path.exists(pkl_path)

def manage_file(start_date, end_date, time_frame, pair_1, generateFiles):
    if not check_file_exists(start_date, end_date, time_frame, pair_1):
        generateFiles(start_date, end_date, time_frame, pair_1)
        print(f"File with time does not exist")
    else:
        print(f"File with time graph already exists.")