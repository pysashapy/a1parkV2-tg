from django.urls import path, include
from .views import AuthView, UserView, ParkingView


urlpatterns = [
    path('auth', AuthView.as_view()),
    path('user', UserView.as_view()),
    path('parking', ParkingView.as_view()),
]
