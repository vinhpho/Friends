from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index),
    url(r'^createuser$', views.createuser),
    url(r'^login$', views.login),
    url(r'^friends$', views.friends),
    url(r'^logout$', views.logout),
    url(r'^user/(?P<id>\d+)$', views.show_profile),
]
