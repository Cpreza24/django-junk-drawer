from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserProfileForm, ItemForm, RoomForm
from .models import Room, Item, UserProfile
from django.db.models import Q
from django.contrib import messages
from django.utils import timezone


@login_required
def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def rooms_index(request):
    try:
        search_query = request.GET.get('search', '')
        sort_by = request.GET.get('sort', 'name')
        
        rooms = Room.objects.filter(user=request.user)
        
        if search_query:
            rooms = rooms.filter(name__icontains=search_query)
        
        if sort_by == 'name':
            rooms = rooms.order_by('name')
        elif sort_by == 'created':
            rooms = rooms.order_by('-created_at')
        elif sort_by == 'updated':
            rooms = rooms.order_by('-updated_at')
        
        return render(request, 'rooms/index.html', {
            'rooms': rooms,
            'search_query': search_query,
            'sort_by': sort_by
        })
    except Exception as e:
        print(f"Error in rooms_index: {str(e)}")
        return render(request, 'rooms/index.html', {
            'rooms': [],
            'search_query': '',
            'sort_by': 'name'
        })

@login_required
def rooms_new(request):
    form = RoomForm()
    return render(request, 'rooms/new.html', {'form': form})

@login_required
def rooms_create(request):
    try:
        if request.method == 'POST':
            form = RoomForm(request.POST)
            if form.is_valid():
                room = form.save(commit=False)
                room.user = request.user
                room.save()
                messages.success(request, f"Room '{room.name}' created successfully")
                return redirect('rooms_detail', room_id=room.id)
            else:
                messages.error(request, "Please correct the errors below.")
                return redirect('rooms_new')
        return redirect('rooms_index')
    except Exception as e:
        print(f"Error in rooms_create: {str(e)}")  # Debug log
        messages.error(request, "An error occurred while creating the room")
        return redirect('rooms_new')

@login_required
def rooms_detail(request, room_id):
    room = get_object_or_404(Room, id=room_id, user=request.user)
    items = Item.objects.filter(room=room, user=request.user)
    return render(request, 'rooms/show.html', {'room': room, 'items': items})

@login_required
def rooms_edit(request, room_id):
    room = get_object_or_404(Room, id=room_id, user=request.user)
    form = RoomForm(instance=room)
    return render(request, 'rooms/edit.html', {'room': room, 'form': form})

@login_required
def rooms_update(request, room_id):
    room = get_object_or_404(Room, id=room_id, user=request.user)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('rooms_detail', room_id=room.id)
    return redirect('rooms_index')

@login_required
def rooms_delete(request, room_id):
    room = get_object_or_404(Room, id=room_id, user=request.user)
    if request.method == 'POST':
        room.delete()
        return redirect('rooms_index')
    return redirect('rooms_index')

@login_required
def profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            profile = form.save(commit=False)
            # Ensure we're properly handling the birth date
            if 'birth_date' in request.POST and request.POST['birth_date']:
                profile.birth_date = request.POST['birth_date']
            profile.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user_profile)
    return render(request, 'registration/profile.html', {'form': form})

@login_required
def items_index(request):
    rooms = Room.objects.filter(user=request.user)
    if not rooms.exists():
        messages.info(request, "Please create a room before adding items.")
        return redirect('rooms_new')

    search_query = request.GET.get('search', '')
    sort_by = request.GET.get('sort', 'name')
    room_filter = request.GET.get('room', '')
    
    items = Item.objects.filter(user=request.user)
    
    if search_query:
        items = items.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    if room_filter:
        items = items.filter(room_id=room_filter)
    
    if sort_by == 'name':
        items = items.order_by('name')
    elif sort_by == 'created':
        items = items.order_by('-created_at')
    elif sort_by == 'updated':
        items = items.order_by('-updated_at')
    elif sort_by == 'quantity':
        items = items.order_by('-quantity')
    
    return render(request, 'items/index.html', {
        'items': items,
        'search_query': search_query,
        'sort_by': sort_by,
        'room_filter': room_filter,
        'rooms': rooms
    })

@login_required
def items_new(request):
    rooms = Room.objects.filter(user=request.user)
    if not rooms.exists():
        messages.info(request, "Please create a room before adding items.")
        return redirect('rooms_new')

    form = ItemForm(request.user)
    return render(request, 'items/new.html', {'form': form})

@login_required
def items_create(request):
    if request.method == 'POST':
        form = ItemForm(request.user, request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.save()
            return redirect('items_detail', item_id=item.id)
    return redirect('items_index')

@login_required
def items_detail(request, item_id):
    item = get_object_or_404(Item, id=item_id, user=request.user)
    return render(request, 'items/show.html', {'item': item})

@login_required
def items_edit(request, item_id):
    item = get_object_or_404(Item, id=item_id, user=request.user)
    form = ItemForm(request.user, instance=item)
    return render(request, 'items/edit.html', {'item': item, 'form': form})

@login_required
def items_update(request, item_id):
    item = get_object_or_404(Item, id=item_id, user=request.user)
    if request.method == 'POST':
        form = ItemForm(request.user, request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('items_detail', item_id=item.id)
    return redirect('items_index')

@login_required
def items_delete(request, item_id):
    item = get_object_or_404(Item, id=item_id, user=request.user)
    if request.method == 'POST':
        item.delete()
        return redirect('items_index')
    return redirect('items_index')







