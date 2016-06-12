from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

api_patterns = [
    url(r'^tasks/(?P<pk>[0-9]+)/solve/$', views.TaskSolve.as_view()),
    url(r'^tasks/(?P<pk>[0-9]+)/$', views.TaskDetail.as_view()),
    url(r'^tasks/$', views.TaskList.as_view()),
]

api_patterns = format_suffix_patterns(api_patterns)
