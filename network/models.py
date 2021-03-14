from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class User(AbstractUser):
    pass


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    bio = models.TextField(null=True, blank=True)
    # pics
    website = models.CharField(max_length=225, null=True, blank=True)
    follower = models.ManyToManyField(User, blank=True, related_name="followed_user") # user following this profile
    following = models.ManyToManyField(User, blank=True, related_name="following_user") # profile user that follows this profile
    
    def __str__(self):
        return f"{self.user}'s' profile id is {self.id}"
        
    def serialize(self):
        return {
            'id': self.id,
            'user': self.user.username,
            'user_id': self.user.id,
            'bio': self.bio,
            'website': self.website,
            'follower': [user.username for user in self.follower.all()],
            'following': [user.username for user in self.following.all()],
        }
        
    def following_users(self):
        for username in self.following:
            return username
        
    def get_absolute_url(self):
        return reverse("network:profile-detail", args=[str(self.id)])

class Post(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50)
    body = models.TextField(max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, blank=True, related_name="liked_post")

    def __str__(self):
        return f"{self.subject} posted by {self.created_by}"
        
    def get_absolute_url(self):
        return reverse("network:post-detail", args=[str(self.id)])
    
    def serialize(self):
        return {
            'id': self.id,
            'created_by': self.created_by.username,
            'user_id': self.created_by.id,
            'created_id': self.created_by.id,
            'body': self.body,
            'timestamp': self.timestamp.strftime('%b %-d %Y, %-I:%M %p'),
            'likes': self.total_likes(),
            'liked': [user.username for user in self.likes.all()],
        }
        
    def total_likes(self):
        return self.likes.count()
        
    class Meta:
        ordering = ["-timestamp"]
    