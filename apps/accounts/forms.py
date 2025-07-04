from django import forms
from django.contrib.auth import get_user_model
from .models import CustomUser
from django.contrib.auth import authenticate

class loginUserForm(forms.Form):
    username = forms.CharField(label="Ім'я користувача", widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError("Невірне ім'я користувача або пароль.")
        return cleaned_data

class CreateUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email")

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if get_user_model().objects.filter(username=username).exists():
            raise forms.ValidationError("Дане ім'я вже зайняте")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError("Ця пошта вже зайнята")
        return email
