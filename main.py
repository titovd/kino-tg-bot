import os

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, filters
from aiogram.utils import executor

from src.constants import KP_SEARCH_END_POINT, KP_MOVIE_BY_ID_END_POINT, KP_SIMILARS_END_POINT
from src.bot import TgBot
from src.parsers import KinopoiskParser


bot = Bot(token=os.environ['BOT_TOKEN'])
dp = Dispatcher(bot)

parser = KinopoiskParser(
    api_key_token=os.environ['KINO_API_KEY_TOKEN'],
    kinopoisk_search_api_end_point=KP_SEARCH_END_POINT,
    kinopoisk_by_id_api_end_point=KP_MOVIE_BY_ID_END_POINT,
    kinoposik_similars_api_end_point=KP_SIMILARS_END_POINT
)

tgbot = TgBot(bot, parser)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await tgbot.start_handler(message)


@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    await tgbot.help_handler(message)


@dp.message_handler(commands=['search'])
async def search_movies(message: types.Message):
    await tgbot.search_handler(message)


@dp.message_handler(filters.RegexpCommandsFilter(regexp_commands=['id([0-9]*)']))
async def search_movies(message: types.Message):
    await tgbot.search_by_id_handler(message)


@dp.message_handler(filters.RegexpCommandsFilter(regexp_commands=['sim([0-9]*)']))
async def similars_movies(message: types.Message):
    await tgbot.similars_by_id_handler(message)


if __name__ == '__main__':
    executor.start_polling(dp)
