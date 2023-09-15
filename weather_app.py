import time

import requests
import http.server
import socketserver
import urllib.parse
import json
import re


class WeatherAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"
        self.requests_per_minute = 10
        self.request_history = []

    def get_temperature(self, city, country):
        params = {
            "q": f"{city},{country}",
            "appid": self.api_key,
            "units": "metric"
        }

        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            temperature = data["main"]["temp"]
            return temperature
        except requests.exceptions.RequestException:
            return None

    def _limit_requests(self):
        current_time = time.time()
        self.request_history = [t for t in self.request_history if current_time - t < 60]

        if len(self.request_history) >= self.requests_per_minute:
            raise Exception("Request limit exceeded")
        else:
            self.request_history.append(current_time)

    @staticmethod
    def validate_input(city, country):
        if not (re.match(r"[a-zA-Z]+$", city) and re.match(r"[a-zA-Z]+$", country)):
            raise ValueError("Invalid city or country name")


class MyRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/weather'):
            query = urllib.parse.urlparse(self.path).query
            params = urllib.parse.parse_qs(query)
            city = params.get('city', [''])[0]
            country = params.get('country', [''])[0]
            if city and country:
                try:
                    weather_api = WeatherAPI(api_key='5e7523329fe5639e8087bac0ea8f1d37')
                    temperature = weather_api.get_temperature(city, country)

                    if temperature is not None:
                        self.send_response(200)
                        self.send_header('Content-type', "application/json")
                        self.end_headers()
                        response = {'temperature': temperature}
                        self.wfile.write(json.dumps(response).encode())
                    else:
                        self.send_error(500, "internal Server Error")
                except ValueError:
                    self.send_error(400, "Bad Request")
            else:
                self.send_error(400, "Bad Request")
        else:
            self.send_error(404, "Not Found")


if __name__ == "__main__":
    PORT = 8000
    with socketserver.TCPServer(('', PORT), MyRequestHandler) as httpd:
        print(f"Our server serving on port {PORT}")
        httpd.serve_forever()
