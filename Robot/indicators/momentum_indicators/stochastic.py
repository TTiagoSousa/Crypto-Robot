import pandas as pd
import talib

def calculate_rsi(df, period=14):
    df['rsi'] = talib.RSI(df['close'], timeperiod=period)
    df['rsi'] = df['rsi'].round(2)
    return df

def calculate_stoch(df, rsi_length=14, stoch_length=14, smooth_k=3, smooth_d=3):
    # Calculate Stochastic RSI using TA-Lib
    df['stoch_rsi_fastk'], df['stoch_rsi_fastd'] = talib.STOCHRSI(
        df['close'],
        timeperiod=rsi_length,
        fastk_period=stoch_length,
        fastd_period=smooth_d,
        fastd_matype=0  # SMA
    )
    
    # Rename columns for clarity
    df['%K'] = df['stoch_rsi_fastk']
    df['%D'] = df['stoch_rsi_fastd']
    
    # Drop unnecessary columns
    df = df.drop(columns=['stoch_rsi_fastk', 'stoch_rsi_fastd'])
    
    return df

# Exemplo de uso:
data = {
    'close': [1, 2, 1, 3, 4, 2, 3, 4, 3, 4, 5, 4, 6, 5, 4, 3, 2, 1, 2, 3, 4, 5, 6, 7, 6, 5, 4, 3, 2, 1]
}
df = pd.DataFrame(data)
df = calculate_stoch(df)