import requests
from tkinter import *
from PIL import Image, ImageTk

# Function to fetch weather
def get_weather():
    city = city_entry.get()
    if city.strip() == "":
        temp_label.config(text="Please enter a city name.")
        humidity_label.config(text="")
        desc_label.config(text="")
        wind_label.config(text="")
        icon_label.config(image="")
        return

    api_key = 'facac****************ac1383a'  # Your API key here
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()

        if data["cod"] != "404":
            main = data["main"]
            weather = data["weather"][0]
            wind = data["wind"]

            temp = main["temp"]
            humidity = main["humidity"]
            description = weather["description"].title()
            wind_speed = wind["speed"]

            temp_label.config(text=f"🌡️ Temperature: {temp}°C")
            humidity_label.config(text=f"💧 Humidity: {humidity}%")
            desc_label.config(text=f"🌥️ Condition: {description}")
            wind_label.config(text=f"🌬️ Wind Speed: {wind_speed} m/s")

            # Weather Icon
            icon_id = weather['icon']
            icon_url = f"http://openweathermap.org/img/wn/{icon_id}@2x.png"
            icon_response = requests.get(icon_url, stream=True)
            img_data = Image.open(icon_response.raw)
            icon = ImageTk.PhotoImage(img_data)
            icon_label.config(image=icon)
            icon_label.image = icon

        else:
            temp_label.config(text="❌ City not found.")
            humidity_label.config(text="")
            desc_label.config(text="")
            wind_label.config(text="")
            icon_label.config(image="")

    except Exception as e:
        temp_label.config(text="⚠️ Error fetching data.")
        humidity_label.config(text="")
        desc_label.config(text="")
        wind_label.config(text="")
        icon_label.config(image="")

# GUI setup
root = Tk()
root.title("🌦️ Weather App")
root.geometry("380x500")
root.config(bg="#eaf6f6")
root.resizable(False, False)

# Title
title_label = Label(root, text="🌤️ Weather Forecast", font=("Helvetica", 20, "bold"), bg="#eaf6f6", fg="#333")
title_label.pack(pady=15)

# Enter City Name Label
city_label = Label(root, text="Enter City Name:", font=("Helvetica", 14), bg="#eaf6f6", fg="#333")
city_label.pack()

# City Entry Box
city_entry = Entry(root, font=("Helvetica", 16), width=20, bd=2, relief="groove", justify="center")
city_entry.pack(pady=10)

# Get Weather Button
get_weather_btn = Button(root, text="Get Weather", font=("Helvetica", 14, "bold"), bg="#1d3557", fg="white", bd=0, padx=15, pady=5, command=get_weather)
get_weather_btn.pack(pady=10)

# Weather Icon
icon_label = Label(root, bg="#eaf6f6")
icon_label.pack(pady=15)

# Weather Info Labels
temp_label = Label(root, text="", font=("Helvetica", 16), bg="#eaf6f6", fg="#333")
temp_label.pack(pady=5)

humidity_label = Label(root, text="", font=("Helvetica", 14), bg="#eaf6f6", fg="#333")
humidity_label.pack()

desc_label = Label(root, text="", font=("Helvetica", 14), bg="#eaf6f6", fg="#333")
desc_label.pack()

wind_label = Label(root, text="", font=("Helvetica", 14), bg="#eaf6f6", fg="#333")
wind_label.pack()

root.mainloop()
