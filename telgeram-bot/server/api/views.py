from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import MainToken, UserToken, Parking, ParkingNotification
from .serializers import ParkingSerializer, NotificationSerializer

from .ssh import StandCommands, StandType, StandSerializer


class AuthView(APIView):
    def get(self, request):
        token = MainToken.objects.latest('pk')
        chat_id = request.query_params.get("chat_id", None)

        if token and chat_id and token.token == request.query_params.get("token", None):
            UserToken.objects.filter(chat_id=chat_id).delete()
            UserToken(chat_id=chat_id).save()
            return Response({"auth": True})
        return Response({"auth": False})


class UserView(APIView):
    def get(self, request):
        chat_id = request.query_params.get("chat_id", None)
        return Response({"auth": bool(UserToken.objects.filter(chat_id=chat_id))})

    def delete(self, request):
        chat_id = request.query_params.get("chat_id", None)
        UserToken.objects.filter(chat_id=chat_id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ParkingNotificationView(APIView):
    def get(self, request):
        id_parking = request.query_params.get("id_parking", None)
        if id_parking:
            notification = ParkingNotification.objects.filter(parking__id_parking=id_parking)
            if notification:
                data = NotificationSerializer(notification, many=True).data
                notification.delete()
                return Response(data)

        return Response({}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, *args, **kwargs):
        id_parking = request.query_params.get('id_parking')
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

        if type_stand and parking_id:
            parking = Parking.objects.filter(id_parking=parking_id)
            if parking:
                parking = ParkingSerializer(parking, many=True).data[0]
                main_stand = StandSerializer(**(
                                                parking['type_stand'] if type_stand == StandType.entry
                                                else parking['stand_exit']))
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


class ParkingView(APIView):
    def get(self, request):
        parking_id = request.query_params.get("parking_id", None)
        parking = Parking.objects.filter(id_parking=parking_id)
        if parking:
            return Response(ParkingSerializer(parking, many=True).data)
        return Response({}, status=status.HTTP_404_NOT_FOUND)
