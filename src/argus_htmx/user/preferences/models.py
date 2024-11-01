from argus.auth.models import Preferences, PreferencesManager


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
