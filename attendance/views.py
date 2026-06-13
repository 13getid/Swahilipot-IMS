from django.shortcuts import  get_object_or_404,redirect, render
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from accounts.decorators import role_required
from .models import AttendanceSession
from .qr import make_qr_data_uri

# Create your views here.

@login_required
@role_required('instructor')
def session_list(request):
    sessions = AttendanceSession.objects.filter(
        instructor = request.user
    ).order_by('-created_at')

    new_qr = None
    new_url = None
    new_session_id = request.GET.get('new')
    if new_session_id:
        try:
            s = sessions.get(id = new_session_id)
            new_url = request.build_absolute_uri(f'/attend{s.token}')
            new_qr = make_qr_data_uri(new_url)
        except AttendanceSession.DoesNotExist:
            pass
    
    return render(request, 'attendance/session_list.html',{
        'session':sessions,
        'new_qr':new_qr,
        'new_url':new_url
    })

@login_required
@role_required('instructor')
def session_create(request):
    if request.method != 'POST':
        return redirect('attendance')

    label = request.POST.get('session_label', '').strip()
    session = AttendanceSession.objects.create(
        instructor=request.user,
        department=request.user.department,
        session_label=label,
    )
    return redirect(f"{request.build_absolute_uri('/attendance/')}?new={session.id}")    