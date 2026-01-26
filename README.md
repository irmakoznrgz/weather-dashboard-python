### Advanced Weather Dashboard ###

A Python-based weather analysis tool that retrieves detailed 7-day hourly forecasts using WeatherAPI. This project is designed to process meteorological data for statistical insights and smart user advice.

##  New Features (v2.0)
- **7-Day Forecasting:** Retrieves weather data for the upcoming week.
- **Hourly Breakdown:** detailed 24-hour analysis for each day.
- **Smart Assistant:** Provides logic-based advice for rain , snow , and freezing temperatures .
- **Data Formatting:** Clean table view with rounded temperatures and aligned columns.
- **Date Handling:** Converts raw dates to `DD.MM.YYYY` format with day names (e.g., Monday).

##  Tech Stack
- Python 3.x
- Requests Library
- Python-dotenv (Security)
- Datetime Module (Time series formatting)

##  How to Run
1. Clone the repo.
2. Create a `.env` file and add your `WEATHER_API_KEY`.
3. Run the script:
   ```bash
   python main.py