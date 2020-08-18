from aiohttp import web
from aiogram import Bot, Dispatcher, executor, types
import configparser
import os


config = configparser.ConfigParser()
# os.chdir('../')
config.read(f'{os.getcwd()}/settings_dev.ini')
bot = Bot(token=config['TELEGRAM_CRED']['API_TOKEN'])
dispatcher = Dispatcher(bot)


@dispatcher.message_handler(commands=['start'])
async def start_info(message: types.Message):
    await message.answer(text="Welcome to Spotify Manager Bot! To see all available options enter /menu")


@dispatcher.message_handler(commands=['menu'])
async def cmd_start(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.InlineKeyboardButton(text='Remove duplicate tracks',
                                            switch_inline_query_current_chat='/remove_duplicate'))
    keyboard.add(types.InlineKeyboardButton(text='Create an artist playlist from your favorite tracks',
                                            switch_inline_query_current_chat='/create_artist_playlist'))
    await message.answer(text='Choose an option by pressing button below', reply_markup=keyboard)


@dispatcher.message_handler(commands=['remove_duplicate'])
async def remove_duplicate_tracks(message: types.Message):
    pass


executor.start_polling(dispatcher, skip_updates=False)
