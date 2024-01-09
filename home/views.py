from django.shortcuts import render,redirect
from django.http import HttpResponse
from home.models import Contact
from django.contrib import messages
from blog.models import Post
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
# Create your views here.
def home(request): 
    return render(request,"home/home.html")

def contact(request):
    if request.method == "POST":
       name = request.POST.get('name')
       email = request.POST.get('email')
       phone = request.POST.get('phone') 
       content = request.POST.get('content')
       if len(name)<2 or len(email)<3 or len(phone)<10 or len(content)<4:
            messages.add_message(request,messages.ERROR, "Please fill the form correctly")
       else:
            contact = Contact(name=name, email=email, phone=phone, content=content)
            contact.save()
            messages.add_message(request, messages.SUCCESS, "Your message has been successfully sent")    
    return render(request,"home/contact.html")

def about(request): 
    return render(request,"home/about.html")

def search(request):
    query = request.GET.get('query')
    if len(query)>78:
        posts=Post.objects.none()
    else:
        poststitle = Post.objects.filter(title__icontains=query)
        postsauthor = Post.objects.filter(author__icontains=query)
        postscontent = Post.objects.filter(content__icontains=query)
        
        posts = poststitle.union(postsauthor, postscontent)
    
    if posts.count()==0:
        messages.add_message(request, messages.WARNING, "No search results found. Please refine your query.")    

    params={'posts': posts, 'query': query}
    return render(request, "home/search.html", params)


def handlesignup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        fname = request.POST['fname']
        lname = request.POST['lname']
        # role = request.POST['role']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        
        # check for errorneous input
        if len(username)<4:
            messages.add_message(request, messages.ERROR, "Your user name must be under 4 characters.") 
            return redirect('home')

        if not username.isalnum():
            messages.add_message(request, messages.ERROR, "User name should only contain letters and numbers.")
            return redirect('home')
        if (pass1!= pass2):
            messages.add_message(request, messages.ERROR, "Passwords do not match.")
            return redirect('home')
        
        # Create the user
        user = User.objects.create_user(username,email,pass1)
        user.first_name= fname
        user.last_name= lname
        user.save()
        messages.success(request, " Your iCoder has been successfully created")
        return redirect('home')
    else:
        return HttpResponse("404 - Not found")
    
def handlelogin(request):
    if request.method == "POST":
        loginusername = request.POST['loginusername']
        loginpass = request.POST['loginpass']
        
        user = authenticate(username=loginusername, password=loginpass)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect("home")
        else:
            messages.error(request, "Invalid credentials! Please try again")
            return redirect("home")
        
    else:
        return HttpResponse("404 - Not found")

def handlelogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('home')