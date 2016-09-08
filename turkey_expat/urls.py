
from datetime import datetime
from django.conf.urls import patterns, url, include
from django.contrib import admin
from  app.views import home, Profile, UserFullProfile, login, CreateEvent, UpcomingEvents,SignUp, EventDetails, UnderConstruction, EventThanks,\
    SignOut,AllUniversities, main_user_profile

from django.conf.urls.static import static
from turkey_expat import settings

urlpatterns=[     
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^likes/', include('likes.urls')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^forum/', include('forums.urls', namespace='forums')),
    url(r'^blog/', include('blog.urls',namespace='blog')),
    url(r'^$', home, name='home'),
    url(r'^accounts/profile/', Profile, name='Profile'),
    url(r'^login$', login, name="login"),
    url(r'^create_event$', CreateEvent, name='create_event'),
    url(r'^upcoming_events$', UpcomingEvents, name="upcoming_events"),
    url(r'^signup$',SignUp, name="signup" ),
    url(r'^upcoming_events/(?P<event_id>[0-9]+)/$', EventDetails, name="event_details"),
    url(r'^under_construction$',UnderConstruction, name="under_construction"),
    url(r'^user_profile$', UserFullProfile, name="user_profile"),
    url(r'^event_thanks$', EventThanks, name='event-thanks'),
    url(r'^signout$', SignOut, name="signout"),
    url(r'^all_universities$', AllUniversities, name="all_universities"),
    url(r'^main_profile',main_user_profile, name="main_profile")
]

if settings.DEBUG==True:
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)