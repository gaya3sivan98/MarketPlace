from django.urls import path
from . import views

urlpatterns = [
    path('checkout/<int:booking_id>/', views.initiate_payment, name='initiate_payment'),
    path('success/<int:booking_id>/', views.payment_success, name='payment_success'),
    path('cancel/', views.payment_cancel, name='payment_cancel'),
]
