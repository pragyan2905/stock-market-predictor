import pandas as pd

class BacktestingPipeline:
    def __init__(self):
        pass

    def run_backtest(self, model, data, model_features):
        """
        Runs a simple backtest on the historical data.
        Strategy: Buy if model predicts 'Up' (1), hold for one day, then sell.
        """
        predictions = model.predict(data[model_features])
        data['prediction'] = predictions

        data['daily_return'] = data['Close'].pct_change()

        data['strategy_return'] = data['daily_return'].shift(-1) * data['prediction']

        data['cumulative_strategy_return'] = (1 + data['strategy_return']).cumprod()

        total_return = (data['cumulative_strategy_return'].iloc[-2] - 1) * 100
        
        return total_return, data