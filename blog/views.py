from django.shortcuts import render, redirect
from django.http import HttpResponse
from blog.models import Post, Blogcomment
from django.contrib.auth.models import User
from django.contrib import messages
from blog.templatetags import extras
# Create your views here.
def blogHome(request):
    post = Post.objects.all()
    context = {'posts':post}
    return render(request,"blog/blogHome.html",context)

def blogPost(request, slug): 
    post=Post.objects.filter(slug=slug).first()
    comments= Blogcomment.objects.filter(post=post, parent=None)
    replies= Blogcomment.objects.filter(post=post).exclude(parent=None)
    replyDict={}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno]=[reply]
        else:
            replyDict[reply.parent.sno].append(reply)

    context={'posts':post, 'comment': comments, 'user': request.user, 'replyDict': replyDict}
    return render(request, "blog/blogPost.html", context)

def blogcomment(request):
    # if request.method == "POST":
    #     comment = request.POST.get('comment')
    #     user = request.user
    #     postsno = request.POST.get('postSno')
    #     post = Post.objects.get(sno=postsno)
    #     if len(comment) < 5:
    #         messages.error(request, "please fill comment")
    #     else:
    #         com = Blogcomment(comment=comment, user=user, post=post)
    #         com.save()
    #         messages.success(request, "Your comment has been posted successfully")
        
    # return redirect(f"/blog/{post.slug}")

    if request.method == "POST":
        comment=request.POST.get('comment')
        user=request.user
        postSno =request.POST.get('postSno')
        post= Post.objects.get(sno=postSno)
        parentSno= request.POST.get('parentSno')
        if parentSno == "":
            comment=Blogcomment(comment= comment, user=user, post=post)
            comment.save()
            messages.success(request, "Your comment has been posted successfully")
        else:
            parent= Blogcomment.objects.get(sno=parentSno)
            comment=Blogcomment(comment= comment, user=user, post=post , parent=parent)
            comment.save()
            messages.success(request, "Your reply has been posted successfully")
    return redirect(f"/blog/{post.slug}")