from argus.auth.models import Preferences, PreferencesManager

from argus_htmx.constants import DATETIME_FORMATS, DATETIME_DEFAULT


class ArgusHtmxPreferencesManager(PreferencesManager):
    def get_queryset(self):
        return super().get_queryset().filter(namespace=ArgusHtmxPreferences._namespace)

    def create(self, **kwargs):
        kwargs["namespace"] = ArgusHtmxPreferences._namespace
        return super().create(**kwargs)


class ArgusHtmxPreferences(Preferences):
    _namespace = "argus_htmx"

    class Meta:
        proxy = True

    objects = ArgusHtmxPreferencesManager()

    def get_datetime_format_name_context(self):
        datetime_format_name = self.preferences.get("datetime_format_name", DATETIME_DEFAULT)
        datetime_format = DATETIME_FORMATS[datetime_format_name]
        return {"datetime_format": datetime_format}
