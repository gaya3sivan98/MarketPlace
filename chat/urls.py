from django.urls import path
from . import views

urlpatterns = [
    path('inbox/', views.inbox, name='inbox'),
    path('room/<int:user_id>/', views.chat_room, name='chat_room'),
]
