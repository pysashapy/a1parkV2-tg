
from telebot.types import ReplyKeyboardMarkup, KeyboardButton


str_status = {
    0: 'Работает',
    1: 'Неизвестно',
    2: 'Не работает'
}

color_status = {
    0: '🟢',
    1: '🟠',
    2: '🔴'
}

paper_status = {
    **color_status
}

work_status = {
    0: color_status[0],
    1: color_status[2],
}

uptime_status = {
    0: str_status[1]
}


def statusForBot(work=0,
                 uptime=0,
                 paper=0,
                 error=''):
    string = f"🤖Статус: {work_status[work]}\n" \
             f"🕜Время работы: {uptime if uptime else uptime_status[uptime]}\n" \
             f"📃Бумага: {paper_status[paper]}"

    string_error = "‼️ERROR‼️: {}"

    if error:
        string += string_error.format(error)

    return string


class Keyboards:
    def __init__(self):
        self.main = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True, one_time_keyboard=True)
        self.parking = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

        self.stand = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

        self.setup()

    def setup(self):
        self.setup_main()
        self.setup_parking()
        self.setup_stand()

    def setup_main(self):
        remote = KeyboardButton(text="Выбрать стойку")
        exit_ = KeyboardButton(text="Выйти")

        self.main.add(remote, exit_)

    def setup_parking(self):
        in_ = KeyboardButton(text="Въезд")
        out_ = KeyboardButton(text="Выезд")

        reboot = KeyboardButton(text="Перезагрузить парковку")
        shutdown = KeyboardButton(text="Выключить парковку")

        exit_ = KeyboardButton(text="Назад")

        self.parking.add(in_, out_, reboot, shutdown, exit_)

    def setup_stand(self):

        reboot = KeyboardButton(text="Перезагрузить стэнд")
        shutdown = KeyboardButton(text="Выключить стэнд")

        logs = KeyboardButton(text="Получить логи")

        exit_ = KeyboardButton(text="Назад")

        self.stand.add(reboot, shutdown, logs, exit_)

