from django.core.checks import Error, register
from django.core.exceptions import ImproperlyConfigured

from .themes.utils import get_theme_names


@register
def check_for_valid_themes_list(app_configs, **kwargs):
    errors = []
    themes = []
    try:
        themes = get_theme_names()
    except ImproperlyConfigured as e:
        errors.append(
            Error(
                str(e),
                hint="Regenerate styles.css",
                id="argus_htmx.T001",
            )
        )
    else:
        if not themes:
            errors.append(
                Error(
                    "no themes installed",
                    hint='Check the settings "DAISYUI_THEMES" and "TAILWIND_THEME_OVERRIDE" and regenerate styles.css',
                    id="argus_htmx.T002",
                )
            )
    return errors
