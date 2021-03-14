import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from .models import User, Profile, Post
from .forms import PostForm, ProfileForm


def index(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 10)
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/index.html", {"page_obj": page_obj})
    

# Posts
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "network/post-add.html"
    success_url = reverse_lazy("network:index")
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class PostDetailView(DetailView):
    model = Post
    

def PostEditView(request, post_id):
    try:
        user = User.objects.get(username=request.user)
        post = Post.objects.get(pk=post_id)

    except Post.DoesNotExist:
        return JsonResponse({"error": "The post you're searching for was not found."}, status=400)
        
    if request.method == "GET":
        return JsonResponse(post.serialize())
        
    if request.method == "PUT":
        data = json.loads(request.body)
        print(data)
        body = data.get("body", "")
        Post.objects.filter(pk=post_id).update(body=body)
        print(post)

        return JsonResponse({"message": "Post updated."}, status=201)


class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy("network:index")
    
 
def allposts_json(request): 
    try:
        posts = Post.objects.all()
    except Post.DoesNotExist:
        return JsonResponse({"error": "Posts not found."}, status=400)
        
    return JsonResponse([post.serialize() for post in posts], safe=False)

            
# Post Likes
def LikeView(request, post_id):
    try:
        user = User.objects.get(username=request.user)
        post = Post.objects.get(pk=post_id)
        
    except Post.DoesNotExist:
        return JsonResponse({"error": "The post you're searching for was not found."}, status=400)
    
    if request.method == "GET":
        return JsonResponse(post.serialize())
    
    if request.method == "PUT":
        liked = False
        if post.likes.filter(username=user).exists():
            post.likes.remove(user)
            liked = False
            print(liked)
            return JsonResponse(post.serialize())
        else:
            post.likes.add(user)
            liked = True
            print(liked)
            return JsonResponse(post.serialize())
    return JsonResponse({"message": f"Like updated."}, status=201)
    

# Profile
class ProfileCreateView(LoginRequiredMixin, CreateView):
    model = Profile
    form_class = ProfileForm
    template_name = "network/profile-add.html"
    success_url = reverse_lazy("network:index")
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
   
        
# Profile/Posts multi-view
def ProfilePostsView(request, pk):
    profile = get_object_or_404(Profile, id=pk)
    posts = Post.objects.filter(created_by=profile.user)
    paginator = Paginator(posts, 10)
    
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    try:
        if request.method == "GET":
            return render(request, "network/post-profile.html", { "profile": profile, "page_obj": page_obj })
    except ValueError:
        return render(request, "network:index.html", {"error": ValueError})

    

class ProfileUpdateView(UpdateView):
    model = Profile
    form_class = ProfileForm
    success_url = reverse_lazy("network:index")
    

class ProfileDeleteView(DeleteView):
    model = Profile
    success_url = reverse_lazy("network:index")
    
    
def FollowView(request, pk):
    profile = get_object_or_404(Profile, id=request.POST.get("profile_id"))
    profile_following = Profile.objects.get(user=request.user)
    user = request.user

    follow = False
    if profile.follower.filter(id=user.id).exists():
        profile.follower.remove(user)
        profile_following.following.remove(profile.user)
        follow = False
    else:
        profile.follower.add(user)
        profile_following.following.add(profile.user)
        follow = True

    return HttpResponseRedirect(profile.get_absolute_url())
    

# Following Users
def FollowingPageView(request, pk):
    profile = get_object_or_404(Profile, id=pk)
    # Filter Profile following users list of posts
    posts = Post.objects.filter(created_by__in=profile.following.all())
   
    # Set up pagination based on filtered posts
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    try:
        if request.method == "GET":
            return render(request, "network/follow-posts.html", { "profile": profile, "page_obj": page_obj })
    except ValueError:
        return render(request, "network:index.html", {"error": ValueError})
    

# Authentication 
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("network:index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("network:index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("network:index"))
    else:
        return render(request, "network/register.html")
