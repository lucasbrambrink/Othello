from django.conf.urls import patterns, include, url
from django.contrib import admin
from game.views import *

urlpatterns = patterns('',
	url(r'^$', Boardview.as_view(), name='board'),
	url(r'^place/', BoardControl.as_view(), name='place'),
	url(r'^board/', BoardControl.as_view(), name='board'),
	url(r'^find-moves/', ShowMoves.as_view(), name='moves'),
)
