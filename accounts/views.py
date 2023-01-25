from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic
from accounts.forms import WebSignUpForm, ProfileUpdateForm
from django.views.generic import TemplateView, CreateView
from django.contrib  import messages
from django.contrib.auth.models import User, auth
from core.models import Profile
# from .forms import *
# Create your views here.

class SignUp(CreateView):
    form_class = WebSignUpForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


    def form_valid(self, form):
        self.object = form.save()
        user_model = User.objects.get(username=self.object.username)
        new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
        return super().form_valid(form)


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'setting.html'
    form_class = ProfileUpdateForm


    def get(self, request, *args, **kwargs):
        user_profile =  Profile.objects.get(user=request.user)
        context = {
            'user_profile':user_profile
        }
        return render(self.request, self.template_name, context=context)


    def post(self, request, *args, **kwargs):
        user_profile =  Profile.objects.get(user=request.user)
        if request.method == 'POST':
            if request.FILES.get('image') == None:
                image = user_profile.profileimg
                bio = request.POST['bio']
                location = request.POST['location']

                user_profile.profileimg = image
                user_profile.bio = bio
                user_profile.location = location
                user_profile.save()
            if request.FILES.get('image') != None:
                image = request.FILES.get('image')
                bio = request.POST['bio']
                location = request.POST['location']

                user_profile.profileimg = image
                user_profile.bio = bio
                user_profile.location = location
                user_profile.save()
                return redirect('setting')
        return render(self.request, self.template_name, {'user_profile': user_profile})        
