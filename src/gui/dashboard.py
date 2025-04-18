import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import traceback
import requests
from geopy.geocoders import Nominatim

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

    def fetch_weather_data(self, city):
        API_KEY = "9bec9e6444e7cf3de8ac3d384ff22c7a"  # AgroMonitoring API key
        base_url = "https://api.agromonitoring.com/agro/1.0/weather"
        
        try:
            # First get coordinates for the city
            geolocator = Nominatim(user_agent="weather_app")
            location = geolocator.geocode(city)
            
            if not location:
                raise Exception("City not found!")

            params = {
                'lat': location.latitude,
                'lon': location.longitude,
                'appid': API_KEY
            }
            
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            
            data = response.json()
            print("API Response:", data)  # Debug print
            
            # AgroMonitoring API returns different structure than OpenWeatherMap
            # Let's standardize the response format
            standardized_data = {
                'name': city,
                'main': {
                    'temp': data.get('temp', {}).get('day', 0),
                    'humidity': data.get('humidity', 0),
                    'pressure': data.get('pressure', 0)
                },
                'weather': [{
                    'description': data.get('weather', [{}])[0].get('description', 'N/A')
                }],
                'wind': {
                    'speed': data.get('wind_speed', 0)
                }
            }
            
            return standardized_data
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch weather data: {e}")
        except Exception as e:
            raise Exception(f"Error processing weather data: {e}")

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
            data = self.fetch_weather_data(city)
            if not data:
                raise ValueError("No data received from API.")
            
            weather_info = (
                f"Weather in {city}:\n"
                f"Temperature: {data['main']['temp']}°C\n"
                f"Humidity: {data['main']['humidity']}%\n"
                f"Conditions: {data['weather'][0]['description']}\n"
                f"Wind Speed: {data['wind']['speed']} m/s\n"
                f"Pressure: {data['main']['pressure']} hPa"
            )
            self.weather_result.delete(1.0, tk.END)
            self.weather_result.insert(tk.END, weather_info)
            self.plot_weather(data)
        
        except KeyError as e:
            print(f"Error: Missing key in response: {e}")
            messagebox.showerror("Error", f"The weather data is missing expected information: {e}")
        except Exception as e:
            print(f"Error fetching weather data: {e}")
            messagebox.showerror("Error", f"Failed to fetch weather: {e}")
            print(traceback.format_exc())

    def plot_weather(self, data):
        self.clear_frame(self.weather_plot_frame)
        fig, ax = plt.subplots(figsize=(6, 3))
        
        # Plot multiple weather parameters
        weather_params = {
            'Temperature': data["main"]["temp"],
            'Humidity': data["main"]["humidity"],
            'Wind Speed': data["wind"]["speed"],
            'Pressure': data["main"]["pressure"]/10  # Convert to kPa for better scale
        }
        
        ax.bar(weather_params.keys(), weather_params.values(), color=['skyblue', 'lightgreen', 'orange', 'pink'])
        ax.set_title(f"Weather in {self.city_entry.get()}")
        ax.set_ylabel("Value")
        plt.xticks(rotation=45)
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

if __name__ == "__main__":
    root = tk.Tk()
    app = IntelligentApp(root)
    root.mainloop()
