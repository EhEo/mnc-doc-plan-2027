# Excel → JSON 변환 스크립트 테스트

import json, pytest, openpyxl
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "kpi-system" / "scripts"))
from excel_to_json import parse_kpi_excel, ExcelParseError

def make_test_xlsx(tmp_path, rows):
    wb = openpyxl.Workbook()
    ws = wb.active
    assert ws is not None
    ws.title = "KPI목록"
    ws["B2"] = "관리부문"
    headers = ["KPI_ID","분류","KPI명","목표치","단위","가중치(%)","측정방법","담당자","기한","비고"]
    for c, h in enumerate(headers, 1):
        ws.cell(3, c, h)
    for r_idx, row in enumerate(rows, 4):
        for c_idx, val in enumerate(row, 1):
            ws.cell(r_idx, c_idx, val)
    p = tmp_path / "test_kpi.xlsx"
    wb.save(p)
    return p

SAMPLE_ROWS = [
    ["MGT-001","인사","교육이수율",95,"%",20,"이수자/대상자×100","인사총무팀","2026-12-31",""],
    ["MGT-002","구매","납기준수율",95,"%",20,"준수건/전체건×100","구매팀","2026-12-31",""],
    ["MGT-003","공무","설비가동률",90,"%",20,"가동시간/총시간×100","공무팀","2026-12-31",""],
]

def test_parse_returns_dict(tmp_path):
    p = make_test_xlsx(tmp_path, SAMPLE_ROWS)
    result = parse_kpi_excel(p, year="2026", half="H2")
    assert isinstance(result, dict)
    assert result["dept"] == "관리부문"

def test_kpi_count(tmp_path):
    p = make_test_xlsx(tmp_path, SAMPLE_ROWS)
    result = parse_kpi_excel(p, year="2026", half="H2")
    assert len(result["kpis"]) == 3

def test_empty_rows_skipped(tmp_path):
    rows = SAMPLE_ROWS + [["","","","","","","","","",""]]
    p = make_test_xlsx(tmp_path, rows)
    result = parse_kpi_excel(p, year="2026", half="H2")
    assert len(result["kpis"]) == 3
