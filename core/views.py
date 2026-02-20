from django.shortcuts import render

from services.models import Service, Category

def home(request):
    categories = Category.objects.all()[:12]
    featured_services = Service.objects.filter(status='active').order_by('-created_at')[:3]
    return render(request, 'index.html', {
        'categories': categories,
        'featured_services': featured_services
    })
