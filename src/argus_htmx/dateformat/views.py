import logging

from django.contrib import messages
from django.shortcuts import render

from django.views.decorators.http import require_GET, require_POST
from django.http import HttpResponse
from django_htmx.http import HttpResponseClientRefresh

from argus_htmx.incidents.views import HtmxHttpRequest

LOG = logging.getLogger(__name__)
DATETIME_DEFAULT = 'LOCALE'
DATETIME_FORMATS = {
    'LOCALE': 'DATETIME_FORMAT',  # default
    'ISO': 'Y-m-d H:i:s',
    'RFC5322': 'r',
    'EPOCH': 'U',
}


@require_GET
def dateformat_names(request: HtmxHttpRequest) -> HttpResponse:
    datetime_formats = DATETIME_FORMATS.keys()
    return render(request, "htmx/dateformat/_dateformat_list.html", {"datetime_formats": datetime_formats})


@require_POST
def change_dateformat(request: HtmxHttpRequest) -> HttpResponse:
    datetime_format_name = request.POST.get("dateformat", DATETIME_DEFAULT)
    if datetime_format_name in DATETIME_FORMATS:
        datetime_format = DATETIME_FORMATS[datetime_format_name]
        request.session["datetime_format"] = datetime_format
        request.session["datetime_format_name"] = datetime_format_name
        messages.success(request, f'Switched dateformat to "{datetime_format_name}"')
        return HttpResponse(f'{datetime_format_name}')
    return HttpResponseClientRefresh()
