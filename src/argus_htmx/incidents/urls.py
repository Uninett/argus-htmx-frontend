from django.urls import path, include

from . import views


app_name = "htmx"
urlpatterns = [
    path("", views.incidents, name="htmx_incidents"),
    path("<int:pk>/", views.incident_detail, name="htmx_incident_detail"),
    path("<int:pk>/ack/", views.incident_add_ack, name="htmx-incident-add-ack"),
    path("table/", views.incidents_table, name="htmx_incidents_table"),
]
