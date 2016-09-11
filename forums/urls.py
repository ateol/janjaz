from django.conf.urls import url
from .views import *

app_name='forums'
urlpatterns =[
    url(r"^$", forums, name="forums_forums"),
    url(r"^category/(\d+)/$", forum_category, name="forums_category"),
    url(r"^forum/(\d+)/$", forum, name="forums_forum"),
    url(r"^thread/(\d+)/$", forum_thread, name="forums_thread"),
    url(r"^new_post/(\d+)/$", post_create, name="forums_post_create"),
    url(r"^reply/(\d+)/$", reply_create, name="forums_reply_create"),
    url(r"^post_edit/(thread|reply)/(\d+)/$", post_edit, name="forums_post_edit"),
    url(r"^subscribe/(\d+)/$", subscribe, name="forums_subscribe"),
    url(r"^unsubscribe/(\d+)/$", unsubscribe, name="forums_unsubscribe"),
    url(r"^thread_updates/$", thread_updates, name="forums_thread_updates"),



    #ajax urls
    url(r'^likes/$', likes, name="likes"),
    url(r'^reply/$', ajax_reply, name="ajax_reply"),
    url(r'^search/$', Search, name="search"),
    url(r'^ajax-search/$', ajax_search, name="ajax-search"),
    url(r'^flag/$', ajax_flag, name="flag")

]
