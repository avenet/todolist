from django.conf.urls import url

from rest_framework.authtoken import views as rest_framework_views
from rest_framework.urlpatterns import format_suffix_patterns


from . import views as user_views

api_patterns = [
    url(r'^users/$', user_views.UserCreate.as_view()),
    url(r'^users/get-token/$', rest_framework_views.obtain_auth_token),
]

api_patterns = format_suffix_patterns(api_patterns)
