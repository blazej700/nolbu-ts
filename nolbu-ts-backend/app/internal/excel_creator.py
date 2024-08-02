from typing import List
import xlsxwriter
import datetime
import calendar
from io import BytesIO
from ..model.work_sheet_dto import WorkSheetDto
from ..model.work_day_dto import WorkDayDto 
import json, dataclasses

from .month_data_creator import MonthDataCreator

class ExcelCreator():

    worksheet = None
    worksheet_data = None
    workbook = None
    output = None
    worksheet_kcp = None

    def __init__(self, work_sheet_data):
        self.output = BytesIO()
        self.workbook = xlsxwriter.Workbook(self.output)
        self.worksheet = self.workbook.add_worksheet("Arkusz1")
        self.worksheet_kcp = self.workbook.add_worksheet("KCP_USUNAC")
        self.worksheet_data = work_sheet_data


    def e_format(self, num_format='', bold=False, bg_color='', border=0, border_color='', align='', wrap=False, border_bottom=0, border_top=0, border_left=0, border_right=0):
        format_dict = {'font_size':8, 'font':'Arial', 'valign':'vcenter'}
        if num_format:
            format_dict['num_format'] = num_format
        if bold:
            format_dict['bold'] = 1
        if bg_color:
            format_dict['bg_color'] = bg_color
        if border > 0:
            format_dict['border'] = border
        if border_color:
            format_dict['border_color'] = border_color
        if align:
            format_dict['align'] = align
        if wrap:
            format_dict['text_wrap'] = True
        if border_bottom:
            format_dict['bottom'] = border_bottom
        if border_top:
            format_dict['top'] = border_top
        if border_left:
            format_dict['left'] = border_left
        if border_right:
            format_dict['right'] = border_right
        return self.workbook.add_format(format_dict)

    def create_upper_table(self):
        self.worksheet.write_string(1, 0, "Zestawienie czasu pracy i wykonanych zadań", self.e_format(bold=True, bg_color='#FCD8BA', border_color='#FF6600', border_left=2, border_top=2))
        self.worksheet.write_string(1, 1, "", self.e_format(bold=True, bg_color='#FCD8BA', border_color='#FF6600', border_top=2))
        self.worksheet.write_string(1, 2, "", self.e_format(bold=True, bg_color='#FCD8BA', border_color='#FF6600', border_top=2))
        self.worksheet.write_string(1, 3, "Osoba raportująca:", self.e_format(bold=True, bg_color='#FCD8BA', border_color='#FF6600', border_top=2, border_right=1))

        self.worksheet.merge_range(1, 4, 2, 5, self.worksheet_data.name, self.e_format(bold=True, border=2, border_color='#FF6600', align='Center'))

        self.worksheet.write_string(2, 0, "w okresie od:", self.e_format(bold=True, bg_color='#FCD8BA', border_color='#FF6600', border_bottom=2, border_left=2))
        self.worksheet.write_datetime(2, 1, self.worksheet_data.date_from, self.e_format(num_format='d.mm.yyyy', bold=True, border_color='#FF6600', border_bottom=2, align='left'))
        self.worksheet.write_string(2, 2, "do:", self.e_format(bold=True, bg_color='#FCD8BA', border_color='#FF6600', border_bottom=2, align='center'))
        self.worksheet.write_datetime(2, 3, self.worksheet_data.date_to, self.e_format(num_format='d.mm.yyyy', bold=True, border_color='#FF6600', border_bottom=2, border_right=1, align='left'))

    def create_main_table(self):
        self.worksheet.write_string(4, 0, "Data", self.e_format(bold=True, border=2, border_color='#FF6600', bg_color='#FCD8BA', wrap=True))
        self.worksheet.write_string(4, 1, "Liczba \n godzin", self.e_format(bold=True, border=2, border_color='#FF6600', bg_color='#FCD8BA', wrap=True))
        self.worksheet.write_string(4, 2, "Projekt/ Strumień", self.e_format(bold=True, border=2, border_color='#FF6600', bg_color='#FCD8BA', wrap=True))
        self.worksheet.merge_range(4, 3, 4, 5, "Realizowane zadanie", self.e_format(bold=True, border=2, border_color='#FF6600', bg_color='#FCD8BA', align='Center', wrap=True))

    def fill_main_table(self):
        for i in range(len(self.worksheet_data.work_days)):
            if not self.worksheet_data.work_days[i].is_free:
                self.worksheet.write(5+i, 0, self.worksheet_data.work_days[i].date, self.e_format(num_format='d.mm.yyyy', bold=True, border=2, border_color='#FF6600', wrap=True, align='center'))
                self.worksheet.write(5+i, 1, self.worksheet_data.work_days[i].hours if self.worksheet_data.work_days[i].hours > 0 else None, self.e_format(num_format='0.00', bold=True, border=2, border_color='#FF6600', wrap=True))
                self.worksheet.write(5+i, 2, self.worksheet_data.work_days[i].project_name if self.worksheet_data.work_days[i].hours >0 else None, self.e_format(bold=True, border=2, border_color='#FF6600', wrap=True))
                self.worksheet.merge_range(5+i, 3, 5+i, 5, ", ".join(self.worksheet_data.work_days[i].task) if self.worksheet_data.work_days[i].hours >0  else None, self.e_format(border=2, border_color='#FF6600', align='center', wrap=True))
            else:
                self.worksheet.write(5+i, 0, self.worksheet_data.work_days[i].date, self.e_format(num_format='d.mm.yyyy', bold=True, border=2, border_color='#FF6600', bg_color='#FCD8BA', wrap=True, align='center'))
                self.worksheet.write(5+i, 1, None, self.e_format(bg_color='#FCD8BA', border=2, border_color='#FF6600', wrap=True))
                self.worksheet.write(5+i, 2, None, self.e_format(bg_color='#FCD8BA', border=2, border_color='#FF6600', wrap=True))
                self.worksheet.merge_range(5+i, 3, 5+i, 5, None, self.e_format(bg_color='#FCD8BA', border=2, border_color='#FF6600', align='center', wrap=True))
    
    def create_total_time_section(self):
        self.worksheet.write(len(self.worksheet_data.work_days)+5, 0, "Razem godzin", self.e_format(bold=True, border=2, border_color='#FF6600', bg_color='#FCD8BA'))
        self.worksheet.write_formula(len(self.worksheet_data.work_days)+5, 1, f"=SUBTOTAL(9,B{6}:B{len(self.worksheet_data.work_days)+5})", self.e_format(num_format='0.00', border=2, border_color='#FF6600', align='center'), self.worksheet_data.month_hours)

    def create_kcp_data(self):
        r=0
        s=0
        for i in range(len(self.worksheet_data.work_days)):
            if not self.worksheet_data.work_days[i].is_free:
                number_of_tasks=len(self.worksheet_data.work_days[i].task) if len(self.worksheet_data.work_days[i].task) > 0 else 1
                subtask_number=0
                for singular_task in self.worksheet_data.work_days[i].task:
                    self.worksheet_kcp.write(i+r+s, 0, self.worksheet_data.work_days[i].date, self.e_format(num_format='yyyy-mm-dd'))
                    self.worksheet_kcp.write(i+r+s, 1, self.worksheet_data.work_days[i].hours*60/number_of_tasks if self.worksheet_data.work_days[i].hours > 0 else None, self.e_format(num_format='0'))
                    self.worksheet_kcp.write(i+r+s, 2, self.worksheet_data.work_days[i].project_name if self.worksheet_data.work_days[i].hours >0 else None, self.e_format())
                    self.worksheet_kcp.write(i+r+s, 3, singular_task if self.worksheet_data.work_days[i].hours > 0 else None, self.e_format())
                    if number_of_tasks > 1 and subtask_number<(number_of_tasks-1):
                        subtask_number=subtask_number+1
                        s=s+1
            else:
                r=r-1


    def compile_worksheet(self):
        self.create_upper_table()
        self.create_main_table()
        self.fill_main_table()
        self.create_total_time_section()
        self.create_kcp_data()
        self.workbook.close()
        return self.output.getvalue()

