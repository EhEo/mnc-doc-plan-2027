# 2027년도 사업계획 경영 요약 보고서 xlsx 생성 스크립트
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from openpyxl import Workbook
from openpyxl.styles import (
    Font, PatternFill, Alignment, Border, Side, numbers
)
from openpyxl.utils import get_column_letter

OUT = '../reports/2027년도_사업계획_경영요약.xlsx'
FONT = '맑은 고딕'

# ─── 스타일 정의 ─────────────────────────────────────────────
def hdr_font(sz=11, bold=True, color='FFFFFF'):
    return Font(name=FONT, size=sz, bold=bold, color=color)

def body_font(sz=10, bold=False, color='000000'):
    return Font(name=FONT, size=sz, bold=bold, color=color)

def fill(hex_color):
    return PatternFill('solid', fgColor=hex_color)

def wrap_align(h='left', v='center'):
    return Alignment(horizontal=h, vertical=v, wrap_text=True)

THIN = Side(style='thin', color='CCCCCC')
THICK = Side(style='medium', color='888888')

def thin_border():
    return Border(left=THIN, right=THIN, top=THIN, bottom=THIN)

def section_border():
    return Border(left=THICK, right=THICK, top=THICK, bottom=THICK)

# 색상 팔레트
C_DARK_BLUE  = '1F3864'   # 헤더 배경
C_MID_BLUE   = '2F5597'   # 소제목
C_LIGHT_BLUE = 'D9E1F2'   # 짝수 행
C_GREEN      = '375623'   # 긍정 지표
C_RED        = 'C00000'   # 위험 지표
C_YELLOW     = 'FFC000'   # 주의

wb = Workbook()

# ════════════════════════════════════════════════════════════════
# Sheet 1: 경영 요약
# ════════════════════════════════════════════════════════════════
ws1 = wb.active
ws1.title = '경영 요약'

def write(ws, row, col, value, font=None, fill_=None, align=None, border=None, num_fmt=None):
    c = ws.cell(row=row, column=col, value=value)
    if font:   c.font = font
    if fill_:  c.fill = fill_
    if align:  c.alignment = align
    if border: c.border = border
    if num_fmt: c.number_format = num_fmt
    return c

def section_title(ws, row, col, text, span_end_col):
    ws.merge_cells(start_row=row, start_column=col, end_row=row, end_column=span_end_col)
    c = write(ws, row, col, text,
              font=Font(name=FONT, size=12, bold=True, color='FFFFFF'),
              fill_=fill(C_DARK_BLUE),
              align=wrap_align('left'))
    ws.row_dimensions[row].height = 20
    return c

def sub_header(ws, row, col, text, span_end_col=None):
    if span_end_col:
        ws.merge_cells(start_row=row, start_column=col, end_row=row, end_column=span_end_col)
    c = write(ws, row, col, text,
              font=Font(name=FONT, size=10, bold=True, color='FFFFFF'),
              fill_=fill(C_MID_BLUE),
              align=wrap_align('left'))
    ws.row_dimensions[row].height = 16
    return c

# 컬럼 너비
ws1.column_dimensions['A'].width = 32
ws1.column_dimensions['B'].width = 18
ws1.column_dimensions['C'].width = 12
ws1.column_dimensions['D'].width = 12
ws1.column_dimensions['E'].width = 20

row = 1
# 타이틀
ws1.merge_cells('A1:E1')
write(ws1, 1, 1, 'M&C Electronics Vietnam — 2027년도 사업계획 경영 요약',
      font=Font(name=FONT, size=14, bold=True, color='FFFFFF'),
      fill_=fill(C_DARK_BLUE),
      align=wrap_align('center'))
ws1.row_dimensions[1].height = 28

ws1.merge_cells('A2:E2')
write(ws1, 2, 1, '보고 기준일: 2026-06-15  |  Rev. 1  |  단위: USD',
      font=body_font(sz=9, color='666666'),
      align=wrap_align('center'))
