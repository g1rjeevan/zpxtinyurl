from django.conf.urls import url
from .views import redirecturl,api_root

urlpatterns = [
    url(r'^api/short/new', api_root, name='POST URL'),
    url(r'^(?P<tiny_id>[-\w]+)/$', redirecturl, name='Redirect URL'),
]