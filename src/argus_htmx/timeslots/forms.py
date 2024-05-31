from django import forms
from django.forms import inlineformset_factory

from argus.notificationprofile.models import Timeslot, TimeRecurrence


class TimeslotForm(forms.ModelForm):
    class Meta:
        model = Timeslot
        fields = ["name"]


class TimeRecurrenceForm(forms.ModelForm):
    class Meta:
        model = TimeRecurrence
        fields = ["days", "start", "end"]


TimeRecurrenceFormSet = inlineformset_factory(
    Timeslot,
    TimeRecurrence,
    form=TimeRecurrenceForm,
    min_num=1,
    extra=0,
    can_delete=False
)
