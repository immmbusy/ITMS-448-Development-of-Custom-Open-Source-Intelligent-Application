import pandas as pd
import matplotlib.pyplot as plt

class TrendAnalyzer:
    def __init__(self, data):
        self.df = pd.DataFrame(data)
    
    def plot_trend(self, column: str, output_path: str):
        """Generate and save trend plots"""
        plt.figure(figsize=(10, 6))
        self.df[column].plot(title=f"{column} Trend Analysis")
        plt.savefig(output_path)
        plt.close()
