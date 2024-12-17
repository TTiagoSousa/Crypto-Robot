from ta.trend import ema_indicator

def calculate_ewm(df, ema_lengths):
    """
    Adds Exponential Moving Averages (EMAs) to the DataFrame for specified lengths.

    Parameters:
    - df: DataFrame containing at least a 'close' column with price data.
    - ema_lengths: List of EMA lengths to calculate.

    Returns:
    - DataFrame with additional EMA columns named 'ewm{length}'.
    """
    for length in ema_lengths:
        column_name = f'ewm{length}'
        df[column_name] = ema_indicator(close=df['close'], window=length)

    return df