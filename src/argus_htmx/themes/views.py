import logging

from django.contrib import messages
from django.shortcuts import render
from django.views.generic import ListView

from django.views.decorators.http import require_GET, require_POST
from django.http import HttpResponse, HttpResponseRedirect
from django_htmx.http import HttpResponseClientRefresh

from argus_htmx.constants import THEME_NAMES
from argus_htmx.incidents.views import HtmxHttpRequest

LOG = logging.getLogger(__name__)
THEMES_MODULE = "argus_htmx"


class ThemeListView(ListView):
    http_method_names = ["get", "post", "head", "options", "trace"]
    template_name = "htmx/themes/themes_list.html"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.themes = THEME_NAMES

    def get_queryset(self):
        return self.themes

    def post(self, request, *args, **kwargs):
        prefs = request.user.get_preferences("argus_htmx")
        form = prefs.FORMS["theme"](request.POST)
        if form.is_valid():
            theme = form.cleaned_data["theme"]
            prefs.save_preference("theme", theme)
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
    prefs = request.user.get_preferences("argus_htmx")
    theme = prefs.preferences.get("theme", None)
    LOG.debug("Changing theme, current theme: %s", theme)
    if request.POST.get("theme", None):
        form = prefs.FORMS["theme"](request.POST)
        LOG.debug("Changing theme, POST: %s, form: %s", request.POST, form)
        if form.is_valid():
            theme = form.cleaned_data["theme"]
            prefs.save_preference("theme", theme)
            messages.success(request, f'Switched theme to "{theme}"')
            LOG.info("Changing theme: changed to %s", theme)
        else:
            LOG.warn("Changing theme: failed to change theme")
        return HttpResponse(theme)
    return HttpResponseClientRefresh()
