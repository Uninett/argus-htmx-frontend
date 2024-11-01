from django import forms

from argus.auth.models import Preferences, PreferencesManager

from argus_htmx.constants import (
    DATETIME_FORMATS,
    DATETIME_DEFAULT,
    DATETIME_CHOICES,
    PAGE_SIZE_CHOICES,
    DEFAULT_PAGE_SIZE,
    THEME_CHOICES,
)


class DateTimeFormatForm(forms.Form):
    datetime_format_name = forms.ChoiceField(required=False, choices=DATETIME_CHOICES)

    def clean_datetime_format(self):
        return self.cleaned_data.get("datetime_format", DATETIME_DEFAULT) or DATETIME_DEFAULT


class PageSizeForm(forms.Form):
    page_size = forms.TypedChoiceField(required=False, choices=PAGE_SIZE_CHOICES, coerce=int)

    def clean_page_size(self):
        return self.cleaned_data.get("page_size", DEFAULT_PAGE_SIZE) or DEFAULT_PAGE_SIZE


class ThemeForm(forms.Form):
    theme = forms.ChoiceField(choices=THEME_CHOICES)


class ArgusHtmxPreferencesManager(PreferencesManager):
    def get_queryset(self):
        return super().get_queryset().filter(namespace=ArgusHtmxPreferences._namespace)

    def create(self, **kwargs):
        kwargs["namespace"] = ArgusHtmxPreferences._namespace
        return super().create(**kwargs)


class ArgusHtmxPreferences(Preferences):
    _namespace = "argus_htmx"
    FORMS = {
        "datetime_format_name": DateTimeFormatForm,
        "page_size": PageSizeForm,
        "theme": ThemeForm,
    }

    class Meta:
        proxy = True

    objects = ArgusHtmxPreferencesManager()

    def get_datetime_format_name_context(self):
        datetime_format_name = self.preferences.get("datetime_format_name", DATETIME_DEFAULT)
        datetime_format = DATETIME_FORMATS[datetime_format_name]
        return {"datetime_format": datetime_format}
