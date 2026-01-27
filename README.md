### Advanced Weather Dashboard ###

A Python-based weather analysis tool that retrieves detailed 7-day hourly forecasts using WeatherAPI. This project is designed to process meteorological data for statistical insights and smart user advice.

##  Features (v3.0)
- **Smart Time Filtering:** Automatically hides past hours for the current day, showing only future forecasts.
- **Dynamic Date Labeling:** Identifies "Today" and displays specific day names (e.g., Monday).
- **Current Status Overview:** Displays immediate temperature and condition upon launch.
- **7-Day Forecasting:** Retrieves weather data for the upcoming week.
- **Smart Assistant:** Provides logic-based advice for rain , snow , and freezing temperatures.
- **Data Formatting:** Clean table view with rounded temperatures and aligned columns.

##  Tech Stack
- Python 3.x
- Requests Library (API Fetching)
- Python-dotenv (Security)
- Datetime Module (Time series & Logic)

##  How to Run
1. Clone the repo.
2. Create a `.env` file and add your `WEATHER_API_KEY`.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt