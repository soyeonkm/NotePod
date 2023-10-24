from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime

User = get_user_model()

# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    profileimg = models.ImageField(upload_to='profile_images', default='blank-profile-picture.png')
    # subject = models.CharField(max_length=50)
    # sub_subject = models.CharField(max_length=50)
    pod = models.CharField(max_length=50, default='')
    # location = models.CharField(max_length=100, blank=True)
    # bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100)
    image = models.FileField(upload_to='post_images')
    caption = models.TextField(default='')
    key1 = models.CharField(max_length=100, default='')
    key2 = models.CharField(max_length=100, default='')
    key3 = models.CharField(max_length=100, default='')
    sub = models.CharField(max_length=50, default='')
    sub_sub = models.CharField(max_length=50, default='')
    pod = models.CharField(max_length=100, default='')

    type = models.CharField(max_length=10, default='')

    created_at = models.DateTimeField(default=datetime.now)
    no_of_likes = models.IntegerField(default=0)


    def __str__(self):
        return self.user

class LikePost(models.Model):
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=100)

    def __str__(self):
        return self.username

# class FollowersCount(models.Model):
#     follower = models.CharField(max_length=100)
#     user = models.CharField(max_length=100)

#     def __str__(self):
#         return self.user
    
# class Subject(models.Model):
#     sub = models.CharField(max_length=50, default='')
    
#     def __str__(self):
#         return self.sub
    
# class SubSubject(models.Model):
#     sub_sub = models.CharField(max_length=50, default='')

#     def __str__(self):
#         return self.sub_sub
#     pass

class Pod(models.Model):
    name = models.CharField(max_length=100, default='')
    district = models.CharField(max_length=10, default='')

    # description = models.TextField(default='')
    # members = models.ManyToManyField(User, related_name='pod_members')

    def __str__(self):
        return self.name
    
class Topic(models.Model):
    subject=models.CharField(max_length=50)
    sub_subject=models.CharField(max_length=50)
    
    

    


    
