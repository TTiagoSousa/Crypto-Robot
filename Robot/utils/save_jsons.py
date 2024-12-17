# save_transactions.py
import os
import json

def save_transactions(transactions, base_dir, start_time):
    # Create the base directory for tests if it doesn't exist
    os.makedirs(base_dir, exist_ok=True)

    # Determine the next folder number based on existing folders
    folder_num = len([name for name in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, name))]) + 1
    folder_path = os.path.join(base_dir, str(folder_num))
    os.makedirs(folder_path, exist_ok=True)

    # Create the filename and save the transactions to JSON
    transactions_filename = f'transactions_{start_time.strftime("%Y%m%d%H%M%S")}.json'
    transactions_filepath = os.path.join(folder_path, transactions_filename)
    
    with open(transactions_filepath, 'w') as f:
        json.dump(transactions, f, indent=4)

    return folder_path  # Return the folder path for saving summary

def save_summary(summary, folder_path, start_time):
    summary_filename = f'summary_{start_time.strftime("%Y%m%d%H%M%S")}.json'
    summary_filepath = os.path.join(folder_path, summary_filename)  # Use folder_path here
    with open(summary_filepath, 'w') as f:
        json.dump(summary, f, indent=4)
        
def save_annual_summary(annual_summary, folder_path, start_time):
    annual_summary_filename = f'annual_summary_{start_time.strftime("%Y%m%d%H%M%S")}.json'
    annual_summary_filepath = os.path.join(folder_path, annual_summary_filename)  # Use folder_path aqui
    with open(annual_summary_filepath, 'w') as f:
        json.dump(annual_summary, f, indent=4)
        
def save_monthly_summary(monthly_summary, folder_path, start_time):
    monthly_summary_filename = f'monthly_summary_{start_time.strftime("%Y%m%d%H%M%S")}.json'
    monthly_summary_filepath = os.path.join(folder_path, monthly_summary_filename)  # Use folder_path aqui
    with open(monthly_summary_filepath, 'w') as f:
        json.dump(monthly_summary, f, indent=4)