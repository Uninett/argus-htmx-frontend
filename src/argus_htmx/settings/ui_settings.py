from argus_htmx.incidents.customization import IncidentFields

from argus.site.settings import get_json_env
from argus_htmx.settings import validate_ui_setting

_ui_env = get_json_env("ARGUS_UI", {}, quiet=False)
UI = validate_ui_setting(_ui_env)
del _ui_env

# customize the displayed columns in the incident table
TABLE_FIELDS = IncidentFields()  # initialize with default fields
if UI and UI.table_fields:
    TABLE_FIELDS.set_fields(UI.table_fields)  # override table fields from JSON setting
