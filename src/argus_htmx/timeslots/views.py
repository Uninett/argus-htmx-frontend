import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Template, RequestContext
from django.views.generic import ListView, DetailView
from django.urls import reverse

from argus.notificationprofile.models import Timeslot, TimeRecurrence
from .forms import TimeslotForm, TimeRecurrenceForm, TimeRecurrenceFormSet


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["create"] = {
            "timeslot_form": TimeslotForm(),
            "timerecurrence_form": TimeRecurrenceForm(),
            "timerecurrence_formset": TimeRecurrenceFormSet(),
        }
        forms = []
        for ts in self.object_list:
            tsf = TimeslotForm(instance=ts)
            forms.append({
                "timeslot_form": tsf,
                "timerecurrence_form": TimeRecurrenceForm(),
                "timerecurrence_formset": TimeRecurrenceFormSet(instance=ts),
            })
        context["timeslots"] = forms
        return context


class TimeslotCreateView(LoginRequiredMixin, DetailView):
    model = Timeslot
    template_name = 'htmx/argus_notificationprofile/timeslot_list.html'
    http_method_names = ['post', 'head', 'options', 'trace']

    def get_form_kwargs(self):
        kwargs = {
            #"initial": self.get_initial(),
            "prefix": "timeslotform",
        }
        if self.request.method in ("POST", "PUT"):
            kwargs.update(
                {
                    "data": self.request.POST,
                    "files": self.request.FILES,
                }
            )
        if hasattr(self, "object"):
            kwargs.update({"instance": self.object})
        return kwargs

    def get_success_url(self):
        return reverse("htmx:timeslot-list")

    def get_queryset(self):
        qs = super().get_queryset().prefetch_related("time_recurrences")
        return qs.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["timeslot_form"] = TimeslotForm()
        context["timerecurrence_formset"] = TimeRecurrenceFormSet()
        return context

    def post(self, request, *args, **kwargs):
        tsf = TimeslotForm(**self.get_form_kwargs())
        tsf.user = self.request.user
        if tsf.is_valid():
            tsf.save()
        else:
            assert False, tsf.errors
            messages.add_message(request, messages.ERROR, f"Problem in tsf form. {tsf.errors}")
        return HttpResponseRedirect(self.get_success_url())
        trf = TimeRecurrenceFormSet(instance=tsf, **self.get_form_kwargs())
        if trf.is_valid():
            trf.save()
        else:
            messages.add_message(request, messages.ERROR, f"Problem in trf form. {tsf.errors}")
        return HttpResponseRedirect(self.get_success_url())
