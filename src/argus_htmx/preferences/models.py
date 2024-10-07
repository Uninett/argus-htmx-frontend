from django.core.exceptions import ValidationError

from argus.auth.models import Preferences, PreferencesManager

from .serializers import ArgusHtmxPreferencesSerializer


class ArgusHtmxPreferencesManager(PreferencesManager):
    def get_queryset(self):
        return super().get_queryset().filter(namespace=NAMESPACE)

    def create(self, **kwargs):
        kwargs["namespace"] = NAMESPACE
        return super().create(**kwargs)


class ArgusHtmxPreferences(Preferences):
    class Meta:
        proxy = True

    app_label = "argus_htmx"
    class_name = "ArgusHtmxPreferences"
    SERIALIZER = ArgusHtmxPreferencesSerializer

    objects = ArgusHtmxPreferencesManager()

    # Try writing a validator using the form instead of changing clean_fields

    def clean(self):
        form = self.FORM(self.preferences)
        if not form.is_valid():
            raise ValidationError(form.errors)


NAMESPACE = ArgusHtmxPreferences.generate_namespace()
