from django.db import models  # noqa: F401 - unused-import

from argus_htmx.preferences.models import ArgusHtmxPreferences, NAMESPACE


__all__ = [
    "ArgusHtmxPreferences",
    "NAMESPACE",
]
