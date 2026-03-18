from django.contrib import admin
from .models import Bus, Seat, Passenger, Booking

@admin.register(Bus)
class BusAdmin(admin.ModelAdmin):
    list_display = ['bus_name', 'bus_number', 'bus_type', 'source', 'destination', 'departure_time', 'price_per_seat']
    list_filter = ['bus_type', 'source', 'destination']
    search_fields = ['bus_name', 'bus_number']

@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ['bus', 'seat_number', 'seat_type', 'price', 'status']
    list_filter = ['status', 'seat_type']
    search_fields = ['seat_number']

@admin.register(Passenger)
class PassengerAdmin(admin.ModelAdmin):
    list_display = ['name', 'age', 'gender', 'email', 'phone']
    search_fields = ['name', 'email', 'phone']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['booking_id', 'passenger', 'bus', 'seat', 'booking_date', 'status']
    list_filter = ['status', 'booking_date']
    search_fields = ['booking_id', 'passenger__name']