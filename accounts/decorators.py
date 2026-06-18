from functools import wraps
from django.http import HttpResponseForbidden
from django.shortcuts import render


def role_required(*roles):
    def decorator (view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if request.user.role not in roles:
                return HttpResponseForbidden('You do not have permission to view this page.')
            return view_func(request,*args, **kwargs)
        return wrapper
    return decorator

def department_feature_required(flag):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request,*args, **kwargs):
            if not getattr(request.user.department,flag,False):
                return render(request,'downtime/not_available.html')
            return view_func(request,*args, **kwargs)
        return wrapper
    return decorator