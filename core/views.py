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


      user_following_list = []
      feed = []

      user_following = FollowersCount.objects.filter(follower=request.user.username)

      for users in user_following:
         user_following_list.append(users.user)

      for usernames in user_following_list:
         feed_lists = Post.objects.filter(user=usernames)
         feed.append(feed_lists)

      feed_list = list(chain(*feed))

      # user suggestion starts
      all_users = User.objects.all()
      user_following_all = []

      for user in user_following:
         user_list = User.objects.get(username=user.user)
         user_following_all.append(user_list)
      
      new_suggestions_list = [x for x in list(all_users) if (x not in list(user_following_all))]
      current_user = User.objects.filter(username=request.user.username)
      final_suggestions_list = [x for x in list(new_suggestions_list) if ( x not in list(current_user))]
      random.shuffle(final_suggestions_list)

      username_profile = []
      username_profile_list = []

      for users in final_suggestions_list:
         username_profile.append(users.id)

      for ids in username_profile:
         profile_lists = Profile.objects.filter(id_user=ids)
         username_profile_list.append(profile_lists)

      suggestions_username_profile_list = list(chain(*username_profile_list))

      context = {
            'user_profile':user_profile,
            'posts': feed_list,
            'suggestions_username_profile_list': suggestions_username_profile_list[:4]
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
     
   def post(self, request, *args, **kwargs):
        if request.method == 'POST':
         user = request.user.username
         image = request.FILES.get('image_upload')
         caption = request.POST['caption']

         new_post = Post.objects.create(user=user, image=image, caption=caption)
         new_post.save()
         return redirect('/')


class LikePostView(LoginRequiredMixin, TemplateView):
   template_name = 'index.html'
     

   def get(self, request, *args, **kwargs):
       username = self.request.user.username
       post_id = request.GET.get('post_id')
       post = Post.objects.get(id=post_id)
       like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()
       if like_filter == None:
         new_like = LikePost.objects.create(post_id=post_id, username=username)
         new_like.save()
         post.no_of_likes = post.no_of_likes+1
         post.save()
         return redirect('/')
       else:
         like_filter.delete()
         post.no_of_likes = post.no_of_likes-1 
         post.save()
         return redirect('/') 
       
       
class ProfilePageView(LoginRequiredMixin, TemplateView):
   template_name = 'profile.html'
     
   def get(self, request, *args, **kwargs):
        user_object = User.objects.get(username=self.kwargs.get('pk'))
        user_profile = Profile.objects.get(user=user_object)
        user_posts = Post.objects.filter(user=self.kwargs.get('pk'))
        user_post_length = len(user_posts)
        follower = self.request.user.username
        user = self.kwargs.get('pk')

        if FollowersCount.objects.filter(follower=follower, user=user).first():
            button_text = "Unfollow"
        else:
            button_text = "follow"

        user_followers = len(FollowersCount.objects.filter(user=self.kwargs.get('pk')))
        user_followering = len(FollowersCount.objects.filter(follower=self.kwargs.get('pk')))

        context = {
            'user_profile':user_profile,
            'user_object': user_object,
            'user_posts': user_posts,
            'user_post_length': user_post_length,
            'button_text': button_text,
            'user_followers': user_followers,
            'user_followering':user_followering
         }
        return render(self.request, self.template_name, context=context)

class FollowView(LoginRequiredMixin, TemplateView):
   template_name = 'profile.html'
     
   def post(self, request, *args, **kwargs):
      follower = self.request.POST['follower']
      user = self.request.POST['user']
      if FollowersCount.objects.filter(follower=follower, user=user).first():
         delete_follower = FollowersCount.objects.get(follower=follower, user=user)
         delete_follower.delete()
         return redirect('profile', user)
      else:
         new_follower = FollowersCount.objects.create(follower=follower, user=user)
         # new_follower.save()
         return redirect('profile', user)



class SearchView(LoginRequiredMixin, TemplateView):
   template_name = 'search.html'


   def get(self, request, *args, **kwargs):
      user_object = User.objects.get(username=request.user.username)
      user_profile = Profile.objects.get(user=user_object)

      context = {
            'user_profile':user_profile,
        }
      return render(self.request, self.template_name, context=context)

     
   def post(self, request, *args, **kwargs):
      username = self.request.POST['username']
      username_object = User.objects.filter(username__icontains=username)

      username_profile= []
      username_profile_list = []

      for users in username_object:
         username_profile.append(users.id)

      for ids in username_profile:
         profile_lists = Profile.objects.filter(id_user=ids)
         username_profile_list.append(profile_lists)   
      
      username_profile_list = list(chain(*username_profile_list))

      context = {
         'username_profile_list': username_profile_list
      }
      return render(self.request, self.template_name, context=context)

   
        