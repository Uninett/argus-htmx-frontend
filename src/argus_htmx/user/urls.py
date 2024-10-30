from django.urls import path

from . import views


app_name = "htmx"
urlpatterns = [
    path("", views.user_preferences, name="user-preferences"),
]
