from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Message
from accounts.models import User

@login_required
def inbox(request):
    # Get all users who have exchanged messages with the current user
    user_messages = Message.objects.filter(
        Q(sender=request.user) | Q(recipient=request.user)
    ).order_by('-timestamp')
    
    users = set()
    for msg in user_messages:
        sender = msg.sender
        recipient = msg.recipient
        if sender != request.user:
            users.add(sender)
        elif recipient != request.user:
            users.add(recipient)
            
    return render(request, 'chat/inbox.html', {'users': users})

@login_required
def chat_room(request, user_id):
    if request.user.id == user_id:
        messages.warning(request, "You cannot chat with yourself.")
        return redirect('inbox')
    
    other_user = get_object_or_404(User, pk=user_id)
    
    # Mark messages from other_user as read
    Message.objects.filter(sender=other_user, recipient=request.user, status='unread').update(status='read')
    
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(
                sender=request.user,
                recipient=other_user,
                content=content
            )
            return redirect('chat_room', user_id=user_id)
            
    chat_messages = Message.objects.filter(
        (Q(sender=request.user) & Q(recipient=other_user)) |
        (Q(sender=other_user) & Q(recipient=request.user))
    ).order_by('timestamp')
    
    return render(request, 'chat/room.html', {'other_user': other_user, 'chat_messages': chat_messages})
