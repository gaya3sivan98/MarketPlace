import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marketplace_project.settings')
django.setup()

from services.models import Category

def populate():
    categories = [
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
        {"name": "Beauty & Salon", "icon": "bi-scissors"},
    ]

    for cat_data in categories:
        category, created = Category.objects.get_or_create(
            name=cat_data["name"],
            defaults={"icon": cat_data["icon"]}
        )
        if created:
            print(f"Created category: {category.name}")
        else:
            print(f"Category already exists: {category.name}")

if __name__ == "__main__":
    print("Starting category population...")
    populate()
    print("Population complete.")
