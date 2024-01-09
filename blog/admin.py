from django.contrib import admin
from blog.models import Post, Blogcomment
# Register your models here.

admin.site.register((Post,Blogcomment))