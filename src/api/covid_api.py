import tkinter as tk
from tkinter import ttk  # Add this import for ttk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import requests
from datetime import datetime
import pandas as pd


# The CovidDataHandler class with the previous functionality
class CovidDataHandler:
    def __init__(self):
        self.BASE_URL = "https://disease.sh/v3/covid-19"
        self.last_updated = None
        self.cached_data = None

    def fetch_global_data(self) -> dict:
        """Fetch global COVID-19 statistics"""
        try:
            response = requests.get(f"{self.BASE_URL}/all")
            response.raise_for_status()
            data = response.json()
            
            # Convert timestamp to readable format
            if 'updated' in data:
                self.last_updated = datetime.fromtimestamp(data['updated']/1000).strftime('%Y-%m-%d %H:%M:%S')
                data['lastUpdated'] = self.last_updated
            
            self.cached_data = data
            return data
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch COVID-19 data: {e}")

    def get_dataframe(self) -> pd.DataFrame:
        """Convert API data to pandas DataFrame"""
        if not self.cached_data:
            self.fetch_global_data()
        
        # Create DataFrame from the nested dictionary
        df = pd.DataFrame([self.cached_data])
        
        # Convert timestamp to datetime
        if 'updated' in df.columns:
            df['lastUpdated'] = pd.to_datetime(df['updated'], unit='ms')
        
        return df

# Integration with the IntelligentApp class
class IntelligentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Intelligent Data Dashboard")
        self.root.geometry("1000x700")
        
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.covid_handler = CovidDataHandler()  # Using the CovidDataHandler

        self.create_covid_tab()  # Initialize the COVID tab

    def create_covid_tab(self):
        """Create the COVID-19 tab"""
        tab = tk.Frame(self.notebook)
        self.notebook.add(tab, text="COVID-19")
        
        tk.Label(tab, text="Global COVID-19 Statistics").pack(pady=10)
        
        # Text widget to display the fetched data
        self.covid_text = tk.Text(tab, height=15, width=80)
        self.covid_text.pack(pady=10)
        
        self.covid_plot_frame = tk.Frame(tab)
        self.covid_plot_frame.pack()
        
        # Button to refresh the data
        tk.Button(
            tab, 
            text="Refresh Data", 
            command=self.display_covid_data
        ).pack(pady=10)

    def display_covid_data(self):
        """Fetch, display, and plot the COVID-19 data"""
        try:
            data = self.covid_handler.fetch_global_data()
            df = self.covid_handler.get_dataframe()
            
            # Display key statistics
            stats_text = (
                f"Last Updated: {data.get('lastUpdated', 'N/A')}\n"
                f"Total Cases: {data.get('cases', 0):,}\n"
                f"Total Deaths: {data.get('deaths', 0):,}\n"
                f"Total Recovered: {data.get('recovered', 0):,}\n"
                f"Active Cases: {data.get('active', 0):,}\n"
                f"Critical Cases: {data.get('critical', 0):,}\n"
                f"Cases Today: {data.get('todayCases', 0):,}\n"
                f"Deaths Today: {data.get('todayDeaths', 0):,}\n"
                f"Recovered Today: {data.get('todayRecovered', 0):,}\n"
                f"Tests Conducted: {data.get('tests', 0):,}\n"
            )
            
            # Insert the statistics into the text widget
            self.covid_text.delete(1.0, tk.END)
            self.covid_text.insert(tk.END, stats_text)
            
            # Plot the data
            self.plot_covid_data(df)
            
        except Exception as e:
            messagebox.showerror("COVID-19 Data Error", str(e))

    def plot_covid_data(self, df: pd.DataFrame):
        """Plot the global COVID-19 statistics"""
        self.clear_frame(self.covid_plot_frame)
        
        if df.empty:
            return
        
        fig, ax = plt.subplots(figsize=(10, 5))
        
        # Select metrics to plot
        metrics = {
            'cases': 'Total Cases',
            'deaths': 'Total Deaths', 
            'recovered': 'Total Recovered',
            'active': 'Active Cases'
        }
        
        # Plot each metric
        for i, (col, label) in enumerate(metrics.items()):
            if col in df.columns:
                ax.bar(label, df[col].iloc[0], color=plt.cm.tab10(i))
        
        ax.set_title("Global COVID-19 Statistics")
        ax.set_ylabel("Count")
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, master=self.covid_plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def clear_frame(self, frame):
        """Clear all widgets from the given frame"""
        for widget in frame.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = IntelligentApp(root)
    root.mainloop()
