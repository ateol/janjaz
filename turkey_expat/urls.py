
from datetime import datetime
from django.conf.urls import patterns, url, include
from django.contrib import admin
from django.conf.urls.static import static
from turkey_expat import settings

urlpatterns=[
    url(r'^', include('app.urls', namespace='app')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^forum/', include('forums.urls', namespace='forums')),
    url(r'^blog/', include('blog.urls',namespace='blog')),
]

if settings.DEBUG==True:
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)