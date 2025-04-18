import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import traceback
import requests
import pandas as pd
from geopy.geocoders import Nominatim

STOCK_API_KEY = "N1SGCNX71B12KFC2"
NEWS_API_KEY = "e34b8e724ef84257a0612a688007e273" 

def fetch_stock_data(symbol):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={STOCK_API_KEY}"
    response = requests.get(url)
    data = response.json()

    if "Error Message" in data:
        raise Exception("Invalid stock symbol!")

    time_series = data.get("Time Series (Daily)", {})
    if not time_series:
        raise Exception("No data available!")

    df = pd.DataFrame(time_series).T
    df.index = pd.to_datetime(df.index)
    df = df.rename(columns={
        "1. open": "Open",
        "2. high": "High",
        "3. low": "Low",
        "4. close": "Close",
        "5. volume": "Volume"
    })

    return df.astype(float)

def fetch_news_data(keyword):
    url = f"https://newsapi.org/v2/everything?q={keyword}&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    data = response.json()
    
    if data.get("status") != "ok":
        raise Exception("Failed to fetch news!")
    
    return data.get("articles", [])[:5]  # Return top 5 articles

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
        API_KEY = "9bec9e6444e7cf3de8ac3d384ff22c7a"
        base_url = "https://api.agromonitoring.com/agro/1.0/weather"

        try:
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

        weather_params = {
            'Temperature': data["main"]["temp"],
            'Humidity': data["main"]["humidity"],
            'Wind Speed': data["wind"]["speed"],
            'Pressure': data["main"]["pressure"]/10
        }

        ax.bar(weather_params.keys(), weather_params.values(), color=['skyblue', 'lightgreen', 'orange', 'pink'])
        ax.set_title(f"Weather in {self.city_entry.get()}")
        ax.set_ylabel("Value")
        plt.xticks(rotation=45)
        plt.tight_layout()
        self.embed_plot(fig, self.weather_plot_frame)

    def create_stock_tab(self):
        tab = tk.Frame(self.notebook)
        self.notebook.add(tab, text="Stocks")

        tk.Label(tab, text="Enter Stock Symbol (e.g., AAPL):").pack(pady=5)
        self.stock_entry = tk.Entry(tab, width=20)
        self.stock_entry.pack(pady=5)

        tk.Button(tab, text="Fetch Stock Data", command=self.fetch_stock).pack(pady=10)

        self.stock_result = tk.Text(tab, height=10, width=80)
        self.stock_result.pack(pady=10)

        self.stock_plot_frame = tk.Frame(tab)
        self.stock_plot_frame.pack()

    def fetch_stock(self):
        symbol = self.stock_entry.get().upper()
        if not symbol:
            messagebox.showerror("Error", "Please enter a stock symbol!")
            return

        try:
            df = fetch_stock_data(symbol)
            latest_data = df.iloc[-1]

            self.stock_result.delete(1.0, tk.END)
            self.stock_result.insert(tk.END, f"Latest data for {symbol}:\n")
            self.stock_result.insert(tk.END, f"Date: {df.index[-1].date()}\n")
            self.stock_result.insert(tk.END, f"Open: ${latest_data['Open']:.2f}\n")
            self.stock_result.insert(tk.END, f"High: ${latest_data['High']:.2f}\n")
            self.stock_result.insert(tk.END, f"Low: ${latest_data['Low']:.2f}\n")
            self.stock_result.insert(tk.END, f"Close: ${latest_data['Close']:.2f}\n")
            self.stock_result.insert(tk.END, f"Volume: {int(latest_data['Volume'])}\n")

            self.plot_stock(df, symbol)

        except Exception as e:
            messagebox.showerror("Error", str(e))
            print(traceback.format_exc())

    def plot_stock(self, df, symbol):
        self.clear_frame(self.stock_plot_frame)
        fig, ax = plt.subplots(figsize=(6, 3))

        ax.plot(df.index[-30:], df['Close'].tail(30), marker='o', linestyle='-', color='blue')
        ax.set_title(f"{symbol} Closing Prices (Last 30 Days)")
        ax.set_ylabel("Price (USD)")
        ax.set_xlabel("Date")
        ax.tick_params(axis='x', rotation=45)
        plt.tight_layout()

        self.embed_plot(fig, self.stock_plot_frame)

    def create_news_tab(self):
        tab = tk.Frame(self.notebook)
        self.notebook.add(tab, text="News")

        tk.Label(tab, text="Enter Keyword for News Search:").pack(pady=5)
        self.news_entry = tk.Entry(tab, width=30)
        self.news_entry.pack(pady=5)

        tk.Button(tab, text="Fetch News", command=self.fetch_news).pack(pady=10)

        self.news_result = tk.Text(tab, height=15, width=80)
        self.news_result.pack(pady=10)

    def fetch_news(self):
        keyword = self.news_entry.get()
        if not keyword:
            messagebox.showerror("Error", "Please enter a keyword for news!")
            return

        try:
            articles = fetch_news_data(keyword)
            self.news_result.delete(1.0, tk.END)
            if articles:
                for i, article in enumerate(articles):
                    self.news_result.insert(tk.END, f"{i+1}. {article['title']}\n")
                    self.news_result.insert(tk.END, f"Source: {article['source']['name']}\n")
                    self.news_result.insert(tk.END, f"Published at: {article['publishedAt']}\n")
                    self.news_result.insert(tk.END, f"Description: {article['description']}\n")
                    self.news_result.insert(tk.END, "-"*80 + "\n")
            else:
                self.news_result.insert(tk.END, "No articles found.")

        except Exception as e:
            messagebox.showerror("Error", str(e))
            print(traceback.format_exc())

    def create_covid_tab(self):
        tab = tk.Frame(self.notebook)
        self.notebook.add(tab, text="COVID-19")
        tk.Label(tab, text="COVID-19 tab coming soon!").pack(pady=20)

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
