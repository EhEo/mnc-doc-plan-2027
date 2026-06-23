# 2027년도 사업계획 경영요약 Rev2 xlsx 생성 스크립트
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from openpyxl import Workbook
from openpyxl.styles import (Font, PatternFill, Alignment, Border, Side,
                              numbers as num_fmt)
from openpyxl.utils import get_column_letter

OUTPUT = '../reports/2027년도_사업계획_경영요약_Rev2.xlsx'

# ── 색상 팔레트 ──────────────────────────────────────────
BLUE_HDR  = PatternFill('solid', fgColor='1F4E79')
BLUE_SUB  = PatternFill('solid', fgColor='2E75B6')
BLUE_LITE = PatternFill('solid', fgColor='D6E4F0')
RED_LITE  = PatternFill('solid', fgColor='FCE4D6')
GREEN_LITE= PatternFill('solid', fgColor='E2EFDA')
GRAY_LITE = PatternFill('solid', fgColor='F2F2F2')
YELLOW    = PatternFill('solid', fgColor='FFF2CC')
WHITE     = PatternFill('solid', fgColor='FFFFFF')

def thin_border():
    s = Side(border_style='thin', color='BFBFBF')
    return Border(left=s, right=s, top=s, bottom=s)

def hdr_font(sz=11, bold=True, color='FFFFFF'):
    return Font(name='맑은 고딕', size=sz, bold=bold, color=color)

def body_font(sz=10, bold=False, color='000000'):
    return Font(name='맑은 고딕', size=sz, bold=bold, color=color)

def center():
    return Alignment(horizontal='center', vertical='center', wrap_text=True)

def left():
    return Alignment(horizontal='left', vertical='center', wrap_text=True)

def right():
    return Alignment(horizontal='right', vertical='center')

def write_cell(ws, row, col, value, fill=None, font=None, align=None, border=True, fmt=None):
    c = ws.cell(row=row, column=col, value=value)
    if fill:  c.fill   = fill
    if font:  c.font   = font
    if align: c.alignment = align
    if border: c.border = thin_border()
    if fmt:   c.number_format = fmt
    return c

def merge_hdr(ws, row, c1, c2, value, fill=BLUE_HDR, font_sz=12):
    ws.merge_cells(start_row=row, start_column=c1, end_row=row, end_column=c2)
    c = ws.cell(row=row, column=c1, value=value)
    c.fill = fill; c.font = hdr_font(font_sz); c.alignment = center()
    c.border = thin_border()

wb = Workbook()

# ═══════════════════════════════════════════════════════
# 시트 1: 경영 요약
# ═══════════════════════════════════════════════════════
ws1 = wb.active
ws1.title = '경영 요약'
ws1.sheet_view.showGridLines = False

# 열 너비
col_widths = [2, 18, 14, 14, 14, 16, 18, 2]
for i, w in enumerate(col_widths, 1):
    ws1.column_dimensions[get_column_letter(i)].width = w

# 제목
ws1.row_dimensions[1].height = 10
ws1.row_dimensions[2].height = 36
ws1.merge_cells('B2:G2')
c = ws1.cell(row=2, column=2,
             value='2027년도 사업계획 경영 요약  (Rev2, 기준일: 2026-06-15)')
c.font = Font(name='맑은 고딕', size=16, bold=True, color='1F4E79')
c.alignment = center()

# ── 섹션 A: 손익 지표 ─────────────────────────────────
ws1.row_dimensions[4].height = 20
merge_hdr(ws1, 4, 2, 7, 'I. 2027년도 손익 목표 (IS 기준)')

headers_is = ['항목', 'Rev2 계획', 'Rev19 (이전)', '증감액', '증감율', '비고']
for j, h in enumerate(headers_is, 2):
    write_cell(ws1, 5, j, h, fill=BLUE_SUB, font=hdr_font(10),
               align=center())
ws1.row_dimensions[5].height = 18

