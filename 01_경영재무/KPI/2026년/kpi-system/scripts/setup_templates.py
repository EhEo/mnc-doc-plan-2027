# KPI 시스템 Excel 템플릿 생성 스크립트
# -*- coding: utf-8 -*-

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

BASE = Path(__file__).parent.parent
TEMPLATES = BASE / "templates"
TEMPLATES.mkdir(parents=True, exist_ok=True)

HEAD_FILL = PatternFill("solid", fgColor="1F4E79")
HEAD_FONT = Font(name="맑은 고딕", bold=True, color="FFFFFF", size=11)
BODY_FONT = Font(name="맑은 고딕", size=10)
BOLD_FONT = Font(name="맑은 고딕", bold=True, size=10)
ALT_FILL  = PatternFill("solid", fgColor="EBF3FB")
BDR = Border(
    left=Side(style="thin"), right=Side(style="thin"),
    top=Side(style="thin"),  bottom=Side(style="thin")
)
CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True)
WRAP   = Alignment(vertical="center", wrap_text=True)

def hcell(ws, row, col, val, width=None):
    c = ws.cell(row, col, val)
    c.font, c.fill, c.alignment, c.border = HEAD_FONT, HEAD_FILL, CENTER, BDR
    if width:
        ws.column_dimensions[c.column_letter].width = width
    return c

def bcell(ws, row, col, val="", alt=False):
    c = ws.cell(row, col, val)
    c.font = BODY_FONT
    c.fill = ALT_FILL if alt else PatternFill("solid", fgColor="FFFFFF")
    c.alignment = WRAP
    c.border = BDR
    return c

# ── 템플릿 1: KPI 수립서 ─────────────────────────────────────
def create_kpi_template():
    wb = Workbook()

    # ── 시트 1: KPI목록 ──
    ws = wb.active
    assert ws is not None
    ws.title = "KPI목록"
    ws.row_dimensions[1].height = 32

    ws.merge_cells("A1:J1")
    t = ws["A1"]
    t.value = "M&C Electronics Vina — KPI 수립서"
    t.font  = Font(name="맑은 고딕", bold=True, size=14, color="1F4E79")
    t.alignment = CENTER

    # 메타 행
    for lbl, col in [("부문명", 1), ("작성자", 4), ("작성일", 7), ("버전", 10)]:
        c = ws.cell(2, col, lbl)
        c.font = Font(name="맑은 고딕", bold=True, size=10)
        c.fill = PatternFill("solid", fgColor="D6E4F0")

    # 헤더
    hdrs = [("KPI_ID",10),("분류",12),("KPI명",28),("목표치",10),("단위",8),
            ("가중치(%)",11),("측정방법",36),("담당자",12),("기한",12),("비고",18)]
    for c, (h, w) in enumerate(hdrs, 1):
        hcell(ws, 3, c, h, w)
    ws.row_dimensions[3].height = 25

    # 샘플 2행 + 빈 6행
    samples = [
        ["MGT-001","인사","교육이수율",95,"%",15,"교육이수자/대상자×100","인사총무팀","2026-12-31",""],
        ["MGT-002","구매","납기준수율",95,"%",15,"납기준수건/전체발주건×100","구매팀","2026-12-31",""],
    ]
    for r, row in enumerate(samples + [[]]*6, 4):
        alt = r % 2 == 0
        for c in range(1, 11):
            bcell(ws, r, c, row[c-1] if c <= len(row) else "", alt)

    # 합계
    ws.cell(12, 1, "합계").font = BOLD_FONT
    ws.cell(12, 6, "=SUM(F4:F11)").font = BOLD_FONT
    ws.cell(12, 6).fill = PatternFill("solid", fgColor="FFF2CC")
    for c in range(1, 11):
        ws.cell(12, c).border = BDR

    ws.freeze_panes = "A4"

    # ── 시트 2: 실행계획 ──
    ws2 = wb.create_sheet("실행계획")
    ws2.merge_cells("A1:H1")
    t2 = ws2["A1"]
    t2.value = "KPI 실행계획 (분기별 마일스톤)"
    t2.font  = Font(name="맑은 고딕", bold=True, size=13, color="1F4E79")
    t2.alignment = CENTER

    plan_hdrs = [("KPI_ID",10),("KPI명",28),("Q3목표\n(7~9월)",14),
                 ("Q3 실행과제",32),("Q4목표\n(10~12월)",14),
                 ("Q4 실행과제",32),("담당자",12),("비고",16)]
    for c, (h, w) in enumerate(plan_hdrs, 1):
        hcell(ws2, 2, c, h, w)
    ws2.row_dimensions[2].height = 36
    for r in range(3, 11):
        for c in range(1, 9):
            bcell(ws2, r, c, "", r % 2 == 0)
        ws2.row_dimensions[r].height = 42

    # ── 시트 3: 작성가이드 ──
    ws3 = wb.create_sheet("작성가이드")
    ws3.column_dimensions["A"].width = 72
    guide = [
        ("KPI 수립서 작성 가이드", True, 14),
        ("", False, 10),
        ("■ SMART 기준", True, 12),
        ("  S(Specific)  : 구체적 목표 — 예) 불량률 0.5% 이하 (×: 품질 향상)", False, 10),
        ("  M(Measurable): 측정 가능 — 수식·데이터 출처 명확히", False, 10),
        ("  A(Achievable): 달성 가능 — 전년 실적 기준 현실적 수치", False, 10),
        ("  R(Relevant)  : 회사 목표 연결 — AS9100D·매출·원가 연계", False, 10),
        ("  T(Time-bound): 기한 명확 — YYYY-MM-DD 형식", False, 10),
        ("", False, 10),
        ("■ KPI_ID 접두사 규칙", True, 12),
        ("  관리부문: MGT-001 …  /  생산1: PR1-001 …  /  생산2: PR2-001 …", False, 10),
        ("  품질부문: QUA-001 …  /  개발영업: SLS-001 …", False, 10),
        ("", False, 10),
        ("■ 가중치 합계 반드시 100% (F12 셀 자동 확인)", True, 11),
        ("■ KPI 항목 수: 5~8개 권장 (최대 8개, 10개 초과 금지)", True, 11),
        ("■ 완성 후 경영지원팀 제출 (기한: 6/28)", True, 11),
    ]
    for r, (txt, bold, sz) in enumerate(guide, 1):
        c = ws3.cell(r, 1, txt)
        c.font = Font(name="맑은 고딕", bold=bold, size=sz)

    out = TEMPLATES / "KPI_수립서_TEMPLATE.xlsx"
    wb.save(out)
    print(f"[OK] 저장: {out}  ({out.stat().st_size:,} bytes)")


