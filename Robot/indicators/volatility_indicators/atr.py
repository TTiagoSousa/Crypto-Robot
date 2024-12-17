import pandas as pd
import talib

def calculate_atr(df, period=14):
    # Utiliza TA-Lib para calcular o ATR
    df['atr'] = talib.ATR(df['high'], df['low'], df['close'], timeperiod=period)
    
    # Arredonda o ATR para 2 casas decimais
    df['atr'] = df['atr'].round(2)

    return df

# Exemplo de uso:
data = {
    'high': [1.1, 2.2, 1.3, 3.1, 4.5, 2.8, 3.2, 4.6, 3.4, 4.1, 5.2, 4.3, 6.2, 5.1, 4.4, 3.3, 2.1, 1.9, 2.8, 3.9, 4.6, 5.5, 6.8, 7.2, 6.1, 5.5, 4.2, 3.7, 2.4, 1.6],
    'low': [0.9, 1.8, 0.9, 2.8, 3.9, 2.1, 3.0, 4.2, 3.0, 3.8, 4.9, 3.7, 5.6, 4.7, 3.9, 2.8, 1.8, 1.6, 2.5, 3.5, 4.1, 5.0, 6.0, 6.5, 5.5, 4.8, 4.0, 3.0, 2.0, 1.0],
    'close': [1, 2, 1, 3, 4, 2, 3, 4, 3, 4, 5, 4, 6, 5, 4, 3, 2, 1, 2, 3, 4, 5, 6, 7, 6, 5, 4, 3, 2, 1]
}
df = pd.DataFrame(data)
df = calculate_atr(df)

print(df)