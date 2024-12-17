from datetime import datetime
import os
from utils.load_pickle import load_pickle_file
from indicators.trend_indicatores.ewm import calculate_ewm
from indicators.momentum_indicators.rsi import calculate_rsi
from indicators.momentum_indicators.stochastic import calculate_stoch
from indicators.pattern_recognition.calculate_engulfing import calculate_engulfing
from indicators.trend_indicatores.adx import calculate_adx
from utils.save_jsons import save_transactions, save_summary, save_annual_summary, save_monthly_summary
from utils.financial_calculations.calculate_transaction_result_long import calculate_transaction_result_long
from utils.financial_calculations.calculate_transaction_result_short import calculate_transaction_result_short
from utils.summarys.summary import robot_summary
from utils.summarys.generate_annual_summary import generate_annual_summary
from utils.summarys.generate_monthly_summary import generate_monthly_summary
from plot_graph import plot_transactions
from indicators.pattern_recognition.calculate_shooting_star import calculate_shooting_star
from indicators.pattern_recognition.calculate_star import calculate_star_patterns

def development_2(start_date, end_date, time_frame, pair_1, capital, fees):
    
    StartTime = datetime.now()
    
    df = load_pickle_file(start_date, end_date, time_frame, pair_1)
    
    initial_capital = capital
    open_trade = False
    open_value = 0
    close_value = 0
    stop_value = 0
    stop_gain = 0
    count_transactions = 0
    open_date = None
    close_date = None
    stop_profit_long = 0.02
    stop_profit_short = 0.02
    transactions = []
    trade_type = None
    
    morning_star_count = 0
    evening_star_count = 0

    
    df = calculate_ewm(df, ema_lengths=[9, 21, 90, 200])
    df = calculate_rsi(df)
    df = calculate_engulfing(df)
    df = calculate_stoch(df)
    df = calculate_adx(df)
    df = calculate_shooting_star(df)
    df = calculate_star_patterns(df)
    
    total_length = len(df)
    print("Starting simulations...")
    
    for i in range(1000, len(df)):
        
        current_day = df['timestamp'].iloc[i].weekday()
        progress = ((i - 1000) / (total_length - 1000)) * 100
        print(f"Simulation progress: {progress:.2f}% complete", end='\r')
        
        if i + 9 >= len(df):
            break
        
        sub_df = df.iloc[:i]
        
        if sub_df['evening_star'].iloc[-2] == -100:
            evening_star_count += 1
        
        if not open_trade:

            if sub_df['morning_star'].iloc[-2] == 100:
                morning_star_high = sub_df['high'].iloc[-2]
                if sub_df['high'].iloc[-1] > morning_star_high:
                    open_trade = True
                    trade_type = 'long'
                    count_transactions += 1
                    open_value = morning_star_high
                    open_date = sub_df['timestamp'].iloc[-1]
                    stop_value = min(sub_df['low'].iloc[-10:-1])
                    stop_gain = open_value * (1 + stop_profit_long)

            if sub_df['evening_star'].iloc[-2] == -100:
                evening_star_low = sub_df['low'].iloc[-2]
                if sub_df['low'].iloc[-1] < evening_star_low:
                    open_trade = True
                    trade_type = 'short'
                    count_transactions += 1
                    open_value = evening_star_low
                    open_date = sub_df['timestamp'].iloc[-1]
                    stop_value = max(sub_df['high'].iloc[-10:-1])
                    stop_gain = open_value * (1 - stop_profit_short)
        
        else:
            
            if trade_type == 'long':

                # Fechar com Stop Loss
                if sub_df['low'].iloc[-1] <= stop_value:
                    open_trade = False
                    close_value = stop_value
                    close_date = sub_df['timestamp'].iloc[-1]
                    capital, total_fees_paid, profit_or_losses = calculate_transaction_result_long(close_value, open_value, capital, fees)
                    
                    transaction = {
                        'Trade Type': 'LONG',
                        'Final capital': capital,
                        'Profit or loss': profit_or_losses,
                        'Open value': open_value,
                        'Close value': close_value,
                        'Stop value': stop_value,
                        'Stop Gain': stop_gain,
                        'Closing of the operation': "Stop Loss",
                        'Fees paid': total_fees_paid,
                        'Open date': open_date.strftime("%Y-%m-%d %H:%M:%S"),
                        'Close date': close_date.strftime("%Y-%m-%d %H:%M:%S"),
                    }
                    transactions.append(transaction)
                
                # Fechar com Stop Gain
                elif sub_df['high'].iloc[-1] >= stop_gain:
                    open_trade = False
                    close_value = stop_gain
                    close_date = sub_df['timestamp'].iloc[-1]
                    capital, total_fees_paid, profit_or_losses = calculate_transaction_result_long(close_value, open_value, capital, fees)
                    
                    transaction = {
                        'Trade Type': 'LONG',
                        'Final capital': capital,
                        'Profit or loss': profit_or_losses,
                        'Open value': open_value,
                        'Close value': close_value,
                        'Stop value': stop_value,
                        'Stop Gain': stop_gain,
                        'Closing of the operation': "Stop Gain",
                        'Fees paid': total_fees_paid,
                        'Open date': open_date.strftime("%Y-%m-%d %H:%M:%S"),
                        'Close date': close_date.strftime("%Y-%m-%d %H:%M:%S"),
                    }
                    transactions.append(transaction)
                    
            elif trade_type == 'short':
                # Fechar com Stop Loss
                if sub_df['high'].iloc[-1] >= stop_value:
                    open_trade = False
                    close_value = stop_value
                    close_date = sub_df['timestamp'].iloc[-1]
                    capital, total_fees_paid, profit_or_losses = calculate_transaction_result_short(close_value, open_value, capital, fees)
                    
                    transaction = {
                        'Trade Type': 'SHORT',
                        'Final capital': capital,
                        'Profit or loss': profit_or_losses,
                        'Open value': open_value,
                        'Close value': close_value,
                        'Stop value': stop_value,
                        'Stop Gain': stop_gain,
                        'Closing of the operation': "Stop Loss",
                        'Fees paid': total_fees_paid,
                        'Open date': open_date.strftime("%Y-%m-%d %H:%M:%S"),
                        'Close date': close_date.strftime("%Y-%m-%d %H:%M:%S"),
                    }
                    transactions.append(transaction)
                
                # Fechar com Stop Gain
                elif sub_df['low'].iloc[-1] <= stop_gain:
                    open_trade = False
                    close_value = stop_gain
                    close_date = sub_df['timestamp'].iloc[-1]
                    capital, total_fees_paid, profit_or_losses = calculate_transaction_result_short(close_value, open_value, capital, fees)
                    
                    transaction = {
                        'Trade Type': 'SHORT',
                        'Final capital': capital,
                        'Profit or loss': profit_or_losses,
                        'Open value': open_value,
                        'Close value': close_value,
                        'Stop value': stop_value,
                        'Stop Gain': stop_gain,
                        'Closing of the operation': "Stop Gain",
                        'Fees paid': total_fees_paid,
                        'Open date': open_date.strftime("%Y-%m-%d %H:%M:%S"),
                        'Close date': close_date.strftime("%Y-%m-%d %H:%M:%S"),
                    }
                    transactions.append(transaction)
                
    base_tests_dir = os.path.join(os.getcwd(), "Tests")
    folder_path = save_transactions(transactions, base_tests_dir, StartTime)  # Obter caminho da pasta para salvar resumo
    
    # Gerar dados de resumo e salvar
    final_capital = capital  # Armazena o capital final
    summary = robot_summary(transactions, count_transactions, initial_capital, final_capital)
    annual_summary = generate_annual_summary(transactions, initial_capital)  # Correção aqui
    monthly_summary = generate_monthly_summary(transactions, initial_capital)  # Correção aqui
    save_summary(summary, folder_path, StartTime)
    save_annual_summary(annual_summary, folder_path, StartTime)
    save_monthly_summary(monthly_summary, folder_path, StartTime)
    
    # fig = plot_transactions(df, transactions, available_indicators=['EVENING_STAR'])
    # fig.show()