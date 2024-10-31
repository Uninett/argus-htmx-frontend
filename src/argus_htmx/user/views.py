from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST
from django_htmx.http import HttpResponseClientRefresh

from argus_htmx.constants import ALLOWED_PAGE_SIZES, DEFAULT_PAGE_SIZE
from argus_htmx.incidents.views import PageSizeForm, HtmxHttpRequest, save_page_size
from .preferences.models import ArgusHtmxPreferences


@require_GET
def page_size_names(request: HtmxHttpRequest) -> HttpResponse:
    page_sizes = sorted(ALLOWED_PAGE_SIZES)
    return render(request, "htmx/page_size/_page_size_list.html", {"page_sizes": page_sizes})


@require_POST
def change_page_size(request: HtmxHttpRequest) -> HttpResponse:
    prefs = request.user.get_preferences("argus_htmx")
    form = prefs.FORMS["page_size"](request.POST)
    if form.is_valid():
        page_size = form.cleaned_data["page_size"]
        save_page_size(request, page_size)
        messages.success(request, f'Switched page_size to "{page_size}"')
    return HttpResponseClientRefresh()


def user_preferences(request) -> HttpResponse:
    """Renders the main preferences page for a user"""
    ArgusHtmxPreferences.ensure_for_user(request.user)
    prefs = ArgusHtmxPreferences.objects.get(user=request.user)
    page_size = prefs.preferences.get("page_size", DEFAULT_PAGE_SIZE)
    context = {
        "page_title": "User preferences",
        "page_size": page_size,
    }
    return render(request, "htmx/user/preferences.html", context=context)
