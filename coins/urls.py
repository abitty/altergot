#coding: utf-8

from django.conf.urls import url
from coins.views import CoinsListView, CoinUpdate, CoinCreate
from . import views

urlpatterns = [
url(r'^$',CoinsListView.as_view(),name='list'), # /coins - список
url(r'^filtered/$', views.filtered, name='filtered'),
url(r'^create/$',CoinCreate.as_view(),name='coin-create'),
url(r'^(?P<pk>\d+)/$', CoinUpdate.as_view(),name='coin-update'), # /coins/число - монета
]


