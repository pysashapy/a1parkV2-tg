import io
import time
import datetime
from threading import Thread
from time import sleep

import telebot

from Core import TelegramApi
from Core.keyboards import Keyboards
from Core.serializers import StandType, SHHAction, statusForBot, LogsAction
from interface import Texts, generateErrorNotification
from settings import url_django_tg_server, tg_secret_key

bot = telebot.TeleBot(tg_secret_key)
client = TelegramApi(url_django_tg_server)
keyboards = Keyboards()

"""
    Telebot funcs
"""


@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, Texts.start_about)
    bot.send_message(message.chat.id, Texts.Auth.start)
    bot.register_next_step_handler(message, create_user)


@bot.message_handler(commands=['create'])  #
def create_user(message):
    if client.createUser(message.text, message.chat.id, message.chat.username):
        bot.send_message(message.chat.id, Texts.main_menu)

    else:
        bot.send_message(message.chat.id, Texts.Auth.error)
        bot.send_message(message.chat.id, Texts.Auth.start)
        bot.register_next_step_handler(message, create_user)


def check_auth_user(message):
    if not client.checkAuth(message.chat.id):
        bot.send_message(message.chat.id, Texts.Auth.start)
        bot.register_next_step_handler(message, create_user)


@bot.message_handler(commands=['exit'])
def exit_user(message):
    client.deleteUser(message.chat.id)
    bot.send_message(message.chat.id, Texts.start_about)
    bot.send_message(message.chat.id, Texts.Auth.start)
    bot.register_next_step_handler(message, create_user)


@bot.message_handler(commands=['find'])
def start_find_parking(message):
    check_auth_user(message)
    bot.send_message(message.chat.id, Texts.find_parking)
    return bot.register_next_step_handler(message, entry_id_parking)


def entry_id_parking(message):
    check_auth_user(message)

    if message.text.isdigit():
        if parking := client.getParking(int(message.text)):
            return menu_parking(message, int(message.text))

    bot.send_message(message.chat.id, Texts.not_found_parking)
    bot.send_message(message.chat.id, Texts.find_parking)
    bot.register_next_step_handler(message, entry_id_parking)


def statuses(message, parking_id):
    info_stand(message, parking_id, StandType.entry, add_text='🚘Стенд въезд:\n')
    info_stand(message, parking_id, StandType.exit, add_text='🚗Стенд выезд:\n')


def menu_parking(message, parking_id):
    check_auth_user(message)
    bot.send_message(message.chat.id, f'🅿️Выбрана парковка: {parking_id}')
    statuses(message, parking_id)
    bot.send_message(message.chat.id, f'✅Загрузка стендов завершена', reply_markup=keyboards.parking)
    bot.register_next_step_handler(message, menu_parking_handler, parking_id)


def menu_parking_handler(message, parking_id):
    check_auth_user(message)
    if message.text == 'Въезд':
        info_stand(message, parking_id, StandType.entry, add_text='🚘Стенд въезд:\n')
        set_stand(message, parking_id, StandType.entry)

    elif message.text == 'Выезд':
        info_stand(message, parking_id, StandType.exit, add_text='🚘Стенд въезд:\n')
        set_stand(message, parking_id, StandType.exit)

    elif message.text == 'Перезагрузить парковку':
        reboot_stand(message, parking_id, StandType.entry, add_text='🚘Стенд въезд:\n')
        reboot_stand(message, parking_id, StandType.exit, add_text='🚗Стенд выезд:\n')
        bot.register_next_step_handler(message, menu_parking_handler, parking_id)

    elif message.text == 'Состояние паровки':
        statuses(message, parking_id)
        bot.register_next_step_handler(message, menu_parking_handler, parking_id)

    elif message.text == 'Выключить парковку':
        reboot_stand(message, parking_id, StandType.entry, add_text='🚘Стенд въезд:\n')
        reboot_stand(message, parking_id, StandType.exit, add_text='🚗Стенд выезд:\n')
        bot.register_next_step_handler(message, menu_parking_handler, parking_id)

    elif message.text in ('Назад', '/exit'):
        bot.send_message(message.chat.id, Texts.main_menu)
        return


