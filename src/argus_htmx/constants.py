from argus_htmx.dateformat.constants import DATETIME_DEFAULT, DATETIME_FORMATS
from argus_htmx.incidents.constants import DEFAULT_PAGE_SIZE, ALLOWED_PAGE_SIZES
from argus_htmx.themes.utils import get_theme_names


__all__ = [
    "ALLOWED_PAGE_SIZES",
    "DATETIME_CHOICES",
    "DATETIME_DEFAULT",
    "DATETIME_FORMATS",
    "DEFAULT_PAGE_SIZE",
    "PAGE_SIZE_CHOICES",
    "THEME_CHOICES",
    "THEME_NAMES",
]


THEME_NAMES = get_theme_names()
DATETIME_CHOICES = tuple((format, format) for format in DATETIME_FORMATS)
PAGE_SIZE_CHOICES = tuple((ps, ps) for ps in ALLOWED_PAGE_SIZES)
THEME_CHOICES = tuple((theme, theme) for theme in THEME_NAMES)
