from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
import os
import get_weather

load_dotenv()


class BotSettings():
    def __init__(self):
        self.TG_TOKEN = os.getenv("TG_TOKEN")
        self.WEATHER_API = os.getenv("WEATHER_API")

        self.bot = Bot(token=self.TG_TOKEN)
        self.dp = Dispatcher(self.bot)


class Handler(BotSettings):
    def __init__(self):
        super().__init__()

        @self.dp.message_handler(commands=['start', 'help'])
        async def send_welcome(message: types.Message):
            await message.answer("Hi! I'm a weather bot. Enter your city name using only letters"
                                 " and I'll tell you about the weather. Example: /weather Tokyo")

        @self.dp.message_handler(commands=['weather'])
        async def get_weather_info(message: types.Message):
            city_name = message.text.split(' ', 1)[1]

            weather_data = get_weather.get_response_of_weather(city_name, self.WEATHER_API)

            if weather_data:
                response_message = f"Weather in {city_name}:\n"
                response_message += f"{weather_data['description']}\n"
                response_message += f"Temperature: {weather_data['temperature']}(°C)\n"
                response_message += f"Feels like: {weather_data['feels like']}(°C)\n"
                response_message += f"Wind speed: {weather_data['wind speed']}(m/s)\n"
                response_message += f"Humidity: {weather_data['humidity']}(%)\n"
                response_message += f"Sunrise: {weather_data['sun rise']}\n"
                response_message += f"Sunset: {weather_data['sun set']}"

                await message.answer(response_message)

            else:
                await message.answer(f"Sorry, couldn't get weather information for {city_name}.")


if __name__ == '__main__':
    handler = Handler()
    executor.start_polling(handler.dp, skip_updates=True)
