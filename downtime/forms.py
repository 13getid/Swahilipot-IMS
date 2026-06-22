from django import forms
from .models import DowntimeReport

class DowntimeForm(forms.ModelForm):
    class Meta:
        model = DowntimeReport
        fields = ['frequency_band','description','severity']