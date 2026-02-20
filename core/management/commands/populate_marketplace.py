from django.core.management.base import BaseCommand
from django.utils.text import slugify
from accounts.models import User, Profile
from services.models import Category, Service
import random

class Command(BaseCommand):
    help = 'Populates the marketplace with categories, providers, and services'

    def handle(self, *args, **kwargs):
        self.stdout.write('Populating marketplace data...')

        categories_data = [
            {"name": "Home Cleaning", "icon": "bi-house-door"},
            {"name": "Plumbing", "icon": "bi-wrench"},
            {"name": "Electrical Works", "icon": "bi-lightning"},
            {"name": "Tutoring", "icon": "bi-book"},
            {"name": "Personal Training", "icon": "bi-heart-pulse"},
            {"name": "Graphic Design", "icon": "bi-palette"},
            {"name": "Photography", "icon": "bi-camera"},
            {"name": "Web Development", "icon": "bi-code-slash"},
            {"name": "Gardening", "icon": "bi-tree"},
            {"name": "Legal Advice", "icon": "bi-briefcase"},
            {"name": "Event Planning", "icon": "bi-calendar-event"},
            {"name": "Interior Design", "icon": "bi-brush"},
        ]

        # Create Categories
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data["name"],
                defaults={"icon": cat_data["icon"]}
            )
            if created:
                self.stdout.write(f'Created category: {category.name}')

            # Create 2 Providers for each category
            for i in range(1, 3):
                username = f'provider_{category.slug}_{i}'
                email = f'{username}@example.com'
                
                user, u_created = User.objects.get_or_create(
                    username=username,
                    defaults={
                        'email': email,
                        'role': 'provider'
                    }
                )
                if u_created:
                    user.set_password('password123')
                    user.save()
                    Profile.objects.get_or_create(
                        user=user,
                        defaults={
                            'bio': f'Professional provider for {category.name} with years of experience.',
                            'location': random.choice(['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix'])
                        }
                    )
                    self.stdout.write(f'  Created provider: {username}')

                # Create 1 Service for each provider in this category
                service_title = f'{category.name} Specialist - {user.username}'
                Service.objects.get_or_create(
                    provider=user,
                    category=category,
                    title=service_title,
                    defaults={
                        'description': f'High quality {category.name} services provided by {user.username}. Affordable and reliable.',
                        'price': random.randint(30, 200),
                        'status': 'active'
                    }
                )
                self.stdout.write(f'    Created service: {service_title}')

        self.stdout.write(self.style.SUCCESS('Successfully populated marketplace data.'))
