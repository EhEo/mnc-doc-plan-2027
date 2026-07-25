# 메타데이터로 HTML/Excel 데이터 사전을 생성 (한글 폰트 맑은 고딕)
from jinja2 import Environment, PackageLoader, select_autoescape
from openpyxl import Workbook
from openpyxl.styles import Font

from u9c_catalog.extractor import ExtractResult

_env = Environment(
    loader=PackageLoader("u9c_catalog", "templates"),
    autoescape=select_autoescape(["html"]),
)


def generate_html(result: ExtractResult, out_path: str) -> None:
    tmpl = _env.get_template("data_dictionary.html.j2")
    html = tmpl.render(tables=result.tables)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)


def generate_excel(result: ExtractResult, out_path: str) -> None:
    wb = Workbook()
    ws_obj = wb.active
    ws_obj.title = "Objects"
    ws_obj.append(["schema", "object", "type", "row_count", "is_auxiliary", "aux_reason"])
    for t in result.tables:
        ws_obj.append([t.schema, t.name, t.object_type, t.row_count,
                       "Y" if t.is_auxiliary else "N", t.auxiliary_reason or ""])

    ws_col = wb.create_sheet("Columns")
    ws_col.append(["schema", "object", "column", "type", "nullable", "pk", "is_system", "system_reason"])
    for t in result.tables:
        for c in t.columns:
            ws_col.append([t.schema, t.name, c.name, c.type_display or c.data_type,
                           "Y" if c.is_nullable else "N", "PK" if c.is_pk else "",
                           "Y" if c.is_system else "N", c.system_reason or ""])

    for ws in (ws_obj, ws_col):
        for cell in ws[1]:
            cell.font = Font(name="맑은 고딕", bold=True)

    wb.save(out_path)
