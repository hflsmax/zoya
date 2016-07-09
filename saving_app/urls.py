from django.conf.urls import url
from . import views

# Create your views here.
urlpatterns = [
    url(r'^$', views.choice_without_id, name = "choice_without_id"),
    # url(r'^([0-9]*)$', views.choice, name = "choice"),
    # url(r'^set/([0-9]*)$', views.set, name = "set"),
    url(r'^choice/$', views.choice, name = "choice"),
    url(r'^set1/$', views.set1, name = "set1"),
    url(r'^set2/$', views.set2, name = "set2"),
    url(r'^set3/$', views.set3, name = "set3"),
    url(r'^update/$', views.update, name = "update"),
]
