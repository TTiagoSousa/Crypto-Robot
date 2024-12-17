def calculate_transaction_result_long(close_value, open_value, capital, fees):
    if open_value < close_value:
        percentual_trade = (close_value - open_value) / open_value
    else:
        percentual_trade = (open_value - close_value) / open_value * -1
        
    fees_paid_from_starting_capital = capital * (fees / 100)
    
    entry_capital_after_fees = capital - fees_paid_from_starting_capital
    
    capital_after_trade = entry_capital_after_fees * (1 + percentual_trade)
    
    fees_paid_at_the_end_of_the_operation = capital_after_trade * (fees / 100)
    
    final_capital = capital_after_trade - fees_paid_at_the_end_of_the_operation
    
    total_fees_paid = fees_paid_from_starting_capital + fees_paid_at_the_end_of_the_operation
    
    profit_or_losses = final_capital - capital
    
    # Update this line to avoid resetting the capital
    return final_capital, total_fees_paid, profit_or_losses