import os
import requests
from dotenv import load_dotenv

load_dotenv()

def get_weather_data(city):

    """
    It retrieves weather data for the stated city from the WeatherApi.
    """

    api_key = os.getenv("WEATHER_API_KEY")

    """
    base_url = http://api.weatherapi.com 
    """
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"

    try:
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()

        location_name = data['location']['name']
        country = data['location']['country']
        temp_c = data['current']['temp_c']
        feels_like = data['current']['feelslike_c'] 
        condition = data['current']['condition']['text']
        humidity = data['current']['humidity']

        print(f"\n--- Weather Report for {location_name}/{country} ---")
        print(f"Condition: {condition}")
        print(f"Tempature: {temp_c}°C (Feels like: {feels_like}°C)")
        print(f"Humidity: {humidity}%")

    except requests.exceptions.HTTPError:
        print(f"Error: City '{city}' not found!")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    print("Welcome to the Weather Dashboard!")

    target_city = input("Enter the city name: ")
    
    get_weather_data(target_city)
