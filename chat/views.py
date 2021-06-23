from django.shortcuts import render, redirect
from chat.models import Room, Message
from django.http import HttpResponse, JsonResponse
from cryptography.fernet import Fernet

# Generamos una key de seguridad, a modo de demostracion, en un proyecto real se debería generar una key por usuario
file = open('key.key', 'rb')
key = file.read()
file.close()

def home(request):
    return render(request, 'home.html')

def room(request, room):
    username = request.GET.get('username')
    room_details = Room.objects.get(name=room)
    return render(request, 'room.html', {
        'username': username,
        'room': room,
        'room_details': room_details
    })

def checkview(request):
    room = request.POST['room_name']
    username = request.POST['username']

    if Room.objects.filter(name=room).exists():
        return redirect('/'+room+'/?username='+username)
    else:
        new_room = Room.objects.create(name=room)
        new_room.save()
        return redirect('/'+room+'/?username='+username)

def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']

    # Creamos un nuevo mensaje
    new_message = Message.objects.create(value=message, user=username, room=room_id)

    # Codificamos el mensaje
    encoded = new_message.encode()

    # Encriptamos el mensaje
    f = Fernet(key)
    encrypted = f.encrypt(encoded)

    # Guardamos el mensaje encriptado
    encrypted_message = Message.objects.create(encrypted)
    encrypted_message.save()
    return HttpResponse('Message sent successfully')

def getMessages(request, room):
    room_details = Room.objects.get(name=room)

    messages = Message.objects.filter(room=room_details.id)

    # Dentro de este método los mensajes llegan desencriptados

    return JsonResponse({"messages":list(messages.values())})