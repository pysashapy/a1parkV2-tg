from requests import get, delete


URL = "http://127.0.0.1:8000/"


class EndPoints:
    create_user = "api/auth?token={}&chat_id={}"
    delete_user = "api/user?chat_id={}"

    check_auth = "api/user?chat_id={}"

    get_parking = "api/parking?parking_id={}"


def authUser(token, chat_id):
    url = URL + EndPoints.create_user.format(token, chat_id)
    return get(url).json()["auth"]


def deleteUser(chat_id):
    delete(URL + EndPoints.delete_user.format(chat_id))


def checkAuth(chat_id):
    url = URL + EndPoints.check_auth.format(chat_id)
    return get(url).json()["auth"]


def getParking(parking_id):
    url = URL + EndPoints.get_parking.format(parking_id)
    return get(url).json().setdefault("parking", None)


if __name__ == '__main__':
    print(authUser("123asdasdasdasdasdaszxczxczxczxc", 123))
    print(checkAuth(123))
    print(deleteUser(123))
    print(checkAuth(123))

    print(getParking(12))


