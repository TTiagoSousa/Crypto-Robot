import os
from generateData import generateFiles
from development.development_1 import development_1
from utils.files_management.file_checker import manage_file

start_date = "2020-01-01"
end_date = "2024-11-14"
time_frame = "3m"
pair_1 = "BTCUSDT"
fees = 0.0153
capital = 1000

manage_file(start_date, end_date, time_frame, pair_1, generateFiles)

development_1(start_date, end_date, time_frame, pair_1, capital, fees)

exit()