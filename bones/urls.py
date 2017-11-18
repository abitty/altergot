#coding: utf-8

from django.conf.urls import url
from bones.views import BonesListView, BoneUpdate, BoneCreate, BoneDelete
from . import views

urlpatterns = [
url(r'^$',BonesListView.as_view(),name='blist'), # /bones - список
url(r'^sel/$', BonesListView.as_view(), name='bsel'),
url(r'^sel/(?P<pk>\d+)/$', BoneUpdate.as_view(),name='bone-update'),
url(r'^create/$',BoneCreate.as_view(),name='bone-create'),
url(r'^(?P<pk>\d+)/$', BoneUpdate.as_view(),name='bone-update'), # /coins/число - монета
url(r'^(?P<pk>\d+)/delete/$', BoneDelete.as_view(),name='bone-delete'),
url(r'^sel/(?P<pk>\d+)/delete/$', BoneDelete.as_view(),name='bone-delete'),
]


