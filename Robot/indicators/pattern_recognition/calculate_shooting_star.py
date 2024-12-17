import pandas as pd
import talib

def calculate_shooting_star(df):
    """
    Identifica o padrão Shooting Star em um DataFrame de dados de preços.

    Parâmetros:
    - df: DataFrame com colunas 'open', 'high', 'low' e 'close'.

    Retorna:
    - df: DataFrame com colunas adicionais 'shooting_star' e 'shooting_star_pattern'.
    """
    # Utiliza TA-Lib para identificar o padrão Shooting Star
    df['shooting_star'] = talib.CDLSHOOTINGSTAR(df['open'], df['high'], df['low'], df['close'])
    
    # Mapeia os valores para descrições mais legíveis
    df['shooting_star_pattern'] = df['shooting_star'].map({
        100: 'Shooting Star',
        0: 'No Pattern'
    })
    return df