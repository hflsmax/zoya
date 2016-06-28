from django.conf.urls import url
from . import views

# Create your views here.
urlpatterns = [
    # url(r'^(?P<user_id>[0-9]+)/$', views.first_page, name='index'),
    url(r'^$', views.choice_without_id, name = "choice_without_id"),
    url(r'^([0-9]*)$', views.choice, name = "choice"),
    url(r'^set/([0-9]*)$', views.set, name = "set"),
]
