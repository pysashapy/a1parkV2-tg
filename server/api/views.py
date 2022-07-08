from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import MainToken, User, Parking, ParkingNotification
from .serializers import ParkingSerializer, NotificationSerializer, UserIdSerializer

from .ssh import StandCommands, StandType


class AuthView(APIView):
    def get(self, request):
        """ check auth """
        chat_id = request.query_params.get("chat_id", None)
        return Response({"auth": bool(User.objects.filter(chat_id=chat_id))})


class UserView(APIView):
    def get(self, request):
        """ create """

        token = MainToken.objects.latest('pk')
        chat_id = request.query_params.get("chat_id", None)

        if token and chat_id and token.token == request.query_params.get("token", None):
            user = User.objects.filter(chat_id=chat_id)
            if user:
                user.delete()

            name = request.query_params.get("chat_name", None)
            print(chat_id, name)
            User(chat_id=chat_id, name_chat=name).save()

            return Response({"auth": True})
        return Response({"auth": False})

    def delete(self, request):
        """ delete """
        chat_id = request.query_params.get("chat_id", None)
        User.objects.filter(chat_id=chat_id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UsersView(APIView):
    def get(self, request):
        action = request.query_params.get("action", '')
        if action == "all":
            return Response(UserIdSerializer(User.objects.all(), many=True).data)
        return Response(status=status.HTTP_404_NOT_FOUND)


class ParkingNotificationView(APIView):
    def get(self, request):
        notification = ParkingNotification.objects.all()
        if notification:
            data = NotificationSerializer(notification, many=True).data
            notification.delete()
            return Response(data)

        return Response({}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        id_parking = request.query_params.get('parking_id')
        secret_key = request.query_params.get('secret_key')
        message = request.query_params.get('message')
        if id_parking and secret_key and message:
            parking = Parking.objects.filter(id_parking=int(id_parking),
                                             secret_key=secret_key)
            if parking:
                ParkingNotification(parking=parking[0], message=message).save()

                return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class LoggingView(APIView):
    def get(self, request):
        action = request.query_params.get("action", '').lower()
        type_stand = request.query_params.get('type_stand', '').lower()
        parking_id = request.query_params.get('parking_id', None)
        print(type_stand, parking_id)
        if type_stand and parking_id:
            parking = Parking.objects.filter(id_parking=parking_id)
            if parking:
                parking = parking[0]
                main_stand = parking.stand_entry if type_stand == StandType.entry else parking.stand_exit
                stand = StandCommands(parking_id, main_stand)
                if action == 'delete':
                    return Response(stand.clearLogs())
                if action == 'all':
                    return Response(stand.getLogs())
                if action == 'take':
                    count = request.query_params.get('count')
                    if count:
                        return Response(stand.getLogs(count))

        return Response({}, status=status.HTTP_400_BAD_REQUEST)


class SSHView(APIView):
    def get(self, request):
        action = request.query_params.get("action", '').lower()
        type_stand = request.query_params.get('type_stand', '').lower()
        parking_id = request.query_params.get('parking_id', None)

        if type_stand and parking_id:
            parking = Parking.objects.filter(id_parking=parking_id)
            if parking:
                parking = parking[0]
                main_stand = parking.stand_entry if type_stand == StandType.entry else parking.stand_exit
                stand = StandCommands(parking_id, main_stand)
                data = {}
                if action == 'reboot':
                    data = stand.reboot()

                elif action == 'shutdown':
                    data = stand.shutdown()

                elif action == 'status':
                    data = stand.getStatus()
                return Response(data)

        return Response({}, status=status.HTTP_400_BAD_REQUEST)


class ParkingView(APIView):
    def get(self, request):
        parking_id = request.query_params.get("parking_id", None)
        parking = Parking.objects.filter(id_parking=parking_id)
        if parking:
            return Response(ParkingSerializer(parking, many=True).data)
        return Response({}, status=status.HTTP_404_NOT_FOUND)


class ParkingIdsView(APIView):
    def get(self, request):
        parkings = list(Parking.objects.all())
        if parkings[0]:
            return Response([parking.id_parking for parking in parkings])
        return Response([], status=status.HTTP_404_NOT_FOUND)
