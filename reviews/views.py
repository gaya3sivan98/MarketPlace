from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from bookings.models import Booking
from .forms import ReviewForm

@login_required
def add_review(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id, customer=request.user)
    
    if booking.status != 'completed':
        messages.error(request, 'You can only review completed bookings.')
        return redirect('customer_bookings')
    
    if hasattr(booking, 'review'):
        messages.error(request, 'You have already reviewed this booking.')
        return redirect('customer_bookings')
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.booking = booking
            review.save()
            messages.success(request, 'Review submitted successfully!')
            return redirect('service_detail', pk=booking.service.pk)
    else:
        form = ReviewForm()
    
    return render(request, 'reviews/add_review.html', {'form': form, 'booking': booking})
