from django.urls import path, include
from .views import AuthView, UserView, ParkingView, ParkingNotificationView, LoggingView, SSHView, UsersView, \
    ParkingIdsView

urlpatterns = [
    path('auth', AuthView.as_view()),
    path('user', UserView.as_view()),
    path('users', UsersView.as_view()),

    path('parking', ParkingView.as_view()),
    path('getParkingIds', ParkingIdsView.as_view()),

    path('notification', ParkingNotificationView.as_view()),

    path('logging', LoggingView.as_view()),
    path('ssh', SSHView.as_view()),
]
