from typing import Optional, List

from argus_htmx.incidents.customization import IncidentField
from pydantic import BaseModel, RootModel


class AppUISetting(BaseModel):
    table_fields: Optional[List[IncidentField]] = None  # list of columns to display in the table


class DictUISetting(RootModel):
    root: AppUISetting
