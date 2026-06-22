from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.utils import timezone

from accounts.decorators import role_required,department_feature_required
from .forms import DowntimeForm
from .models import DowntimeReport
# Create your views here.

@login_required
@department_feature_required('has_radio_report')
def downtime_list(request):
    if request.user.role == 'instructor':
        reports = DowntimeReport.objects.filter(instructor=request.user)
    else:
        reports = DowntimeReport.objects.filter(
            instructor__department= request.user.department
        )
    reports = reports.select_related('instructor').order_by('-reported_at')  

    return render(request, 'downtime/downtime_list.html',{
        'report': reports,
        'form':DowntimeForm(),
    })      

@login_required
@role_required('instructor')
@department_feature_required('has_radio_report')
def downtime_report(request):
    if request.method =='[POST]':
        form = DowntimeForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.instructor = request.user
            report.save()
            messages.success(request,'Downtime report.')
    
    return redirect('downtime') 

@login_required
@role_required('supervisor')
@department_feature_required('has_radio_report')
def downtime_resolve(request,pk):
    if request.method == 'POST': 
        note = request.POST.get('resolution_note', '').strip()
        if not note:
            messages.error(request,'A resolution note is required.')
            return redirect('downtime')

        report = get_object_or_404(
            DowntimeReport,pk=pk , instructor__department = request.user.department
        )
        report.status = 'resolved'
        report.resolution_note = note
        report.resolved_at = timezone.now()
        report.save()
    return redirect('downtime')    
              