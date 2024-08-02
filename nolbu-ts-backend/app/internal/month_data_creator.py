from typing import List
import datetime
import calendar
import random
from ..model.work_sheet_dto import WorkSheetDto
from ..model.work_day_dto import WorkDayDto 
import json, dataclasses

class MonthDataCreator():

    def create_hour_mask(self, month: int, year: int, hours: int, additional_free_days: List, days_in_month: int):
        hour_mask = []

        for day in range(days_in_month):
            current_date = datetime.date(year, month, day+1)
            is_free = (current_date.weekday() == 5) or (current_date.weekday() == 6) or (day in additional_free_days)
            if is_free:
                hour_mask.append(-1)
            else:
                hour_mask.append(0)

        return hour_mask


    def distribute_hours(self, hours: int, hour_mask: List, days_in_month: int):
        number_of_chunks = int(hours / 4)
        rest = hours % 4
        shift = 0

        for i in range(number_of_chunks):
            while hour_mask[(i+shift)%(days_in_month-1)] < 0:
                shift += 1
            hour_mask[(i+shift)%(days_in_month-1)] += 4 
        
        shortest_workday_index = -1
        shortest_hours = float('inf')
        for i in range(days_in_month):
            if 0 < hour_mask[i] < shortest_hours:
                shortest_hours = hour_mask[i]
                shortest_workday_index = i

        if shortest_workday_index != -1:
            hour_mask[shortest_workday_index] += rest


    def get_random_task(self, pre_pre_task, pre_task, possible_tasks, len_pos_tasks):
        number_set = [*range(0, len_pos_tasks)]
        if pre_task in number_set: number_set.remove(pre_task)
        if pre_pre_task in number_set: number_set.remove(pre_pre_task)
        rnd = random.choice(number_set)
        return pre_task, rnd, possible_tasks[rnd]


    def distribute_tasks(self, hour_mask, possible_tasks):
        len_pos_tasks = len(possible_tasks)
        tasks = []
        pre_task=-1
        pre_pre_task=-1
        for hour in hour_mask:
            if hour > 4:
                pre_pre_task, pre_task, task_first_part = self.get_random_task(pre_pre_task, pre_task, possible_tasks, len_pos_tasks)
                pre_pre_task, pre_task, task_second_part = self.get_random_task(pre_pre_task, pre_task, possible_tasks, len_pos_tasks)
                tasks.append([task_first_part, task_second_part])
            elif hour > 0:
                pre_pre_task, pre_task, task = self.get_random_task(pre_pre_task, pre_task, possible_tasks, len_pos_tasks)
                tasks.append([task])
            else:
                tasks.append([])

        return tasks


    def compile_month_data(self, month: int, year: int, hours: int, project: str, name: str, additional_free_days: List, possible_tasks: List):
        start_date = datetime.date(year, month, 1)
        _, days_in_month = calendar.monthrange(year, month)
        end_date = datetime.date(year, month, days_in_month)

        hour_mask = self.create_hour_mask(month, year, hours, additional_free_days, days_in_month)
        self.distribute_hours(hours, hour_mask, days_in_month)

        work_sheet = WorkSheetDto(date_from=start_date, date_to=end_date, month_hours=hours, work_days=[], name=name)
        work_day_list = []

        tasks = self.distribute_tasks(hour_mask, possible_tasks)

        for day in range(1, days_in_month+1):
            current_date = datetime.date(year, month, day)

            work_day_list.append(WorkDayDto(
                current_date,
                hour_mask[day-1] if hour_mask[day-1] > 0 else 0,
                project,
                tasks[day-1],
                hour_mask[day-1] < 0))
            
            if hour_mask[day-1] > 0:
                work_sheet.number_of_work_days += 1
        
        work_sheet.work_days = work_day_list
        return work_sheet

