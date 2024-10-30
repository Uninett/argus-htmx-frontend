import logging

from django.contrib import messages
from django import forms
from django.shortcuts import render

from django.views.decorators.http import require_GET, require_POST
from django.http import HttpResponse
from django_htmx.http import HttpResponseClientRefresh

from argus_htmx.incidents.views import HtmxHttpRequest
from argus_htmx.models import ArgusHtmxPreferences
from .constants import DATETIME_DEFAULT, DATETIME_FORMATS, DATETIME_CHOICES

LOG = logging.getLogger(__name__)


class DateTimeFormatForm(forms.Form):
    datetime_format_name = forms.ChoiceField(required=False, choices=DATETIME_CHOICES)

    def clean_datetime_format(self):
        return self.cleaned_data.get("datetime_format", DATETIME_DEFAULT) or DATETIME_DEFAULT


def save_datetime_format(request, datetime_format_name):
    default_format = DATETIME_FORMATS[DATETIME_DEFAULT]
    datetime_format = DATETIME_FORMATS.get(datetime_format_name, default_format)
    request.session["datetime_format"] = datetime_format
    request.session["datetime_format_name"] = datetime_format_name
    ArgusHtmxPreferences.ensure_for_user(request.user)
    prefs = ArgusHtmxPreferences.objects.get(user=request.user)
    prefs.preferences["datetime_format_name"] = datetime_format_name
    prefs.save()


@require_GET
def dateformat_names(request: HtmxHttpRequest) -> HttpResponse:
    datetime_formats = DATETIME_FORMATS.keys()
    return render(request, "htmx/dateformat/_dateformat_list.html", {"datetime_formats": datetime_formats})


@require_POST
def change_dateformat(request: HtmxHttpRequest) -> HttpResponse:
    form = DateTimeFormatForm(request.POST)
    if form.is_valid():
        datetime_format_name = form.cleaned_data["datetime_format_name"]
        save_datetime_format(request, datetime_format_name)
        messages.success(request, f'Switched dateformat to "{datetime_format_name}"')
    return HttpResponseClientRefresh()
