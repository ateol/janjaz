import datetime
from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone
from time import time

def profile_destination(instance, filename):
    return "profile_pictures/%s_%s"%(str(time()).replace('.','_'), filename)

class UserProfile(models.Model):
    user=models.OneToOneField(User, null=True)

    living_in_turkey=models.CharField(max_length=3)
    country_of_origin=models.CharField(max_length=50)
    city_living=models.CharField(max_length=50)
    profile_picture=models.FileField(upload_to=profile_destination, null=True)

    gender=models.CharField(max_length=6)
    status=models.CharField(max_length=50, blank=True)
    about_yourself=models.CharField(max_length=500, blank=True)
    interests=models.CharField(max_length=500, blank=True)
    languages=models.CharField(max_length=500, blank=True)
    occupation=models.CharField(max_length=20, blank=True)

    def __string__(self):
        return self.user.username


class City(models.Model):
   name=models.CharField(max_length=50)

   def __str__(self):
       return self.name

class EventWebsite(models.Model):
    event_website=models.URLField(blank=True)
    def _str__(self):
        return str(self.event_website)

class EventDetails(models.Model):
    contact_name=models.CharField(max_length=50,blank=True)
    company_name=models.CharField(max_length=50, blank=True)
    address=models.CharField(max_length=200, blank=True)
    phone_number=PhoneNumberField(blank=True)
    email=models.EmailField(blank=True)
    organisers_website=models.URLField(blank=True)

    def __str__(self):
        return self.contact_name

class EventComment(models.Model):
    comment_text=models.TextField()
    author=models.ForeignKey(User, null=True)
    author_profile=models.ForeignKey(UserProfile, null=True)
    post_date=models.DateTimeField(default=timezone.now(), null=True)
    num_likes=models.IntegerField(default=0)

    def __str__(self):
        return self.comment_text

class Event(models.Model):
    category=models.CharField(max_length=20)
    title=models.CharField(max_length=20)
    description=models.CharField(max_length=2000)
    event_privacy=models.CharField(max_length=20)
    city=models.CharField(max_length=50)
    event_venue=models.CharField(max_length=100)
    start_time=models.DateTimeField(blank=False, null=True)
    end_time=models.DateTimeField(blank=False, null=True)
    event_website=models.OneToOneField(EventWebsite,null=True)
    event_organizer=models.OneToOneField(EventDetails, null=True)
    comments=models.ManyToManyField(EventComment)

    def __str__(self):
        return self.title

class University(models.Model):
    name=models.CharField(max_length=50, blank=True)
    status=models.CharField(max_length=10, blank=True)
    city=models.ForeignKey(City, blank=True)
    university_website=models.URLField( blank=True)
    logo=models.FileField( blank =True)
    description=models.TextField(blank=True)

    def __str__(self):
        return self.name


        