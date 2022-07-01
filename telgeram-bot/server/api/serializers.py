from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from .models import Parking, ParkingSettings, Stand, StandSettings, ParkingNotification


class StandSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StandSettings
        exclude = ('id', )


class ParkingSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingSettings
        exclude = ('id', )


class StandSerializer(serializers.ModelSerializer):
    settings = StandSettingsSerializer()

    class Meta:
        model = Stand
        exclude = ('id', )


class ParkingSerializer(serializers.ModelSerializer):
    settings = ParkingSettingsSerializer()

    stand_entry = StandSerializer()
    stand_exit = StandSerializer()

    class Meta:
        model = Parking
        exclude = ('id', )


class NotificationSerializer(serializers.ModelSerializer):
    id_parking = SerializerMethodField()

    class Meta:
        model = ParkingNotification
        fields = ('message', 'id_parking')

    def get_id_parking(self, obj):
        return obj.parking.id_parking
