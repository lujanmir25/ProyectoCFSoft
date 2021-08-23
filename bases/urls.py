from django.urls import path
from django.urls.resolvers import URLPattern

from bases.views import Home

urlpatterns = [
    path('',Home.as_view(),name='home'),
]