from django.db import models
from django.contrib.auth.models import User

# Create your models here.

#inherit from django.db.models.Model
#when define a mode, you need to specify the list of attributes and their associated types
class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    def __unicode__(self):
        return self.name

#ForeignKey, OneToOneField, ManyToManyField
#DJango creates an ID field for you automatically, no need to definea primary key

class Page(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __unicode__(self):
        return self.title

#__unicode__(), __str__() are just like toString() in java
#a good practice to include

class UserProfile(models.Model):
    #This line is required. Links UserProfile to a User model instance
    user = models.OneToOneField(User)

    #additional attributes
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __unicode__(self):
        return self.user.username
