import numpy as np


class Backtester:
    """Simple long/short backtester with a buy-and-hold benchmark."""

    def __init__(self, initial_capital: float = 10_000.0):
        self.initial_capital = initial_capital

    def run(self, prices, predictions) -> dict:
        """
        Simulate a long/short strategy:
          - Go long  if predicted_price > current_price
          - Go short if predicted_price <= current_price

        Parameters
        ----------
        prices      : list or np.ndarray of actual close prices
        predictions : list or np.ndarray of model-predicted prices (same length)

        Returns
        -------
        dict with keys: final_capital, return_pct, equity_curve
        """
        capital = self.initial_capital
        portfolio_values = []

        for i in range(len(prices) - 1):
            current_price = prices[i]
            next_price = prices[i + 1]

            # Trading signal
            position = 1 if predictions[i] > current_price else -1  # long / short

            daily_return = (next_price - current_price) / current_price
            capital *= (1 + position * daily_return)
            portfolio_values.append(capital)

        return {
            "final_capital": capital,
            "return_pct": ((capital - self.initial_capital) / self.initial_capital) * 100,
            "equity_curve": portfolio_values,
        }

    @staticmethod
    def buy_and_hold(prices, initial_capital: float = 10_000.0) -> dict:
        """
        Passive buy-and-hold benchmark.

        Returns the same dict shape as run() so results can be compared directly.
        """
        start_price = prices[0]
        end_price = prices[-1]
        final_capital = initial_capital * (end_price / start_price)

        # Reconstruct a simple equity curve assuming linear price path
        equity_curve = [
            initial_capital * (prices[i] / start_price)
            for i in range(1, len(prices))
        ]

        return {
            "final_capital": final_capital,
            "return_pct": ((final_capital - initial_capital) / initial_capital) * 100,
            "equity_curve": equity_curve,
        }
