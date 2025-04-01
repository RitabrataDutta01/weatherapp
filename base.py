import tkinter as tk
from tkinter import ttk
import requests
import json
from tkinter import messagebox
import threading

root = tk.Tk()
root.title("Weather App")
root.geometry("500x500")

unit = tk.StringVar()
unit.set("Celcius")

history = []

# Function to convert temperature from Celsius to Fahrenheit
def to_fahrenheit(temp):
    return (temp * 9/5) + 32

# Function to search for weather data
def search():
    city = tb.get()
    
    if not city:
        messagebox.showerror("Input Error", "Please enter a city name.")
        search_btn.config(state=tk.NORMAL)
        return

    threading.Thread(target= fetch_weather, args=(city,), daemon= True).start()

def fetch_weather(city):
    try:
        url = f"http://api.weatherapi.com/v1/current.json?key="API KEY"&q={city}"
        response = requests.get(url)
        data = json.loads(response.text)
        city = data["location"]["name"]
        temp = data["current"]["temp_c"]
        desc = data["current"]["condition"]["text"]
        
        if "air_quality" in data["current"]:
            aqi = data["current"]["air_quality"].get("us-epa-index", "N/A")
        else:
            aqi = "N/A"
        
        if unit.get() == "Fahrenheit":
            temp = to_fahrenheit(temp)
        
        # Add to history
        if len(history) >= 5:
            history.pop(0)
        
        history.append((city, f"{temp:.2f} °{'F' if unit.get() == 'Fahrenheit' else 'C'}", desc, aqi))

        # Update Treeview on the main thread
        root.after(0, update_treeview)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
    finally:
        search_btn.config(state=tk.NORMAL)
    
def update_treeview():
    treeview.delete(*treeview.get_children())
    for entry in history:
        treeview.insert("", "end", values=entry)
    


# GUI elements
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

tf = tk.Frame(root)
tf.grid(row=3, column=0, columnspan=2)

treeview = ttk.Treeview(tf, columns=("City", "Temperature", "Description", "AQI"), show="headings", height=5)
treeview.heading("City", text="City")
treeview.heading("Temperature", text="Temperature")
treeview.heading("Description", text="Description")
treeview.heading("AQI", text="AQI")

treeview.column("City", width=100, anchor="center")
treeview.column("Temperature", width=100, anchor="center")
treeview.column("Description", width=150, anchor="center")
treeview.column("AQI", width=100, anchor="center")

treeview.grid(row=3, column=0, columnspan=3)

root.grid_rowconfigure(0, weight=1, minsize=50)
root.grid_rowconfigure(1, weight=1, minsize=50)
root.grid_rowconfigure(2, weight=1, minsize=50)
root.grid_rowconfigure(3, weight=3, minsize=200)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

if __name__ == "__main__":
    root.mainloop()
