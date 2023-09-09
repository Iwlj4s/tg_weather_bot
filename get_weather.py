from dotenv import load_dotenv
import datetime as dt
import requests
import emoji

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


def get_emoji(city_name, token):
    weather_data_for_emoji = get_request_of_weather(city_name, token)

    if weather_data_for_emoji:
        weather_info_emoji = {
            "Clear": f"{emoji.emojize(':sun:')} Clear",
            "Clouds": f"{emoji.emojize(':cloud:')} Cloudy",
            "Rain": f"{emoji.emojize(':umbrella:')} Rainy",
            "Drizzle": f"{emoji.emojize(':cloud_with_rain:')} Drizzle",
            "Thunderstorm": f"{emoji.emojize(':thunder_cloud_rain:')} Thunderstorm",
            "Snow": f"{emoji.emojize(':snowflake:')} Snowy",
            "Mist": f"{emoji.emojize(':fog:')} Misty",
            "Haze": f"{emoji.emojize(':fog:')} Hazy",
            "Fog": f"{emoji.emojize(':fog:')} Foggy",
            "Smoke": f"{emoji.emojize(':fog:')} Smoky",
            "Dust": f"{emoji.emojize(':fog:')} Dusty",
            "Sand": f"{emoji.emojize(':fog:')} Sandy",
            "Ash": f"{emoji.emojize(':fog:')} Ashy",
            "Squall": f"{emoji.emojize(':cloud_with_rain:')} Squall",
            "Tornado": f"{emoji.emojize(':tornado_cloud:')} Tornado",
        }

        return weather_info_emoji


def get_response_of_weather(city_name, token):
    weather_data = get_request_of_weather(city_name, token)
    weather_emoji = get_emoji(city_name, token)

    if 'main' in weather_data:
        weather_info = {
            'temperature': round(kelvin_to_celsius(weather_data['main']['temp'])),
            'feels like': round(kelvin_to_celsius(weather_data['main']['feels_like'])),
            'wind speed': round(weather_data['wind']['speed']),
            'humidity': round(weather_data['main']['humidity'])
        }

        # --- Get Description With Emoji --- #
        description = weather_data['weather'][0]['main']
        if description in weather_emoji:
            description = weather_emoji[description]
            weather_info['description'] = description

        else:
            description = "Look out the window, I don’t understand what’s happening"
            weather_info['description'] = description

        # --- Get Sin Rise And Sun Set --- #
        sunrise_time = dt.datetime.utcfromtimestamp(weather_data['sys']['sunrise'] + weather_data['timezone'])
        sunset_time = dt.datetime.utcfromtimestamp(weather_data['sys']['sunset'] + weather_data['timezone'])

        weather_info['sun rise'] = sunrise_time
        weather_info['sun set'] = sunset_time

        return weather_info

    else:
        return None
