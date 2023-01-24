from django.urls import path
from .import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView


urlpatterns = [
     path('signup/', views.SignUp.as_view(), name='register'),
     path('login/', LoginView.as_view(), name='login')
]