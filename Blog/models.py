from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(null=True)
    creation_date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.name} {self.last_name}"


class Post(models.Model):
    userprofile = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=100)
    text = models.TextField()
    creation_date = models.DateField(auto_now_add=True, blank=True, null=True)
    viewCount = models.IntegerField(default=0)
    published = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} created by: {self.userprofile}"


class ImagePost(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True,)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='Images')
    image = models.ImageField(null=True, blank=True)
    main_image = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Photo connected with: {self.post}"


class PostComment(models.Model):
    user = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name='user_post_comment',)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="post_comment",)
    text = models.CharField(max_length=100, null=True, blank=True,)
    creation_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user} commented {self.post}"
