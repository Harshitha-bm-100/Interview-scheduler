from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views

urlpatterns = [
    path('', views.opening_list, name='opening_list'),
    path('openings/new/', views.opening_create, name='opening_create'),
    path('openings/<int:pk>/', views.opening_detail, name='opening_detail'),
    path('openings/<int:pk>/apply/', views.apply, name='apply'),
    path('applications/<int:pk>/interview/', views.schedule_interview, name='schedule_interview'),
    path('availability/new/', views.availability_create, name='availability_create'),
    path('register/', views.register, name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
