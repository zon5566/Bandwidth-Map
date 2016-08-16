from django.conf.urls import url
from . import views

app_name = 'map'

urlpatterns = [
	url(r'^$', views.homepage, name='homepage'),
#	url(r'^(?P<carrier_id>\d+)$', views.selectpage, name='selectpage'),
]