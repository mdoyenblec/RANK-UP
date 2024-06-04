from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from chat.models import Message
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404

User = get_user_model()

@login_required
def chat_list_view(request, username=None):
    contacts = User.objects.all()  # ou une méthode pour obtenir les contacts pertinents
    current_contact = None
    messages = []

    if username:
        current_contact = get_object_or_404(User, email=username)
        messages = Message.objects.filter(
            sender__in=[request.user, current_contact],
            receiver__in=[request.user, current_contact]
        ).order_by('timestamp')

    context = {
        'contacts': contacts,
        'current_contact': current_contact,
        'messages': messages,
    }
    return render(request, 'chat/chat_list.html', context)


