from __future__ import annotations

import logging
from datetime import datetime

from django import forms
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404

from django.views.decorators.http import require_POST, require_GET
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from django_htmx.middleware import HtmxDetails
from django_htmx.http import HttpResponseClientRefresh

from argus.incident.models import Incident
from argus.util.datetime_utils import make_aware

from .constants import DEFAULT_PAGE_SIZE, ALLOWED_PAGE_SIZES, PAGE_SIZE_CHOICES
from .customization import get_incident_table_columns
from .utils import get_filter_function
from .forms import AckForm, DescriptionOptionalForm, EditTicketUrlForm, AddTicketUrlForm
from ..models import ArgusHtmxPreferences
from ..utils import (
    bulk_change_incidents,
    bulk_ack_queryset,
    bulk_close_queryset,
    bulk_reopen_queryset,
    bulk_change_ticket_url_queryset,
)

User = get_user_model()
LOG = logging.getLogger(__name__)


# Map request trigger to parameters for incidents update
INCIDENT_UPDATE_ACTIONS = {
    "ack": (AckForm, bulk_ack_queryset),
    "close": (DescriptionOptionalForm, bulk_close_queryset),
    "reopen": (DescriptionOptionalForm, bulk_reopen_queryset),
    "update-ticket": (EditTicketUrlForm, bulk_change_ticket_url_queryset),
    "add-ticket": (AddTicketUrlForm, bulk_change_ticket_url_queryset),
}


class PageSizeForm(forms.Form):
    page_size = forms.TypedChoiceField(required=False, choices=PAGE_SIZE_CHOICES, coerce=int)

    def clean_page_size(self):
        return self.cleaned_data.get("page_size", DEFAULT_PAGE_SIZE) or DEFAULT_PAGE_SIZE


def save_page_size(request, page_size):
    ArgusHtmxPreferences.ensure_for_user(request.user)
    prefs = ArgusHtmxPreferences.objects.get(user=request.user)
    prefs.preferences["page_size"] = page_size
    prefs.save()


def prefetch_incident_daughters():
    return Incident.objects.select_related("source").prefetch_related(
        "incident_tag_relations",
        "incident_tag_relations__tag",
        "events",
        "events__ack",
    )


class HtmxHttpRequest(HttpRequest):
    htmx: HtmxDetails


# fetch with htmx
def incident_detail(request, pk: int):
    incident = get_object_or_404(Incident, id=pk)
    context = {
        "incident": incident,
        "page_title": str(incident),
    }
    return render(request, "htmx/incidents/incident_detail.html", context=context)


def get_form_data(request, formclass: forms.Form):
    formdata = request.POST or None
    incident_ids = []
    cleaned_form = None
    if formdata:
        incident_ids = request.POST.getlist("incident_ids", [])
        form = formclass(formdata)
        if form.is_valid():
            cleaned_form = form.cleaned_data
    return cleaned_form, incident_ids


@require_POST
def incidents_update(request: HtmxHttpRequest, action: str):
    try:
        formclass, callback_func = INCIDENT_UPDATE_ACTIONS[action]
    except KeyError:
        LOG.error("Unrecognized action name %s when updating incidents.", action)
        return HttpResponseBadRequest("Invalid update action")
    formdata, incident_ids = get_form_data(request, formclass)
    if formdata:
        bulk_change_incidents(request.user, incident_ids, formdata, callback_func)
    return HttpResponseClientRefresh()


@require_GET
def filter_form(request: HtmxHttpRequest):
    incident_list_filter = get_filter_function()
    filter_form, _ = incident_list_filter(request, None)
    context = {"filter_form": filter_form}
    return render(request, "htmx/incidents/_incident_filterbox.html", context=context)


def incident_list(request: HtmxHttpRequest) -> HttpResponse:
    columns = get_incident_table_columns()

    # Load incidents
    qs = prefetch_incident_daughters().order_by("-start_time")
    total_count = qs.count()
    last_refreshed = make_aware(datetime.now())

    params = dict(request.GET.items())

    incident_list_filter = get_filter_function()
    filter_form, qs = incident_list_filter(request, qs)
    filtered_count = qs.count()

    # Standard Django pagination
    page_size_form = PageSizeForm(request.GET)
    if page_size_form.is_valid():
        page_size = page_size_form.cleaned_data["page_size"]
        save_page_size(request, page_size)
    paginator = Paginator(object_list=qs, per_page=page_size)
    page_num = params.pop("page", "1")
    page = paginator.get_page(page_num)

    # The htmx magic - use a different, minimal base template for htmx
    # requests, allowing us to skip rendering the unchanging parts of the
    # template.
    if request.htmx:
        base_template = "htmx/incidents/responses/_incidents_table_refresh.html"
    else:
        base_template = "htmx/incidents/_base.html"
    context = {
        "columns": columns,
        "filtered_count": filtered_count,
        "count": total_count,
        "filter_form": filter_form,
        "page_title": "Incidents",
        "base": base_template,
        "page": page,
        "last_refreshed": last_refreshed,
        "update_interval": 30,
        "all_page_sizes": ALLOWED_PAGE_SIZES,
    }

    return render(request, "htmx/incidents/incident_list.html", context=context)
