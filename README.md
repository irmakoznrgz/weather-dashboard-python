### 🌤️ WeatherHub - Advanced Weather Dashboard ###

WeatherHub is a comprehensive weather analysis tool built with Python and Streamlit. It allows users to check real-time weather conditions, 7-day forecasts, and detailed hourly data for specific cities. It also features a comparison mode to analyze two cities side-by-side.

# Features

* **Real-time Weather Data:** Displays temperature, humidity, wind speed, and weather conditions.
* **City Comparison:** Compare weather data between two different cities instantly.
* **24-Hour Forecast:** Horizontal scrollable hourly forecast for better visualization.
* **Interactive Charts:** Temperature comparison charts for the next 24 hours.
* **7-Day Forecast:** Detailed daily weather outlook.
* **AI Weather Assistant:** Provides smart clothing and activity advice based on temperature, rain probability, and weather conditions.
* **Astronomy & Air Quality:** Shows sunrise/sunset times, moon phases, and air quality index (AQI).

# Tech Stack

* **Python:** Core programming language.
* **Streamlit:** For building the interactive web interface.
* **Pandas:** For data manipulation and chart preparation.
* **WeatherAPI:** External API used to fetch real-time and forecast data.

# Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/irmakoznrgz/weather-dashboard.git](https://github.com/irmakoznrgz/weather-dashboard.git)
    cd weather-dashboard
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **API Key Configuration:**
    * Get a free API key from [WeatherAPI.com](https://www.weatherapi.com/).
    * Create a `.env` file in the root directory.
    * Add your API key:
        ```
        WEATHER_API_KEY=your_api_key_here
        ```

4.  **Run the App:**
    ```bash
    streamlit run dashboard.py
    ```

# Project Structure

* `dashboard.py`: The main application file containing the Streamlit code.
* `cities.csv`: Dataset containing city names for the selection dropdown.
* `requirements.txt`: List of Python dependencies.
* `.env`: (Not included in repo) Stores the API key securely.

# Usage

Select a primary city from the dropdown menu to view its weather report. Optionally, select a second city to enable the comparison mode. The AI assistant will automatically update its advice based on the weather conditions of the selected cities.