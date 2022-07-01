from django.contrib import admin
from .models import *


@admin.register(StandSettings)
class StandSettingsAdmin(admin.ModelAdmin):
    list_display = ('name_profile', 'loop1_type', 'loop2_type', 'infSensor_type', 'buttonPrinter_type')

    fieldsets = (
        (None, {
            'fields': ('name_profile',)
        }),
        ('Type connect loop, buttons, sensors', {
            'classes': ('wide', 'extrapretty'),

            'fields': (('loop1_type', 'loop2_type'), 'infSensor_type', 'buttonPrinter_type')
        }),
        ('Printer', {
            'classes': ('wide', 'extrapretty'),
            'fields': (('idVendor', 'idProduct'), ('in_ep', 'out_ep'))
        }),
        ('Pins', {
            'classes': ('wide', 'extrapretty'),
            'fields': (('pin_led_red', 'pin_led_green'), ('pin_button', 'pin_infSensor'),
                       ('pin_open', 'pin_closed'), ('pin_loop1', 'pin_loop2'))
        }),
    )


@admin.register(ParkingSettings)
class ParkingSettingsAdmin(admin.ModelAdmin):
    list_display = ('tariff_id', 'money_day', 'money_h')

    fieldsets = (
        (None, {
            'fields': ('tariff_id',)
        }),
        ('Cash', {
            'fields': (('money_day', 'money_h'),)
        }),
        ('Communications', {
            'fields': (('email', 'phone'),)
        }),
    )


@admin.register(Stand)
class StandAdmin(admin.ModelAdmin):
    list_display = ('is_entry', 'ip', 'port')

    fieldsets = (

        (None, {
            'classes': ('wide', 'extrapretty'),
            'fields': ('is_entry', 'settings')
        }),
        ('SSH', {
            'classes': ('wide', 'extrapretty'),
            'fields': (('ip', 'port'), ('login', 'password'))
        }),
    )


@admin.register(Parking)
class ParkingAdmin(admin.ModelAdmin):
    list_display = ('id_parking', 'secret_key')
    fieldsets = (
        (None, {
            'classes': ('wide', 'extrapretty'),
            'fields': (('id_parking', 'secret_key'), 'settings')
        }),
        ('Stands', {
            'classes': ('wide', 'extrapretty'),
            'fields': (('stand_entry', 'stand_exit'),)
        }),
    )


@admin.register(ParkingNotification)
class ParkingNotificationAdmin(admin.ModelAdmin):
    list_display = ('parking', 'message')


admin.site.register(MainToken)
admin.site.register(UserToken)
