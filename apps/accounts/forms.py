from django import forms
from django.contrib.auth import get_user_model
from .models import CustomUser
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm

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

class CreateUserForm(UserCreationForm):
    password2 = forms.CharField(
        label='Повторіть пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    class Meta:
        model = CustomUser
        fields = (
            'username',
            'email',
            'full_name',
            'date_of_birth',
            'phone_number',
            'gender'
        )
        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
        }


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

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if get_user_model().objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError("Цей номер вже занятий")
        return phone_number


class ChangeAccountDetailsForm(forms.ModelForm):
    old_password = forms.CharField(
        label="Старий пароль",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False
    )
    new_password1 = forms.CharField(
        label="Новий пароль",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False
    )
    new_password2 = forms.CharField(
        label="Повторіть новий пароль",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False
    )
    class Meta:
        model = CustomUser
        fields = (
            'full_name',
            'date_of_birth',
            'gender'
        )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        old_password = cleaned_data.get('old_password')
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')
        if old_password and new_password1 and new_password2:
            if not self.user.check_password(old_password):
                self.add_error('old_password', 'Неправильний старий пароль.')

            if new_password1 != new_password2:
                self.add_error('new_password1', 'Нові паролі не співпадають.')

            if not new_password1:
                self.add_error('new_password1', 'Поле нового пароля не може бути порожнім.')

        return cleaned_data