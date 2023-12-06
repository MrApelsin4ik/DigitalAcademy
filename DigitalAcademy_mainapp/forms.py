from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser, UserProfile


class RegistrationForm(UserCreationForm):
    is_participant = forms.BooleanField(initial=True, required=False)
    region = forms.CharField(max_length=255, required=False)
    school_name = forms.CharField(max_length=255, required=False)
    full_name = forms.CharField(max_length=255, required=False)
    age = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'type': 'number', 'min': '0'}))
    grade_or_course = forms.CharField(max_length=255, required=False)
    organization_name = forms.CharField(max_length=255, required=False)

    class Meta:
        model = CustomUser
        fields = ['email', 'password1', 'password2', 'is_participant', 'region', 'school_name', 'full_name', 'age', 'grade_or_course', 'organization_name']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.set_password(self.cleaned_data['password1'])
        user.save()

        profile = UserProfile.objects.create(
            user=user,
            is_participant=self.cleaned_data['is_participant'],
            region=self.cleaned_data['region'],
            school_name=self.cleaned_data['school_name'],
            full_name=self.cleaned_data['full_name'],
            age=self.cleaned_data['age'],
            grade_or_course=self.cleaned_data['grade_or_course'],
            organization_name=self.cleaned_data['organization_name']
        )

        return user
