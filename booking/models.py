from django.db import models
from django.utils import timezone

class Bus(models.Model):
    BUS_TYPES = [
        ('AC', 'AC Sleeper'),
        ('NON_AC', 'Non-AC Sleeper'),
        ('SEATER', 'Seater'),
    ]
    
    bus_number = models.CharField(max_length=20, unique=True)
    bus_name = models.CharField(max_length=100)
    bus_type = models.CharField(max_length=10, choices=BUS_TYPES)
    total_seats = models.IntegerField(default=40)
    price_per_seat = models.DecimalField(max_digits=10, decimal_places=2)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    
    def __str__(self):
        return f"{self.bus_name} - {self.bus_number}"

    class Meta:
        ordering = ['departure_time']

class Seat(models.Model):
    SEAT_TYPES = [
        ('WINDOW', 'Window Seat'),
        ('NORMAL', 'Normal Seat'),
    ]
    
    SEAT_STATUS = [
        ('AVAILABLE', 'Available'),
        ('BOOKED', 'Booked'),
        ('SELECTED', 'Selected'),
    ]
    
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name='seats')
    seat_number = models.CharField(max_length=10)
    seat_type = models.CharField(max_length=10, choices=SEAT_TYPES, default='NORMAL')
    seat_row = models.IntegerField()
    seat_column = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=SEAT_STATUS, default='AVAILABLE')
    
    class Meta:
        unique_together = ['bus', 'seat_number']
        ordering = ['seat_row', 'seat_column']
    
    def __str__(self):
        return f"{self.bus} - Seat {self.seat_number}"

class Passenger(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    
    def __str__(self):
        return self.name

class Booking(models.Model):
    BOOKING_STATUS = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    booking_id = models.CharField(max_length=20, unique=True)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(default=timezone.now)
    travel_date = models.DateField()
    status = models.CharField(max_length=10, choices=BOOKING_STATUS, default='CONFIRMED')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    terms_accepted = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Booking {self.booking_id} - {self.passenger.name}"

    def save(self, *args, **kwargs):
        if not self.booking_id:
            import uuid
            self.booking_id = f"BK{str(uuid.uuid4())[:8].upper()}"
        super().save(*args, **kwargs)