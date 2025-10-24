import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import requests
import geocoder
from geopy.geocoders import Nominatim
import io

# Your OpenWeatherMap API key
API_KEY = "your_openweathermap_api_key"

def get_location():
    g = geocoder.ip('me')
    return g.city, g.latlng

def get_coordinates(city):
    geolocator = Nominatim(user_agent="weather_app")
    location = geolocator.geocode(city)
    return location.latitude, location.longitude

def get_elevation(lat, lon):
    url = f"https://api.open-elevation.com/api/v1/lookup?locations={lat},{lon}"
    response = requests.get(url).json()
    return response['results'][0]['elevation']

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url).json()
    return response

def get_weather_icon(icon_code):
    url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
    response = requests.get(url)
    img_data = response.content
    img = Image.open(io.BytesIO(img_data))
    return ImageTk.PhotoImage(img)

def update_weather():
    city = city_entry.get()
    if not city:
        messagebox.showwarning("Input Error", "Please enter a city name.")
        return

    try:
        weather_data = get_weather(city)
        if weather_data.get("cod") != 200:
            messagebox.showerror("Error", weather_data.get("message", "Unknown error"))
            return

        lat, lon = get_coordinates(city)
        elevation = get_elevation(lat, lon)

        weather = weather_data["weather"][0]["description"].title()
        temp = weather_data["main"]["temp"]
        humidity = weather_data["main"]["humidity"]
        wind = weather_data["wind"]["speed"]
        icon_code = weather_data["weather"][0]["icon"]

        icon = get_weather_icon(icon_code)
        icon_label.config(image=icon)
        icon_label.image = icon

        result_label.config(text=(
            f"City: {city}\n"
            f"Latitude: {lat:.2f}, Longitude: {lon:.2f}\n"
            f"Elevation: {elevation} m\n"
            f"Weather: {weather}\n"
            f"Temperature: {temp}°C\n"
            f"Humidity: {humidity}%\n"
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
default_city, _ = get_location()
city_entry.insert(0, default_city)

root.mainloop()