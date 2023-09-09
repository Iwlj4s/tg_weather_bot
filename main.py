from aiogram import Bot, Dispatcher, executor, types
from googletrans import Translator
from dotenv import load_dotenv
import traceback
import os
import get_weather
from translate_dict import translate_text

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

        self.translator = Translator()

        # --- Info Handler --- #
        @self.dp.message_handler(commands=['start', 'help'])
        async def send_welcome(message: types.Message):
            await message.answer("Hi! I'm a weather bot. Enter your city name using only letters"
                                 " and I'll tell you about the weather. Example: /weather Tokyo or /погода Токио")

        # --- Main Handler --- #
        @self.dp.message_handler(lambda message: message.text.startswith(('/weather', '/погода')))
        async def get_weather_info(message: types.Message):

            try:
                # --- Split Message -- #
                user_message_parts = message.text.split(' ', 1)

                # --- Check if there at least two parts --- #
                if len(user_message_parts) < 2:
                    await message.answer("Please provide a valid city name after the /weather or /погода command.")
                    return

                # --- Get City Name And Weather Data --- #
                city_name = user_message_parts[1].capitalize()

                weather_data = get_weather.get_response_of_weather(city_name, self.WEATHER_API)

                # --- Sending Weather --- #
                if not weather_data:
                    await message.answer(f"Sorry, couldn't get weather information for {city_name}.")

                else:

                    city_name_output = f"Weather in {city_name}:\n"

                    response_message = (
                        f"{weather_data['description']}\n"
                        f"Temperature: {weather_data['temperature']}°C\n"
                        f"Feels like: {weather_data['feels like']}°C\n"
                        f"Wind speed: {weather_data['wind speed']}m/s\n"
                        f"Humidity: {weather_data['humidity']}%\n"
                        f"SunRise: {weather_data['sun rise']}\n"
                        f"SunSet: {weather_data['sun set']}"
                    )

                    # --- Ru or En  --- #
                    if message.text.startswith('/погода'):
                        translated_message = translate_text(response_message, 'en', 'ru')
                        await message.answer(city_name_output + translated_message)
                    else:
                        await message.answer(city_name_output + response_message)

            except Exception as e:
                traceback.print_exc()
                print(f"An error occurred: {e}")
                await message.answer("An error occurred while processing your request.")


if __name__ == '__main__':
    handler = Handler()
    executor.start_polling(handler.dp, skip_updates=True)
