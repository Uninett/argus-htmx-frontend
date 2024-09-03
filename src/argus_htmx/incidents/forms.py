from django import forms

class AckForm(forms.Form):
    description = forms.CharField()
    expiration = forms.DateTimeField(required=False)


class DescriptionOptionalForm(forms.Form):
    "For closing/reopening"
    description = forms.CharField(required=False)
