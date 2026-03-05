import numpy as np


class Backtester:

    def __init__(self, initial_capital=10000):
        self.initial_capital = initial_capital

    def run(self, prices, predictions):

        capital = self.initial_capital
        position = 0
        portfolio_values = []

        for i in range(len(prices) - 1):

            current_price = prices[i]
            next_price = prices[i + 1]

            # Trading Signal
            if predictions[i] > current_price:
                position = 1  # long
            else:
                position = -1  # short

            daily_return = (next_price - current_price) / current_price
            capital *= (1 + position * daily_return)

            portfolio_values.append(capital)

        return {
            "final_capital": capital,
            "return_pct": ((capital - self.initial_capital)
                           / self.initial_capital) * 100,
            "equity_curve": portfolio_values
        }
#add buy and hold benchmark
    def buy_and_hold(prices, initial_capital=10000):

        start_price = prices[0]
        end_price = prices[-1]

        return initial_capital * (end_price / start_price)