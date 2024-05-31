import telebot
import webbrowser

# TOKEN = "7493480182:AAGUGN-znKk2e3Yyhr2xmh1bLNroqS3c2KY"
TOKEN = ''

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):  # Команда /start
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name} {message.from_user.last_name}')


@bot.message_handler(commands=['site'])
def open_website(message):
    webbrowser.open('https://vk.com/id228634888')


@bot.message_handler()
def user_input(message):  # Ввод пользователя
    if message.text.lower() == 'привет':
        # Простая отправка сообщения
        bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name} {message.from_user.last_name}')
    elif message.text.lower() == 'id':
        # Сообщение оформляется как ответ на сообщение
        bot.reply_to(message, f'Твой id: {message.from_user.id}')


bot.infinity_polling()  # Бесконечная работа
