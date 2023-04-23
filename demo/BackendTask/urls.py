from django.urls import path

from . import views

urlpatterns = [
    path("/v1/calendar/init/", views.GoogleCalendarInitView, name="oAuth"),
    path("/v1/calendar/redirect/", views. GoogleCalendarRedirectView, name="redirect"),
]