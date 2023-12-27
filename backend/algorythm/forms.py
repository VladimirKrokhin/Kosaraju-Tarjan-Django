
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from algorythm.models import Graph


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(label='Email')  # Добавление label для лучшего отображения меток

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'username': 'Имя пользователя',  # Указание меток для полей
            'password1': 'Пароль',
            'password2': 'Повторный пароль',
        }



class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Имя пользователя'  # Установка меток для полей
        self.fields['password'].label = 'Пароль'
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Имя пользователя'})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Пароль'})


class GraphForm(forms.ModelForm):
    class Meta:
        model = Graph 
        fields = ['name'] 