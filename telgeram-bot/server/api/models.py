from django.db import models


class MainToken(models.Model):
    token = models.CharField(max_length=120)


class UserToken(models.Model):
    chat_id = models.CharField(max_length=120)


class StandSettings(models.Model):
    name_profile = models.CharField(max_length=255, default='a')

    type_connect = ((True, 'Type NO'), (False, 'Type NC'))
    """time signal"""
    delay_barrier = models.FloatField(default=0.5)

    """TrafficLight"""
    pin_led_red = models.IntegerField(default=24)
    pin_led_green = models.IntegerField(default=23)

    """button print"""
    pin_button = models.IntegerField(default=13)

    """BarrierBoom"""
    pin_open = models.IntegerField(default=27)
    pin_closed = models.IntegerField(default=22)

    """pins loops"""
    pin_loop1 = models.IntegerField(default=5)
    pin_loop2 = models.IntegerField(default=6)

    """infSensor"""
    pin_infSensor = models.IntegerField(default=26)

    """Types input connect"""
    loop1_type = models.BooleanField(default=True, choices=type_connect)
    loop2_type = models.BooleanField(default=True, choices=type_connect)

    infSensor_type = models.BooleanField(default=True, choices=type_connect)
    buttonPrinter_type = models.BooleanField(default=True, choices=type_connect)

    """printer"""
    idVendor = models.IntegerField(default=3540)
    idProduct = models.IntegerField(default=517)
    in_ep = models.IntegerField(default=130)
    out_ep = models.IntegerField(default=1)

    def __str__(self):
        return self.name_profile


class ParkingSettings(models.Model):
    """Parking"""
    tariff_id = models.IntegerField(default=714811)

    """info for check"""
    money_day = models.IntegerField(default=1000)
    money_h = models.IntegerField(default=150)
    email = models.CharField(max_length=255, default="info@a1park.com")
    phone = models.CharField(max_length=255, default="+7 495 646 87 02")


class Stand(models.Model):
    is_entry = models.BooleanField(default=True, choices=((True, 'Въезд'), (False, 'Выезд')))

    settings = models.ForeignKey(StandSettings, on_delete=models.CASCADE)

    ip = models.CharField(max_length=255)
    port = models.IntegerField()
    login = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    path_manage = models.CharField(max_length=255, default='~/a1parkV2-stand/manage.py')


class Parking(models.Model):
    id_parking = models.IntegerField()

    secret_key = models.CharField(max_length=255, default="goe6t9sk41g09vm38v")
    settings = models.ForeignKey(ParkingSettings, on_delete=models.CASCADE)

    stand_entry = models.ForeignKey(Stand, on_delete=models.CASCADE, related_name="stand_entry")
    stand_exit = models.ForeignKey(Stand, on_delete=models.CASCADE, related_name="stand_exit")

    def __str__(self):
        return str(self.id_parking)


class ParkingNotification(models.Model):
    parking = models.ForeignKey(Parking, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)