# ── 템플릿 2: 월간실적 ────────────────────────────────────────
def create_monthly_template():
    wb = Workbook()
    ws = wb.active
    assert ws is not None
    ws.title = "월간실적"
    ws.row_dimensions[1].height = 32

    ws.merge_cells("A1:J1")
    t = ws["A1"]
    t.value = "M&C Electronics Vina — 월간 KPI 실적 보고"
    t.font  = Font(name="맑은 고딕", bold=True, size=14, color="1F4E79")
    t.alignment = CENTER

    for lbl, col in [("부문명",1),("보고월",3),("작성자",5),("작성일",7)]:
        c = ws.cell(2, col, lbl)
        c.font = Font(name="맑은 고딕", bold=True, size=10)
        c.fill = PatternFill("solid", fgColor="D6E4F0")

    hdrs = [("KPI_ID",10),("KPI명",28),("단위",8),("연간목표",10),
            ("월목표",10),("실적",10),("달성률(%)",13),("전월대비",13),
            ("이슈/원인",30),("개선계획",30)]
    for c, (h, w) in enumerate(hdrs, 1):
        hcell(ws, 3, c, h, w)
    ws.row_dimensions[3].height = 25

    for r in range(4, 12):
        alt = r % 2 == 0
        for c in range(1, 11):
            bcell(ws, r, c, "", alt)
        ws.cell(r, 7, f"=IF(E{r}=0,\"\",F{r}/E{r})").number_format = "0.0%"
        ws.cell(r, 7).font = BODY_FONT
        ws.cell(r, 7).border = BDR

    ws.freeze_panes = "A4"

    out = TEMPLATES / "월간실적_TEMPLATE.xlsx"
    wb.save(out)
    print(f"[OK] 저장: {out}  ({out.stat().st_size:,} bytes)")


if __name__ == "__main__":
    create_kpi_template()
    create_monthly_template()
    print("[SUCCESS] 템플릿 2종 생성 완료.")
