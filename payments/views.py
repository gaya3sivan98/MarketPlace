from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from bookings.models import Booking
from .models import Payment
import uuid

@login_required
def initiate_payment(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id, customer=request.user)
    
    if booking.status != 'confirmed':
        messages.error(request, 'You can only pay for confirmed bookings.')
        return redirect('customer_bookings')
        
    if hasattr(booking, 'payment') and booking.payment.status == 'completed':
        messages.info(request, 'Payment already completed for this booking.')
        return redirect('customer_bookings')

    if request.method == 'POST':
        # Simulate payment processing
        # In a real app, this would redirect to Stripe/Razorpay
        return redirect('payment_success', booking_id=booking.id)
        
    return render(request, 'payments/checkout.html', {'booking': booking})

@login_required
def payment_success(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id, customer=request.user)
    
    # Create or update payment record
    payment, created = Payment.objects.get_or_create(
        booking=booking,
        defaults={
            'amount': booking.service.price,
            'transaction_id': str(uuid.uuid4()),
            'status': 'completed'
        }
    )
    
    if not created and payment.status != 'completed':
        payment.status = 'completed'
        payment.save()
        
    return render(request, 'payments/success.html', {'payment': payment})

@login_required
def payment_cancel(request):
    return render(request, 'payments/cancel.html')
