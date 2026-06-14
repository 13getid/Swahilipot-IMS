from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from accounts.decorators import role_required
from .models import AttendanceSession, AttendanceRecord
from .forms import CheckInForm
from .qr import make_qr_data_uri


@login_required
@role_required('instructor')
def session_list(request):
    sessions = AttendanceSession.objects.filter(
        instructor=request.user
    ).order_by('-created_at')

    new_qr = None
    new_url = None
    new_session_id = request.GET.get('new')
    if new_session_id:
        try:
            s = sessions.get(id=new_session_id)
            new_url = request.build_absolute_uri(f'/attend/{s.token}/')
            new_qr = make_qr_data_uri(new_url)
        except AttendanceSession.DoesNotExist:
            pass

    return render(request, 'attendance/session_list.html', {
        'sessions': sessions,
        'new_qr': new_qr,
        'new_url': new_url,
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


def attend_page(request, token):
    session = get_object_or_404(AttendanceSession, token=token)

    if session.is_expired:
        return render(request, 'attendance/attend_expired.html')

    if request.method == 'POST':
        form = CheckInForm(request.POST)
        if form.is_valid():
            record = AttendanceRecord.objects.create(
                session=session,
                trainee_name=form.cleaned_data['trainee_name'],
                trainee_phone=form.cleaned_data['trainee_phone'],
                tasks_completed=form.cleaned_data['tasks_completed'],
            )
            return render(request, 'attendance/attend_success.html', {
                'session': session,
                'record': record,
            })
    else:
        form = CheckInForm()

    return render(request, 'attendance/attend_form.html', {
        'session': session,
        'form': form,
    })


def attend_checkout(request, token, record_id):
    if request.method == 'POST':
        record = get_object_or_404(AttendanceRecord, id=record_id, session__token=token)
        record.check_out = timezone.now()
        record.save()
    return render(request, 'attendance/attend_done.html')

def _user_can_view_session(user, session):
    if user.role == 'instructor':
        return session.instructor_id == user.id
    if user.role == 'supervisor':
        return session.department_id == user.department_id
    return False

@login_required
@role_required('instructor', 'supervisor')
def session_detail(request,pk):
    session = get_object_or_404(AttendanceSession, pk=pk)

    if not _user_can_view_session(request.user,session):
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden('You can not view this session')
    
    records = session.records.all().order_by('check_in')

    return render(request, 'attendance/session_detail.html', {
        'session': session,
        'records': records,
        'total': records.count(),
        'confirmed': records.filter(is_confirmed=True).count(),
        'pending': records.filter(is_confirmed=False).count(),
    })

@login_required
@role_required('instructor')
def record_confirm(request,pk):
    if request.method == 'POST':
        record = get_object_or_404(
            AttendanceRecord,pk=pk, session__instructor= request.user
        )
        record.is_confirmed = True
        record.confirmed_at = timezone.now()
        record.save()
        return redirect('session_detail', pk=record.session_id)
    return redirect('attendance')