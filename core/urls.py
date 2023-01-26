from django.urls import path
from . import views

urlpatterns = [
    # path('',views.index, name='index'),
    path('', views.IndexView.as_view(), name='index'),
    path('upload/', views.UploadView.as_view(), name='upload'),
    path('like-post/', views.LikePostView.as_view(), name='like-post'),
    path('profile/<str:pk>', views.ProfilePageView.as_view(), name='profile'),

    

]