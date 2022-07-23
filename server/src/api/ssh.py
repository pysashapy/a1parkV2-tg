from paramiko.agent import AgentRequestHandler
from paramiko.client import SSHClient, AutoAddPolicy


class StandType:
    entry = 'entry'
    exit = 'exit'


class ClientSSH:
    def __init__(self, ip, port, login=None, password=None):
        self.client = SSHClient()
        self.client.set_missing_host_key_policy(AutoAddPolicy())

        self.ip = ip
        self.port = port
        self.login = login
        self.password = password

    def connect(self):
        self.client.connect(self.ip, self.port, self.login, self.password, timeout=1)
        return self.client

    def customCommand(self, bash_command, recv=False, pswd=False):
        out = None
        err = False

        try:
            with self.connect() as client:

                if pswd:
                    stdin, stdout, stderr = client.exec_command(bash_command, get_pty=True)
                    stdin.write(f'{self.password}\n')
                    stdin.flush()
                else:
                    stdin, stdout, stderr = client.exec_command(bash_command)

                if recv:
                    stdout.channel.recv_exit_status()
                out, err = stdout.read().decode().strip(), err
        except BaseException as e:
            out, err = out, str(e)
        return out, err


class StandCommands:
    def __init__(self, parking_id: int, settings):
        self.type = type
        self.parking_id = parking_id
        self.settings = settings
        self.ssh = ClientSSH(settings.ip, settings.port, settings.login, settings.password)

    def reboot(self) -> tuple[str, bool]:
        return self.ssh.customCommand("sudo reboot", pswd=True)

    def shutdown(self) -> tuple[str, bool]:
        return self.ssh.customCommand("sudo poweroff", pswd=True)

    def getLogs(self, count=9999999999) -> tuple[str, bool]:
        return self.ssh.customCommand(f'python3 {self.settings.path_manage} --loggingOS take --count {count}')

    def clearLogs(self) -> tuple[str, bool]:
        return self.ssh.customCommand(f'sudo python3 {self.settings.path_manage} --loggingOS delete', pswd=True)

    def getStatus(self) -> tuple[str, bool]:
        out_ssh = self.ssh.customCommand(f'python3 {self.settings.path_manage} --status p')
        return out_ssh


if __name__ == '__main__':
    cl = ClientSSH('89.17.58.114', 8701, 'pi', 'ktcq4wlj26z5d8v')
    print(cl.customCommand(f'sudo python3 a1parkV2-stand/manage.py --loggingOS delete', pswd=True))