import tkinter as tk
from tkinter import ttk, messagebox
from api.weather_api import fetch_weather_data
from api.stocks_api import fetch_stock_data
from api.news_api import fetch_news_data
from api.covid_api import fetch_covid_data
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class IntelligentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Intelligent Data Dashboard")
        self.root.geometry("1000x700")
        
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        self.create_weather_tab()
        self.create_stock_tab()
        self.create_news_tab()
        self.create_covid_tab()
    
    # Weather Tab methods
    def create_weather_tab(self):
        tab = tk.Frame(self.notebook)
        self.notebook.add(tab, text="Weather")
        
        tk.Label(tab, text="Enter City:").pack(pady=5)
        self.city_entry = tk.Entry(tab, width=30)
        self.city_entry.pack(pady=5)
        
        tk.Button(tab, text="Fetch Weather", command=self.fetch_weather).pack(pady=10)
        
        self.weather_result = tk.Text(tab, height=10, width=80)
        self.weather_result.pack(pady=10)
        
        self.weather_plot_frame = tk.Frame(tab)
        self.weather_plot_frame.pack()
    
    def fetch_weather(self):
        city = self.city_entry.get()
        if not city:
            messagebox.showerror("Error", "Please enter a city!")
            return
        
        try:
            data = fetch_weather_data(city)
            weather_info = (
                f"Weather in {city}:\n"
                f"Temperature: {data['main']['temp']}°C\n"
                f"Humidity: {data['main']['humidity']}%\n"
                f"Conditions: {data['weather'][0]['description']}\n"
                f"Wind Speed: {data['wind']['speed']} m/s"
            )
            self.weather_result.delete(1.0, tk.END)
            self.weather_result.insert(tk.END, weather_info)
            self.plot_weather(data)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch weather: {e}")
    
    def plot_weather(self, data):
        self.clear_frame(self.weather_plot_frame)
        fig, ax = plt.subplots(figsize=(6, 3))
        ax.bar(["Temperature (°C)"], [data["main"]["temp"]], color='skyblue')
        ax.set_title(f"Weather in {data['name']}")
        plt.tight_layout()
        self.embed_plot(fig, self.weather_plot_frame)
    
    # ... (similar methods for other tabs)
    
    # Utility methods
    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()
    
    def embed_plot(self, fig, frame):
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack()
