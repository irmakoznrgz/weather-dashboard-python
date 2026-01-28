import os
import requests
from dotenv import load_dotenv
from datetime import datetime, date
import matplotlib.pyplot as plt

load_dotenv()

def get_full_hourly_forecast(city):

    api_key = os.getenv("WEATHER_API_KEY")

    base_url = "http://api.weatherapi.com/v1/"
    url = f"{base_url}forecast.json?key={api_key}&q={city}&days=7"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        today_hours = []
        today_temps = []

        week_days = []
        week_avg_temps = []


        now_temp = round(data['current']['temp_c'])
        now_feels = round(data['current']['feelslike_c'])
        now_condition = data['current']['condition']['text']

        print(f"\n{'='*50}")
        print(f" FULL HOURLY REPORT: {data['location']['name']}/{data['location']['country']}")
        print(f"\n NOW: {now_temp}°C (Feels: {now_feels}°C) | {now_condition}")
        print(f"\n{'='*50}")

        current_date = date.today()
        current_hour = datetime.now().hour

        for day in data['forecast']['forecastday']:

            raw_date = day['date']
            date_obj = datetime.strptime(raw_date, '%Y-%m-%d').date()
            formatted_date = date_obj.strftime('%d.%m.%Y')


            day_name_short = date_obj.strftime('%a')
            week_days.append(day_name_short)

            week_avg_temps.append(day['day']['avgtemp_c'])


            if date_obj == current_date:
                day_label = f"Today | {date_obj.strftime('%A')}" 
            else:
                day_label = date_obj.strftime('%A')


            max_temp = round(day['day']['maxtemp_c'])
            min_temp = round(day['day']['mintemp_c'])
            avg_daily_temp = round(day['day']['avgtemp_c'])

            hourly_feels_list = [hour['feelslike_c']  for hour in day['hour']]
            avg_feels_temp = round(sum(hourly_feels_list) / len(hourly_feels_list))

            print(f"\nDATE: {formatted_date} | {day_label} | {max_temp}°C / {min_temp}°C  Avg Temp: {avg_daily_temp}°C  Feels Temp: {avg_feels_temp}°C")
            print(f"{'-'*70}")

            print(f"{'TIME':<6} | {'TEMP':<6} | {'FEELS':<6} | {'CONDITION':<20} | {'HUMID':<6} | {'RAIN':<5} | {'SNOW':<5}")
            print(f"{'-'*70}")

            for hour in day['hour']:

                time_only = hour['time'].split(" ")[1]
                forecast_hour = int(time_only.split(':')[0])


                if date_obj == current_date:
                    today_hours.append(time_only)
                    today_temps.append(hour['temp_c'])

                if date_obj == current_date and forecast_hour <= current_hour:
                    continue

                temp = round(hour['temp_c'])                                    
                feels_temp = round(hour['feelslike_c'])                         
                condition = hour['condition']['text'][:20]
                humidity = hour['humidity']
                rain_chance = hour['chance_of_rain']
                snow_chance = hour['chance_of_snow']

                print(f"{time_only:<6} | {temp:>3}°C | {feels_temp:>3}°C | {condition:<20} | %{humidity:<5} | %{rain_chance:<4} | %{snow_chance:<4}")

                if temp < 0:
                    print(f"DANGER! Freezing temperatures at {time_only} watch out for black ice.")

                elif rain_chance >= 50:
                    print(f"It's likely to rain %{rain_chance} Don't forget your umbrella!")

                elif snow_chance >=40:
                    print(f"High chance of snow %{snow_chance}!")


        plt.figure(figsize=(15,6))

        plt.subplot(1,2,1)
        plt.plot(today_hours, today_temps, marker='o', color='red', linestyle='-')
        plt.title(f"Today's Hourly Temperature ({city.capitalize()})", fontweight='bold')
        plt.xlabel("Hour", fontweight='bold')
        plt.ylabel("Temp (°C)", fontweight='bold')
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.5)

        plt.subplot(1,2,2)
        bars = plt.bar(week_days, week_avg_temps, color='tab:green', alpha=0.8)
        plt.title(f"7-Day Forecast Average Temperature", fontweight='bold')
        plt.xlabel("Days", fontweight='bold')
        plt.ylabel("Avg temp (°C)", fontweight='bold')
        #plt.bar_label(bars, fmt='%.0f')

        if week_avg_temps:
            plt.ylim(0, max(week_avg_temps) + 3)

        for bar in bars :
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2, yval + 0.5 , f'{yval:.1f}', ha= 'center', va='bottom', fontsize=10, fontweight='bold')

        plt.tight_layout()
        plt.show()


    except requests.exceptions.HTTPError as errh:
        print(f"HTTP error occurred: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print("Connection Error. Check the internet connection!")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    print("Welcome to the Advanced Weather Dashboard!")

    target_city = input("Enter the city name for a 24 hour analysis: ")
    get_full_hourly_forecast(target_city)

