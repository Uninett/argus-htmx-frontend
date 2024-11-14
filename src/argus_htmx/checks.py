from django.core.checks import Error, Warning, register
from django.core.exceptions import ImproperlyConfigured

from .themes.utils import get_theme_names


@register
def check_for_valid_themes_list(app_configs, **kwargs):
    themes = []
    try:
        themes = get_theme_names(quiet=False)
    except ImproperlyConfigured as e:
        return [
            Warning(
                str(e),
                hint="Regenerate styles.css",
                id="argus_htmx.T001",
            )
        ]
    if not themes:
        return [
            Error(
                "no themes installed",
                hint='Check the settings "DAISYUI_THEMES" and "TAILWIND_THEME_OVERRIDE" and regenerate styles.css',
                id="argus_htmx.T002",
            )
        ]
