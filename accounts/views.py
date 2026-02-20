from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Avg, Count
from .forms import UserRegistrationForm, ProfileForm
from .models import Profile, User
from bookings.models import Booking
from payments.models import Payment
 
def register_customer(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'customer'
            user.save()
            Profile.objects.create(user=user)
            login(request, user)
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register_customer.html', {'form': form})

def register_provider(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'provider'
            user.save()
            Profile.objects.create(user=user)
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register_provider.html', {'form': form})

@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        p_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if p_form.is_valid():
            p_form.save()
            return redirect('profile')
    else:
        p_form = ProfileForm(instance=profile)
    
    return render(request, 'accounts/profile.html', {'p_form': p_form})


def public_profile(request, user_id):
    """View another user's public profile."""
    profile_user = get_object_or_404(User, id=user_id)
    # Ensure profile exists
    Profile.objects.get_or_create(user=profile_user)
    
    # Get services offered by this user (if they are a provider)
    services = profile_user.services.all() if profile_user.is_provider else []
    
    # Get review stats for this provider
    review_stats = Booking.objects.filter(
        service__provider=profile_user,
        review__isnull=False
    ).aggregate(
        avg_rating=Avg('review__rating'),
        total_reviews=Count('review')
    )
    
    completed_jobs = Booking.objects.filter(
        service__provider=profile_user,
        status='completed'
    ).count()
    
    context = {
        'profile_user': profile_user,
        'services': services,
        'avg_rating': review_stats['avg_rating'],
        'total_reviews': review_stats['total_reviews'],
        'completed_jobs': completed_jobs,
    }
    return render(request, 'accounts/public_profile.html', context)

@login_required
def dashboard(request):
    # Stats for the Customer/Buying side
    total_spend = Booking.objects.filter(
        customer=request.user,
        status='completed'
    ).aggregate(total=Sum('service__price'))['total'] or 0

    active_bookings = Booking.objects.filter(
        customer=request.user,
        status__in=['pending', 'confirmed']
    ).count()

    completed_bookings = Booking.objects.filter(
        customer=request.user,
        status='completed'
    ).count()

    my_recent_bookings = Booking.objects.filter(customer=request.user)[:10]

    context = {
        'total_spend': total_spend,
        'active_bookings': active_bookings,
        'completed_bookings': completed_bookings,
        'my_recent_bookings': my_recent_bookings,
    }

    # If the user is a provider, add Selling/Provider stats
    if request.user.role in ['provider', 'both']:
        earnings = Booking.objects.filter(
            service__provider=request.user,
            status='completed'
        ).aggregate(total=Sum('service__price'))['total'] or 0
        
        active_jobs = Booking.objects.filter(
            service__provider=request.user,
            status__in=['pending', 'confirmed']
        ).count()
        
        completed_jobs = Booking.objects.filter(
            service__provider=request.user,
            status='completed'
        ).count()
        
        provider_services = request.user.services.all()
        incoming_bookings = Booking.objects.filter(service__provider=request.user)[:10]

        context.update({
            'earnings': earnings,
            'active_jobs': active_jobs,
            'completed_jobs': completed_jobs,
            'provider_services': provider_services,
            'incoming_bookings': incoming_bookings,
        })

    return render(request, 'accounts/dashboard.html', context)
