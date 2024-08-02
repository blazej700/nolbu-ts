from dataclasses import dataclass
from typing import List
import datetime

@dataclass
class WorkDayDto():
    date: datetime.date
    hours: int
    project_name: str
    task: List[str]
    is_free: bool
