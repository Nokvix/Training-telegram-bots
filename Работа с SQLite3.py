import telebot
import sqlite3

# TOKEN = '7493480182:AAGUGN-znKk2e3Yyhr2xmh1bLNroqS3c2KY'
TOKEN = ''

bot = telebot.TeleBot(TOKEN)

name = None


@bot.message_handler(commands=['start'])
def start(message):
    connection = sqlite3.connect('training.sql')  # Подключаем БД и создаём файл с названием "training.sql"
    cursor = connection.cursor()  # Позволяет выполнять действия с БД

    # execute - позволяет выполнять SQL-команды (подготавливает SQL-команду)
    # CREATE TABLE IF NOT EXIST users - создаём таблицу если её нет
    # (id int auto_increment primary key) - одно из полей в таблице (целое, автоматически изменяется, первичный ключ)

    cursor.execute(
        'CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, name varchar(50), password varchar(50))')
    # Добавляет таблицу в файл
    connection.commit()
    # Закрываем соеднение
    cursor.close()
    connection.close()

    bot.send_message(message.chat.id, 'Привет! Нужно зарегистрироваться. Введите своё имя')
    bot.register_next_step_handler(message, user_name)


def user_name(message):
    global name
    name = message.text.strip()
    bot.send_message(message.chat.id, 'Введите пароль')
    bot.register_next_step_handler(message, user_password)


def user_password(message):
    global name
    password = message.text.strip()

    connection = sqlite3.connect('training.sql')
    cursor = connection.cursor()
    cursor.execute("INSERT INTO users (name, password) VALUES ('%s', '%s')" % (name, password))
    connection.commit()
    cursor.close()
    connection.close()

    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton('Список пользователей', callback_data='print_users'))
    bot.send_message(message.chat.id, 'Пользователь зарегистрирован!', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def print_users(call):
    connection = sqlite3.connect('training.sql')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()

    info = ''
    for user in users:
        info += f"Имя: {user[1]}\nПароль: {user[2]}\n\n"

    cursor.close()
    connection.close()

    bot.send_message(call.message.chat.id, info)


bot.infinity_polling()
