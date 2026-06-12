from django import forms
from django.core.validators import RegexValidator
from.models import Trainee

Kenyan_phone = RegexValidator(
    regex= r'^0(7|1)\d{8}$',
    message ='Enter A valid Kenyan phone number,e.g. 0712345678',
)

class TraineeForm(forms.ModelForm):
    phone = forms.CharField(validators=[Kenyan_phone])

    class Meta:
        model = Trainee
        fields = ['name', 'phone']
