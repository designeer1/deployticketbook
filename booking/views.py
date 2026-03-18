from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse
from .models import Bus, Seat, Booking, Passenger
from .forms import PassengerForm, BookingForm
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import uuid

def home(request):
    """Home page with bus search"""
    return render(request, 'home.html')

def seat_booking(request):
    """Seat selection page"""
    # For demo purposes, using a default bus
    bus = Bus.objects.first()
    if not bus:
        # Create a demo bus if none exists
        bus = Bus.objects.create(
            bus_number="BUS001",
            bus_name="City Express",
            bus_type="AC",
            total_seats=40,
            price_per_seat=500,
            source="City A",
            destination="City B",
            departure_time=timezone.now() + timezone.timedelta(days=1),
            arrival_time=timezone.now() + timezone.timedelta(days=1, hours=6)
        )
        # Create seats
        for row in range(1, 11):
            for col in range(1, 5):
                seat_number = f"{row}{chr(64+col)}"
                seat_type = 'WINDOW' if col in [1, 4] else 'NORMAL'
                Seat.objects.create(
                    bus=bus,
                    seat_number=seat_number,
                    seat_type=seat_type,
                    seat_row=row,
                    seat_column=col,
                    price=bus.price_per_seat,
                    status='AVAILABLE'
                )
    
    seats = Seat.objects.filter(bus=bus).order_by('seat_row', 'seat_column')
    
    # Group seats by row for display
    seat_layout = {}
    for seat in seats:
        if seat.seat_row not in seat_layout:
            seat_layout[seat.seat_row] = []
        seat_layout[seat.seat_row].append(seat)
    
    context = {
        'bus': bus,
        'seat_layout': seat_layout,
    }
    return render(request, 'seat_booking.html', context)

@csrf_exempt
def confirm_booking(request):
    """Confirm booking and save to database"""
    if request.method == 'POST':
        try:
            # Get form data
            seat_id = request.POST.get('seat_id')
            name = request.POST.get('name')
            age = request.POST.get('age')
            gender = request.POST.get('gender')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            terms_accepted = request.POST.get('terms_accepted') == 'on'
            
            # Validate required fields
            if not all([seat_id, name, age, gender, email, phone]):
                return JsonResponse({
                    'success': False,
                    'message': 'All fields are required'
                }, status=400)
            
            # Get seat
            try:
                seat = Seat.objects.get(id=seat_id)
            except Seat.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'message': 'Seat not found'
                }, status=404)
            
            # Check if seat is available
            if seat.status == 'BOOKED':
                return JsonResponse({
                    'success': False,
                    'message': 'This seat is already booked'
                }, status=400)
            
            # Use transaction to ensure data consistency
            with transaction.atomic():
                # Create passenger
                passenger = Passenger.objects.create(
                    name=name,
                    age=int(age),
                    gender=gender,
                    email=email,
                    phone=phone
                )
                
                # Generate unique booking ID
                booking_id = f"BK{str(uuid.uuid4())[:8].upper()}"
                
                # Create booking
                booking = Booking.objects.create(
                    booking_id=booking_id,
                    bus=seat.bus,
                    seat=seat,
                    passenger=passenger,
                    travel_date=seat.bus.departure_time.date(),
                    total_amount=seat.price,
                    terms_accepted=terms_accepted,
                    status='CONFIRMED'
                )
                
                # Update seat status
                seat.status = 'BOOKED'
                seat.save()
            
            # Return success response
            return JsonResponse({
                'success': True,
                'message': 'Booking confirmed successfully',
                'booking_id': booking.booking_id
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            }, status=500)
    
    return JsonResponse({
        'success': False,
        'message': 'Invalid request method'
    }, status=405)