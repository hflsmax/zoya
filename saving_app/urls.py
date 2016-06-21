from django.conf.urls import url
from . import views

# Create your views here.
urlpatterns = [
    url(r'^(?P<user_id>[0-9]+)/$', views.first_page, name='index'),
]
