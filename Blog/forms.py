from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import *

class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, label="Imię") 
    last_name = forms.CharField(max_length=50, label="Nazwisko")
    class Meta:
        model = User
        fields = ['username', 'email','first_name','last_name', 'password1', 'password2',]
        
class CreatePostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title','text','published',]
        
        labels = {
            'title':"Tytuł",
            'text':"Opis",
            'published':'Opublikowany',
        }
    
class EditPostForm(CreatePostForm):
     images = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
     main_image = forms.ImageField()
     
     class Meta(CreatePostForm.Meta):
         fields = CreatePostForm.Meta.fields + ['images','main_image',]
    
 
