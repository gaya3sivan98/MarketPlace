from django.core.management.base import BaseCommand
from django.utils.text import slugify
from accounts.models import User, Profile
from services.models import Category, Service
from bookings.models import Booking
from reviews.models import Review

class Command(BaseCommand):
    help = 'Populates the database with dummy data for testing'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating dummy data...')

        # Create Categories
        categories = ['Plumbing', 'Electrical', 'Cleaning', 'Carpentry', 'Painting', 'Beauty']
        for cat_name in categories:
            Category.objects.get_or_create(name=cat_name, slug=slugify(cat_name))
        
        self.stdout.write(f'Created {len(categories)} categories.')

        # Create Provider
        provider, created = User.objects.get_or_create(username='provider', email='provider@example.com')
        if created:
            provider.set_password('provider123')
            provider.role = 'provider'
            provider.save()
            Profile.objects.create(user=provider, bio='Experienced professional with 5 years of experience.', location='New York')
            self.stdout.write('Created provider user: provider / provider123')

        # Create Customer
        customer, created = User.objects.get_or_create(username='customer', email='customer@example.com')
        if created:
            customer.set_password('customer123')
            customer.role = 'customer'
            customer.save()
            Profile.objects.create(user=customer, location='Brooklyn')
            self.stdout.write('Created customer user: customer / customer123')

        # Create Services
        cat_plumbing = Category.objects.get(name='Plumbing')
        cat_cleaning = Category.objects.get(name='Cleaning')

        s1, _ = Service.objects.get_or_create(
            provider=provider,
            title='Fix Leaky Faucet',
            category=cat_plumbing,
            defaults={'description': 'Fixing all kinds of leaks in kitchen and bathroom.', 'price': 50.00}
        )
        
        s2, _ = Service.objects.get_or_create(
            provider=provider,
            title='Full Home Cleaning',
            category=cat_cleaning,
            defaults={'description': 'Deep cleaning for 2BHK apartment.', 'price': 120.00}
        )

        self.stdout.write('Created dummy services.')

        self.stdout.write(self.style.SUCCESS('Successfully populated dummy data.'))
