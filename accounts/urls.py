from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('', views.login_view, name='home'),      # root -> login
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
]
