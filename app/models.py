import datetime
from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone
from time import time

def profile_picture_destination(instance, filename):
    return "profile_pictures/%s_%s"%(str(time()).replace('.','_'), filename)


def city_picture_destination(instance, filename):
    return "city_pictures/%s_%s" % (str(time()).replace('.', '_'), filename)


def prominent_place_picture_destination(instance, filename):
    return "prominent_places_pictures/%s_%s" % (str(time()).replace('.', '_'), filename)

def transportaion_picture_destination(instance, filename):
    return "transportation_pictures/%s_%s" % (str(time()).replace('.', '_'), filename)

def university_logo_destination(instance, filename):
    return "university_logos/%s_%s" % (str(time()).replace('.', '_'), filename)



class UserProfile(models.Model):
    user=models.OneToOneField(User, null=True)

    firstName=models.CharField(max_length=50, blank=True)
    lastName=models.CharField(max_length=50, blank=True)
    living_in_turkey=models.CharField(max_length=3)
    country_of_origin=models.CharField(max_length=50)
    city_living=models.CharField(max_length=50)
    date_joined=models.DateTimeField(blank=False ,null=True)
    profile_picture=models.FileField(upload_to=profile_picture_destination, null=True)

    gender=models.CharField(max_length=6)
    status=models.CharField(max_length=50, blank=True)
    about_yourself=models.CharField(max_length=500, blank=True)
    interests=models.CharField(max_length=500, blank=True)
    languages=models.CharField(max_length=500, blank=True)
    occupation=models.CharField(max_length=20, blank=True)

    def __string__(self):
        return self.user.username
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
"""
class EventComment(models.Model):
    comment_text=models.TextField()
    author=models.ForeignKey(User, null=True)
    author_profile=models.ForeignKey(UserProfile, null=True)
    post_date=models.DateTimeField(default=timezone.now(), null=True)
    num_likes=models.IntegerField(default=0)

    def __str__(self):
        return self.comment_text"""

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

    def __str__(self):
        return self.title

class Transportation(models.Model):
    category=models.CharField(max_length=30)
    image=models.ImageField(upload_to=transportaion_picture_destination, blank=True)

class City(models.Model):
    name=models.CharField(max_length=50)
    profile_image=models.ImageField(upload_to=city_picture_destination, blank=True)
    transportation=models.ForeignKey(Transportation)

    def __str__(self):
        return self.name


class University(models.Model):
    name=models.CharField(max_length=50, blank=True)
    status=models.CharField(max_length=10, blank=True)
    city=models.ForeignKey(City, blank=True)
    university_website=models.URLField( blank=True)
    logo=models.ImageField(upload_to=university_logo_destination, blank=True)
    description=models.TextField(blank=True)

    def __str__(self):
        return self.name

class ProminentPlace(models.Model):
    city=models.ForeignKey(City)
    title=models.CharField(max_length=50)
    Image=models.ImageField(upload_to=prominent_place_picture_destination, blank=True)
    description=models.TextField()

    def __str__(self):
        return (self.title)

    #add google maps and commenting from external apos

class Job(models.Model):
    title=models.CharField(max_length=100)
    brief_description=models.CharField(max_length=300)
    employer=models.ForeignKey(User)
    location=models.CharField(max_length=100)
    description=models.TextField()
    qualifications_and_skills=models.TextField()
    job_status=models.CharField(max_length=10)
    method_of_application=models.CharField(max_length=10)
    category=models.CharField(max_length=20)
    date_posted=models.DateTimeField()
    deadline=models.DateTimeField()

    def __str__(self):
        return self.title




