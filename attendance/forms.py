from django import forms 

class CheckInForm(forms.Form):
    trainee_name = forms.CharField(max_length=150)
    trainee_phone = forms.CharField(max_length=20)
    tasks_completed = forms.CharField(widget=forms.Textarea)