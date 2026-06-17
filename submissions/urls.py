from django.urls import path
from . import views

urlpatterns = [
    path('submissions/', views.submission_list, name='submissions'),
    path('submissions/new/', views.submission_create, name='submission_new'),
    path('submissions/<int:pk>/acknowledge/', views.submission_acknowledge, name='submission_acknowledge'),
    path('submissions/<int:pk>/return/', views.submission_return, name='submission_return'),
]