from django.contrib import admin
from .models import Message

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'timestamp', 'status')
    list_filter = ('timestamp', 'status')
    search_fields = ('sender__username', 'recipient__username', 'content')
