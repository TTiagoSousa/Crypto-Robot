import talib

def calculate_adx(df, period=14):
    """
    Calcula o ADX (Average Directional Index) e adiciona ao DataFrame.

    Parâmetros:
    - df: DataFrame com colunas 'high', 'low' e 'close'.
    - period: Período para o cálculo do ADX (padrão é 14).

    Retorna:
    - DataFrame com coluna adicional 'ADX'.
    """
    df['ADX'] = talib.ADX(df['high'], df['low'], df['close'], timeperiod=period)
    return df