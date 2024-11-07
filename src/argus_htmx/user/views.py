from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST
from django_htmx.http import HttpResponseClientRefresh

from argus_htmx.constants import ALLOWED_PAGE_SIZES
from argus_htmx.incidents.views import HtmxHttpRequest


@require_GET
def page_size_names(request: HtmxHttpRequest) -> HttpResponse:
    page_sizes = sorted(ALLOWED_PAGE_SIZES)
    return render(request, "htmx/page_size/_page_size_list.html", {"page_sizes": page_sizes})


@require_POST
def change_page_size(request: HtmxHttpRequest) -> HttpResponse:
    prefs = request.user.get_namespaced_preferences("argus_htmx")
    form = prefs.FORMS["page_size"](request.POST)
    if form.is_valid():
        page_size = form.cleaned_data["page_size"]
        prefs = request.user.get_namespaced_preferences("argus_htmx")
        prefs.save_preference("page_size", page_size)
        messages.success(request, f'Switched page_size to "{page_size}"')
    return HttpResponseClientRefresh()


def user_preferences(request) -> HttpResponse:
    """Renders the main preferences page for a user"""
    context = {
        "page_title": "User preferences",
    }
    return render(request, "htmx/user/preferences.html", context=context)