ws1.row_dimensions[2].height = 14

row = 4
# ── 1. 목표 개요 ──────────────────────────────────────────────
section_title(ws1, row, 1, '1. 2027년 목표 개요', 5); row += 1
headers = ['지표', '목표']
for i, h in enumerate(headers):
    sub_header(ws1, row, i+1, h)
row += 1

targets = [
    ('매출 (Sales)',              43977859, '#,##0'),
    ('영업이익 (Operating Income)', 11343869, '#,##0'),
    ('경상이익 (Ordinary Profit)',  10148413, '#,##0'),
    ('순이익 (Net Income)',         8624307,  '#,##0'),
    ('EBITDA',                    12450762, '#,##0'),
]
margins = {
    '매출 (Sales)': '100.0%',
    '영업이익 (Operating Income)': '25.8%',
    '경상이익 (Ordinary Profit)': '23.1%',
    '순이익 (Net Income)': '19.6%',
    'EBITDA': '28.3%',
}
for i, (label, val, fmt) in enumerate(targets):
    bg = C_LIGHT_BLUE if i % 2 == 0 else 'FFFFFF'
    write(ws1, row, 1, label, font=body_font(), fill_=fill(bg),
          align=wrap_align(), border=thin_border())
    write(ws1, row, 2, val, font=body_font(), fill_=fill(bg),
          align=wrap_align('right'), border=thin_border(), num_fmt='$#,##0')
    ws1.merge_cells(start_row=row, start_column=3, end_row=row, end_column=5)
    write(ws1, row, 3, margins.get(label, ''), font=body_font(color='444444'),
          fill_=fill(bg), align=wrap_align('center'), border=thin_border())
    row += 1

# 총인원
bg = C_LIGHT_BLUE
write(ws1, row, 1, '총인원 (Grand Total)', font=body_font(), fill_=fill(bg),
      align=wrap_align(), border=thin_border())
ws1.merge_cells(start_row=row, start_column=2, end_row=row, end_column=5)
write(ws1, row, 2, '749명', font=body_font(bold=True), fill_=fill(bg),
      align=wrap_align('center'), border=thin_border())
row += 2

# ── 2. 손익계산서 핵심 지표 ───────────────────────────────────
section_title(ws1, row, 1, '2. 손익계산서 핵심 지표 (IS P열 — Rev19)', 5); row += 1
for h, col in [('항목', 1), ('금액 (USD)', 2), ('매출 대비', 3)]:
    sub_header(ws1, row, col, h)
row += 1

is_rows = [
    ('매출 (Sales)',           43977859, '100.0%', False, False),
    ('매출원가 (COGS)',         26197488, '59.6%',  False, False),
    ('매출총이익 (Gross Profit)',17780370, '40.4%',  True,  False),
    ('판관비 (SG&A)',           6436501,  '14.6%',  False, False),
    ('영업이익 (Op. Income)',   11343869, '25.8%',  True,  False),
    ('이자비용 (Interest)',      863642,   '2.0%',   False, False),
    ('경상이익 (Ordinary Profit)',10148413,'23.1%',  True,  False),
    ('법인세 (Tax)',             1524105,  '3.5%',   False, False),
    ('순이익 (Net Income)',      8624307,  '19.6%',  True,  True),
    ('EBITDA',                 12450762, '28.3%',  True,  True),
]
for i, (label, val, pct, is_sub, is_key) in enumerate(is_rows):
    bg = C_LIGHT_BLUE if i % 2 == 0 else 'FFFFFF'
    bold = is_sub or is_key
    color = '000000'
    write(ws1, row, 1, label, font=Font(name=FONT, size=10, bold=bold, color=color),
          fill_=fill(bg), align=wrap_align(), border=thin_border())
    write(ws1, row, 2, val,   font=Font(name=FONT, size=10, bold=bold, color=color),
          fill_=fill(bg), align=wrap_align('right'), border=thin_border(), num_fmt='$#,##0')
    ws1.merge_cells(start_row=row, start_column=3, end_row=row, end_column=5)
    pct_color = C_GREEN if (is_sub and float(pct.strip('%')) > 20) else '444444'
    write(ws1, row, 3, pct,   font=Font(name=FONT, size=10, bold=bold, color=pct_color),
          fill_=fill(bg), align=wrap_align('center'), border=thin_border())
    row += 1
