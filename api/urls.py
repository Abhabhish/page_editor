from django.urls import path
from . import views
from django.urls import re_path

urlpatterns = [
    re_path(r'^page_content/(?P<slug>.+)/$', views.post_detail_view),
]

