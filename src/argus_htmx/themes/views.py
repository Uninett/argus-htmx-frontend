import logging

from django.contrib import messages
from django import forms
from django.shortcuts import render
from django.views.generic import ListView

from django.views.decorators.http import require_GET, require_POST
from django.http import HttpResponse, HttpResponseRedirect
from django_htmx.http import HttpResponseClientRefresh

from argus_htmx.constants import THEME_NAMES
from argus_htmx.incidents.views import HtmxHttpRequest
from argus_htmx.models import ArgusHtmxPreferences

LOG = logging.getLogger(__name__)
THEMES_MODULE = "argus_htmx"


class ThemeForm(forms.Form):
    THEME_NAMES = tuple((t, t) for t in get_theme_names())
    theme = forms.ChoiceField(choices=THEME_NAMES)


def save_theme(request, theme):
    request.session["theme"] = theme
    ArgusHtmxPreferences.ensure_for_user(request.user)
    prefs = ArgusHtmxPreferences.objects.get(user=request.user)
    prefs.preferences["theme"] = theme
    prefs.save()


class ThemeListView(ListView):
    http_method_names = ["get", "post", "head", "options", "trace"]
    template_name = "htmx/themes/themes_list.html"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.themes = THEME_NAMES

    def get_queryset(self):
        return self.themes

    def post(self, request, *args, **kwargs):
        form = ThemeForm(request.POST)
        if form.is_valid():
            theme = form.cleaned_data["theme"]
            save_theme(request, theme)
            messages.success(request, f'Switched theme to "{theme}"')
        else:
            messages.warning(request, "Did not switch theme, theme not installed")
        return HttpResponseRedirect("")


@require_GET
def theme_names(request: HtmxHttpRequest) -> HttpResponse:
    themes = THEME_NAMES
    return render(request, "htmx/themes/theme_list.html", {"theme_list": themes})


@require_POST
def change_theme(request: HtmxHttpRequest) -> HttpResponse:
    form = ThemeForm(request.POST)
    if form.is_valid():
        theme = form.cleaned_data["theme"]
        save_theme(request, theme)
        messages.success(request, f'Switched theme to "{theme}"')
        return render(request, "htmx/themes/_current_theme.html")
    return HttpResponseClientRefresh()
