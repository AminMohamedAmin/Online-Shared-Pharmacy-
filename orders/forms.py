from django import forms
from .models import order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = order
        fields = ('first_name','last_name','email','street','address','country')
        COUNTRY_CHOICES = (
            ('Meet massoud', 'Meet massoud'),
            ('Ekhtab', 'Ekhtab'),
            ('Damas', 'Damas'),
            ('Tonamel', 'Tonamel'),
            ('Galmoh', 'Galmoh'),
            ('Elbakly', 'Elbakly'),
            ('Elshoky', 'Elshoky'),
        )

        widgets = {
            'first_name': forms.TextInput(attrs={'class' : 'w3-center', 'style' : 'width:300px; border-radius: 5px; padding: 5px', 'placeholder': 'first name'}),
            'last_name': forms.TextInput(attrs={'class': 'w3-center', 'style': 'width:300px; border-radius: 5px; padding: 5px', 'placeholder': 'last name' }),
            'email': forms.TextInput(attrs={'class': 'w3-center', 'style': 'width:300px; border-radius: 5px; padding: 5px', 'placeholder': 'email' }),
            'street': forms.TextInput(attrs={'class': 'w3-center', 'style': 'width:300px; border-radius: 5px; padding: 5px', 'placeholder': 'street' }),
            'address': forms.TextInput(attrs={'class': 'w3-center', 'style': 'width:300px; border-radius: 5px; padding: 5px', 'placeholder': 'address' }),
            'country': forms.Select(choices=COUNTRY_CHOICES, attrs={'class': 'w3-center', 'style': 'width:300px; border-radius: 5px; padding: 5px'}),
        }