from django import forms
from .models import Room, Item, UserProfile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name']

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'location', 'birth_date']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'})
        }

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'description', 'quantity', 'room']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'quantity': forms.NumberInput(attrs={'min': 1}),
        }

    def __init__(self, user, *args, **kwargs):
        super(ItemForm, self).__init__(*args, **kwargs)
        # Filter rooms to only show the current user's rooms
        self.fields['room'].queryset = Room.objects.filter(user=user)
        # Make room selection optional
        self.fields['room'].required = False
        # Add placeholder for room selection
        self.fields['room'].empty_label = "-- Select a Room --"
