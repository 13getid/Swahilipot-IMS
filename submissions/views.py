from django.shortcuts import get_object_or_404,redirect,render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from accounts.decorators import role_required
from .forms import SubmissionForm
from .models import FormSubmission

# Create your views here.
@login_required 
def submission_list(request):
    status_filter = request.GET.get('status','all')

    if request.user.role == 'instructor':
        submission = FormSubmission.objects.filter(instructor= request.user)
    else:
        submission = FormSubmission.objects.filter(department=request.user.department)    
    if status_filter != 'all':
        submission = submission.filter(status =status_filter)    
    submissions = submission.select_related('instructor').order_by('-submitted_at')

    return render(request,'submissions/submission_list.html',{
        'submissions': submissions,
        'status_filter': status_filter,
        'tabs':['all','submitted','acknowledge','returned']
    })  

@login_required
@role_required('instructor')
def submission_create(request):
    if request.method == 'POST':
        form = SubmissionForm(request.POST,request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.instructor = request.user
            submission.department = request.user.department
            submission.save()
            messages.success(request, 'Submission filed successfully.')
            return redirect('submissions')
        else:
            return render(request,'submissions/submission_new.html', {'form': form})

@login_required
@role_required('supervisor')
def submission_acknowledge(request, pk):
    if request.method == 'POST':
        submission = get_object_or_404(
            FormSubmission, pk=pk, department=request.user.department
        )
        submission.status = 'acknowledged'
        submission.supervisor_note = request.POST.get('supervisor_note', '').strip()
        submission.acknowledged_at = timezone.now()
        submission.save()
    return redirect('submissions')

@login_required
@role_required('supervisor')
def submission_return(request, pk):
    if request.method == 'POST':
        note = request.POST.get('supervisor_note', '').strip()
        if not note:
            messages.error(request, 'A note is required when returning a submission.')
            return redirect('submissions')

        submission = get_object_or_404(
            FormSubmission, pk=pk, department=request.user.department
        )
        submission.status = 'returned'
        submission.supervisor_note = note
        submission.save()
    return redirect('submissions')