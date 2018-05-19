from django.conf.urls import url
from .views import redirect_url,api_root

urlpatterns = [
    url(r'^api/short/new', api_root, name='POST URL'),
    url(r'^(?P<tiny_id>[-\w]+)/$', redirect_url, name='Redirect URL'),
]