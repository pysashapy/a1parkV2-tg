from telebot.types import ReplyKeyboardMarkup, KeyboardButton


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
        statuses = KeyboardButton(text="Состояние паровки")

        exit_ = KeyboardButton(text="Назад")

        self.parking.add(in_, out_, reboot, statuses, shutdown, exit_)

    def setup_stand(self):

        reboot = KeyboardButton(text="Перезагрузить стэнд")
        shutdown = KeyboardButton(text="Выключить стэнд")

        logs = KeyboardButton(text="Логи")
        status = KeyboardButton(text="Состояние")

        exit_ = KeyboardButton(text="Назад")

        self.stand.add(reboot, shutdown, status, logs, exit_)

