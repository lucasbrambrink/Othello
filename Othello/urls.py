from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
	url(r'^game/', include('game.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', include('game.urls'))
)
