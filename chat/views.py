from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden, JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Room, Message
from .encryption import encrypt_message, decrypt_message
import uuid
from cryptography.fernet import Fernet


@login_required
def index(request):
    user_rooms = Room.objects.filter(users=request.user)
    return render(request, 'chat/index.html', {'user_rooms': user_rooms})

@login_required
def create_room(request):
    if request.method == 'POST':
        room_key = Fernet.generate_key().decode()
        url_path = str(uuid.uuid4())
        room = Room.objects.create(key=room_key, url_path=url_path)
        room.users.add(request.user)
        room.save()

        return redirect('chat:room', url_path=url_path)
    return render(request, 'chat/create_room.html')

@login_required
def room(request, url_path):
    room = get_object_or_404(Room, url_path=url_path)
    if request.user not in room.users.all():
        return HttpResponseForbidden("You do not have access to this room.")
    
    if request.method == 'POST':
        message_content = request.POST.get('message')
        encrypted_content = encrypt_message(message_content)
        Message.objects.create(room=room, sender=request.user, encrypted_content=encrypted_content)

    
    messages = Message.objects.filter(room=room).order_by('timestamp')
    decrypted_messages = []
    for msg in messages:
        try:
            decrypted_messages.append({
                'id': msg.id,
                'sender': msg.sender.username,
                'content': decrypt_message(msg.encrypted_content),
                'timestamp': msg.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            })
        except Exception as e:
            decrypted_messages.append({
                'id': msg.id,
                'sender': msg.sender.username,
                'content': "Decryption error: " + str(e),
                'timestamp': msg.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            })
    
    return render(request, 'chat/room.html', {'room': room, 'messages': decrypted_messages,'users':room.users.all()})

@login_required
def join_room(request):
    if request.method == 'POST':
        room_key = request.POST.get('room_key')
        room = get_object_or_404(Room, key=room_key)
        room.users.add(request.user)
        room.save()
        return redirect('chat:room', url_path=room.url_path)
    return render(request, 'chat/join_room.html')

@login_required
def get_new_messages(request, url_path):
    room = get_object_or_404(Room, url_path=url_path)
    last_message_id = request.GET.get('last_message_id', 0)
    
    messages = Message.objects.filter(room=room, id__gt=last_message_id).order_by('timestamp')

    message_list = []
    for msg in messages:
        try:
            message_list.append({
                'id': msg.id,
                'sender': msg.sender.username,
                'content': decrypt_message(msg.encrypted_content),
                'timestamp': msg.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            })
        except Exception as e:
            message_list.append({
                'id': msg.id,
                'sender': msg.sender.username,
                'content': "Decryption error: " + str(e),
                'timestamp': msg.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            })

    return JsonResponse({'messages': message_list})
