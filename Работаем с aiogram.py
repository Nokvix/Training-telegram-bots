from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder

# TOKEN = '7493480182:AAGUGN-znKk2e3Yyhr2xmh1bLNroqS3c2KY'
TOKEN = ''
bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(Command('start'))
async def start(message: types.Message):
    # await bot.send_message(message.chat.id, 'Привет') #  Возможный способ отправки сообщения
    # await message.reply('Привет') #  Ответ на присланное сообщение

    # file = open('image.jpg', 'rb')
    # await message.answer_photo(file) #  Отправка фото
    # file.close()

    await message.answer('Привет')  # Отправка сообщения


@dp.message(F.Photo)
async def photo_came_in(message: types.Message):
    await message.reply('Классное фото')


@dp.message()
async def info(message: types.Message):
    # Инлайн кнопки
    # buttons = [
    #     [
    #         types.InlineKeyboardButton(text='Сайт', url='https://vk.com/id228634888'),
    #         types.InlineKeyboardButton(text='Привет', callback_data='hello')
    #     ]
    # ]
    #
    # keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

    # Кнопки в в текстовом поле
    # buttons = [
    #     [
    #         types.KeyboardButton(text='Сайт', url='https://vk.com/id228634888'),
    #         types.KeyboardButton(text='Привет', callback_data='hello')
    #     ]
    # ]
    #
    # keyboard = types.ReplyKeyboardMarkup(keyboard=buttons, one_time_keyboard=True, resize_keyboard=True)

    # Можно ещё создавать кнопки так
    builder = ReplyKeyboardBuilder()
    for i in range(1, 17):
        builder.add(types.KeyboardButton(text=f"{i}"))

    builder.adjust(4)  # Делит кнопки по 4 в ряд
    await message.answer(
        text='Выберите число от 1 до 16',
        reply_markup=builder.as_markup(resize_keyboard=True, one_time_keyboard=True),
        # as_markup - возвращает готовый объект клавиатуры
    )


@dp.callback_query(F.data == 'hello')
async def hello(callback: types.CallbackQuery):
    await callback.message.answer(callback.data)
    await callback.answer()


dp.run_polling(bot)
