import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api.weather_api import fetch_weather_data
import tkinter as tk
from tkinter import ttk, messagebox
from api.stocks_api import fetch_stock_data  # Keep this even if unused yet
from api.news_api import fetch_news_data     # Same here
from api.covid_api import fetch_covid_data   # And here
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import traceback  # For detailed error reporting

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
            # Fetch weather data
            data = fetch_weather_data(city)
            if not data:
                raise ValueError("No data received from API.")
            
            print("API Response:", data)  # For debugging, can be removed later
            
            # Check if the data contains the expected keys
            if 'main' not in data:
                raise KeyError("Missing 'main' key in response")
            
            # Proceed with weather info extraction if 'main' key is present
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
        
        except KeyError as e:
            print(f"Error: Missing key in response: {e}")  # Specific key missing
            messagebox.showerror("Error", f"The weather data is missing expected information: {e}")
        
        except ValueError as e:
            print(f"Error: {e}")
            messagebox.showerror("Error", str(e))
        
        except Exception as e:
            print(f"Error fetching weather data: {e}")  # General error
            messagebox.showerror("Error", f"Failed to fetch weather: {e}")
            print(traceback.format_exc())  # Print detailed traceback for debugging

    def plot_weather(self, data):
        self.clear_frame(self.weather_plot_frame)
        fig, ax = plt.subplots(figsize=(6, 3))
        ax.bar(["Temperature (°C)"], [data["main"]["temp"]], color='skyblue')
        ax.set_title(f"Weather in {data['name']}")
        plt.tight_layout()
        self.embed_plot(fig, self.weather_plot_frame)
    
    # Placeholder for Stock Tab
    def create_stock_tab(self):
        tab = tk.Frame(self.notebook)
        self.notebook.add(tab, text="Stocks")
        tk.Label(tab, text="Stock tab coming soon!").pack(pady=20)

    # Placeholder for News Tab
    def create_news_tab(self):
        tab = tk.Frame(self.notebook)
        self.notebook.add(tab, text="News")
        tk.Label(tab, text="News tab coming soon!").pack(pady=20)

    # Placeholder for COVID-19 Tab
    def create_covid_tab(self):
        tab = tk.Frame(self.notebook)
        self.notebook.add(tab, text="COVID-19")
        tk.Label(tab, text="COVID-19 tab coming soon!").pack(pady=20)
    
    # Utility methods
    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()
    
    def embed_plot(self, fig, frame):
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack()
