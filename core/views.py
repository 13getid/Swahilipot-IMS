from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required


@login_required
def dashboard(request):
    return render(request, 'core/dashboard.html')

def home(request):
     return redirect('dashboard')
