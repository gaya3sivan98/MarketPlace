from django.db import models
from accounts.models import User

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES = (
        ('unread', 'Unread'),
        ('read', 'Read'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='unread')

    @property
    def is_read(self):
        return self.status == 'read'

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"Message from {self.sender.username} to {self.recipient.username}"
