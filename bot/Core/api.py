from enum import Enum

import requests as req

from .serializers import LogsAction, StandType, SHHAction


class EndPoints:
    """ user """
    check_auth = "api/auth?chat_id={}"  # get
    delete_user = "api/user?chat_id={}"  # delete
    create_user = "api/user?token={}&chat_id={}&chat_name={}"  # get return True

    get_users = "api/users?action={}"  # get return [{'chat_id'}...]

    """ parking """
    get_parking = "api/parking?parking_id={}"  # get
    get_parking_ids = "api/getParkingIds"  # get

    """ notifications """
    get_notifications = "api/notification"  # get

    """ logs """
    get_logs = "api/logging?parking_id={}&action={}&type_stand={}&count={}"  # get

    """ remote """
    remote_ssh_command = "api/ssh?parking_id={}&action={}&type_stand={}"  # get


class TelegramApi:
    def __init__(self, url_host: str):
        self.url_host = url_host
        self.endpoints = EndPoints

    def getUrl(self, api_method) -> str:
        return self.url_host + api_method

    def createUser(self, token: str, chat_id: int, name: str) -> bool:
        return req.get(self.getUrl(
            self.endpoints.create_user.format(token, chat_id, name))
        ).json()['auth']

    def deleteUser(self, chat_id: int):
        req.delete(self.getUrl(self.endpoints.delete_user.format(chat_id)))

    def checkAuth(self, chat_id: int) -> bool:
        return req.get(self.getUrl(
            self.endpoints.check_auth.format(chat_id))
        ).json()['auth']

    def getParking(self, parking_id: int):
        return req.get(self.getUrl(
            self.endpoints.get_parking.format(parking_id))
        ).json()

    def getParkingIds(self):
        return req.get(self.getUrl(
            self.endpoints.get_parking_ids)
        ).json()

    def getUsers(self, action='all'):
        return req.get(self.getUrl(
            self.endpoints.get_users.format(action))
        ).json()

    def getNotifications(self):
        return req.get(self.getUrl(
            self.endpoints.get_notifications)
        ).json()

    def getLogs(self, parking_id: int, action: LogsAction, type_stand: StandType, count=None):
        if data := req.get(self.getUrl(
                self.endpoints.get_logs.format(parking_id, action, type_stand, count))
        ).json():
            if data[0]:
                return eval(data[0])
        return []

    def sendSHHCommand(self, parking_id: int, action: SHHAction, type_stand: StandType):
        return req.get(self.getUrl(
            self.endpoints.remote_ssh_command.format(parking_id, action, type_stand))
        ).json()
