from telebot import *
import paho.mqtt.client as client

mqtt_username = 'ucewloud'
mqtt_password = 'pq-X01BNYdaC'
mqtt_name = 'm16.cloudmqtt.com'

apihelper.proxy = {'https': 'https://180.183.128.97:8080'}
bot = TeleBot("877468244:AAFpxV3uCDKZiDKYQth12rnN8U02lK__bAg")


@bot.message_handler(commands=['start'])
def start(msg):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('/On')
    item2 = types.KeyboardButton('/Off')
    markup.row(item1)
    markup.row(item2)
    bot.send_message(msg.chat.id, 'Привет, У меня есть такие команды для тебя', reply_markup=markup)
    bot.send_message(msg.chat.id, msg.chat.id)


@bot.message_handler(commands=['On', 'Off'])
def light(msg):
    msg.text = str(msg.text).replace('/', '')
    mqtt.publish('light/', msg.text + ' ' + str(msg.chat.id), retain=False)


def mqtt_callback(client, userdata, msg):
    msg_callback = msg.payload.decode('utf-8')
    msg_callback = str(msg_callback).split(' ')

    if 'On' == msg_callback[0]:
        bot.send_message(int(msg_callback[1]), 'Я включил свет')
    if 'Off' == msg_callback[0]:
        bot.send_message(int(msg_callback[1]), 'Я выключил свет')


mqtt = client.Client()
mqtt.will_clear()
mqtt.username_pw_set(mqtt_username, mqtt_password)
mqtt.message_callback_add('light/', mqtt_callback)
mqtt.connect(mqtt_name, 13089, 60)
mqtt.subscribe('light/')
mqtt.loop_start()

bot.polling(none_stop=True)