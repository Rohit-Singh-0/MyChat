from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import random
import time
import json
from .models import RoomMember
from agora_token_builder import RtcTokenBuilder
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def getToken(request):
    from django.conf import settings
    appId = settings.AGORA_APP_ID
    appCertificate = settings.AGORA_APP_CERTIFICATE
    channelName = request.GET.get('channel')
    uid = random.randint(1, 230)
    expirationTimeInSeconds = 3600 * 24
    currentTimestamp = int(time.time())
    privilegeExpiredTs = currentTimestamp + expirationTimeInSeconds
    role = 1

    token = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, channelName, uid, role, privilegeExpiredTs)
    return JsonResponse({'token':token, 'uid':uid, 'appId': appId}, safe=False)


@login_required(login_url='login')
def lobby(request):
    return render(request, 'base/lobby.html')


@login_required(login_url='login')
def room(request):
    return render(request, 'base/room.html')
@login_required(login_url='login')
def getMember(request):
    uid =request.GET.get('UID')
    room_name = request.GET.get('room_name') 

    member = RoomMember.objects.get(
        uid = uid,
        room_name = room_name,
        
    )
    name = member.name
    return JsonResponse({'name': member.name}, safe=False)

def login_view(request):
    if request.user.is_authenticated:
        return redirect('lobby')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password  = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('lobby')
        else:
            messages.error(request, 'Invalid username or password.')
            
    return render(request, 'base/login.html')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('lobby')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password  = request.POST.get('password')
        confirm_password  = request.POST.get('confirm_password')
        
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
        else:
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            return redirect('lobby')
            
    return render(request, 'base/register.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def about_view(request):
    return render(request, 'base/about.html')

def contact_view(request):
    return render(request, 'base/contact.html')
