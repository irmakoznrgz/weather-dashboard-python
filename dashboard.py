import streamlit as st
import requests
import os
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime

load_dotenv()

st.set_page_config(page_title="WeatherHub", page_icon="🌤️", layout="wide")


def get_emoji(condition_text):
    text = condition_text.lower()
    if "sunny" in text or "clear" in text: return "☀️"
    elif "partly cloud" in text: return "⛅"
    elif "cloud" in text or "overcast" in text: return "☁️"
    elif "rain" in text or "drizzle" in text: return "🌧️"
    elif "snow" in text or "blizzard" in text: return "❄️"
    elif "thuder" in text: return "⛈️"
    elif "fog" in text or "mist" in text: return "🌫️"
    else: return "🌡️"

def get_weather_data(city):
    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key:
        st.error("Error: API Key not found!")
        return None

    base_url = "http://api.weatherapi.com/v1/"
    url = f"{base_url}forecast.json?key={api_key}&q={city}&days=7&aqi=no&alerts=no"

    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except:
        return None


st.title("Advanced Weather and Comparison Dashboard ⛅")
st.markdown("Please select a city for a detailed analysis.")

col_input1, col_input2, = st.columns(2)

df_cities = pd.read_csv("cities.csv")
city_list = df_cities["city_name"].tolist()

with col_input1:
    city1 = st.selectbox("City-1", city_list, index=None, placeholder="Select City...")

with col_input2:
    city2 = st.selectbox("City-2 (Comparison (Optional))", city_list, index=None, placeholder="select a city for comparing.")
 
btn = st.button("Get the Weather Forecast")

if btn:
    if city1:
        data1 = get_weather_data(city1)
        data2 = None
        if city2 and city2 != "No":
            data2 = get_weather_data(city2)

        if data1:
            current1 = data1['current']
            location1 = data1['location']
            forecast1 = data1['forecast']['forecastday'][0]['hour']


            now_hour = datetime.now().hour
            forecast_today_remaining = data1['forecast']['forecastday'][0]['hour'][now_hour:]
            if len(data1['forecast']['forecastday']) > 1:
                forecast_tomorrow_start = data1['forecast']['forecastday'][1]['hour'][:now_hour]
                combined_hourly_forecast = forecast_today_remaining + forecast_tomorrow_start
            else:
                combined_hourly_forecast = forecast_today_remaining


            daily_forecast = data1['forecast']['forecastday']


            st.divider()
            st.subheader(f"📍 {location1['name']} Weather Report")

            m1, m2, m3 = st.columns(3)
            m1.metric("Tempature", f"{current1['temp_c']}°C", f"Feels: {current1['feelslike_c']}°C")
            m2.metric("Condition", current1['condition']['text'], get_emoji(current1['condition']['text']))
            m3.metric("Humidity & Wind", f"%{current1['humidity']}", f"{current1['wind_kph']} km/h")

            if data2:
                current2 = data2['current']
                location2 = data2['location']
                forecast2 = data2['forecast']['forecastday'][0]['hour']

                st.divider()
                st.subheader(f"📍 {location2['name']} Weather Report")

                k1, k2, k3 = st.columns(3)
                k1.metric("Tempature", f"{current2['temp_c']}°C", f"Feels: {current2['feelslike_c']}°C")
                k2.metric("Condition", current2['condition']['text'], get_emoji(current2['condition']['text']))
                k3.metric("Humidity & Wind", f"%{current2['humidity']}", f"{current2['wind_kph']} km/h")

            
            st.divider()
            st.write("24 Hourly Forecast")

            cols = st.columns(6)
            for i, hour_data in enumerate(combined_hourly_forecast):
                if i >= 24: break

                col = cols[i % 6]

                hour = hour_data['time'].split()[1]
                icon = get_emoji(hour_data['condition']['text'])
                temp = hour_data['temp_c']
                humidity = hour_data['humidity']

                with col:
                    st.markdown(f"{hour}")
                    st.markdown(f"<h3>{icon}</h3>", unsafe_allow_html=True)
                    st.markdown(f"{temp}°C")
                    st.caption(f"💧 %{humidity}")
            st.divider()
            st.subheader("📊 24 Hourly Tempature Chart")

            hours = [h['time'].split()[1] for h in combined_hourly_forecast]
            temps1 = [h['temp_c'] for h in combined_hourly_forecast]

            chart_data = {
                'Hour': hours,
                f'{location1["name"]} Tempature': temps1
            }

            chart_colors = ["#1c1fe1"]

            if data2:

                forecast2_today = data2['forecast']['forecastday'][0]['hour'][now_hour:]
                if len(data2['forecast']['forecastday']) > 1:
                    forecast2_tomorrow = data2['forecast']['forecastday'][1]['hour'][:now_hour]
                    combined_hourly_forecast2 = forecast2_today + forecast2_tomorrow
                else:
                    combined_hourly_forecast2 = forecast2_today

                temps2 = [h['temp_c'] for h in combined_hourly_forecast2]

                min_len = min(len(temps1), len(temps2))
                chart_data[f'{location1["name"]} Tempature'] = temps1[:min_len]
                chart_data[f'{location2["name"]} Tempature'] = temps2[:min_len]

                chart_colors.append("#d42215")

            df = pd.DataFrame(chart_data)
            df = df.set_index('Hour')
            st.line_chart(df, color=chart_colors)

            st.divider()
            st.subheader("📅 7 Day Forecast")

            for day in daily_forecast:
                date_str = day['date']
                date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                day_name = date_obj.strftime("%A")

                condition = day['day']['condition']['text']
                icon = get_emoji(condition)
                max_temp = day['day']['maxtemp_c']
                min_temp = day['day']['mintemp_c']
                rain_chance = day['day'].get('daily_chance_of_rain', '0')

                d_col1, d_col2, d_col3, d_col4, d_col5 = st.columns([2, 1 ,3, 2, 2])

                with d_col1:
                    st.markdown(f"{day_name}")
                    st.caption(date_str)
                with d_col2:
                    st.markdown(f"<h3>{icon}</h3>", unsafe_allow_html=True)
                with d_col3:
                    st.write(f"{condition}")
                with d_col4:
                    st.write(f"💧 {rain_chance}%")
                with d_col5:
                    st.write(f"H: {max_temp}°C L: {min_temp}°C")

                st.divider()
        
        else:
            st.error("First city data could not be retrieved. Check the city name...")

