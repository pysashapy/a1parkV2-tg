from rest_framework import serializers
from .models import Parking, ParkingSettings, Stand, StandSettings


class StandSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StandSettings
        fields = '__all__'


class ParkingSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingSettings
        fields = '__all__'


class StandSerializer(serializers.ModelSerializer):
    settings = StandSettingsSerializer()

    class Meta:
        model = Stand
        fields = '__all__'


class ParkingSerializer(serializers.ModelSerializer):
    settings = ParkingSettingsSerializer()

    stand_entry = StandSerializer()
    stand_exit = StandSerializer()

    class Meta:
        model = Parking
        fields = '__all__'