row += 1

# ── 3. 고객사별 계획 ──────────────────────────────────────────
section_title(ws1, row, 1, '3. 고객사별 사업 계획 요약', 5); row += 1
for h, col in [('고객사', 1), ('상태', 2), ('주요 내용', 3), ('리스크', 5)]:
    sub_header(ws1, row, col, h, span_end_col=4 if col == 3 else None)
row += 1

customers = [
    ('삼성 Bracket', '성장',    '26.10월 15대 가동, 계획상 최대 230만대/월. AI 디바이스 교체로 출하량 증가',      '양산 안정화 불량률'),
    ('삼성 CNC',    '확대',    'LGIT+Mando 종료 설비 이관. 추가 비용 없이 생산능력 확대',                      '이관 가동률 저하'),
    ('Qualcomm',   '유지·확대','기존 양산 안정화 + 신규 수주 지속',                                         '신규 수주 지연'),
    ('LGIT',       '감소',    '납품처 YT→MX 변경. 단계적 철수',                                           '잔여 수량 조기 종료'),
    ('Mando',      '종료',    '3/16 거래 종료 통보 예정. 최종 수량 협의 필요',                               '매출 공백 리스크'),
    ('ZF',         '유지',    '2026 Forecast 반영. ADAS 외 견적 수주 지속',                               '발주 하락 가능'),
    ('A사',        '신규',    '2026 하반기 LRIP 예정. 시제품 평가 완료(2026.3)',                            'LRIP 일정 지연'),
]
STATUS_COLOR = {
    '성장': 'E2EFDA', '확대': 'E2EFDA', '유지': 'FFF2CC', '유지·확대': 'FFF2CC',
    '감소': 'FCE4D6', '종료': 'FCE4D6', '신규': 'DDEBF7',
}
for i, (cust, status, content, risk) in enumerate(customers):
    bg = 'FFFFFF' if i % 2 else C_LIGHT_BLUE
    s_bg = STATUS_COLOR.get(status, 'FFFFFF')
    write(ws1, row, 1, cust,    font=body_font(bold=True), fill_=fill(bg),
          align=wrap_align(), border=thin_border())
    write(ws1, row, 2, status,  font=body_font(), fill_=fill(s_bg),
          align=wrap_align('center'), border=thin_border())
    ws1.merge_cells(start_row=row, start_column=3, end_row=row, end_column=4)
    write(ws1, row, 3, content, font=body_font(), fill_=fill(bg),
          align=Alignment(horizontal='left', vertical='center', wrap_text=True),
          border=thin_border())
    write(ws1, row, 5, risk,    font=body_font(color='C00000'), fill_=fill(bg),
          align=Alignment(horizontal='left', vertical='center', wrap_text=True),
          border=thin_border())
    ws1.row_dimensions[row].height = 28
    row += 1
row += 1

# ── 4. 핵심 위험 요소 ─────────────────────────────────────────
section_title(ws1, row, 1, '4. 핵심 위험 요소', 5); row += 1
risks = [
    'LGIT·Mando 매출 공백 미정량화 — 삼성 증산으로의 상쇄 가능성 검증 필요',
    '삼성 단일 의존도 심화 — 삼성 정책 변경 시 전사 영향',
    'A사 LRIP 지연 시 2027년 신규 매출 기여 없음',
    'MES 미집행 시 다품종 대량 생산 관리 한계',
    '1분기 현금 유출 집중 ($650K 연체채무 상환 Jan~Mar)',
]
for i, r in enumerate(risks):
    ws1.merge_cells(start_row=row, start_column=1, end_row=row, end_column=5)
    bg = 'FFF2CC' if i % 2 == 0 else 'FFFFFF'
    write(ws1, row, 1, f'⚠ {r}', font=body_font(color='7F3F00'), fill_=fill(bg),
          align=wrap_align(), border=thin_border())
    ws1.row_dimensions[row].height = 18
    row += 1
