def robot_summary(transactions, total_operations, initial_capital, final_capital):
    # Calculate profitable and losing operations
    profitable_operations = sum(1 for t in transactions if t['Profit or loss'] > 0)
    losing_operations = total_operations - profitable_operations
    difference = final_capital - initial_capital
    
    # Initialize variables for total profits and losses
    total_profit = sum(t['Profit or loss'] for t in transactions if t['Profit or loss'] > 0)
    total_loss = sum(t['Profit or loss'] for t in transactions if t['Profit or loss'] < 0)
    
    # Dictionary to count types of closures
    count_types_of_transitions = {}
    
    # Variables for total fees, max return, and max loss
    total_fees_paid = 0
    max_return = float('-inf')  # Start with the smallest possible value
    max_loss = float('inf')     # Start with the largest possible value

    # Count closure types and calculate fees, returns, and losses
    for transaction in transactions:
        closing_type = transaction['Closing of the operation']
        
        # Increment the counter or initialize it at 1 if it doesn't exist
        if closing_type in count_types_of_transitions:
            count_types_of_transitions[closing_type] += 1
        else:
            count_types_of_transitions[closing_type] = 1  # Add new closure type
        
        # Add the fees paid
        total_fees_paid += transaction['Fees paid']
        
        # Calculate return and loss
        profit_or_loss = transaction['Profit or loss']
        
        if profit_or_loss > max_return:
            max_return = profit_or_loss
        
        if profit_or_loss < max_loss:
            max_loss = profit_or_loss

    # Calculate accuracy percentage
    accuracy_percentage = (profitable_operations / total_operations * 100) if total_operations > 0 else 0
    
    # Calculate Average Return
    average_return = difference / total_operations if total_operations > 0 else 0
    
    # Calculate Average Return for Profitable Operations
    average_profitable_return = total_profit / profitable_operations if profitable_operations > 0 else 0
    
    # Calculate Average Return for Losing Operations
    average_losing_return = total_loss / losing_operations if losing_operations > 0 else 0
    
    # Calculate the percentage gain
    gain_percentage = (difference / initial_capital * 100) if initial_capital > 0 else 0

    # Final summary
    summary = {
        "Capital Information": {
            "Initial Capital": initial_capital,
            "Final Capital": final_capital,
            "Difference": difference
        },
        "Performance Metrics": {
            "Total Transactions": total_operations,
            "Profitable Operations": profitable_operations,
            "Losing Operations": losing_operations,
            "Accuracy Percentage": round(accuracy_percentage, 2),
            "Total Fees Paid": total_fees_paid,
            "Max Return": max_return if max_return != float('-inf') else 0,
            "Max Loss": max_loss if max_loss != float('inf') else 0,
            "Gain Percentage": f"{round(gain_percentage, 2)}%"
        },
        "Average Returns": {
            "Overall Average Return per Transaction": average_return,
            "Average Return from Profitable Transactions": average_profitable_return,
            "Average Return from Losing Transactions": average_losing_return
        },
        "Operation Outcomes": count_types_of_transitions
    }
    
    return summary