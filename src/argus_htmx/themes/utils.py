from importlib.resources import files
from pathlib import Path

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from argus_htmx import settings as default_htmx_settings


__all__ = ["get_theme_names"]


def get_themes_from_setting():
    themes_setting = getattr(settings, "DAISYUI_THEMES", default_htmx_settings.DAISYUI_THEMES)
    theme_names = []
    for theme in themes_setting:
        if isinstance(theme, str):
            theme_names.append(theme)
        elif isinstance(theme, dict):
            theme_names.extend(theme.keys())
    return theme_names


def get_themes_from_css():
    static_url = Path(settings.STATIC_URL).relative_to("/")
    stylesheet_path = static_url / default_htmx_settings.STYLESHEET_PATH
    styles_css = files("argus_htmx").joinpath(stylesheet_path).read_text()
    styles_css_lines = styles_css.split("{")
    theme_names = []
    for line in styles_css_lines:
        if "data-theme=" not in line:
            continue
        _, after = line.split("=", 1)
        theme_name, _ = after.split("]", 1)
        theme_names.append(theme_name.strip())
    return theme_names


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
