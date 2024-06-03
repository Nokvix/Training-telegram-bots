import telebot
import requests
import json

TOKEN = '7493480182:AAGUGN-znKk2e3Yyhr2xmh1bLNroqS3c2KY'
# TOKEN = ''
API = 'ac4ff4c358e39c408578fa91c2cfb6b8'

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет! Напиши название города, в котором хочешь узнать погоду')


@bot.message_handler(content_types=['text'])
def get_weather(message):
    dictionary = {
        'Rain': 'Дождь',
        'Clear': 'Ясно',
        'Clouds': 'Облачно',
        'Mist': 'Туман',
    }
    city = message.text.strip()
    response = requests.get(
        f'https://api.openweathermap.org/data/2.5/weather?q={city.lower()}&appid={API}&units=metric')
    data = json.loads(response.text)
    try:
        temp = round(data["main"]["temp"])
        weather = data['weather'][0]['main']
        weather = dictionary[weather] if weather in dictionary else weather
        bot.reply_to(message, f'Сейчас в {city.title()} {temp}°C, {weather}')
    except KeyError as e:
        bot.reply_to(message, f'Города {city} нет')


bot.infinity_polling()