is_data = [
    ('매출',          50065917, 43970000, None, None, ''),
    ('COGS',          35420898, 26220000, None, None, '⚠ 70.75% — H1 85.7% 최고'),
    ('매출총이익(GP)', 14645019, 17750000, None, None, ''),
    ('GP율',          0.2925,   0.404,    None, None, ''),
    ('SG&A',          4489948,  6440000,  None, None, '✅ 인원절감 효과'),
    ('영업이익',      10155071, 11310000, None, None, ''),
    ('영업이익율',    0.2028,   0.257,    None, None, ''),
    ('순이익',        7256695,  8600000,  None, None, ''),
    ('EBITDA',        14264028, None,     None, None, ''),
]

for i, (lbl, rev2, rev19, _, __, note) in enumerate(is_data):
    r = 6 + i
    ws1.row_dimensions[r].height = 16
    is_pct = lbl in ('GP율', '영업이익율')
    delta = (rev2 - rev19) if (rev2 and rev19) else None
    delta_pct = (delta / rev19) if (delta and rev19) else None

    fill_row = RED_LITE if (delta and delta < 0 and not is_pct) else \
               GREEN_LITE if (delta and delta > 0 and not is_pct) else WHITE

    write_cell(ws1, r, 2, lbl,   fill=GRAY_LITE, font=body_font(10, True), align=left())
    if is_pct:
        write_cell(ws1, r, 3, rev2,  fill=fill_row, font=body_font(), align=right(), fmt='0.00%')
        write_cell(ws1, r, 4, rev19 if rev19 else '', fill=fill_row, font=body_font(), align=right(), fmt='0.00%')
        d_val = (rev2 - rev19) if rev19 else ''
        write_cell(ws1, r, 5, d_val if d_val != '' else '', fill=fill_row,
                   font=body_font(), align=right(), fmt='+0.00%;-0.00%')
    else:
        write_cell(ws1, r, 3, rev2,  fill=fill_row, font=body_font(), align=right(), fmt='#,##0')
        write_cell(ws1, r, 4, rev19 if rev19 else '', fill=fill_row, font=body_font(), align=right(), fmt='#,##0')
        write_cell(ws1, r, 5, delta if delta else '', fill=fill_row,
                   font=body_font(), align=right(), fmt='+#,##0;-#,##0')

    write_cell(ws1, r, 6, delta_pct if (delta_pct and not is_pct) else '',
               fill=fill_row, font=body_font(), align=right(), fmt='+0.0%;-0.0%')
    write_cell(ws1, r, 7, note, fill=fill_row, font=body_font(9), align=left())

# ── 섹션 B: 고객사별 매출 ─────────────────────────────
r_start = 6 + len(is_data) + 2
merge_hdr(ws1, r_start, 2, 7, 'II. 고객사별 매출 구성 (S Plan 기준)')
ws1.row_dimensions[r_start].height = 20

cust_hdr = ['고객사', '주요 제품', '금액 (USD)', '비율', '', '비고']
r_start += 1
for j, h in enumerate(cust_hdr, 2):
    write_cell(ws1, r_start, j, h, fill=BLUE_SUB, font=hdr_font(10), align=center())
ws1.row_dimensions[r_start].height = 18

cust_data = [
    ('Samsung Bracket',  'A17~A38, Galaxy Tap',           19938149, 0.3983, '', ''),
    ('Samsung CNC',      'CNC 부품 (A시리즈)',              6314820,  0.1261, '', ''),
    ('ZF TRW',           'FCA/GM Housing·Cover·Lens',      8516702,  0.1701, '', ''),
    ('Mando',            'NX4/IMEB2/JK Housing·Cover',     7313286,  0.1461, '', '⚠ #REF! 항목 포함'),
    ('Samsung Camera ZN','Camera Bracket ZN',               2708558,  0.0541, '', ''),
    ('신규 고객 A',       '고부가가치 부품 ($20K/unit)',     1404000,  0.0280, '', '양산 일정 미확정'),
    ('신규 고객 B',       '—',                              1262964,  0.0252, '', ''),
    ('Qualcomm',         'MTP+IDP+ADP 외',                 1014591,  0.0203, '', ''),
    ('LGIT',             'DCU15/MPC5.5 Housing·Cover',     845248,   0.0169, '', ''),
    ('A사(ZF계열)',       'Glass Frame ZF60A 외',            747600,   0.0149, '', ''),
    ('합계',             '',                                50065917, 1.0,    '', ''),
]

