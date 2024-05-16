import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.template import Template, RequestContext
from django.views.generic import ListView

from argus.notificationprofile.models import Timeslot


LOG = logging.getLogger(__name__)


def placeholder(request):
    template = Template(
        """{% extends "htmx/base.html" %}
        {% block main %}
        <h1>TIMESLOT PLACEHOLDER</h1>
        {% endblock main %}
        """
    )
    context = RequestContext(request)
    return HttpResponse(template.render(context))


class TimeslotListView(LoginRequiredMixin, ListView):
    model = Timeslot
    template_name = 'htmx/argus_notificationprofile/timeslot_list.html'

    def get_queryset(self):
        qs = super().get_queryset().prefetch_related("time_recurrences")
        return qs.filter(user=self.request.user)
