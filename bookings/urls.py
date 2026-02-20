from django.urls import path
from . import views

urlpatterns = [
    path('book/<int:service_id>/', views.book_service, name='book_service'),
    path('my-bookings/', views.customer_bookings, name='customer_bookings'),
    path('manage-bookings/', views.provider_bookings, name='provider_bookings'),
    path('update-status/<int:booking_id>/<str:status>/', views.update_booking_status, name='update_booking_status'),
    path('cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
]
