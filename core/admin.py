from django.contrib import admin
from .models import Profile, Post, LikePost, Pod

# Register your models here.
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(LikePost)
# admin.site.register(FollowersCount)
# admin.site.register(Subject)
# admin.site.register(SubSubject)
admin.site.register(Pod)
