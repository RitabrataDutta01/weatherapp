import tkinter as tk
from tkinter import ttk
import requests
import json
from tkinter import messagebox
import threading

root = tk.Tk()
root.title("Weather App")
root.geometry("800x600")

unit = tk.StringVar()
unit.set("Celsius")

photo_image = None
history = []
forecast_history = []

def to_fahrenheit(temp):
    return (temp * 9/5) + 32

def search():
    city = tb.get()
    
    if not city:
        messagebox.showerror("Input Error", "Please enter a city name.")
        search_btn.config(state=tk.NORMAL)
        return

    threading.Thread(target=fetch_weather, args=(city,), daemon=True).start()

def fetch_weather(city):
    try:
        url = f"http://api.weatherapi.com/v1/forecast.json?key=9e01f9a69b824793a5474312252203&q={city}&days=3"
        response = requests.get(url)
        data = json.loads(response.text)

        city = data["location"]["name"]
        current_weather = data["current"]
        forecasts = data["forecast"]["forecastday"]

        temp = current_weather["temp_c"]
        desc = current_weather["condition"]["text"]
        if "air_quality" in current_weather:
            aqi = current_weather["air_quality"].get("us-epa-index", "N/A")
        else:
            aqi = "N/A"

        if unit.get() == "Fahrenheit":
            temp = to_fahrenheit(temp)

        history.clear()
        history.append((city, f"{temp:.2f} °{'F' if unit.get() == 'Fahrenheit' else 'C'}", desc, aqi))

        forecast_history.clear()
        for forecast in forecasts:
            date = forecast["date"]
            temp = forecast["day"]["avgtemp_c"]
            desc = forecast["day"]["condition"]["text"]
            if "air_quality" in forecast["day"]:
                aqi = forecast["day"]["air_quality"].get("us-epa-index", "N/A")
            else:
                aqi = "N/A"

            if unit.get() == "Fahrenheit":
                temp = to_fahrenheit(temp)

            forecast_history.append((city, f"{temp:.2f} °{'F' if unit.get() == 'Fahrenheit' else 'C'}", desc, aqi, date))

        root.after(0, update_current_weather)
        root.after(0, update_forecast)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
    finally:
        search_btn.config(state=tk.NORMAL)
    
def update_current_weather():
    current_weather_treeview.delete(*current_weather_treeview.get_children())
    for entry in history:
        current_weather_treeview.insert("", "end", values=entry)

def update_forecast():
    forecast_treeview.delete(*forecast_treeview.get_children())
    for entry in forecast_history:
        forecast_treeview.insert("", "end", values=entry)

tbl = tk.Label(root, text="Enter City Name", font=("Helvetica", 15))
tbl.grid(row=0, column=0)
tb = tk.Entry(root, font=("Helvetica", 15))
tb.grid(row=0, column=1)

temp_unit = tk.Frame(root)
temp_unit.grid(row=1, column=0, columnspan=2)

celcius = tk.Radiobutton(temp_unit, text="Celsius", font=("Helvetica", 15), variable=unit, value="Celsius")
celcius.grid(row=0, column=0)

fahrenheit = tk.Radiobutton(temp_unit, text="Fahrenheit", font=("Helvetica", 15), variable=unit, value="Fahrenheit")
fahrenheit.grid(row=0, column=1)

search_btn = tk.Button(root, text="Search", font=("Helvetica", 15), command=search)
search_btn.grid(row=2, column=0, columnspan=2)

current_weather_frame = tk.LabelFrame(root, text="Current Weather", font=("Helvetica", 15), padx=10, pady=10)
current_weather_frame.grid(row=3, column=0, columnspan=2, padx=20, pady=10)

current_weather_treeview = ttk.Treeview(current_weather_frame, columns=("City", "Temperature", "Description", "AQI"), show="headings", height=3)
current_weather_treeview.heading("City", text="City")
current_weather_treeview.heading("Temperature", text="Temperature")
current_weather_treeview.heading("Description", text="Description")
current_weather_treeview.heading("AQI", text="AQI")

current_weather_treeview.column("City", width=100, anchor="center")
current_weather_treeview.column("Temperature", width=100, anchor="center")
current_weather_treeview.column("Description", width=150, anchor="center")
current_weather_treeview.column("AQI", width=100, anchor="center")

current_weather_treeview.grid(row=0, column=0, columnspan=3)

forecast_frame = tk.LabelFrame(root, text="Weather Forecast (Next 3 Days)", font=("Helvetica", 15), padx=10, pady=10)
forecast_frame.grid(row=4, column=0, columnspan=2, padx=20, pady=10)

forecast_treeview = ttk.Treeview(forecast_frame, columns=("City", "Temperature", "Description", "AQI", "Date"), show="headings", height=5)
forecast_treeview.heading("City", text="City")
forecast_treeview.heading("Temperature", text="Temperature")
forecast_treeview.heading("Description", text="Description")
forecast_treeview.heading("AQI", text="AQI")
forecast_treeview.heading("Date", text="Date")

forecast_treeview.column("City", width=100, anchor="center")
forecast_treeview.column("Temperature", width=100, anchor="center")
forecast_treeview.column("Description", width=150, anchor="center")
forecast_treeview.column("AQI", width=100, anchor="center")
forecast_treeview.column("Date", width=100, anchor="center")

forecast_treeview.grid(row=0, column=0, columnspan=3)

root.grid_rowconfigure(0, weight=1, minsize=50)
root.grid_rowconfigure(1, weight=1, minsize=50)
root.grid_rowconfigure(2, weight=1, minsize=50)
root.grid_rowconfigure(3, weight=3, minsize=200)
root.grid_rowconfigure(4, weight=3, minsize=200)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

if __name__ == "__main__":
    root.mainloop()
