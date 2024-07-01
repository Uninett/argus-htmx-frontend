"""
Definitions and defaults for UI customization on the incidents page.

Currently customizable UI elements:
- table columns: hide default columns and/or show additional columns

Expected to be customizable in the future [WIP list]:
- table row colors
- table row effects
- add custom components to the incidents page
"""

from dataclasses import dataclass
from typing import Optional, OrderedDict, Union


@dataclass
class FieldContext:
    """Class for providing additional context to a dynamic field."""

    ack: Optional[str] = None  # team or user group
    tag: Optional[dict] = None  # incident tag name


@dataclass
class IncidentField:
    """Class for keeping track of columns in the incidents table."""

    name: str  # identifier
    label: str  # display value
    cell_template: str
    context: Optional[Union[FieldContext, dict]] = None


DEFAULT_FIELDS = OrderedDict[str, IncidentField]([
    ("row_select", IncidentField("checkbox", "Selected", "htmx/incidents/_incident_checkbox.html")),
    ("start_time", IncidentField("start_time", "Timestamp", "htmx/incidents/_incident_start_time.html")),
    ("status", IncidentField("status", "Status", "htmx/incidents/_incident_status.html")),
    ("level", IncidentField("level", "Severity level", "htmx/incidents/_incident_level.html")),
    ("source", IncidentField("source", "Source", "htmx/incidents/_incident_source.html")),
    ("description", IncidentField("description", "Description", "htmx/incidents/_incident_description.html")),
    ("links", IncidentField("links", "Actions", None))
])

# TODO remove before alpha release
# Fields for demo/debug/dev purposes
TEMP_FIELDS = {
    "id": IncidentField("id", "ID", "htmx/incidents/_incident_pk.html"),
}

EXTRA_FIELDS = {
    "location_tag": IncidentField("location", "Location", "htmx/incidents/_incident_tag.html",
                                  context=FieldContext(tag={"key": "location"})),
    "problem_type_tag": IncidentField("problem_type", "Problem Type", "htmx/incidents/_incident_tag.html",
                                      context=FieldContext(tag={"key": "problem_type"})),
    "any_ack": IncidentField("ack", "Ack", "htmx/incidents/_incident_ack.html"),
    "sd_ack": IncidentField("sd_ack", "SD Ack", "htmx/incidents/_incident_ack.html",
                            context=FieldContext(ack="sd")),
    "noc_ack": IncidentField("noc_ack", "NOC Ack", "htmx/incidents/_incident_ack.html",
                             context=FieldContext(ack="noc")),
}


class IncidentFields:

    def __init__(self):
        self.fields = list(DEFAULT_FIELDS.values())

    def get_fields(self):
        return self.fields

    def set_fields(self, fields: list[IncidentField]):
        self.fields = fields

    def get_merged_context(self):
        return {k: v for field in self.fields if field.context for k, v in
                (field.context.__dict__.items() if isinstance(field.context, FieldContext) else field.context.items())}

    def __str__(self):
        return self.fields.__str__()
