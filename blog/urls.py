from django.urls import path,include
from . import views

urlpatterns = [
    path('blogcomment',views.blogcomment, name="blogcomment"),
    path('', views.blogHome, name="bloghome"),
    path('<str:slug>', views.blogPost, name="blogPost"),
]