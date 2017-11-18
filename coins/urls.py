#coding: utf-8

from django.conf.urls import url
from coins.views import CoinsListView, CoinUpdate, CoinCreate, CoinDelete
from . import views

urlpatterns = [
url(r'^$',CoinsListView.as_view(),name='list'), # /coins - список
url(r'^sel/$', CoinsListView.as_view(), name='sel'),
url(r'^sel/(?P<pk>\d+)/$', CoinUpdate.as_view(),name='coin-update'),
url(r'^create/$',CoinCreate.as_view(),name='coin-create'),
url(r'^(?P<pk>\d+)/$', CoinUpdate.as_view(),name='coin-update'), # /coins/число - монета
url(r'^(?P<pk>\d+)/delete/$', CoinDelete.as_view(),name='coin-delete'),
url(r'^sel/(?P<pk>\d+)/delete/$', CoinDelete.as_view(),name='coin-delete'),
]


