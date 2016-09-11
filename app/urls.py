from django.conf.urls import url, include
from  app.views import home, Profile, UserFullProfile, login, CreateEvent, UpcomingEvents,SignUp, EventDetails, UnderConstruction, EventThanks,\
    SignOut,AllUniversities, main_user_profile, like
app_name='app'
urlpatterns=[
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
    url(r'^main_profile$',main_user_profile, name="main_profile"),
    url(r'^likes/$', like, name='like')
]