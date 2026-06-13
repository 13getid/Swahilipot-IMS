from django.urls import path
from . import views

urlpatterns = [
    path('attendance/', views.session_list, name='attendance'),
    path('attendance/create/', views.session_create, name='session_create'),
   
]