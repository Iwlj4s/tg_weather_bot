from dotenv import load_dotenv
import datetime as dt
import requests

load_dotenv()


def kelvin_to_celsius(kelvin):
    celsius = kelvin - 273.15

    return celsius


def get_request_of_weather(city_name, token):
    # Get Request #
    BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"

    url = BASE_URL + "appid=" + token + "&q=" + city_name
    response = requests.get(url).json()

    return response


def get_response_of_weather(city_name, token):
    weather_data = get_request_of_weather(city_name, token)

    if weather_data:
        weather_info = {
            'description': weather_data['weather'][0]['description'],
            'temperature': round(kelvin_to_celsius(weather_data['main']['temp'])),
            'feels like': round(kelvin_to_celsius(weather_data['main']['feels_like'])),
            'wind speed': round(weather_data['wind']['speed']),
            'humidity': round(weather_data['main']['humidity'])
        }

        # --- Get Sin Rise And Sun Set --- #
        sunrise_time = dt.datetime.utcfromtimestamp(weather_data['sys']['sunrise'] + weather_data['timezone'])
        sunset_time = dt.datetime.utcfromtimestamp(weather_data['sys']['sunset'] + weather_data['timezone'])

        weather_info['sun rise'] = sunrise_time
        weather_info['sun set'] = sunset_time

        return weather_info

    else:
        return None
