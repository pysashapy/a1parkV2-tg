from rest_framework import serializers
from .models import Parking, ParkingSettings, Stand, StandSettings


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
