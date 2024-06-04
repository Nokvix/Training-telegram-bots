import telebot
from currency_converter import CurrencyConverter
from telebot import types

# TOKEN = '7493480182:AAGUGN-znKk2e3Yyhr2xmh1bLNroqS3c2KY'
TOKEN = ''

bot = telebot.TeleBot(TOKEN)
currency_converter = CurrencyConverter()
amount = 0


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Введите сумму')
    bot.register_next_step_handler(message, get_sum)


def get_sum(message):
    global amount
    try:
        amount = float(message.text.strip().replace(',', '.'))
    except ValueError:
        bot.send_message(message.chat.id, 'Введена некоректная сумма. Попробуйте снова')
        bot.register_next_step_handler(message, get_sum)
        return

    if amount > 0:
        markup = types.InlineKeyboardMarkup(row_width=2)
        button1 = types.InlineKeyboardButton('USD/EUR', callback_data='USD/EUR')
        button2 = types.InlineKeyboardButton('EUR/USD', callback_data='EUR/USD')
        button3 = types.InlineKeyboardButton('USD/RUB', callback_data='USD/RUB')
        button4 = types.InlineKeyboardButton('RUB/USD', callback_data='RUB/USD')
        button5 = types.InlineKeyboardButton('EUR/RUB', callback_data='EUR/RUB')
        button6 = types.InlineKeyboardButton('RUB/EUR', callback_data='RUB/EUR')
        button7 = types.InlineKeyboardButton('Другие валюты', callback_data='other')

        markup.add(button1, button2, button3, button4, button5, button6, button7)
        bot.send_message(message.chat.id, 'Выберите валюты для конвертации', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Сумма должна быть больше 0. Поробуйте снова')
        bot.register_next_step_handler(message, get_sum)
        return


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data != 'other':
        from_currency, to_currency = call.data.upper().split('/')
        result = round(currency_converter.convert(amount, from_currency, to_currency), 2)
        bot.send_message(call.message.chat.id,
                         f"{amount} {from_currency} равно {result} {to_currency}\nМожете ввести следующую сумму для конвертации")
        bot.register_next_step_handler(call.message, get_sum)
    else:
        bot.send_message(call.message.chat.id, 'Введите пару наимнований валют через слэш (USD/EUR)')
        bot.register_next_step_handler(call.message, other_currency)


def other_currency(message):
    try:
        from_currency, to_currency = message.text.strip().upper().split('/')
        result = round(currency_converter.convert(amount, from_currency, to_currency), 2)
        bot.send_message(message.chat.id,
                         f"{amount} {from_currency} равно {result} {to_currency}\nМожете ввести следующую сумму для конвертации")
        bot.register_next_step_handler(message, get_sum)
    except Exception:
        bot.send_message(message.chat.id, 'Что-то пошло не так. Заново введите пару наименований валют')
        bot.register_next_step_handler(message, other_currency)


bot.infinity_polling()
