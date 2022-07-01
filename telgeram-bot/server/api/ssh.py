from dataclasses import dataclass
from typing import Union, Tuple

from dataclasses_json import dataclass_json
from paramiko.client import SSHClient, AutoAddPolicy


class StandType:
    entry = 'stand_entry'
    exit = 'stand_exit'


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


class ClientSSH:
    def __init__(self, ip, port, login=None, password=None):
        print(ip,port,login,password)
        self.client = SSHClient()
        self.client.set_missing_host_key_policy(AutoAddPolicy())

        self.ip = ip
        self.port = port
        self.login = login
        self.password = password

    def connect(self):
        self.client.connect(self.ip, self.port, self.login, self.password, timeout=1)
        return self.client

    def customCommand(self, bash_command, recv=False):
        out = None
        err = False

        try:
            with self.connect() as client:
                stdin, stdout, stderr = client.exec_command(bash_command)
                if recv:
                    stdout.channel.recv_exit_status()

            out, err = stdout.read().decode().strip(), err
        except BaseException as e:
            out, err = out, str(e)
        return out, err


class StandCommands:
    def __init__(self, parking_id: int, settings: StandSerializer):
        self.type = type
        self.parking_id = parking_id
        self.settings = settings
        self.ssh = ClientSSH(settings.ip, settings.port, settings.login, settings.password)

    def reboot(self) -> str:
        return self.ssh.customCommand("sudo reboot")[1]

    def shutdown(self) -> str:
        return self.ssh.customCommand("sudo shutdown now")[1]

    def getLogs(self, count=9999999999) -> tuple[str, bool]:
        return self.ssh.customCommand(f'python3 {self.settings.path_manage} --loggingOS take --count {count}')

    def clearLogs(self) -> str:
        return self.ssh.customCommand(f'python3 {self.settings.path_manage} --loggingOS delete')[1]

    def getStatus(self) -> Union[tuple[StatusSerializer, bool], tuple[str, bool]]:
        out_ssh = self.ssh.customCommand(f'python3 {self.settings.path_manage} --status p')
        return (StatusSerializer(**eval(out_ssh[0])), True) if out_ssh[0] else (out_ssh[1], False)
