from importlib.resources import files
from pathlib import Path
from re import findall

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from argus_htmx import settings as default_htmx_settings


__all__ = [
    "get_theme_names",
    "get_theme_default",
]


def get_themes_from_setting():
    themes_setting = getattr(settings, "DAISYUI_THEMES", default_htmx_settings.DAISYUI_THEMES)
    theme_names = []
    for theme in themes_setting:
        if isinstance(theme, str):
            theme_names.append(theme)
        elif isinstance(theme, dict):
            theme_names.extend(theme.keys())
    return theme_names


def get_stylesheet_path():
    return getattr(settings, "STYLESHEET_PATH", default_htmx_settings.STYLESHEET_PATH)


def get_themes_from_css():
    THEME_NAME_RE = "(?P<theme>\w+)"
    DATA_THEME_RE = f"\[data-theme={THEME_NAME_RE}\]"

    static_url = Path(settings.STATIC_URL).relative_to("/")
    stylesheet_path = static_url / get_stylesheet_path()
    styles_css = files("argus_htmx").joinpath(stylesheet_path).read_text()

    return findall(DATA_THEME_RE, styles_css)


def get_theme_names():
    themes_from_setting = set(get_themes_from_setting())
    themes_from_css = set(get_themes_from_css())
    installed_themes = themes_from_setting | themes_from_css
    all_themes = themes_from_setting & themes_from_css
    if all_themes != installed_themes:
        raise ImproperlyConfigured("Themes in settings is out of sync with themes installed")
    return installed_themes


def get_theme_default():
    return getattr(settings, "THEME_DEFAULT", default_htmx_settings.THEME_DEFAULT)
