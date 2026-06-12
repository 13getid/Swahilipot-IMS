from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404,redirect, render

from accounts.decorators import role_required
from.forms import TraineeForm
from .models import Trainee

# Create your views here.
@login_required
@role_required('instructor')
def trainee_list(request):
    show = request.GET.get('show','active')
    trainees = Trainee.objects.filter(
        department = request.user.department,
        is_active=(show != 'inactive'),
    ).order_by('name')

    return render(request, 'trainees/trainee_list.html',{
        'trainees': trainees,
        'form':TraineeForm(),
        'show':show,
        })

@login_required
@role_required('instructor')
def trainee_add(request):
    if request.method != 'POST':
        return redirect('trainees')
    
    form = TraineeForm(request.POST)
    if form.is_valid():
        trainee = form.save(commit=False)
        trainee.department = request.user.department
        trainee.added_by = request.user
        trainee.save()
        return redirect('trainees')
    
    trainee = Trainee.objects.filter(
        department = request.user.department,is_active = True
    ).order_by('name')
    return render(request,'trainees/trainee_list.html',{
        'trainees':trainee,
        'form': form,
        'show':'active',
        'open_modal':True,
    })

@login_required
@role_required('instructor')
def trainee_deactivate(request,pk):
    if request.method =="POST":
        trainee = get_object_or_404(
            Trainee,pk=pk, department = request.user.department
        )
        trainee.is_active = False
        trainee.save()
    return redirect('trainees')    