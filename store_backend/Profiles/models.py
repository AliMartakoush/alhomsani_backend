'''from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Link to Django user
    name = models.CharField(max_length=255)
    profile_picture = models.URLField(blank=True, null=True)
    contact_info = models.TextField(blank=True, null=True)
    favorite_cars = models.ManyToManyField('store.Product', related_name='favorited_by', blank=True)

    def __str__(self):
        return self.user.username'''

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from store.models import Product  # Assuming Product model is in store app

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    member_since = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    contact_info = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_picture_url = models.URLField(blank=True, null=True)
    profile_picture_public_id=models.CharField(max_length=255, blank=True, null=True)
    favorite_cars = models.ManyToManyField(Product, related_name='favorited_by', blank=True)
    bookmarked_cars = models.ManyToManyField(Product, related_name='bookmarked_by', blank=True)
    
    def __str__(self):
        return self.user.username

class ActivityLog(models.Model):
    ACTION_CHOICES = [
        ('purchase', 'Purchase'),
        ('bookmark', 'Bookmark'),
        ('favorite', 'Favorite'),
    ]
    
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='activity_logs')
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.profile.user.username} {self.action} {self.product.name} at {self.timestamp}"
    
class Reviews(models.Model):
    reviewer=models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='reviews')
    car=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='reviews')
    review=models.CharField(max_length=500)
    time_written=models.DateTimeField(auto_now_add=True)


    


