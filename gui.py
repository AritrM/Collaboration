import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import requests
import geocoder
from geopy.geocoders import Nominatim
import io
import json

# Your OpenWeatherMap API key
API_KEY = "VGH2EXmyclRgyevMXbNcvtDEuZBvV2l4"
query = {
    "lang" : "en",
    "units" : "si",
    "exclude":"hourly,minutely,flag"
}


icon_pack = {
    "clear-day": "01d",
    "clear-night": "01n",
    "cloudy": "04d",
    "partly-cloudy-day": "02d",
    "partly-cloudy-night": "02n",
    "rain": "09d",
    "light-rain": "10d",
    "heavy-rain": "09d",
    "snow": "13d",
    "light-snow": "13d",
    "heavy-snow": "13d",
    "sleet": "13d",
    "very-light-sleet": "13d",
    "light-sleet": "13d",
    "heavy-sleet": "13d",
    "wind": "50d",
    "breezy": "50d",
    "dangerous-wind": "50d",
    "mist": "50d",
    "fog": "50d",
    "haze": "50d",
    "smoke": "50d",
    "drizzle": "09d",
    "flurries": "13d",
    "precipitation": "09d",
    "mostly-clear-day": "02d",
    "mostly-clear-night": "02n",
    "mostly-cloudy-day": "04d",
    "mostly-cloudy-night": "04n",
    "possible-rain-day": "10d",
    "possible-rain-night": "10n",
    "possible-snow-day": "13d",
    "possible-snow-night": "13n",
    "possible-sleet-day": "13d",
    "possible-sleet-night": "13n",
    "possible-precipitation-day": "09d",
    "possible-precipitation-night": "09n"
}



city = geocoder.ip('me').city
lat,lon = geocoder.ip('me').latlng
lalong = f"{lat},{lon}"


def get_coordinates(city):
    geolocator = Nominatim(user_agent="weather_app")
    location = geolocator.geocode(city)
    return location.latitude, location.longitude

lat, lon = get_coordinates(city)


def get_weather(city):
    lat, lon = get_coordinates(city)
    loc = f"{lat},{lon}"
    url = f"https://api.pirateweather.net/forecast/{API_KEY}/{loc}"
    response = requests.get(url,params=query).json()
    return response

def get_weather_icon(icon_code):
    url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
    response = requests.get(url)
    img_data = response.content
    img = Image.open(io.BytesIO(img_data))
    return ImageTk.PhotoImage(img)

def update_weather(event):
    city = city_entry.get()
    if not city:
        messagebox.showwarning("Input Error", "Please enter a city name.")
        return

    try:
        
        weather_data = get_weather(city)
        # if weather_data.get("cod") != 200:
        #     messagebox.showerror("Error", weather_data.get("message", "Unknown error"))
        #     return

        lat, lon = get_coordinates(city)
        elevation = weather_data["elevation"]
        offset = weather_data["offset"]
        weather = weather_data["daily"]["data"][0]["summary"].title()
        if weather_data["currently"]["temperature"] > -273 :
            
            temp = f"{weather_data["currently"]["temperature"]}°C"
        else:
            temp = "data error"
        if weather_data["currently"]["humidity"] < 0:
            humidity = f"{weather_data["currently"]["humidity"]}%"
        else:
            humidity = "data error"
        wind = weather_data["currently"]["windSpeed"]
        icon_n = weather_data["daily"]["data"][0]["icon"]
        icon_code = icon_pack[icon_n]

        icon = get_weather_icon(icon_code)
        icon_label.config(image=icon)
        icon_label.image = icon

        result_label.config(text=(
            f"City: {city}\n"
            f"Latitude: {lat:.2f}, Longitude: {lon:.2f}\n"
            f"Elevation: {elevation} m\n"
            f"Offset: {offset} hr\n"
            f"Weather: {weather}\n"
            f"Today in short: {icon_n}\n"
            f"Temperature: {temp}\n"
            f"Humidity: {humidity}\n"
            f"Wind Speed: {wind} m/s"
        ))

    except Exception as e:
        messagebox.showerror("Error", str(e))

# GUI Setup
root = tk.Tk()
root.title("🌦️ Weather App")
root.geometry("400x500")
root.configure(bg="#e0f7fa")

style = ttk.Style()
style.theme_use('clam')
style.configure("TButton", font=("Arial", 12), padding=6)
style.configure("TLabel", font=("Arial", 12), background="#e0f7fa")

ttk.Label(root, text="Enter City Name:").pack(pady=10)
city_entry = ttk.Entry(root, font=("Arial", 12))
city_entry.pack(pady=5)

ttk.Button(root, text="Get Weather", command=update_weather).pack(pady=10)

icon_label = ttk.Label(root)
icon_label.pack(pady=10)

result_label = ttk.Label(root, text="", justify="left")
result_label.pack(pady=10)

# Autofill city from IP
default_city = city
city_entry.insert(0, default_city)


root.bind("<Return>", update_weather)

root.mainloop()