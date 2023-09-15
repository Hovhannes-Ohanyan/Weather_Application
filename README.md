Weather Application

Usage

To retrieve weather data for a specific city and country, send a GET request to the server's /weather endpoint with query parameters:

city: The name of the city (e.g., "New York").
country: The name of the country (e.g., "US" for the United States).


Configuration

If you need to configure the application, you can modify the following parameters in the weather_app.py file:

api_key: Replace 'your_api_key_here' with your OpenWeatherMap API key.
requests_per_minute: Adjust the rate limiting threshold (e.g., 10 requests per minute).
