from django.urls import path, include

from . import views


app_name = "htmx"
urlpatterns = [
    path("", views.incident_list, name="incident-list"),
    path("<int:pk>/", views.incident_detail, name="incident-detail"),
    path("update/<str:action>/", views.incidents_update, name="incidents-update"),
    path("<int:pk>/update/<str:action>/", views.incidents_update, name="incidents-update"),
]