for i, (cust, prod, amt, pct, _, note) in enumerate(cust_data):
    r = r_start + 1 + i
    ws1.row_dimensions[r].height = 16
    is_total = cust == '합계'
    f = BLUE_LITE if is_total else (YELLOW if '신규' in cust else WHITE)
    bf = body_font(10, True) if is_total else body_font()
    write_cell(ws1, r, 2, cust, fill=f, font=bf, align=left())
    write_cell(ws1, r, 3, prod, fill=f, font=body_font(9), align=left())
    write_cell(ws1, r, 4, amt,  fill=f, font=bf, align=right(), fmt='#,##0')
    write_cell(ws1, r, 5, pct,  fill=f, font=bf, align=right(), fmt='0.0%')
    write_cell(ws1, r, 6, '',   fill=f, font=body_font(), align=center())
    write_cell(ws1, r, 7, note, fill=f, font=body_font(9), align=left())

# ── 섹션 C: 인원 절감 ─────────────────────────────────
r_start = r_start + 1 + len(cust_data) + 1
merge_hdr(ws1, r_start, 2, 7, 'III. 인원 절감 현황 (2027년)')
ws1.row_dimensions[r_start].height = 20

r_start += 1
hc_hdr = ['구분', '2027 기초(Jan)', '2027 기말(Dec)', '증감', '증감율', '비고']
for j, h in enumerate(hc_hdr, 2):
    write_cell(ws1, r_start, j, h, fill=BLUE_SUB, font=hdr_font(10), align=center())

hc_data = [
    ('외국인 (Korean Expat)', 15,  16,  +1,  +0.067, ''),
    ('베트남 직원',            237, 219, -18, -0.076, ''),
    ('생산직 근로자',          497, 418, -79, -0.159, ''),
    ('합계',                   749, 653, -96, -0.128, ''),
]

for i, (lbl, start, end, chg, chg_pct, note) in enumerate(hc_data):
    r = r_start + 1 + i
    ws1.row_dimensions[r].height = 16
    is_total = lbl == '합계'
    f = BLUE_LITE if is_total else (GREEN_LITE if chg < 0 else WHITE)
    bf = body_font(10, True) if is_total else body_font()
    write_cell(ws1, r, 2, lbl,      fill=f, font=bf, align=left())
    write_cell(ws1, r, 3, start,    fill=f, font=bf, align=right(), fmt='#,##0')
    write_cell(ws1, r, 4, end,      fill=f, font=bf, align=right(), fmt='#,##0')
    write_cell(ws1, r, 5, chg,      fill=f, font=bf, align=right(), fmt='+#,##0;-#,##0')
    write_cell(ws1, r, 6, chg_pct,  fill=f, font=bf, align=right(), fmt='+0.0%;-0.0%')
    write_cell(ws1, r, 7, note,     fill=f, font=body_font(9), align=left())

# ── 섹션 D: 결정 필요 항목 ────────────────────────────
r_start = r_start + 1 + len(hc_data) + 1
merge_hdr(ws1, r_start, 2, 7, 'IV. 결정 필요 항목 (Action Required)')
ws1.row_dimensions[r_start].height = 20

r_start += 1
act_hdr = ['우선순위', '항목', '내용', '영향', '기한', '담당']
for j, h in enumerate(act_hdr, 2):
    write_cell(ws1, r_start, j, h, fill=BLUE_SUB, font=hdr_font(10), align=center())

act_data = [
    ('1 (최우선)', 'Samsung SOP 물량 확정',        'A18 12.3M units, A38 3.8M units PO 확보',       '매출 ±$7~10M',  '긴급',  'EM팀'),
    ('2',         'COGS 구조 개선',                'H1 COGS% 85.7% 원인 파악 (원가 분해)',           'GP율 개선',      '2026 Q3','재무·생산'),
    ('3',         '자동화 투자 일정 확정',          'CNC(1×3·1×2), 검사·사상 자동화 완료 시점',      '인원절감 전제', '2026 Q3','생산팀'),
    ('4',         'Mando #REF! 오류 수정',          'NX4/IMEB2/JK 계약 재확인, 금액 확정',           '$7.3M 신뢰성',  '긴급',  'EM팀'),
    ('5',         'CNC 단가 $1.23 협상 완료',       'Samsung 단가 승인 이메일·견적서 확보',           '매출 ±$461K',   '2026 Q3','EM팀'),
]

