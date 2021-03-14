from django.forms import ModelForm
from django import forms
from .models import Post, Profile

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('subject', 'body')
        labels = {
            'body': 'Post',
        }
        
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control w-75'}),
            'body': forms.Textarea(attrs={'class': 'form-control w-75'}),
        }
        
        
class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'website')
        labels = {
            'website': 'Webpage',
        }
        
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control w-75'}),
            'website': forms.TextInput(attrs={'class': 'form-control w-75'}),
        }