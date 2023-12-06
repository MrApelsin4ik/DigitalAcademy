from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):
    username = forms.CharField(max_length=50, label='Имя пользователя')
    is_participant = forms.BooleanField(initial=True, required=False)
    region = forms.CharField(max_length=255, required=False)
    school_name = forms.CharField(max_length=255, required=False)
    full_name = forms.CharField(max_length=255, required=False)
    age = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'type': 'number', 'min': '0'}))
    grade_or_course = forms.CharField(max_length=255, required=False)
    organization_name = forms.CharField(max_length=255, required=False)



    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'is_participant', 'region', 'school_name', 'full_name', 'age',
                  'grade_or_course', 'organization_name']

