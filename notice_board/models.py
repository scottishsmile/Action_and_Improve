from django.db import models
from datetime import datetime
from django.contrib.auth.models import User


# Database Models
class Action(models.Model):
    title = models.CharField(max_length=250)
    text = models.TextField()
    created = models.DateTimeField(default=datetime.now)
    due = models.DateTimeField(default=datetime.now)
    assigned = models.TextField()
    complete = models.BooleanField(default=False)

    # API Authentication
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.title


class Improvement(models.Model):
    title = models.CharField(max_length=250)
    text = models.TextField()
    created = models.DateTimeField(default=datetime.now)
    due = models.DateTimeField(default=datetime.now)
    assigned = models.TextField()
    complete = models.BooleanField(default=False)

    # API Authentication
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.title


class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    portfolio_site = models.URLField(blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)

    def __str__(self):
        return self.user.username

