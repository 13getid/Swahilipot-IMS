from django.urls import path
from . import views

urlpatterns = [
    path('attendance/', views.session_list, name='attendance'),
    path('attendance/create/', views.session_create, name='session_create'),
    path('attend/<uuid:token>/', views.attend_page, name='attend'),
    path('attend/<uuid:token>/checkout/<int:record_id>/', views.attend_checkout, name='attend_checkout'),
    path('attendance/<int:pk>/', views.session_detail, name='session_detail'),
    path('attendance/records/<int:pk>/confirm/', views.record_confirm, name='record_confirm'),
]