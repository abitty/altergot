"""altergot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^coins/', include('coins.urls')),
    url(r'^bones/', include('bones.urls')),
	url(r'^api/',include('rest.urls')),
	url(r'', include('idxpage.urls')),
	url(r'^login/$', auth_views.LoginView.as_view(template_name='login.html'),name='login'),
	url(r'^logout/$', auth_views.LogoutView.as_view(template_name='logout.html')),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
	if settings.MEDIA_ROOT:
		urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
# Эта строка опциональна и будет добавлять url'ы только при DEBUG = True
urlpatterns += staticfiles_urlpatterns()


