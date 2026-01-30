import streamlit as st
import requests
import os
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime, date

load_dotenv()

st.set_page_config(page_title="WeatherHub", page_icon="🌤️", layout="wide")

def get_advice(temp, condition, rain_chance):

    advice = []

    if temp < 5:
        advice.append("🥶 It's freezing!")
    
    cond_lower = condition.lower()

    if "rain" in cond_lower or "drizzle" in cond_lower or rain_chance > 40:
        advice.append("☔ Don't forget your umbrella!")
    
    elif "snow" in cond_lower:
        advice.append("❄️ Watch out for snow!")

    if "sunny" in cond_lower and temp > 24:
        advice.append("🧢 The sun is strong!")

    if not advice:
        return "Weather is stable..."

    return " ".join(advice)



def get_emoji(condition_text):
    text = condition_text.lower()
    if "sunny" in text or "clear" in text: return "☀️"
    elif "partly cloud" in text: return "⛅"
    elif "cloud" in text or "overcast" in text: return "☁️"
    elif "rain" in text or "drizzle" in text: return "🌧️"
    elif "snow" in text or "blizzard" in text: return "❄️"
    elif "thuder" in text: return "⛈️"
    elif "fog" in text or "mist" in text: return "🌫️"
    else: return "🌤️"

def get_weather_data(city):
    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key:
        st.error("Error: API Key not found!")
        return None

    base_url = "http://api.weatherapi.com/v1/"
    url = f"{base_url}forecast.json?key={api_key}&q={city.strip()}&days=7&aqi=no&alerts=no"

    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"No Data Found! ({city}): {e}")
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

            forecast1_day0 = data1['forecast']['forecastday'][0]
            
            now = datetime.now()
            current_date = date.today()
            current_hour = now.hour
            current_minute = now.minute

            if current_minute <= 30:
                start_hour = current_hour
            else:
                start_hour = current_hour + 1

            forecast_today_remaining = data1['forecast']['forecastday'][0]['hour'][start_hour:]

            if len(data1['forecast']['forecastday']) > 1:
                forecast_tomorrow_start = data1['forecast']['forecastday'][1]['hour'][:start_hour]
                combined_hourly_forecast = forecast_today_remaining + forecast_tomorrow_start
            else:
                combined_hourly_forecast = forecast_today_remaining


            combined_hourly_forecast2 = []
            
            if data2:
                forecast2_today = data2['forecast']['forecastday'][0]['hour'][start_hour:]
                if len(data2['forecast']['forecastday']) > 1:
                    forecast2_tomorrow = data2['forecast']['forecastday'][1]['hour'][:start_hour]
                    combined_hourly_forecast2 = forecast2_today + forecast2_tomorrow
                else:
                    combined_hourly_forecast2 = forecast2_today


            st.divider()
            st.subheader(f"📍 {location1['name']} Weather Report")

            daily_rain_chance = forecast1_day0['day'].get('daily__chance_of_rain', 0)
            advice_text = get_advice(current1['temp_c'], current1['condition']['text'], daily_rain_chance)
            st.info(f"💡 **AI Assistant:** {advice_text}")

            m1, m2, m3 = st.columns(3)
            m1.metric("Tempature", f"{round(current1['temp_c'])}°C", f"Feels: {round(current1['feelslike_c'])}°C")
            m2.metric("Condition", current1['condition']['text'], get_emoji(current1['condition']['text']))
            m3.metric("Humidity & Wind", f"%{current1['humidity']}", f"{current1['wind_kph']} km/h")

            if data2:
                current2 = data2['current']
                location2 = data2['location']
                forecast2_day0 = data2['forecast']['forecastday'][0]

                st.divider()
                st.subheader(f"📍 {location2['name']} Weather Report")

                daily_rain_chance2 = forecast2_day0['day'].get('daily_chance_of_rain', 0)
                advice_text2 = get_advice(current2['temp_c'], current2['condition']['text'], daily_rain_chance2)
                st.info(f"💡 **AI Assistant:** {advice_text2}")

                k1, k2, k3 = st.columns(3)
                k1.metric("Tempature", f"{round(current2['temp_c'])}°C", f"Feels: {round(current2['feelslike_c'])}°C")
                k2.metric("Condition", current2['condition']['text'], get_emoji(current2['condition']['text']))
                k3.metric("Humidity & Wind", f"%{current2['humidity']}", f"{current2['wind_kph']} km/h")

            
            st.divider()
            
            st.subheader(f"24 Hourly Forecast ({city1})")

            subset_forecast = combined_hourly_forecast[:24]
            cols = st.columns(len(subset_forecast))

            for i, (col, hour_data) in enumerate(zip(cols, subset_forecast)):
               
                hour_text = hour_data['time'].split()[1]
                icon = get_emoji(hour_data['condition']['text'])
                temp = round(hour_data['temp_c'])
                humidity = hour_data['humidity']

                with col:       
                    st.markdown(f"<div style='text-align:center; font-size:10px; font-weight:bold;'>{hour_text}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div style='text-align:center; font-size:20px; margin-top:-5px;'>{icon}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div style='text-align:center; font-size:12px; font-weight:bold; margin-top:-5px;'>{temp}°C</div>", unsafe_allow_html=True)
                    st.caption(f"<div style='text-align:center; font-size:9px; color:gray; margin-top:-2px;'>💧{humidity}</div>", unsafe_allow_html=True)


            if data2 and combined_hourly_forecast2:
                st.markdown("")
                st.subheader(f"24 Hourly Forecast ({city2})")

                subset_forecast2 = combined_hourly_forecast2[:24]
                cols2 = st.columns(len(subset_forecast2))

                for i, (col, hour_data) in enumerate(zip(cols2, subset_forecast2)):
               
                    hour_text = hour_data['time'].split()[1]
                    icon = get_emoji(hour_data['condition']['text'])
                    temp = round(hour_data['temp_c'])
                    humidity = hour_data['humidity']

                    with col:       
                        st.markdown(f"<div style='text-align:center; font-size:10px; font-weight:bold;'>{hour_text}</div>", unsafe_allow_html=True)
                        st.markdown(f"<div style='text-align:center; font-size:20px; margin-top:-5px;'>{icon}</div>", unsafe_allow_html=True)
                        st.markdown(f"<div style='text-align:center; font-size:12px; font-weight:bold; margin-top:-5px;'>{temp}°C</div>", unsafe_allow_html=True)
                        st.caption(f"<div style='text-align:center; font-size:9px; color:gray; margin-top:-2px;'>💧{humidity}</div>", unsafe_allow_html=True)

                

            st.divider()
            st.subheader("📊 24 Hourly Tempature Chart")

            hours = [h['time'] for h in combined_hourly_forecast]
            temps1 = [h['temp_c'] for h in combined_hourly_forecast]

            chart_data = {
                'Hour': hours,
                f'{location1["name"]} Tempature': temps1
            }

            chart_colors = ["#1c1fe1"]

            if data2:
                temps2 = [h['temp_c'] for h in combined_hourly_forecast2]

                min_len = min(len(temps1), len(temps2))
                chart_data[f'{location1["name"]} Tempature'] = temps1[:min_len]
                chart_data[f'{location2["name"]} Tempature'] = temps2[:min_len]

                chart_colors.append("#d42215")

            df = pd.DataFrame(chart_data)
            df = df.set_index('Hour')
            st.line_chart(df, color=chart_colors)

            
            st.divider()
            st.subheader(f"📅 7 Day Forecast ({city1})")

            daily_forecast = data1['forecast']['forecastday']

            current_date = date.today()

            for day in daily_forecast:
                date_str = day['date']
                date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
                formatted_date = date_obj.strftime('%d.%m.%Y')

                if date_obj == current_date:
                    day_display = f"Today | {date_obj.strftime('%A')}"
                else:
                    day_display = date_obj.strftime('%A')

                condition = day['day']['condition']['text']
                icon = get_emoji(condition)
                max_temp = round(day['day']['maxtemp_c'])
                min_temp = round(day['day']['mintemp_c'])
                rain_chance = day['day'].get('daily_chance_of_rain', '0')

                d_col1, d_col2, d_col3, d_col4, d_col5 = st.columns([2, 1 ,3, 2, 2])

                with d_col1:
                    st.markdown(f"**{day_display}**")
                    st.caption(formatted_date)
                with d_col2:
                    st.markdown(f"<h3>{icon}</h3>", unsafe_allow_html=True)
                with d_col3:
                    st.write(f"{condition}")
                with d_col4:
                    st.write(f"💧 {rain_chance}%")
                with d_col5:
                    st.write(f"{max_temp}°C / {min_temp}°C")

                st.divider()

            if data2:
                st.subheader(f"📅 7 Day Forecast ({city2})")

                daily_forecast2 = data2['forecast']['forecastday']


                for day in daily_forecast2:
                    date_str = day['date']
                    date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
                    formatted_date = date_obj.strftime('%d.%m.%Y')

                    if date_obj == current_date:
                        day_display = f"Today | {date_obj.strftime('%A')}"
                    else:
                        day_display = date_obj.strftime('%A')

                    condition = day['day']['condition']['text']
                    icon = get_emoji(condition)
                    max_temp = round(day['day']['maxtemp_c'])
                    min_temp = round(day['day']['mintemp_c'])
                    rain_chance = day['day'].get('daily_chance_of_rain', '0')

                    d_col1, d_col2, d_col3, d_col4, d_col5 = st.columns([2, 1 ,3, 2, 2])

                    with d_col1:
                        st.markdown(f"**{day_display}**")
                        st.caption(formatted_date)
                    with d_col2:
                        st.markdown(f"<h3>{icon}</h3>", unsafe_allow_html=True)
                    with d_col3:
                        st.write(f"{condition}")
                    with d_col4:
                        st.write(f"💧 {rain_chance}%")
                    with d_col5:
                        st.write(f"{max_temp}°C / {min_temp}°C")

                    st.divider()


        else:
            st.error("First city data could not be retrieved. Check the city name...")

