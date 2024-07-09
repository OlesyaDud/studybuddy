from django.shortcuts import redirect, render
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import Room, Topic
from .forms import RoomForm



# LOGIN

def loginPage(request):

    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password does not exist')


    context = {'page': page}
    return render(request, 'baseapp/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')



def registerUser(request):
    form = UserCreationForm()
    page = 'register'

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home') 
        else:
            messages.error(request, 'Something went wrong. Please try again.')

    context = {'form': form, 'page': page}
    return render(request, 'baseapp/login_register.html', context)

# HOME

def home(request):
    q = request.GET.get('q', '')  # Use get method to retrieve the value of 'q' parameter
    if q:
        # searching by topic name only
        # rooms = Room.objects.filter(topic__name__icontains=q)

        # dynamic search
        rooms = Room.objects.filter(Q(topic__name__icontains=q) |
                                    Q(name__icontains=q) |
                                    Q(description__icontains=q))
    else:
        rooms = Room.objects.all()

    topics = Topic.objects.all()
    room_count = rooms.count()

    context = {'rooms': rooms, 'topics': topics, 'room_count':room_count}
    return render(request, 'baseapp/home.html', context)


# ROOM CRUD

def room(request, id):
    room = Room.objects.get(id=id)
    context = {'room': room}
    return render(request, 'baseapp/room.html', context)

# if user is not authenticated will be redirected to login page
@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        print(request.POST)
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form}
    return render(request, 'baseapp/room_form.html', context)

@login_required(login_url='login')
def updateRoom(request, id):
    room = Room.objects.get(id=id)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse('Action not allowed')
    


    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'baseapp/room_form.html', context)

@login_required(login_url='login')
def deleteRoom(request, id):
    room = Room.objects.get(id=id)

    if request.user != room.host:
        return HttpResponse('Action not allowed')
    
    if request.method == 'POST':
        room.delete()
        return redirect('home')

    return render(request, 'baseapp/delete.html', {'obj':room})