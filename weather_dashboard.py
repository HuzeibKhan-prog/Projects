import io
import requests
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates

API_KEY = "95cdb2fd6bf94206884114904260602"
CITY = "Mumbai"

def fetch_weather():
    try:
        city = city_entry.get() or CITY
        url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={city}&days=3"

        response = requests.get(url)
        data = response.json()
        if "error" in data:
            messagebox.showerror("Error", data["error"]["message"])
            return

        for widget in scrollable_frame.winfo_children():
            widget.destroy()

        temps, times = [], []
        row = 0

        for forecast in data["forecast"]["forecastday"]:
            for hour in forecast["hour"][::6]:
                temp = hour["temp_c"]
                time = datetime.strptime(hour["time"], "%Y-%m-%d %H:%M")
                temps.append(temp)
                times.append(time)

                condition = hour["condition"]["text"]

                icon_url = "http:" + hour["condition"]["icon"]
                icon_response = requests.get(icon_url)
                icon_img = Image.open(io.BytesIO(icon_response.content))
                icon_img = icon_img.resize((30,30))

                icon_photo = ImageTk.PhotoImage(icon_img)

                label = tk.Label(scrollable_frame,
                                 text=f"{time.strftime('%d %b %H:%M')} → {temp} °C, {condition}",
                                 font=("Arial", 12), anchor="w", bg="white",
                                 image=icon_photo, compound="left")
                label.image = icon_photo
                label.grid(row=row, column=0, sticky="w", padx=10, pady=2)
                row += 1

        last_updated.config(text=f"Last updated: {datetime.now().strftime('%H:%M:%S')}")
        plot_graph(times, temps, city)

    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch weather data:\n{e}")

def plot_graph(times, temps, city):
    for widget in graph_frame.winfo_children():
        widget.destroy()

    fig = Figure(figsize=(7,4), dpi=100)
    ax = fig.add_subplot(111)
    ax.plot(times, temps, marker="o", ls="--", color="blue")
    ax.set_title(f"Temperature Trend ({city})")
    ax.set_xlabel("Time")
    ax.set_ylabel("Temp (°C)")
    ax.grid(True)

    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d %H:%M"))
    fig.autofmt_xdate(rotation=45)

    fig.tight_layout()
    fig.subplots_adjust(bottom=0.45)

    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True, pady=10)

# ---------------- GUI ----------------
root = tk.Tk()
root.title("🌤Weather Dashboard")
root.geometry("800x650")
root.configure(bg="lightgray")

title = tk.Label(root, text="Weather Forecast", font=("Arial", 18, "bold"), bg="lightgray")
title.pack(pady=10)

top_frame = tk.Frame(root, bg="lightgray")
top_frame.pack(pady=5)

city_entry = tk.Entry(top_frame, font=("Arial", 12))
city_entry.grid(row=0, column=0, padx=5)
city_entry.insert(0, CITY)

refresh_btn = tk.Button(top_frame, text="Refresh", command=fetch_weather,
                        bg="green", fg="white", font=("Arial", 12))
refresh_btn.grid(row=0, column=1, padx=5)

frame = tk.Frame(root, bg="white")
frame.pack(fill="both", expand=True, padx=10, pady=10)

forecast_canvas = tk.Canvas(frame, bg="white")
scrollbar = tk.Scrollbar(frame, orient="vertical", command=forecast_canvas.yview)
scrollable_frame = tk.Frame(forecast_canvas, bg="white")

scrollable_frame.bind(
    "<Configure>",
    lambda e: forecast_canvas.configure(scrollregion=forecast_canvas.bbox("all"))
)

forecast_canvas.create_window((0,0), window=scrollable_frame, anchor="nw")
forecast_canvas.configure(yscrollcommand=scrollbar.set)

forecast_canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

graph_frame = tk.Frame(root, bg="white", height=300)
graph_frame.pack(fill="x", expand=False, padx=10, pady=10)

last_updated = tk.Label(root, text="", font=("Arial", 10), bg="lightgray")
last_updated.pack(pady=5)

fetch_weather()
root.mainloop()
