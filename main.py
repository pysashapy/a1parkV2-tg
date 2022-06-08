import telebot
from telebot.types import ReplyKeyboardMarkup

from core import Keyboards
from core.api import *
from core.ssh import *

bot = telebot.TeleBot("5478243033:AAGVUbIDiTLrHh3D1j3RtNCab_nDIY5C58M")
keyboards = Keyboards()


def start_(message, text="Введите ваш токен для продолжения!"):
    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, auth)


def main_menu(message):
    bot.send_message(message.chat.id, "Меню")
    bot.register_next_step_handler(message, auth)


@bot.message_handler(commands=['start'])
def start(message):
    start_(message)


@bot.message_handler(commands=['auth'])
def auth(message):
    token = message.text

    if authUser(token, message.chat.id):
        bot.send_message(message.chat.id, "Успешный вход.", reply_markup=keyboards.main)
        bot.register_next_step_handler(message, main)
    else:
        start_(message, "Токен не верный! Повторите ещё раз")


def find(message):
    bot.send_message(message.chat.id, "Введите ID парковки!", reply_markup=ReplyKeyboardMarkup())
    bot.register_next_step_handler(message, setParking)


@bot.message_handler(commands=['not load'])
def setParking(message):
    id_parking = message.text

    parking_ = Parking(id_parking)
    parking_remote = ParkingSSH(parking_)
    setup = parking_remote.setup()

    if not setup:
        bot.send_message(message.chat.id, f"🅿️Парковка №{parking_.id} не найдена!", reply_markup=keyboards.main)

        return bot.register_next_step_handler(message, main)

    bot.send_message(message.chat.id,  f"🅿️Парковка №{parking_.id}")
    bot.send_message(message.chat.id, "Стэнд на Въезде\n" + parking_remote.stand_entry.getInfo())
    bot.send_message(message.chat.id, "Стэнд на Выезде\n" + parking_remote.stand_exit.getInfo(),
                     reply_markup=keyboards.parking)
    bot.register_next_step_handler(message, parkingRemote, parking_remote)


@bot.message_handler(commands=['not load'])
def parkingRemote(message, parking_remote):
    keyboard = keyboards.stand
    text = "🅿️Выбрана Парковка №"+f"{parking_remote.parking.id}"
    err = ''
    if message.text == "Въезд":
        parking_remote.parking.setTypeStand(True)
        text += "\n" + parking_remote.stand_entry.getInfo()
        bot.register_next_step_handler(message, stand, parking_remote)

    elif message.text == "Выезд":
        parking_remote.parking.setTypeStand(False)
        text += "\n" + parking_remote.stand_exit.getInfo()
        bot.register_next_step_handler(message, stand, parking_remote)

    elif message.text == "Перезагрузить парковку":
        text = "Успешно"
        err = parking_remote.reboot()

        keyboard = keyboards.parking
        bot.register_next_step_handler(message, parkingRemote, parking_remote)

    elif message.text == "Выключить парковку":
        text = "Успешно"
        err = parking_remote.shutdown()
        keyboard = keyboards.parking
        bot.register_next_step_handler(message, parkingRemote, parking_remote)

    elif message.text == "Назад":
        bot.send_message(message.chat.id, "Главное меню", reply_markup=keyboards.main)
        return bot.register_next_step_handler(message, main)

    if err:
        text = err

    bot.send_message(message.chat.id, text, reply_markup=keyboard)


@bot.message_handler(commands=['not load'])
def stand(message, parking_remote: ParkingSSH):
    text = "Успешно."
    if parking_remote.parking.type == StandType.entry:
        stand_ = parking_remote.stand_entry
    else:
        stand_ = parking_remote.stand_exit

    if message.text == "Перезагрузить стэнд":
        stand_.reboot()

    elif message.text == "Выключить стэнд":
        stand_.shutdown()

    elif message.text == "Получить логи":
        text = stand_.getLogs(23)

    elif message.text == "Назад":
        bot.send_message(message.chat.id, "Выбрана парковка: " + parking_remote.parking.id,
                         reply_markup=keyboards.parking)
        return bot.register_next_step_handler(message, parkingRemote, parking_remote)

    bot.send_message(message.chat.id, text, reply_markup=keyboards.stand)
    bot.register_next_step_handler(message, stand, parking_remote)


@bot.message_handler(content_types=['text'])
def main(message):
    if not checkAuth(message.chat.id) or message.text == "Выйти":
        return start_(message)

    if message.text == "Выбрать стойку":
        find(message)


if __name__ == '__main__':
    bot.polling(none_stop=True)