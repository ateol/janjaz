from django.contrib import admin
from app.models import UserProfile, City, Event,EventWebsite, EventDetails, EventComment, University


class UserProfileAdmin(admin.ModelAdmin):
    list_display=['city_living', 'country_of_origin']

class EventProfileAdmin(admin.ModelAdmin):
    list_display=['title', 'city', 'event_venue']

class EventWebsiteAdmin(admin.ModelAdmin):
    list_display=['event_website']

admin.site.register(University)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(City,)
admin.site.register(Event, EventProfileAdmin)
admin.site.register(EventWebsite, EventWebsiteAdmin)
admin.site.register(EventDetails)
admin.site.register(EventComment)