from django.urls import path
from .import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView


urlpatterns = [
     path('signup/', views.SignUp.as_view(), name='register'),
     path('login/', LoginView.as_view(), name='login'),
     path('logout/', auth_views.LogoutView.as_view(), name='logout'),
     path('create/setting/', views.ProfileView.as_view(), name='setting'),
]