from dataclasses import dataclass
from typing import List
import datetime

@dataclass
class GenerateExcelRequest():
    username: str
    year: int
    month: int
    hours: int
    project_name: str
    task: List[str]
