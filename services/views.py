from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Service, Category
from .forms import ServiceForm

def service_list(request):
    query = request.GET.get('q')
    category_slug = request.GET.get('category')
    services = Service.objects.filter(status='active')

    if query:
        services = services.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query)
        )
    
    if category_slug:
        services = services.filter(category__slug=category_slug)

    categories = Category.objects.all()
    return render(request, 'services/service_list.html', {
        'services': services, 
        'categories': categories,
        'selected_category': category_slug
    })

def service_detail(request, pk):
    service = get_object_or_404(Service, pk=pk)
    return render(request, 'services/service_detail.html', {'service': service})

@login_required
def create_service(request):
    if not request.user.is_provider:
        return redirect('home')
    
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            service = form.save(commit=False)
            service.provider = request.user
            service.save()
            return redirect('dashboard')
    else:
        form = ServiceForm()
    return render(request, 'services/service_form.html', {'form': form, 'title': 'Add Service'})

@login_required
def edit_service(request, pk):
    service = get_object_or_404(Service, pk=pk, provider=request.user)
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ServiceForm(instance=service)
    return render(request, 'services/service_form.html', {'form': form, 'title': 'Edit Service'})

@login_required
def delete_service(request, pk):
    service = get_object_or_404(Service, pk=pk, provider=request.user)
    if request.method == 'POST':
        service.delete()
        return redirect('dashboard')
    return render(request, 'services/service_confirm_delete.html', {'service': service})