for i, row_data in enumerate(act_data):
    r = r_start + 1 + i
    ws1.row_dimensions[r].height = 22
    fills = [RED_LITE, WHITE, YELLOW, WHITE, WHITE]
    f = fills[i]
    for j, val in enumerate(row_data, 2):
        write_cell(ws1, r, j, val, fill=f,
                   font=body_font(10, i==0), align=left())

# ═══════════════════════════════════════════════════════
# 시트 2: 타당성 검토 요약
# ═══════════════════════════════════════════════════════
ws2 = wb.create_sheet('타당성 검토 요약')
ws2.sheet_view.showGridLines = False

col_widths2 = [2, 18, 22, 16, 16, 18, 2]
for i, w in enumerate(col_widths2, 1):
    ws2.column_dimensions[get_column_letter(i)].width = w

ws2.row_dimensions[1].height = 10
ws2.row_dimensions[2].height = 36
ws2.merge_cells('B2:F2')
c2 = ws2.cell(row=2, column=2,
              value='2027년도 사업계획 타당성 검토 요약  (Rev2)')
c2.font = Font(name='맑은 고딕', size=16, bold=True, color='1F4E79')
c2.alignment = center()

# ── COGS 월별 ─────────────────────────────────────────
merge_hdr(ws2, 4, 2, 6, 'I. COGS% 월별 추이 — 수익성 구조 분석')
ws2.row_dimensions[4].height = 20

cogs_hdr = ['구분', '매출 ($)', 'COGS ($)', 'COGS%', '비고']
for j, h in enumerate(cogs_hdr, 2):
    write_cell(ws2, 5, j, h, fill=BLUE_SUB, font=hdr_font(10), align=center())

cogs_monthly = [
    ('1월',  3865054, 2838300, 0.734, ''),
    ('2월',  3121949, 2676897, 0.857, '⚠ 최고'),
    ('3월',  4189259, 3243267, 0.774, ''),
    ('4월',  4504617, 2825043, 0.627, '✅'),
    ('5월',  4311921, 2932171, 0.680, ''),
    ('6월',  4254963, 3198939, 0.752, ''),
    ('─ H1 평균 ─', None, None, 0.737, ''),
    ('7월',  4333800, 3174958, 0.733, ''),
    ('8월',  4478366, 3215585, 0.718, ''),
    ('9월',  4299226, 2970188, 0.691, ''),
    ('10월', 4226202, 2833006, 0.670, ''),
    ('11월', 4293868, 2780424, 0.648, '✅'),
    ('12월', 4186693, 2732121, 0.653, '✅'),
    ('─ H2 평균 ─', None, None, 0.685, ''),
    ('연간',  50065917, 35420898, 0.7075, ''),
]

for i, (lbl, s, c_val, pct, note) in enumerate(cogs_monthly):
    r = 6 + i
    ws2.row_dimensions[r].height = 16
    is_avg = '평균' in lbl
    is_yr  = lbl == '연간'
    f = BLUE_LITE if is_yr else (GRAY_LITE if is_avg else
        (RED_LITE if pct > 0.80 else (GREEN_LITE if pct < 0.65 else WHITE)))
    bf = body_font(10, is_yr or is_avg)
    write_cell(ws2, r, 2, lbl,   fill=f, font=bf, align=center())
    write_cell(ws2, r, 3, s if s else '', fill=f, font=bf, align=right(), fmt='#,##0')
    write_cell(ws2, r, 4, c_val if c_val else '', fill=f, font=bf, align=right(), fmt='#,##0')
    write_cell(ws2, r, 5, pct,   fill=f, font=bf, align=right(), fmt='0.0%')
    write_cell(ws2, r, 6, note,  fill=f, font=body_font(9), align=center())

# ── 달성 필요 요건 5가지 ──────────────────────────────
r_req = 6 + len(cogs_monthly) + 2
merge_hdr(ws2, r_req, 2, 6, 'II. 목표 달성 필요 요건 5가지')
ws2.row_dimensions[r_req].height = 20

r_req += 1
req_hdr = ['요건', '내용', '미달 시 영향', '요구 산출물', '판정']
for j, h in enumerate(req_hdr, 2):
    write_cell(ws2, r_req, j, h, fill=BLUE_SUB, font=hdr_font(10), align=center())

