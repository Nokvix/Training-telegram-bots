from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types.web_app_info import WebAppInfo

TOKEN = '7493480182:AAGUGN-znKk2e3Yyhr2xmh1bLNroqS3c2KY'
bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(Command('start'))
async def start(message: types.Message):
    button = [[types.KeyboardButton(text='Открыть веб страницу', web_app=WebAppInfo(url='https://github.com/Nokvix/Training-telegram-bots/blob/main/index.html'))]]
    keyboard = types.ReplyKeyboardMarkup(keyboard=button, resize_keyboard=True, one_time_keyboard=True)
    await message.answer(text='Привет', reply_markup=keyboard)


dp.run_polling(bot)
