from django import forms
from .models import Room, Item, UserProfile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'})
        }

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserProfileForm(forms.ModelForm):
    birth_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control'
            },
            format='%Y-%m-%d'
        ),
        required=False,
        input_formats=['%Y-%m-%d']
    )
    
    class Meta:
        model = UserProfile
        fields = ['bio', 'location', 'birth_date']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'location': forms.TextInput(attrs={'placeholder': 'Where are you from?', 'class': 'form-control'}),
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
        self.fields['room'].queryset = Room.objects.filter(user=user)
        self.fields['room'].required = False
        self.fields['room'].empty_label = "-- Select a Room --"
