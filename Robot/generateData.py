
def generateFiles(start_date, end_date, timeframe, pair1):
    import os
    import api
    from functions import get_candles_batched, create_df, plot_chart
    binance_api_key = "-"
    binance_secret_key = "-"
    client = api.Binance_API(api_key=binance_api_key, secret_key=binance_secret_key)
    

    # Download single asset data
    candles = get_candles_batched(client, symbol=pair1, interval=timeframe, start_date=start_date, end_date=end_date, delay=0.4)
    df = create_df(candles)

    print(df)
    plot_chart(df)
    
    # Define the folder path
    folder_path = "Currencies_History"
    
    # Create the folder if it doesn't exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Save the DataFrame as a CSV file in the folder
    csv_path = os.path.join(folder_path, f"df_{start_date}_{end_date}_{timeframe}_{pair1}.csv")
    df.to_csv(csv_path, index=False)

    # Save the DataFrame as a pickle file in the same folder
    pickle_path = os.path.join(folder_path, f"df_{start_date}_{end_date}_{timeframe}_{pair1}.pkl")
    df.to_pickle(pickle_path)

    # Save the DataFrame as a JSON file in the same folder
    json_path = os.path.join(folder_path, f"df_{start_date}_{end_date}_{timeframe}_{pair1}.json")
    df.to_json(json_path, orient='records', lines=True, indent=4)

    # Check the columns of the DataFrame
    print(df.columns)