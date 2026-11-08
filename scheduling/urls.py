from django.urls import path

from . import views

urlpatterns = [
    path('api/interviews/', views.APIInterviews, name='api_interviews'),
    path('api/interviews/<int:interview_id>/delete/', views.APIDelete, name='api_delete_interview'),
    path('', views.Home, name='home'),
    path('view/', views.View, name='view'),
    path('delete/<int:interview_id>/', views.Delete, name='delete'),
    path('edit/<int:interview_id>/', views.Edit, name='edit'),
]
