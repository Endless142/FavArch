from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *
from django.forms import ModelForm, TextInput, PasswordInput, EmailInput

from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _

class RegistrationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Пароль',
            'style': 'width: 200px; margin-top: 5px'})
        self.fields['password2'].widget = PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Подтвредите пароль',
            'style': 'width: 200px; margin-top: 5px'})
    class Meta:


        model = User
        fields = ('username', 'email', 'password1', 'password2')

        widgets = {
            'username': TextInput(attrs={
                'class': 'form',
                'placeholder': 'Логин',
                'style': 'width: 200px; margin-top: 5px'
            }),
            'email': EmailInput(attrs={
                'class': 'form',
                'placeholder': 'Email',
                'style': 'width: 200px; margin-top: 5px'
            })


        }
        error_messages = {
            'password2': {
                'no_match': _('Пароли не совпадают.'),  # Перевод сообщения
            },
            'password1': {
                'user_attribute_similarity': _('Пароль слишком похож на имя пользователя.'),
                'too_short': _('Пароль слишком короткий. Он должен содержать не менее 8 символов.'),
                'common': _('Этот пароль слишком распространен.'),
            }
        }

class AuthUserForm(AuthenticationForm, ModelForm):
    def __init__(self, *args, **kwargs):
        super(AuthUserForm, self).__init__(*args, **kwargs)
        self.fields['password'].widget = PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Пароль',
            'style': 'width: 200px; margin-top: 5px'})
        self.fields['username'].widget = TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Логин',
            'style': 'width: 200px; margin-top: 5px'})
    class Meta:
        model = User
        fields = ['username', 'password']


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'author', 'premiere', 'text']  # Добавьте 'author' в fields

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields['author'].widget = forms.HiddenInput()
            self.fields['author'].initial = user

            self.fields['title'].widget.attrs['placeholder'] = 'Заголовок'

            self.fields['premiere'].widget.attrs['placeholder'] = 'Премьера'
            self.fields['premiere'].widget.attrs['style'] = 'height: 100px;'

            self.fields['text'].widget.attrs['placeholder'] = 'Текст статьи'
