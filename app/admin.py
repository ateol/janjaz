from django.contrib import admin
from app.models import  City, Event,EventWebsite, EventDetails, University, Transportation, Job, ProminentPlace


class EventProfileAdmin(admin.ModelAdmin):
    list_display=['title', 'city', 'event_venue']

class EventWebsiteAdmin(admin.ModelAdmin):
    list_display=['event_website']

admin.site.register(University)
admin.site.register(City,)
admin.site.register(Event, EventProfileAdmin)
admin.site.register(EventWebsite, EventWebsiteAdmin)
admin.site.register(EventDetails)
admin.site.register(Transportation)
admin.site.register(Job)
admin.site.register(ProminentPlace)