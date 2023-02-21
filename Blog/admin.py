from django.contrib import admin
from .models import UserProfile, Post, ImagePost, PostComment

admin.site.register(UserProfile)
admin.site.register(Post)
admin.site.register(ImagePost)
admin.site.register(PostComment)