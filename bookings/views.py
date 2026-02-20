from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Booking
from services.models import Service
from .forms import BookingForm

@login_required
def book_service(request, service_id):
    service = get_object_or_404(Service, pk=service_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.customer = request.user
            booking.service = service
            booking.save()
            messages.success(request, 'Booking request sent successfully!')
            return redirect('customer_bookings')
    else:
        form = BookingForm()
    
    return render(request, 'bookings/book_service.html', {'form': form, 'service': service})

@login_required
def customer_bookings(request):
    bookings = Booking.objects.filter(customer=request.user)
    return render(request, 'bookings/customer_bookings.html', {'bookings': bookings})

@login_required
def provider_bookings(request):
    if not request.user.is_provider:
        return redirect('home')
    # Get bookings for all services provided by this user
    bookings = Booking.objects.filter(service__provider=request.user)
    return render(request, 'bookings/provider_bookings.html', {'bookings': bookings})

@login_required
def update_booking_status(request, booking_id, status):
    booking = get_object_or_404(Booking, pk=booking_id)
    
    # Ensure only the provider of the service can update status
    if request.user != booking.service.provider:
        return redirect('home')
    
    if status in ['confirmed', 'completed', 'cancelled']:
        booking.status = status
        booking.save()
        messages.success(request, f'Booking status updated to {status}.')
        
    return redirect('provider_bookings')

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id, customer=request.user)
    if booking.status == 'pending':
        booking.status = 'cancelled'
        booking.save()
        messages.info(request, 'Booking cancelled.')
    return redirect('customer_bookings')
