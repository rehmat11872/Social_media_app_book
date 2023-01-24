from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic
from accounts.forms import WebSignUpForm
from django.views.generic import CreateView
# from .forms import *
# Create your views here.

class SignUp(generic.CreateView):
    form_class = WebSignUpForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

