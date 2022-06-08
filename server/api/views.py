from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import MainToken, UserToken, Parking
from .serializers import StandSerializer, ParkingSerializer


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


class ParkingView(APIView):
    def get(self, request):
        parking_id = request.query_params.get("parking_id", None)
        parking = Parking.objects.filter(id_parking=parking_id)
        if parking:
            return Response(ParkingSerializer(parking, many=True).data)
        return Response({}, status=status.HTTP_404_NOT_FOUND)