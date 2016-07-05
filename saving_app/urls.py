from django.conf.urls import url
from . import views

# Create your views here.
urlpatterns = [
    url(r'^$', views.choice_without_id, name = "choice_without_id"),
    # url(r'^([0-9]*)$', views.choice, name = "choice"),
    # url(r'^set/([0-9]*)$', views.set, name = "set"),
    url(r'^choice/$', views.choice, name = "choice"),
    url(r'^set/$', views.set, name = "set"),
    url(r'^update/$', views.update, name = "update"),
]
