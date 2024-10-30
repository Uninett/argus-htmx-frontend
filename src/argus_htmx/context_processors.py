"""
How to use:

Append the "context_processors" list for the TEMPLATES-backend
``django.template.backends.django.DjangoTemplates`` with the full dotted path.

See django settings for ``TEMPLATES``.
"""

from .models import ArgusHtmxPreferences

from .constants import DATETIME_DEFAULT, DATETIME_FORMATS


def theme_via_GET(request):
    # Move to theme-app?
    theme = request.GET.get("theme", None)
    if not theme:
        prefs = ArgusHtmxPreferences.objects.get(user=request.user)
        theme = prefs.preferences.get("theme", None)
    return {"theme": theme}


def theme_via_session(request):
    # Move to theme-app?
    theme = request.session.get("theme", None)
    if not theme:
        prefs = ArgusHtmxPreferences.objects.get(user=request.user)
        theme = prefs.preferences.get("theme", None)
        request.session["theme"] = theme
    return {"theme": theme}


def theme_via_saved_preference(request):
    prefs = ArgusHtmxPreferences.objects.get(user=request.user)
    theme = prefs.preferences.get("theme", None)
    return {"theme": theme}


def datetime_format_via_session(request):
    datetime_format_name = request.session.get("datetime_format_name")
    if not datetime_format_name:
        prefs = ArgusHtmxPreferences.objects.get(user=request.user)
        datetime_format_name = prefs.preferences.get("datetime_format_name", DATETIME_DEFAULT)
        request.session["datetime_format_name"] = datetime_format_name

    if datetime_format_name not in DATETIME_FORMATS:
        datetime_format_name = DATETIME_DEFAULT
    # The named format always wins
    datetime_format = DATETIME_FORMATS[datetime_format_name]
    return {
        "datetime_format": datetime_format,
        "datetime_format_name": datetime_format_name,
    }
