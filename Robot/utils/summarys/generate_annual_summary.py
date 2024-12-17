from collections import defaultdict
from datetime import datetime

def generate_annual_summary(transactions, initial_capital):
    annual_summary = defaultdict(lambda: {
        'Initial Capital': 0,
        'Final Capital': 0,
        'Total Transactions': 0,
        'Profitable operations': 0,
        'Loss operations': 0,
        'Count type of transitions': defaultdict(int),
    })

    current_capital = initial_capital

    for transaction in transactions:
        close_date = transaction['Close date']
        year = datetime.strptime(close_date, "%Y-%m-%d %H:%M:%S").year

        # If it's the first transaction of the year, set the initial capital
        if annual_summary[year]['Initial Capital'] == 0:
            annual_summary[year]['Initial Capital'] = current_capital

        # Update total transactions
        annual_summary[year]['Total Transactions'] += 1

        # Check if the operation was profitable or not
        profit_or_loss = transaction['Profit or loss']
        if profit_or_loss > 0:
            annual_summary[year]['Profitable operations'] += 1
        else:
            annual_summary[year]['Loss operations'] += 1

        # Update final capital
        current_capital += profit_or_loss
        annual_summary[year]['Final Capital'] = current_capital

        # Count the type of closure of the operation
        closing_type = transaction.get('Closing of the operation', 'Unknown')
        annual_summary[year]['Count type of transitions'][closing_type] += 1

    # Create a structured summary
    structured_summary = {}

    for year, data in annual_summary.items():
        # Calculate the difference in capital and gain percentage
        difference = data['Final Capital'] - data['Initial Capital']
        gain_percentage = (difference / data['Initial Capital'] * 100) if data['Initial Capital'] > 0 else 0
        
        # Calculate the overall average return
        overall_average_return = difference / data['Total Transactions'] if data['Total Transactions'] > 0 else 0

        # Calculate average returns
        average_profitable_return = (difference / data['Profitable operations']) if data['Profitable operations'] > 0 else 0
        average_losing_return = (difference / data['Loss operations']) if data['Loss operations'] > 0 else 0
        
        # Add to structured summary
        structured_summary[year] = {
            "Capital Information": {
                "Initial Capital": data['Initial Capital'],
                "Final Capital": data['Final Capital'],
                "Difference": difference,
                "Gain Percentage": f"{round(gain_percentage, 2)}%"
            },
            "Performance Metrics": {
                "Total Transactions": data['Total Transactions'],
                "Profitable Operations": data['Profitable operations'],
                "Losing Operations": data['Loss operations'],
            },
            "Average Returns": {
                "Overall Average Return": overall_average_return,
                "Average Return from Profitable Transactions": average_profitable_return,
                "Average Return from Losing Transactions": average_losing_return
            },
            "Operation Outcomes": dict(data['Count type of transitions'])
        }

    return structured_summary