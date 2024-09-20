"""
How to use:

Append the "context_processors" list for the TEMPLATES-backend
``django.template.backends.django.DjangoTemplates`` with the full dotted path.

See django settings for ``TEMPLATES``.
"""

def theme_via_GET(request):
    # Move to theme-app?
    theme = request.GET.get("theme", None)
    return {"theme": theme}


def theme_via_session(request):
    # Move to theme-app?
    theme = request.session.get("theme", None)
    return {"theme": theme}


def datetime_format_via_session(request):
    datetime_format = request.session.get("datetime_format", "DATETIME_FORMAT")  # fallback to locale
    datetime_format_name = request.session.get("datetime_format_name", "LOCALE")  # fallback to locale
    return {
        "datetime_format": datetime_format,
        "datetime_format_name": datetime_format_name,
    }
