import pandas as pd
import talib

def calculate_engulfing(df):
    # Utiliza TA-Lib para identificar padrões de engolfo
    df['engulfing'] = talib.CDLENGULFING(df['open'], df['high'], df['low'], df['close'])
    
    # Mapeia os valores para descrições mais legíveis
    df['engulfing_pattern'] = df['engulfing'].map({
        100: 'Bullish Engulfing',
        -100: 'Bearish Engulfing',
        0: 'No Pattern'
    })
    return df

# Exemplo de uso:
data = {
    'open': [1, 2, 3, 3, 4, 4, 4, 5, 6, 5, 5, 4, 6, 7, 6, 5, 6, 1, 3, 2, 4, 4, 5, 6, 7, 5, 5, 4, 3, 2],
    'high': [2, 3, 4, 4, 5, 5, 5, 6, 7, 6, 6, 5, 7, 8, 7, 6, 7, 2, 4, 3, 5, 5, 6, 7, 8, 6, 6, 5, 4, 3],
    'low':  [1, 1, 2, 2, 3, 3, 3, 4, 5, 4, 4, 3, 5, 6, 5, 4, 5, 1, 2, 1, 3, 3, 4, 5, 6, 4, 4, 3, 2, 1],
    'close': [2, 3, 3, 4, 5, 4, 5, 6, 5, 6, 5, 4, 6, 7, 6, 5, 6, 2, 4, 3, 5, 5, 6, 7, 6, 5, 4, 3, 2, 1]
}
df = pd.DataFrame(data)
df = calculate_engulfing(df)