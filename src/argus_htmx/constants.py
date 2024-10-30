from argus_htmx.dateformat.constants import DATETIME_DEFAULT, DATETIME_FORMATS, DATETIME_CHOICES
from argus_htmx.incidents.constants import DEFAULT_PAGE_SIZE, ALLOWED_PAGE_SIZES
from argus_htmx.themes.constants import THEME_CHOICES, THEME_NAMES


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


PAGE_SIZE_CHOICES = tuple((ps, ps) for ps in ALLOWED_PAGE_SIZES)
