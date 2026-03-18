from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('seat-booking/', views.seat_booking, name='seat_booking'),
    path('confirm-booking/', views.confirm_booking, name='confirm_booking'),
]