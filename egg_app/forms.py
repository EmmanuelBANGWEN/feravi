from django import forms
from .models import Data

class DataForm(forms.ModelForm):
    class Meta:
        model = Data
        fields = ["date", "time_slot", "temperature", "humidity", "egg_count", "chicken_count"]
        widgets = {
            "date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "time_slot": forms.Select(attrs={"class": "form-control"}),  # Sélection du créneau
            "temperature": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Température (°C)"}),
            "humidity": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Humidité (%)"}),
            "egg_count": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Nombre d'œufs"}),
            "chicken_count": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Nombre de poules"}),
        }



class Datetodate(forms.Form):
    from_date=forms.DateField(label='De', widget=forms.DateInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD','type': 'date'}))
    to_date=forms.DateField(label='à', widget=forms.DateInput(attrs={'class': 'flatpickr', 'placeholder': 'YYYY-MM-DD','type': 'date'}))
    



# class DateFilterForm(forms.Form):
#     start_date = forms.DateField(
#         required=False,
#         widget=forms.DateInput(attrs={"type": "date", "class": "form-control"})
#     )
#     end_date = forms.DateField(
#         required=False,
#         widget=forms.DateInput(attrs={"type": "date", "class": "form-control"})
#     )

# from django import forms
class DateFilterForm(forms.Form):
    TIME_SLOTS = [
        ("", "Tous les créneaux"),  # Pour laisser le champ facultatif
        ("08:00", "08:00"),
        ("13:00", "13:00"),
        ("17:00", "17:00"),
    ]

    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        label="Date de début",
        required=False
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        label="Date de fin",
        required=False
    )
    time_slot = forms.ChoiceField(
        choices=TIME_SLOTS,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Créneau horaire"
    )





from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Repeat Password'}),
        }

class LoginUserForm(forms.Form):
    username = forms.CharField(label='Username', max_length=150, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(label='Password', max_length=150, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))



