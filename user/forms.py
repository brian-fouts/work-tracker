from django import forms

from .models import User


class UserCreateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email", "username", "password", "first_name", "last_name"]
