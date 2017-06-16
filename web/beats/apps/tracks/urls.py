""" URL routes for Tracks non-API views """
from django.conf.urls import url

from .views import IndexView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
]
