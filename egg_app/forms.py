from django import forms
from .models import Data

class DataForm(forms.ModelForm):
    class Meta:
        model = Data
        fields = ["date", "temperature", "humidity", "egg_count", "chicken_count"]
        widgets = {
            "temperature": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Température (°C)"}),
            # "date": forms.DateInput(attrs={"class": "form-control", "placeholder": "Date"}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'YYYY-MM-DD','type': 'date'}),

            "humidity": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Humidité (%)"}),
            "egg_count": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Nombre d'œufs"}),
            "chicken_count": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Nombre de poules"}),
        }
