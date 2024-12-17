import pandas as pd
import talib

def calculate_star_patterns(df):
    """
    Identifica os padrões Morning Star e Evening Star em um DataFrame de dados de preços.

    Parâmetros:
    - df: DataFrame com colunas 'open', 'high', 'low' e 'close'.

    Retorna:
    - df: DataFrame com colunas adicionais 'morning_star' e 'evening_star', contendo os padrões identificados.
    """
    # Identifica o padrão Morning Star
    df['morning_star'] = talib.CDLMORNINGSTAR(df['open'], df['high'], df['low'], df['close'])
    # df['morning_star'] = talib.CDLMORNINGSTAR(df['open'], df['high'], df['low'], df['close'], penetration=1)
    
    # Identifica o padrão Evening Star
    df['evening_star'] = talib.CDLEVENINGSTAR(df['open'], df['high'], df['low'], df['close'])

    # Mapeia os valores para descrições mais legíveis
    df['morning_star_pattern'] = df['morning_star'].map({
        100: 'Morning Star',
        0: 'No Pattern',
        -100: 'Negative Morning Star'  # Ajuste se aplicável, dependendo da interpretação de -100 para o padrão
    })
    
    df['evening_star_pattern'] = df['evening_star'].map({
        100: 'Evening Star',
        0: 'No Pattern',
        -100: 'Negative Evening Star'  # Ajuste se aplicável
    })

    return df