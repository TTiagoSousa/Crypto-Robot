import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
from indicators.trend_indicatores.ewm import calculate_ewm
from indicators.momentum_indicators.rsi import calculate_rsi
from indicators.momentum_indicators.stochastic import calculate_stoch
from indicators.pattern_recognition.calculate_engulfing import calculate_engulfing
from indicators.pattern_recognition.calculate_shooting_star import calculate_shooting_star

def plot_transactions(df, transactions, available_indicators):
    # Função interna para criar o gráfico com base nos indicadores selecionados
    def create_figure(selected_indicators):
        df_local = df.copy()  # Faz uma cópia do DataFrame original

        # Inicializa listas para os subplots
        subplot_titles = []
        num_rows = 1  # Sempre começamos com o gráfico principal
        row_heights = [0.7]  # Altura inicial do gráfico principal
        specs = [[{'type': 'xy'}]]  # Especificações dos subplots

        # Verifica se 'RSI' está nos indicadores selecionados
        if 'RSI' in selected_indicators:
            num_rows += 1
            row_heights.append(0.3)
            specs.append([{'type': 'xy'}])
            subplot_titles.append('RSI')

        # Verifica se 'STOCH' está nos indicadores selecionados
        if 'STOCH' in selected_indicators:
            num_rows += 1
            row_heights.append(0.3)
            specs.append([{'type': 'xy'}])
            subplot_titles.append('Stochastic Oscillator')

        # Cria subplots dinamicamente com base nos indicadores
        fig = make_subplots(
            rows=num_rows,
            cols=1,
            shared_xaxes=True,
            vertical_spacing=0.05,
            row_heights=row_heights,
            specs=specs,
            subplot_titles=['Preço'] + subplot_titles
        )

        # Adiciona gráfico de candlestick no primeiro subplot
        fig.add_trace(
            go.Candlestick(
                x=df_local['timestamp'],
                open=df_local['open'],
                high=df_local['high'],
                low=df_local['low'],
                close=df_local['close'],
                name='Candlesticks',
            ),
            row=1,
            col=1,
        )

        # Plota indicadores EWM no primeiro subplot
        df_local = calculate_ewm(df_local, ema_lengths=[9, 21, 90, 200])
        ewm_lengths = [9, 21, 90, 200]
        ewm_colors = {9: 'green', 21: 'yellow', 90: 'red', 200: 'purple'}
        for length in ewm_lengths:
            ewm_name = f'EWM{length}'
            if ewm_name in selected_indicators:
                fig.add_trace(
                    go.Scatter(
                        x=df_local['timestamp'],
                        y=df_local[f'ewm{length}'],
                        mode='lines',
                        name=ewm_name,
                        line=dict(color=ewm_colors[length], width=1),
                    ),
                    row=1,
                    col=1,
                )

        # Plota padrões de engolfo se 'ENGULFING_BULLISH' ou 'ENGULFING_BEARISH' estiver nos indicadores
        if 'ENGULFING_BULLISH' in selected_indicators or 'ENGULFING_BEARISH' in selected_indicators:
            # Calcula os padrões de engolfo
            df_local = calculate_engulfing(df_local)

            # Plota marcadores para Bullish Engulfing
            if 'ENGULFING_BULLISH' in selected_indicators:
                bullish_engulfing = df_local[df_local['engulfing'] == 100]
                fig.add_trace(
                    go.Scatter(
                        x=bullish_engulfing['timestamp'],
                        y=bullish_engulfing['low'],
                        mode='markers',
                        marker=dict(color='green', size=10, symbol='triangle-up'),
                        name='Bullish Engulfing',
                    ),
                    row=1,
                    col=1,
                )

            # Plota marcadores para Bearish Engulfing
            if 'ENGULFING_BEARISH' in selected_indicators:
                bearish_engulfing = df_local[df_local['engulfing'] == -100]
                fig.add_trace(
                    go.Scatter(
                        x=bearish_engulfing['timestamp'],
                        y=bearish_engulfing['high'],
                        mode='markers',
                        marker=dict(color='red', size=10, symbol='triangle-down'),
                        name='Bearish Engulfing',
                    ),
                    row=1,
                    col=1,
                )
                
            if 'SHOOTING_STAR' in selected_indicators:
                shooting_stars = df_local[df_local['shooting_star'] == 100]
                fig.add_trace(
                    go.Scatter(
                        x=shooting_stars['timestamp'],
                        y=shooting_stars['high'],
                        mode='markers',
                        marker=dict(color='orange', size=10, symbol='star'),
                        name='Shooting Star',
                    ),
                    row=1,
                    col=1,
                )

        # Plota setas de abertura e fechamento de transações no primeiro subplot
        for transaction in transactions:
            open_date = datetime.strptime(transaction['Open date'], "%Y-%m-%d %H:%M:%S")
            close_date = datetime.strptime(transaction['Close date'], "%Y-%m-%d %H:%M:%S")
            # Posição "Open" sem aparecer na legenda
            fig.add_trace(
                go.Scatter(
                    x=[open_date],
                    y=[transaction['Open value']],
                    mode='markers+text',
                    marker=dict(color='green', size=10),
                    text=['Open'],
                    textposition='top center',
                    showlegend=False,  # Não exibir na legenda
                ),
                row=1,
                col=1,
            )
            # Posição "Close" sem aparecer na legenda
            fig.add_trace(
                go.Scatter(
                    x=[close_date],
                    y=[transaction['Close value']],
                    mode='markers+text',
                    marker=dict(color='red', size=10),
                    text=['Close'],
                    textposition='top center',
                    showlegend=False,  # Não exibir na legenda
                ),
                row=1,
                col=1,
            )

        current_row = 2  # Linha atual para plotar indicadores adicionais

        # Se 'RSI' estiver nos indicadores selecionados, calcula e plota o RSI
        if 'RSI' in selected_indicators:
            # Calcula o RSI
            df_local = calculate_rsi(df_local, period=14)

            # Plota o RSI no subplot atual
            fig.add_trace(
                go.Scatter(
                    x=df_local['timestamp'],
                    y=df_local['rsi'],
                    mode='lines',
                    name='RSI',
                    line=dict(color='blue', width=1),
                ),
                row=current_row,
                col=1,
            )

            # Adiciona linhas de sobrecompra (70) e sobrevenda (30)
            fig.add_hline(y=70, line_dash='dash', line_color='red', row=current_row, col=1)
            fig.add_hline(y=30, line_dash='dash', line_color='green', row=current_row, col=1)

            # Define o título do eixo y para o subplot atual
            fig.update_yaxes(title_text='RSI', row=current_row, col=1)

            current_row += 1  # Incrementa a linha para o próximo indicador

        # Se 'STOCH' estiver nos indicadores selecionados, calcula e plota o Oscilador Estocástico
        if 'STOCH' in selected_indicators:
            # Calcula o Oscilador Estocástico
            df_local = calculate_stoch(df_local)

            # Plota %K e %D no subplot atual
            fig.add_trace(
                go.Scatter(
                    x=df_local['timestamp'],
                    y=df_local['%K'],
                    mode='lines',
                    name='%K',
                    line=dict(color='orange', width=1),
                ),
                row=current_row,
                col=1,
            )
            fig.add_trace(
                go.Scatter(
                    x=df_local['timestamp'],
                    y=df_local['%D'],
                    mode='lines',
                    name='%D',
                    line=dict(color='purple', width=1),
                ),
                row=current_row,
                col=1,
            )

            # Adiciona linhas de sobrecompra (80) e sobrevenda (20)
            fig.add_hline(y=80, line_dash='dash', line_color='red', row=current_row, col=1)
            fig.add_hline(y=20, line_dash='dash', line_color='green', row=current_row, col=1)

            # Define o título do eixo y para o subplot atual
            fig.update_yaxes(title_text='Stochastic Oscillator', row=current_row, col=1)

            current_row += 1  # Incrementa a linha se houver mais indicadores

        # Personaliza o gráfico
        fig.update_layout(
            title='Estratégia de Trading - Sinais de Abertura e Fechamento',
            legend=dict(x=1.02, y=1, traceorder='normal'),
            hovermode='x unified',
            xaxis_rangeslider_visible=False  # Remove o rangeslider
        )

        # Define o título do eixo y para o primeiro subplot
        fig.update_yaxes(title_text='Preço', row=1, col=1)

        return fig

    # Cria o gráfico inicial com os indicadores disponíveis
    initial_fig = create_figure(available_indicators)

    # Como você está executando isso em um ambiente não interativo, simplesmente retornamos o gráfico
    return initial_fig
