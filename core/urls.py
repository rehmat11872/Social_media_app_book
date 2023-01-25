from django.urls import path
from . import views

urlpatterns = [
    # path('',views.index, name='index'),
    path('', views.IndexView.as_view(), name='index'),
    path('upload/', views.UploadView.as_view(), name='upload')
    

]