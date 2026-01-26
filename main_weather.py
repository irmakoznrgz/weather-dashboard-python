import os
import requests
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

def get_full_hourly_forecast(city):

    api_key = os.getenv("WEATHER_API_KEY")

    base_url = "http://api.weatherapi.com/v1/"
    url = f"{base_url}forecast.json?key={api_key}&q={city}&days=7"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        print(f"\n{'='*50}")
        print(f"  FULL HOURLY REPORT: {data['location']['name']}/{data['location']['country']}")
        print(f"\n{'='*50}")

        for day in data['forecast']['forecastday']:
            raw_date = day['date']
            date_obj = datetime.strptime(raw_date, '%Y-%m-%d')
            formatted_date = date_obj.strftime('%d.%m.%Y')
            day_name = date_obj.strftime('%A')

            print(f"\n DATE: {formatted_date} | {day_name}")
            print(f"{'-'*50}")

            print(f"{'TIME':<8} | {'TEMP':<7} | {'CONDİTİON':<20} | {'RAIN':<8} | {'SNOW':<8}")
            print(f"{'-'*70}")

            for hour in day['hour']:

                time_only = hour['time'].split(" ")[1]
                temp = round(hour['temp_c'])
                condition = hour['condition']['text']
                rain_chance = hour['chance_of_rain']
                snow_chance = hour['chance_of_snow']

                print(f"{time_only:<8} | {temp:>3}°C | {condition:<20} | %{rain_chance:<5} | %{snow_chance:<5}")

                if temp < 0:
                    print(f"DANGER! Freezing temperatures at {time_only} watch out for black ice.")

                elif rain_chance >= 50:
                    print(f"It's likely to rain %{rain_chance} Don't forget your umbrella!")

                elif snow_chance >=40:
                    print(f"High chance of snow %{snow_chance}!")

    except requests.exceptions.HTTPError as errh:
        print(f"HTTP error occurred: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print("Connectin Error. Check the internet connection!")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    print("Welcome to the Advenced Weather Dashboard!")

    target_city = input("Enter the city name for a 24 hour analysis: ")
    get_full_hourly_forecast(target_city)
