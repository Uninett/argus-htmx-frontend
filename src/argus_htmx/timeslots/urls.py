from django.urls import path

from .views import TimeslotListView


app_name = "htmx"
urlpatterns = [
    path("", TimeslotListView.as_view(), name="timeslot-list"),
]
