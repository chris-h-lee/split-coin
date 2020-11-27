from .models import Create, Profile
from django import forms


class CreateForm(forms.ModelForm):
    class Meta:
        model = Create
        fields = ('Name', 'Description', 'Event', 'Date', 'Time', 'duration')