req_data = [
    ('요건 1\nSamsung SOP 확정',  'A18 12.3M·A38 3.8M units\nSOP 일정 서면 확정',
     '매출 $7~10M 미달',         'Samsung 공식 PO / SOP 확인서',   '⚠ 미완료'),
    ('요건 2\nCOGS 구조 개선',    'H1 COGS% 85.7% 원인 규명\n목표: H1 70% 이하',
     'GP율 하락, 영업이익 악화',   '품목별 원가 분해표 (Q1기준)',    '❌ 미수행'),
    ('요건 3\n자동화 투자 실행',   'CNC/검사/사상 자동화\n투자 일정 확정·선행 집행',
     '인원절감 전제 붕괴',         '설비 투자 계획서·납기 확정서',   '⚠ 진행중'),
    ('요건 4\nMando 계약 재확인', '#REF! 오류 수정\nNX4/IMEB2/JK 계약 재확인',
     '$7.3M 신뢰성 손상',         'Mando 계약별 수량·단가 확인서',  '⚠ 미완료'),
    ('요건 5\nCNC 단가 협상',     'Samsung CNC $1.23 승인\n(현 계획: +7.9% 인상)',
     '매출 $461K 미달',           'Samsung 단가 승인 이메일',       '⚠ 미완료'),
]

for i, (req, cont, impact, output, status) in enumerate(req_data):
    r = r_req + 1 + i
    ws2.row_dimensions[r].height = 32
    s_fill = RED_LITE if '❌' in status else (YELLOW if '⚠' in status else GREEN_LITE)
    write_cell(ws2, r, 2, req,    fill=s_fill, font=body_font(10, True), align=center())
    write_cell(ws2, r, 3, cont,   fill=s_fill, font=body_font(9),        align=left())
    write_cell(ws2, r, 4, impact, fill=s_fill, font=body_font(9),        align=left())
    write_cell(ws2, r, 5, output, fill=s_fill, font=body_font(9),        align=left())
    write_cell(ws2, r, 6, status, fill=s_fill, font=body_font(10, True), align=center())

# ── 종합 판정 ─────────────────────────────────────────
r_sum = r_req + 1 + len(req_data) + 1
merge_hdr(ws2, r_sum, 2, 6, 'III. 종합 판정')
ws2.row_dimensions[r_sum].height = 20

sum_data = [
    ('매출 $50M 달성 가능성',   '⚠ 조건부 달성',  '5가지 요건 충족 전제'),
    ('COGS 70.75% 타당성',     '❌ 재검토 필요',  '한계 COGS 151% — 구조적 문제'),
    ('인원절감 SG&A -$1.95M',  '✅ 타당',         '월별 데이터로 확인됨'),
    ('자동화 전제 타당성',      '⚠ 조건부',       '투자 일정 확정 후 재평가'),
    ('H2 수익성 개선 추세',     '✅ 확인됨',       'Q4 COGS% 65.7% — 개선 뚜렷'),
]

for i, (item, verdict, note) in enumerate(sum_data):
    r = r_sum + 1 + i
    ws2.row_dimensions[r].height = 18
    f = GREEN_LITE if '✅' in verdict else (RED_LITE if '❌' in verdict else YELLOW)
    write_cell(ws2, r, 2, item,    fill=f, font=body_font(10, True), align=left())
    ws2.merge_cells(start_row=r, start_column=3, end_row=r, end_column=4)
    write_cell(ws2, r, 3, verdict, fill=f, font=body_font(11, True), align=center())
    ws2.merge_cells(start_row=r, start_column=5, end_row=r, end_column=6)
    write_cell(ws2, r, 5, note,    fill=f, font=body_font(9),        align=left())

wb.save(OUTPUT)
print('저장 완료: ' + OUTPUT)

# 검증
from openpyxl import load_workbook as lw
v = lw(OUTPUT)
print('시트: ' + str(v.sheetnames))
print('경영 요약 최대 행: ' + str(v['경영 요약'].max_row))
print('타당성 검토 최대 행: ' + str(v['타당성 검토 요약'].max_row))
print('생성 검증 완료.')
