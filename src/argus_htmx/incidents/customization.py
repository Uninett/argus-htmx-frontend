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
from typing import Optional, OrderedDict


@dataclass
class IncidentField:
    """Class for keeping track of columns in the incidents table."""

    name: str  # identifier
    label: str  # display value
    cell_template: str
    context: Optional[dict] = None


DEFAULT_FIELDS = OrderedDict[str, IncidentField]([
    ("row_select", IncidentField("checkbox", "Selected", "htmx/incidents/_incident_checkbox.html")),
    ("id", IncidentField("id", "ID", "htmx/incidents/_incident_pk.html")),
    ("start_time", IncidentField("start_time", "Timestamp", "htmx/incidents/_incident_start_time.html")),
    ("status", IncidentField("status", "Status", "htmx/incidents/_incident_status.html")),
    ("level", IncidentField("level", "Severity level", "htmx/incidents/_incident_level.html")),
    ("source", IncidentField("source", "Source", "htmx/incidents/_incident_source.html")),
    ("description", IncidentField("description", "Description", "htmx/incidents/_incident_description.html")),
    ("links", IncidentField("links", "Actions", None))
])


class IncidentFields:

    def __init__(self):
        self.fields = list(DEFAULT_FIELDS.values())

    def get_fields(self):
        return self.fields

    def set_fields(self, fields: list[IncidentField]):
        self.fields = fields

    def __str__(self):
        return self.fields.__str__()
