from django.urls import path

from . import views


app_name = "htmx"
urlpatterns = [
    path("", views.TimeslotListView.as_view(), name="timeslot-list"),
    path("create/", views.TimeslotCreateView.as_view(), name="timeslot-create"),
]
