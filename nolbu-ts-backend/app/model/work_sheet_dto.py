from dataclasses import dataclass
from typing import List
import datetime
from .work_day_dto import WorkDayDto 

@dataclass
class WorkSheetDto():
    date_from: datetime.date 
    date_to: datetime.date 
    work_days: List[WorkDayDto]
    month_hours: int
    name: str = ''
    number_of_work_days: int = 0
