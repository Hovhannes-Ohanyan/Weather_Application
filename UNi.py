import unittest
from unittest.mock import patch

import requests

from main import WeatherAPI


class TestWeatherAPI(unittest.TestCase):
    def setUp(self):
        self.api_key = 'your_api_key_here'
        self.weather_api = WeatherAPI(self.api_key)

    @patch('requests.get')  # Mock the requests.get method
    def test_get_temperature_valid_response(self, mock_get):
        # Mock the response from the API
        mock_response = unittest.mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'main': {
                'temp': 25.5  # Example temperature in Celsius
            }
        }
        mock_get.return_value = mock_response

        temperature = self.weather_api.get_temperature("New York", "US")
        self.assertEqual(temperature, 25.5)

    @patch('requests.get')
    def test_get_temperature_request_exception(self, mock_get):
        # Simulate a request exception
        mock_get.side_effect = requests.exceptions.RequestException("Network error")

        temperature = self.weather_api.get_temperature("New York", "US")
        self.assertIsNone(temperature)

    @patch('requests.get')
    def test_get_temperature_invalid_response_format(self, mock_get):
        # Simulate an invalid API response format
        mock_response = unittest.mock.Mock()
        mock_response.status_code = 200
        mock_response.json.side_effect = ValueError("Invalid JSON format")
        mock_get.return_value = mock_response

        temperature = self.weather_api.get_temperature("New York", "US")
        self.assertIsNone(temperature)

    def test_validate_input_valid(self):
        self.assertIsNone(self.weather_api.validate_input("New York", "US"))

    def test_validate_input_invalid_city(self):
        with self.assertRaises(ValueError):
            self.weather_api.validate_input("12345", "US")

    def test_validate_input_invalid_country(self):
        with self.assertRaises(ValueError):
            self.weather_api.validate_input("New York", "12345")


if __name__ == '__main__':
    unittest.main()
