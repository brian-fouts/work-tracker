from django.contrib.auth.models import User

from django import forms

class UserCreateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email", "username", "password", "first_name", "last_name"]
