import time

from paramiko.client import SSHClient, AutoAddPolicy
from .api import getParking


class StandType:
    entry = True
    exit = False


class ClientSSH:
    def __init__(self, ip, port, login=None, password=None):
        self.client = SSHClient()
        self.client.set_missing_host_key_policy(AutoAddPolicy())

        self.ip = ip
        self.port = port
        self.login = login
        self.password = password

    def connect(self):
        return self.client.connect(self.ip, self.port, self.login, self.password, timeout=1)


class StandSSH:
    def __init__(self, parking_id, type, ip, port, login=None, password=None):
        self.type = type
        self.parking_id = parking_id
        self.ssh = ClientSSH(ip, port, login, password)

    def reboot(self):
        return self.customCommand("sudo reboot")[1]

    def shutdown(self):
        return self.customCommand("sudo shutdown now")[1]

    def getLogs(self, count=99999):
        api = f"http://hostname/getLogs?parking_id={self.parking_id}&type={self.type}&count={count}"
        data = self.customCommand(f'Логи: ' + f'')
        return data[bool(data[1])]

    def getInfo(self):
        status = False

        date = "Неизвестно"
        paper = "Неизвестно"
        count = "Неизвестно"

        out_text = "🤖Статус: {}\n🚗Кол-во свободных мест: {}\n🕜Последний запуск: {}\n📃Бумага: {}"
        data = self.customCommand('uptime -s', True)

        if data[0]:
            status = True
            date = data[0]
        else:
            out_text += "\n‼ERROR‼: "+str(data[1])
        return out_text.format(["🔴", "🟢"][status], count, date, paper)

    def customCommand(self, bash_command, recv=False):
        out = False
        err = False

        try:
            self.ssh.connect()
            stdin, stdout, stderr = self.ssh.client.exec_command(bash_command)
            if recv:
                stdout.channel.recv_exit_status()
            self.ssh.client.close()
            out, err = stdout.read().decode().strip(), err
        except BaseException as e:
            out, err = out, str(e)
        return out, err


class Parking:
    id = None
    type = None

    def __init__(self, id_):
        self.id = id_

    def setParkingId(self, id_):
        self.id = id_

    def setTypeStand(self, type):
        self.type = type


class ParkingSSH:
    stand_exit: StandSSH
    stand_entry: StandSSH

    def __init__(self, parking: Parking):
        self.parking = parking

    def setup(self):
        return self.setupStands(getParking(self.parking.id))

    def setupStands(self, data):
        if data:
            self.stand_entry = StandSSH(self.parking.id, StandType.entry, *tuple(data['entry'].values())[1:])
            self.stand_exit = StandSSH(self.parking.id, StandType.exit, *tuple(data['exit'].values())[1:])
            return True
        return False

    def shutdown(self):
        self.stand_exit.shutdown()
        self.stand_entry.shutdown()

    def reboot(self):
        self.stand_exit.reboot()
        self.stand_entry.reboot()
