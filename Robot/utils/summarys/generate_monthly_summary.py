from collections import defaultdict
from datetime import datetime

def generate_monthly_summary(transactions, initial_capital):
    monthly_summary = defaultdict(lambda: {
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
        year_month = datetime.strptime(close_date, "%Y-%m-%d %H:%M:%S").strftime('%Y-%m')  # Formato 'YYYY-MM'

        # Se for a primeira transação do mês, define o capital inicial
        if monthly_summary[year_month]['Initial Capital'] == 0:
            monthly_summary[year_month]['Initial Capital'] = current_capital

        # Atualiza o total de transações
        monthly_summary[year_month]['Total Transactions'] += 1

        # Verifica se a operação foi lucrativa ou não
        profit_or_loss = transaction['Profit or loss']
        if profit_or_loss > 0:
            monthly_summary[year_month]['Profitable operations'] += 1
        else:
            monthly_summary[year_month]['Loss operations'] += 1

        # Atualiza o capital final
        current_capital += profit_or_loss
        monthly_summary[year_month]['Final Capital'] = current_capital

        # Conta o tipo de encerramento da operação
        closing_type = transaction.get('Closing of the operation', 'Unknown')
        monthly_summary[year_month]['Count type of transitions'][closing_type] += 1

    # Cria um resumo estruturado
    structured_summary = {}

    for year_month, data in monthly_summary.items():
        # Calcula a diferença de capital e percentual de ganho
        difference = data['Final Capital'] - data['Initial Capital']
        gain_percentage = (difference / data['Initial Capital'] * 100) if data['Initial Capital'] > 0 else 0
        
        # Calcula o retorno médio geral
        overall_average_return = difference / data['Total Transactions'] if data['Total Transactions'] > 0 else 0

        # Calcula os retornos médios
        average_profitable_return = (difference / data['Profitable operations']) if data['Profitable operations'] > 0 else 0
        average_losing_return = (difference / data['Loss operations']) if data['Loss operations'] > 0 else 0
        
        # Adiciona ao resumo estruturado
        structured_summary[year_month] = {
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