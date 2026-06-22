from django.urls import path
from . import views

urlpatterns = [
    path('downtime/', views.downtime_list, name='downtime'),
    path('downtime/report/', views.downtime_report, name='downtime_report'),
    path('downtime/<int:pk>/resolve/', views.downtime_resolve, name='downtime_resolve'),

    ]