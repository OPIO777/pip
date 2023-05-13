
from .models import Tasking

from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.contrib.auth.models import User


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserResetPasswordForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'autocomplete': 'email'}))


class TaskingForm(forms.ModelForm):
    reminder_time = forms.IntegerField()


class TaskingForm(forms.ModelForm):
    class Meta:
        model = Tasking
        fields = ['task', 'description', 'due_date', 'reminder_time', 'completed', 'skipped']
        widgets = {
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
