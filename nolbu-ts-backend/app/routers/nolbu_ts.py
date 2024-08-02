from fastapi import APIRouter, Response
import urllib

from ..internal.excel_creator import ExcelCreator
from ..internal.month_data_creator import MonthDataCreator
from ..model.generate_excel_request import GenerateExcelRequest

router = APIRouter()

@router.post('/file', tags=["File"], responses = {200: {"content": {"application/octet-stream": {}}}}, response_class=Response)
async def generate_file(request: GenerateExcelRequest):

    mdc = MonthDataCreator()
    dt = mdc.compile_month_data(request.month, request.year, request.hours, request.project_name, request.username, [], request.task)

    ec = ExcelCreator(dt)
    excel_file = ec.compile_worksheet()

    months_polish=["styczeń", "luty", "marzec", "kwiecień", "maj", "czerwiec", "lipiec", "sierpień", "wrzesień", "październik", "listopad", "grudzień"]

    filename = f'{request.username.strip().lower().replace(" ", "_")}_TS_{months_polish[request.month-1]}_{request.year}.xlsx'
    
    encoded_filename=urllib.parse.quote_plus(filename, encoding='UTF-8')

    return Response(content=excel_file, media_type="application/octet-stream", headers={'content-disposition': f'attachment; filename="{encoded_filename}"*=UTF-8'}, status_code=200)