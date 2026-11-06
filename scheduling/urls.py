from django.urls import path

from . import views

urlpatterns = [
    path('', views.Home, name='home'),
    path('view/', views.View, name='view'),
    path('delete/<int:interview_id>/', views.Delete, name='delete'),
]
