from django.urls import path
from . import views

urlpatterns = [
    path('trainees/', views.trainee_list, name='trainees'),
    path('trainees/add/', views.trainee_add, name='trainee_add'),
    path('trainees/<int:pk>/deactivate/', views.trainee_deactivate, name='trainee_deactivate')
]
