from django.urls import path
from . import views
from .views import PostCreateView, PostDetailView, PostDeleteView, ProfileCreateView, ProfileUpdateView, ProfileDeleteView, ProfilePostsView, FollowingPageView


app_name = "network"
urlpatterns = [
    # Authentication
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    
    # Posts
    path("post/add/", PostCreateView.as_view(), name="post-add"),
    path("<int:pk>/viewpost/", PostDetailView.as_view(), name="post-detail"),
    path("updatepost/<int:post_id>", views.PostEditView, name="updatepost"),
    path("<int:pk>/deletepost/", PostDeleteView.as_view(), name="post-delete"),
    path("allposts/", views.allposts_json, name="allposts"),
    
    # Post Likes
    path("like/<int:post_id>", views.LikeView, name="like-post"),
    
    # Follow/Following
    path("<int:pk>/follow/", views.FollowView, name="follow-profile"),
    path("<int:pk>/followposts/",  views.FollowingPageView, name="follow-posts"),

    # Profile
    path("profile/add/", ProfileCreateView.as_view(), name="profile-add"),
    path("<int:pk>/viewprofile/", views.ProfilePostsView, name="profile-detail"),
    path("<int:pk>/updateprofile/", ProfileUpdateView.as_view(), name="profile-update"),
    path("<int:pk>/deleteprofile/", ProfileDeleteView.as_view(), name="profile-delete"),
]
