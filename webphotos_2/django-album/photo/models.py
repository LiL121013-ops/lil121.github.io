# #from django.db import models
# from django.utils.timezone import now
#
# class Photo(models.Model):
#     image   = models.ImageField(upload_to='photo/%Y%m%d/')
#     created = models.DateTimeField(default=now)
#
#     def __str__(self):
#         return self.image.name
#
#     class Meta:
#         ordering = ('-created',)

from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.db import models

class Image(models.Model):
    url = models.URLField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.jpg')

    def __str__(self):
        return self.user.username

class Photo(models.Model):
    image   = models.ImageField(upload_to='photo/%Y%m%d/')
    created = models.DateTimeField(default=now)

    def __str__(self):
        return self.image.name

    class Meta:
        ordering = ('-created',)