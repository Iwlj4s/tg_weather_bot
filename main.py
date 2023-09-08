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

        @self.dp.message_handler()
        async def echo(message: types.Message):
            await message.answer(message.text)


if __name__ == '__main__':
    handler = Handler()
    executor.start_polling(handler.dp, skip_updates=True)