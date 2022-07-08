from dataclasses import dataclass

from dataclasses_json import dataclass_json


class StandType:
    entry = 'entry'
    exit = 'exit'


class LogsAction:
    delete = 'delete'
    all = 'all'
    take = 'take'


class SHHAction:
    reboot = 'reboot'
    shutdown = 'shutdown'
    status = 'status'


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


def statusForBot(work=1,
                 uptime=0,
                 paper=2,
                 error=''):
    string = f"🤖Статус: {work_status[work]}\n" \
             f"🕜Время работы: {uptime if isinstance(uptime, str) else uptime_status[uptime]}\n" \
             f"📃Бумага: {paper_status[paper]}"

    string_error = "\n‼️ERROR‼️: {}"

    if error:
        string += string_error.format(error)

    return string



@dataclass_json
@dataclass
class StandSettingsSerializer:
    name_profile: str

    """time signal"""
    delay_barrier: float

    """TrafficLight"""
    pin_led_red: int
    pin_led_green: int

    """button print"""
    pin_button: int

    """BarrierBoom"""
    pin_open: int
    pin_closed: int

    """pins loops"""
    pin_loop1: int
    pin_loop2: int

    """infSensor"""
    pin_infSensor: int

    """Types input connect"""
    loop1_type: bool
    loop2_type: bool

    infSensor_type: bool
    buttonPrinter_type: bool

    """printer"""
    idVendor: int
    idProduct: int
    in_ep: int
    out_ep: int


@dataclass_json
@dataclass
class StandSerializer:
    is_entry: bool

    settings: StandSettingsSerializer

    ip: str
    port: int
    login: str
    password: str

    path_manage: str


@dataclass_json
@dataclass
class ParkingSettingsSerializer:
    """Parking"""
    tariff_id: int

    """info for check"""
    money_day: int
    money_h: int
    email: str
    phone: str


@dataclass_json
@dataclass
class ParkingSerializer:
    id_parking: int
    secret_key: str

    settings: ParkingSettingsSerializer

    stand_entry: StandSerializer
    stand_exit: StandSerializer


@dataclass_json
@dataclass
class StatusSerializer:
    work: int = 1
    uptime: str = ''
    paper: int = 1
    error: str = ''
