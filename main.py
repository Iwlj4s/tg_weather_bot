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

        @self.dp.message_handler(commands=['weather', 'погода'])
        async def get_weather_info(message: types.Message):
            city_name = message.text.split(' ', 1)[1]

            weather_data = get_weather.get_response_of_weather(city_name, self.WEATHER_API)

            try:
                if not weather_data:
                    await message.answer(f"Sorry, couldn't get weather information for {city_name}.")

                else:
                    response_message = (
                        f"Weather in {city_name}:\n"
                        f"{weather_data['description']}\n"
                        f"Temperature: {weather_data['temperature']}°C\n"
                        f"Feels like: {weather_data['feels like']}°C\n"
                        f"Wind speed: {weather_data['wind speed']}m/s\n"
                        f"Humidity: {weather_data['humidity']}%\n"
                        f"Sunrise: {weather_data['sun rise']}\n"
                        f"Sunset: {weather_data['sun set']}"
                    )

                    await message.answer(response_message)

            except IndexError:
                await message.answer("Please provide a valid city name after the /weather command.")

            except KeyError:
                await message.answer(f"Sorry, can't take You Information about {city_name}")


if __name__ == '__main__':
    handler = Handler()
    executor.start_polling(handler.dp, skip_updates=True)
