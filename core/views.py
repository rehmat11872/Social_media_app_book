from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponse
from .models import Profile, Post, LikePost, FollowersCount
from itertools import chain
import random
# Create your views here.
class IndexView(LoginRequiredMixin, TemplateView):
   template_name = 'index.html'
     


   def get(self, request, *args, **kwargs):
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)
        posts = Post.objects.all()
        context = {
            'user_profile':user_profile,
            'posts': posts
        }
        return render(self.request, self.template_name, context=context)


# def index(request):
#     user_object = User.objects.get(username=request.user.username)
#     user_profile = Profile.objects.get(user=user_object)

#     user_following_list = []
#     feed = []

#     user_following = FollowersCount.objects.filter(follower=request.user.username)

#     for users in user_following:
#         user_following_list.append(users.user)

#     for usernames in user_following_list:
#         feed_lists = Post.objects.filter(user=usernames)
#         feed.append(feed_lists)

#     feed_list = list(chain(*feed))

#     # user suggestion starts
#     all_users = User.objects.all()
#     user_following_all = []

#     for user in user_following:
#         user_list = User.objects.get(username=user.user)
#         user_following_all.append(user_list)
    
#     new_suggestions_list = [x for x in list(all_users) if (x not in list(user_following_all))]
#     current_user = User.objects.filter(username=request.user.username)
#     final_suggestions_list = [x for x in list(new_suggestions_list) if ( x not in list(current_user))]
#     random.shuffle(final_suggestions_list)

#     username_profile = []
#     username_profile_list = []

#     for users in final_suggestions_list:
#         username_profile.append(users.id)

#     for ids in username_profile:
#         profile_lists = Profile.objects.filter(id_user=ids)
#         username_profile_list.append(profile_lists)

#     suggestions_username_profile_list = list(chain(*username_profile_list))


#     return render(request, 'index.html', {'user_profile': user_profile, 'posts':feed_list, 'suggestions_username_profile_list': suggestions_username_profile_list[:4]})


class UploadView(LoginRequiredMixin, TemplateView):
   template_name = 'index.html'
     


   # def get(self, request, *args, **kwargs):
   #      user_object = User.objects.get(username=request.user.username)
   #      user_profile = Profile.objects.get(user=user_object)
   #      context = {
   #          'user_profile':user_profile
   #      }
   #      return render(self.request, self.template_name, context=context)


   def post(self, request, *args, **kwargs):
        if request.method == 'POST':
         user = request.user.username
         image = request.FILES.get('image_upload')
         caption = request.POST['caption']

         new_post = Post.objects.create(user=user, image=image, caption=caption)
         new_post.save()
         return redirect('/')
      # return render(self.request, self.template_name)        
