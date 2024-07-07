from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from chat.models import Message
from chat.forms import MessageForm
from datetime import timedelta
from django.utils import timezone

User = get_user_model()

@login_required
def chat_list_view(request, username=None):
    user = request.user
    
    # Contacts avec lesquels l'utilisateur a échangé des messages
    contacts = User.objects.filter(
        Q(sent_messages__receiver=user) | Q(received_messages__sender=user)
    ).distinct()

    current_contact = None
    messages = []

    # If no username is provided, default to the first contact
    if not username and contacts.exists():
        current_contact = contacts.first()
        username = current_contact.email
    elif username:
        current_contact = get_object_or_404(User, email=username)
    
    if current_contact:
        messages = Message.objects.filter(
            sender__in=[user, current_contact],
            receiver__in=[user, current_contact]
        ).order_by('timestamp')
        
        # Marquer les messages comme lus lorsque l'utilisateur ouvre le chat
        messages.filter(receiver=user, is_read=False).update(is_read=True)

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = user
            message.receiver = current_contact
            message.save()
            return redirect('chat_list', username=username)
    else:
        form = MessageForm()

    # Determine online status and unread message count
    for contact in contacts:
        profile = contact.profile
        profile.is_online = profile.last_active and timezone.now() - profile.last_active < timedelta(minutes=5)
        profile.was_recently_online = profile.last_active and timezone.now() - profile.last_active < timedelta(hours=72)
        contact.unread_count = Message.objects.filter(sender=contact, receiver=user, is_read=False).count()
    
    # Count unread messages for navbar
    unread_messages_count = Message.objects.filter(receiver=user, is_read=False).count()

    context = {
        'contacts': contacts,
        'current_contact': current_contact,
        'messages': messages,
        'form': form,
        'active_chat': username,  # Ajouter l'email du contact actuel au contexte
        'unread_messages_count': unread_messages_count,  # Ajouter le nombre de messages non lus au contexte
    }
    return render(request, 'chat/chat_list.html', context)
