import telebot
from telebot import types

# TOKEN = "7493480182:AAGUGN-znKk2e3Yyhr2xmh1bLNroqS3c2KY"
TOKEN = ''

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    # Создание кнопок в тексте ввода сообщений
    markup = types.ReplyKeyboardMarkup()
    button1 = types.KeyboardButton('Перейти на страницу разработчика')
    button2 = types.KeyboardButton('Удалить фотку')
    button3 = types.KeyboardButton('Изменить текст')
    # Добавление кнопок
    markup.add(button1)
    markup.row(button2, button3)

    # bot.send_message(message.chat.id, 'Привет', reply_markup=markup)
    file = open("photo.png", 'rb')
    bot.send_photo(message.chat.id, file)  # Отправка фото
    bot.register_next_step_handler(message, on_click)  # Определяет следующее действие


def on_click(message):
    if message.text == 'Перейти на страницу разработчика':
        bot.send_message(message.chat.id, 'Открыл страницу разработчика')
    elif message.text == 'Удалить фотку':
        bot.send_message(message.chat.id, 'Фото удалено')
    elif message.text == 'Изменить текст':
        bot.send_message(message.chat.id, 'Текст изменён')



@bot.message_handler(content_types=['photo'])  # Обработка приёма различных видов данных (фото, видео, аудио и др)
def get_photo(message):
    markup = types.InlineKeyboardMarkup()
    # Создание кнопок под сообщением (inline button)
    button1 = types.InlineKeyboardButton('Перейти на страницу разработчика', url='https://vk.com/id228634888')
    button2 = types.InlineKeyboardButton('Удалить фотку', callback_data='delete')
    button3 = types.InlineKeyboardButton('Изменить текст', callback_data='edit')
    # Добавление кнопок
    markup.add(button1)
    markup.row(button2, button3)  # Позволяет добавлять в одну строку несколько кнопок

    bot.reply_to(message, 'Топ фото😉', reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'delete':
        bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
    elif callback.data == 'edit':
        bot.edit_message_text('Исправленный текст', callback.message.chat.id, callback.message.message_id)


bot.infinity_polling()
