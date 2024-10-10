from django.conf import settings
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.urls import reverse

from argus.auth.utils import (
    has_model_backend,
    has_remote_user_backend,
    get_psa_authentication_backends,
    get_authentication_backend_classes,
)


REMOTE_USER_METHOD_NAME = getattr(settings, "ARGUS_REMOTE_USER_METHOD_NAME", "REMOTE_USER")


def get_htmx_authentication_backend_name_and_type():
    # Needed for HTMX LoginView
    backends = get_authentication_backend_classes()

    data = {}
    if has_model_backend(backends):
        data["username_password"] = {
            "url": reverse("htmx:login"),
            "button": "Log In",
        }

    if has_remote_user_backend(backends):
        remote_user_data = {
            "url": "/",
            "button": REMOTE_USER_METHOD_NAME,
        }
        data.setdefault("link", []).append(remote_user_data)

    for backend in get_psa_authentication_backends(backends):
        psa_backend_data = {
            "url": reverse("social:begin", kwargs={"backend": backend.name}),
            "button": backend.name,
        }
        data.setdefault("link", []).append(psa_backend_data)

    return data


class LoginView(DjangoLoginView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        urlname = "htmx:login"
        backends = get_htmx_authentication_backend_name_and_type()
        context["backends"] = backends
        return context
