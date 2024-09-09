from django.urls import include, path

app_name = "htmx"
urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
]