row += 1

# ── 5. 결정 필요 항목 ─────────────────────────────────────────
section_title(ws1, row, 1, '5. 즉시 결정이 필요한 항목', 5); row += 1
for h, col in [('항목', 1), ('내용', 2), ('기한', 5)]:
    sub_header(ws1, row, col, h, span_end_col=4 if col == 2 else None)
row += 1

decisions = [
    ('MES+서버 집행 여부', 'Bracket 다품종 관리 필수. 미집행 시 운영 리스크 임원 보고', '2026 Q3'),
    ('LGIT·Mando 공백 정량화', '3개 시나리오(Base/Down/Up) + 매출 브릿지 작성', '2026 Q3'),
    ('1분기 한도 대출 준비', '연체채무 상환 $650K + 예치금 집중 구간 대비', '2026 Q4 이전'),
    ('A사 LRIP 일정 확인', '지연 시 매출 목표 재조정 필요', '수시'),
]
for i, (item, content, deadline) in enumerate(decisions):
    bg = C_LIGHT_BLUE if i % 2 == 0 else 'FFFFFF'
    write(ws1, row, 1, item, font=body_font(bold=True), fill_=fill(bg),
          align=wrap_align(), border=thin_border())
    ws1.merge_cells(start_row=row, start_column=2, end_row=row, end_column=4)
    write(ws1, row, 2, content, font=body_font(), fill_=fill(bg),
          align=wrap_align(), border=thin_border())
    write(ws1, row, 5, deadline, font=body_font(color='C00000', bold=True),
          fill_=fill(bg), align=wrap_align('center'), border=thin_border())
    ws1.row_dimensions[row].height = 22
    row += 1

# ════════════════════════════════════════════════════════════════
# Sheet 2: 타당성 검토 요약
# ════════════════════════════════════════════════════════════════
ws2 = wb.create_sheet('타당성 검토 요약')
ws2.column_dimensions['A'].width = 22
ws2.column_dimensions['B'].width = 10
ws2.column_dimensions['C'].width = 38
ws2.column_dimensions['D'].width = 38

ws2.merge_cells('A1:D1')
write(ws2, 1, 1, '2027년도 사업계획 타당성 검토 요약',
      font=Font(name=FONT, size=14, bold=True, color='FFFFFF'),
      fill_=fill(C_DARK_BLUE), align=wrap_align('center'))
ws2.row_dimensions[1].height = 28

ws2.merge_cells('A2:D2')
write(ws2, 2, 1, '상세 분석: tasks/biz-plan-review/artifacts/타당성검토.md 참조',
      font=body_font(sz=9, color='666666'), align=wrap_align('center'))

row2 = 4
section_title(ws2, row2, 1, '항목별 종합 평가', 4); row2 += 1
for h, col in [('항목', 1), ('신뢰도', 2), ('긍정 요인', 3), ('우려 사항', 4)]:
    sub_header(ws2, row2, col, h)
row2 += 1

