from django import forms

from .models import Participant, Partner


class ParticipantRegistrationForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['region', 'school_name', 'full_name', 'age', 'grade_or_course', 'email', 'password']

class PartnerRegistrationForm(forms.ModelForm):
    class Meta:
        model = Partner
        fields = ['organization_name', 'full_name', 'email', 'password']