def set_stand(message, parking_id: int, type_stand: StandType):
    bot.send_message(message.chat.id, f'Меню стэнда', reply_markup=keyboards.stand)
    bot.register_next_step_handler(message, stand_handler, parking_id, type_stand)


def stand_handler(message, parking_id: int, type_stand: StandType):
    check_auth_user(message)
    text = message.text.lower()

    if text == 'перезагрузить стэнд':
        reboot_stand(message, parking_id, type_stand)
    elif text == 'выключить стэнд':
        shutdown_stand(message, parking_id, type_stand)
    elif text == 'состояние':
        info_stand(message, parking_id, type_stand)
    elif text == 'логи':
        logs_stand(message, parking_id, type_stand)
    elif text in ('назад', '/exit'):
        bot.send_message(message.chat.id, f'🅿️Выбрана парковка: {parking_id}', reply_markup=keyboards.parking)
        bot.register_next_step_handler(message, menu_parking_handler, parking_id)
        return
    bot.register_next_step_handler(message, stand_handler, parking_id, type_stand)


def ssh_generator(message, parking_id: int, action: SHHAction, type_stand: StandType, add_text=''):
    if data := client.sendSHHCommand(parking_id, action, type_stand):
        if data[0]:
            try:
                return bot.send_message(message.chat.id, add_text + statusForBot(**eval(data[0])))
            except:
                pass
        if data[1]:
            bot.send_message(message.chat.id, add_text + Texts.error.format(data[1]))

        else:
            bot.send_message(message.chat.id, add_text + "Успешно!")


def reboot_stand(message, parking_id: int, type_stand: StandType, add_text=''):
    ssh_generator(message, parking_id, SHHAction.reboot, type_stand, add_text)


def logs_stand(message, parking_id: int, type_stand: StandType, add_text=''):
    data = ''.join(client.getLogs(parking_id, LogsAction.take, type_stand, count=30))
    if not data:
        data = 'Логи не найдены'
    bot.send_message(message.chat.id, data)


def logs_file_stand(id, parking_id: int, type_stand: StandType, add_text=''):
    data = ''.join(client.getLogs(parking_id, LogsAction.all, type_stand))
    name_file = f'{parking_id}_{type_stand}_{time.strftime("%Y_%m_%d_%H_%M")}.txt'

    file_obj = io.BytesIO(data.encode('utf-8'))
    file_obj.name = name_file

    if data:
        bot.send_document(id, file_obj.read(), visible_file_name=name_file)
    else:
        bot.send_message(id, f'Неудалось получить логи у паркинга №{parking_id}, стэнд {type_stand}')


def shutdown_stand(message, parking_id: int, type_stand: StandType, add_text=''):
    ssh_generator(message, parking_id, SHHAction.shutdown, type_stand, add_text)


def info_stand(message, parking_id: int, type_stand: StandType, add_text=''):
    ssh_generator(message, parking_id, SHHAction.status, type_stand, add_text)


"""
    Telebot End
"""


def getNotificationLogic():
    while True:
        try:
            last_day = open('last_time_send', 'r')

            if day := last_day.read():
                last_day = int(day)
            else:
                last_day = 99

            while True:
                if data := client.getNotifications():
                    users = client.getUsers('all')
                    for user in users:
                        chat_id = user["chat_id"]
                        for message in data:
                            text = generateErrorNotification(message['message'], message['id_parking'])
                            bot.send_message(chat_id, text)

                if (day := datetime.datetime.now().day) != last_day:
                    parkings = (parking for parking in client.getParkingIds())
                    for parking_id in parkings:
                        users = client.getUsers('all')
                        for user in users:
                            chat_id = user["chat_id"]
                            logs_file_stand(chat_id, parking_id=parking_id, type_stand=StandType.entry)
                            client.getLogs(parking_id, type_stand=StandType.entry, action=LogsAction.delete)
                            logs_file_stand(chat_id, parking_id=parking_id, type_stand=StandType.exit)
                            client.getLogs(parking_id, type_stand=StandType.exit, action=LogsAction.delete)
                    last_day = day
                    open('last_time_send', 'w').write(str(last_day))
                sleep(5)
        except BaseException as e:
            print(e)


th = Thread(target=getNotificationLogic)
th.start()


bot.enable_save_next_step_handlers(delay=1)
bot.load_next_step_handlers()
bot.infinity_polling()