evaluations = [
    ('매출 목표',   '중',    '삼성 Bracket 확정 라인 가동\nCNC 설비 이관 확장',
     'LGIT/Mando 공백 미정량화\nA사 LRIP 일정 불확실'),
    ('원가 구조',   '중상',  'COGS 59.6% 업종 추정 합리적\n대량 생산 시 고정비 분산',
     '자동화 투자 미반영\n원자재 가격 변동 리스크'),
    ('인원 계획',   '중',    '497명 현 수준 유지 시 적합\n삼성 전용 103명 분리 운영',
     '증산 시 충원 계획 불명\nLGIT/Mando 재배치 미정'),
    ('투자 계획',   '중하',  '실행 투자 $1.24M — 매출 직결\n아연캐스팅 설비 즉시 효과',
     'MES $800K 보류 — 운영 리스크\n보류 총액 $2.87M 미결정'),
    ('현금흐름',    '중상',  'EBITDA $12.5M 충분한 여력\n삼성 AR 회수 개선 기대',
     '1분기 $650K 상환 집중\nAP/AR 불일치 구간 존재'),
]
CONF_COLOR = {'중상': 'E2EFDA', '중': 'FFF2CC', '중하': 'FCE4D6', '높음': 'E2EFDA'}
for i, (item, conf, pos, neg) in enumerate(evaluations):
    bg = C_LIGHT_BLUE if i % 2 == 0 else 'FFFFFF'
    c_bg = CONF_COLOR.get(conf, 'FFFFFF')
    write(ws2, row2, 1, item, font=body_font(bold=True), fill_=fill(bg),
          align=wrap_align(), border=thin_border())
    write(ws2, row2, 2, conf, font=body_font(), fill_=fill(c_bg),
          align=wrap_align('center'), border=thin_border())
    write(ws2, row2, 3, pos, font=body_font(color='375623'), fill_=fill(bg),
          align=Alignment(horizontal='left', vertical='center', wrap_text=True),
          border=thin_border())
    write(ws2, row2, 4, neg, font=body_font(color='C00000'), fill_=fill(bg),
          align=Alignment(horizontal='left', vertical='center', wrap_text=True),
          border=thin_border())
    ws2.row_dimensions[row2].height = 36
    row2 += 1

row2 += 1
section_title(ws2, row2, 1, '보완 권고사항 (우선순위 순)', 4); row2 += 1
recs = [
    ('1. LGIT·Mando 공백 정량화', 'Base/Down/Up 3개 시나리오 + 고객별 매출 브릿지 테이블'),
    ('2. MES 투자 결정',           'MES+서버($800K) — 2026 Q3 내 집행 여부 결정. 미집행 시 리스크 임원 보고'),
    ('3. 1분기 유동성 계획',       '월별 최저 현금잔고 시뮬레이션 + 한도 대출 필요액 산정'),
    ('4. A사 LRIP 일정 관리',     '고객사 일정 확인 + 지연 시 목표 재조정 시나리오 준비'),
    ('5. 삼성 의존도 분산',        'ZF·Qualcomm·A사 비삼성 비중 목표를 중장기 계획에 반영'),
]
for i, (rec, desc) in enumerate(recs):
    bg = C_LIGHT_BLUE if i % 2 == 0 else 'FFFFFF'
    write(ws2, row2, 1, rec, font=body_font(bold=True), fill_=fill(bg),
          align=wrap_align(), border=thin_border())
    ws2.merge_cells(start_row=row2, start_column=2, end_row=row2, end_column=4)
    write(ws2, row2, 2, desc, font=body_font(), fill_=fill(bg),
          align=wrap_align(), border=thin_border())
    ws2.row_dimensions[row2].height = 24
    row2 += 1

# ════════════════════════════════════════════════════════════════
# 저장
# ════════════════════════════════════════════════════════════════
wb.save(OUT)
print(f'저장 완료: {OUT}')

# 검증
from openpyxl import load_workbook
wb_v = load_workbook(OUT)
print(f'시트 수: {len(wb_v.sheetnames)} — {wb_v.sheetnames}')
ws_v = wb_v['경영 요약']
print(f'경영 요약 최대 행: {ws_v.max_row}')
ws_v2 = wb_v['타당성 검토 요약']
print(f'타당성 검토 최대 행: {ws_v2.max_row}')
print('한글 확인:', ws_v.cell(1, 1).value[:10])
print('검증 완료')
