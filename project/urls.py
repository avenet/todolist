from django.conf.urls import include, url
from django.contrib import admin

from apps.users.urls import api_patterns as user_api_patterns

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/v1/', include(user_api_patterns)),
]
