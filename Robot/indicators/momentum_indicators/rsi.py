import pandas as pd
import talib

def calculate_rsi(df, period=14):
    # Utiliza TA-Lib para calcular o RSI
    df['rsi'] = talib.RSI(df['close'], timeperiod=period)
    
    # Arredonda o RSI para 2 casas decimais
    df['rsi'] = df['rsi'].round(2)

    return df

# Exemplo de uso:
data = {
    'close': [1, 2, 1, 3, 4, 2, 3, 4, 3, 4, 5, 4, 6, 5, 4, 3, 2, 1, 2, 3, 4, 5, 6, 7, 6, 5, 4, 3, 2, 1]
}
df = pd.DataFrame(data)
df = calculate_rsi(df)