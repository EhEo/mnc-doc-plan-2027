# 2026 vs 2027 매출원가 분석 보고서 xlsx 생성 (임원 보고용)
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from openpyxl import Workbook
from openpyxl.styles import (Font, PatternFill, Alignment, Border, Side,
                              GradientFill)
from openpyxl.utils import get_column_letter
from openpyxl.drawing.image import Image as XLImage
from openpyxl.chart import BarChart, Reference
from openpyxl.chart.series import DataPoint
import datetime

OUTPUT = '../reports/2026vs2027_매출원가_분석보고서.xlsx'
TODAY = '2026-06-15'
COMPANY = 'M&C Electronics Vina Co., Ltd.'

# ── 공통 스타일 ─────────────────────────────────────────────
def s(border_style='thin', color='C0C0C0'):
    side = Side(border_style=border_style, color=color)
    return Border(left=side, right=side, top=side, bottom=side)

def thick_border(color='2E75B6'):
    side = Side(border_style='medium', color=color)
    return Border(left=side, right=side, top=side, bottom=side)

def mk_font(name='맑은 고딕', size=10, bold=False, color='000000', italic=False):
    return Font(name=name, size=size, bold=bold, color=color, italic=italic)

def mk_fill(hex_color):
    return PatternFill('solid', fgColor=hex_color)

def al(h='center', v='center', wrap=False):
    return Alignment(horizontal=h, vertical=v, wrap_text=wrap)

# 색상 팔레트
C = {
    'navy':    '1F3864',
    'blue1':   '1F4E79',
    'blue2':   '2E75B6',
    'blue3':   '4472C4',
    'blue_lt': 'D6E4F0',
    'blue_xl': 'EBF3FB',
    'gray1':   '404040',
    'gray2':   '595959',
    'gray3':   'A6A6A6',
    'gray_lt': 'F2F2F2',
    'gray_md': 'D9D9D9',
    'green1':  '375623',
    'green2':  '548235',
    'green_lt':'E2EFDA',
    'green_xl':'F0F7EC',
    'red1':    'C00000',
    'red2':    'FF0000',
    'red_lt':  'FCE4D6',
    'yellow':  'FFF2CC',
    'orange':  'F4B942',
    'white':   'FFFFFF',
    'black':   '000000',
}

def wc(ws, r, c, v='', fill=None, font=None, align=None, fmt=None, border=None):
    cell = ws.cell(row=r, column=c, value=v)
    if fill:   cell.fill   = fill
    if font:   cell.font   = font
    if align:  cell.alignment = align
    if fmt:    cell.number_format = fmt
    cell.border = border or s()
    return cell

def mc(ws, r1, c1, r2, c2, v='', fill=None, font=None, align=None, border=None):
    ws.merge_cells(start_row=r1, start_column=c1, end_row=r2, end_column=c2)
    cell = ws.cell(row=r1, column=c1, value=v)
    if fill:  cell.fill  = fill
    if font:  cell.font  = font
    if align: cell.alignment = align
    cell.border = border or s()
    return cell

def set_col(ws, cols_widths):
    for col, w in cols_widths.items():
        ws.column_dimensions[col].width = w

def no_grid(ws):
    ws.sheet_view.showGridLines = False

wb = Workbook()

# ═══════════════════════════════════════════════════════════════════
# 시트 0: 표지
# ═══════════════════════════════════════════════════════════════════
ws0 = wb.active
ws0.title = '표지'
no_grid(ws0)
ws0.sheet_view.showGridLines = False
ws0.column_dimensions['A'].width = 3
for col in ['B','C','D','E','F','G','H']:
    ws0.column_dimensions[col].width = 16
ws0.row_dimensions[1].height  = 40
ws0.row_dimensions[2].height  = 8
ws0.row_dimensions[3].height  = 100
ws0.row_dimensions[4].height  = 8
ws0.row_dimensions[5].height  = 48
ws0.row_dimensions[6].height  = 36
ws0.row_dimensions[7].height  = 8
ws0.row_dimensions[8].height  = 24
ws0.row_dimensions[9].height  = 24
ws0.row_dimensions[10].height = 24
ws0.row_dimensions[11].height = 24
ws0.row_dimensions[12].height = 24
ws0.row_dimensions[13].height = 8
ws0.row_dimensions[14].height = 30
ws0.row_dimensions[15].height = 24

# 상단 네이비 바
mc(ws0, 1,2, 1,8, COMPANY,
   fill=mk_fill(C['navy']),
   font=mk_font(size=12, bold=True, color=C['white']),
   align=al('center','center'))

# 파란 배경 메인 영역
mc(ws0, 3,2, 3,8, '',
   fill=mk_fill(C['blue1']),
   align=al())

# 보고서 제목 (메인 영역 위에 덮어씌우기 — 병합셀 이후 별도 셀로)
# 실제로는 Row3의 텍스트를 삽입
ws0.cell(row=3, column=2).value = '2026 vs 2027\n매출원가 변동 분석 보고서'
ws0.cell(row=3, column=2).font  = mk_font(size=28, bold=True, color=C['white'])
ws0.cell(row=3, column=2).alignment = al('center','center',wrap=True)
ws0.cell(row=3, column=2).fill  = mk_fill(C['blue1'])

# 부제
mc(ws0, 5,2, 5,8, '2026년 Rev27 (예상 실적) 대비 2027년 Rev2 (사업계획) 비교 분석',
   fill=mk_fill(C['blue2']),
   font=mk_font(size=14, bold=True, color=C['white']),
   align=al('center','center'))

# 핵심 수치 박스 (3개)
boxes = [
    ('COGS율 개선', '77.23% → 70.75%', '-6.48%p', C['green2'], C['green_lt']),
    ('매출총이익 성장', '$9.6M → $14.6M', '+51.9%', C['blue2'], C['blue_lt']),
    ('영업이익 성장',   '$5.1M → $10.2M', '+99.1%', C['orange'], C['yellow']),
]
cols_start = [2, 4, 6]
for i, (title, val, chg, hdr_c, bg_c) in enumerate(boxes):
    c = cols_start[i]
    mc(ws0, 6, c, 6, c+1, title,
       fill=mk_fill(hdr_c),
       font=mk_font(size=11, bold=True, color=C['white']),
       align=al('center','center'))
    mc(ws0, 7, c, 7, c+1, val,
       fill=mk_fill(bg_c),
       font=mk_font(size=12, bold=True, color=C['black']),
       align=al('center','center'))
    mc(ws0, 8, c, 8, c+1, chg,
       fill=mk_fill(bg_c),
       font=mk_font(size=12, bold=True,
                    color=C['green1'] if '+' in chg else C['red1']),
       align=al('center','center'))

# 메타 정보
meta = [
    ('보고서 기준일', TODAY),
    ('대상 파일', '20260613-2026Y BIZ Plan_Rev27 / 20260615-2027Y BIZ Plan_Rev2'),
    ('작성', 'Claude Code (AI Assistant) — M&C Electronics Vina'),
]
for i, (k, v) in enumerate(meta):
    r = 10+i
    mc(ws0, r,2, r,3, k,
       fill=mk_fill(C['gray_md']),
       font=mk_font(size=10, bold=True),
       align=al('center','center'))
    mc(ws0, r,4, r,8, v,
       fill=mk_fill(C['gray_lt']),
       font=mk_font(size=10),
       align=al('left','center'))

# 목차
mc(ws0, 14,2, 14,8, '목  차',
   fill=mk_fill(C['blue1']),
   font=mk_font(size=12, bold=True, color=C['white']),
   align=al('center','center'))
toc = [
    ('Ⅰ. 핵심 요약', '핵심요약'),
    ('Ⅱ. 손익 비교 분석', '손익비교'),
    ('Ⅲ. COGS 변동 원인 분석', 'COGS원인'),
    ('Ⅳ. 고객사별 매출 변동', '고객사분석'),
    ('Ⅴ. 재료비·인건비 세부', '원가세부'),
    ('Ⅵ. 종합 진단 및 시사점', '종합진단'),
]
for i, (title, _sheet) in enumerate(toc):
    r = 15+i
    ws0.row_dimensions[r].height = 20
    mc(ws0, r,2, r,8, f'  {title}',
       fill=mk_fill(C['blue_xl'] if i%2==0 else C['white']),
       font=mk_font(size=11, color=C['blue1']),
       align=al('left','center'))

# ═══════════════════════════════════════════════════════════════════
# 시트 1: 핵심 요약 (Executive Summary)
# ═══════════════════════════════════════════════════════════════════
ws1 = wb.create_sheet('핵심요약')
no_grid(ws1)
set_col(ws1, {'A':3,'B':28,'C':16,'D':16,'E':14,'F':20,'G':3})
for r in range(1,60):
    ws1.row_dimensions[r].height = 18

# 헤더
mc(ws1, 1,2, 1,6, 'Ⅰ. 핵심 요약 (Executive Summary)',
   fill=mk_fill(C['navy']),
   font=mk_font(size=15, bold=True, color=C['white']),
   align=al())
ws1.row_dimensions[1].height = 36

# ── 주요 재무 지표 ─────────────────────────────────────────
mc(ws1, 3,2, 3,6, '① 주요 재무 지표 비교',
   fill=mk_fill(C['blue2']),
   font=mk_font(size=12, bold=True, color=C['white']),
   align=al())
ws1.row_dimensions[3].height = 26

hdr_row = ['지표', '2026 Rev27', '2027 Rev2', '증감액/증감폭', '평가']
for j,h in enumerate(hdr_row, 2):
    wc(ws1, 4, j, h,
       fill=mk_fill(C['blue3']),
       font=mk_font(size=10, bold=True, color=C['white']),
       align=al())

kpi = [
    ('매출',       '$42,339,208', '$50,065,917', '+$7,726,709 (+18.2%)', '✅ 목표 근접'),
    ('총 COGS',    '$32,698,641', '$35,420,898', '+$2,722,257 (+8.3%)',  '✅ 매출보다 낮은 증가율'),
    ('COGS율',     '77.23%',      '70.75%',      '-6.48%p',              '✅ 수익성 개선'),
    ('매출총이익', '$9,640,567',  '$14,645,019', '+$5,004,452 (+51.9%)', '✅ 대폭 개선'),
    ('GP율',       '22.77%',      '29.25%',      '+6.48%p',              '✅'),
    ('영업이익',   '$5,099,485',  '$10,155,071', '+$5,055,586 (+99.1%)', '✅ 2배 달성'),
    ('영업이익율', '12.04%',      '20.28%',      '+8.24%p',              '✅'),
    ('순이익',     '$3,273,771',  '$7,256,695',  '+$3,982,924 (+121.7%)', '✅'),
    ('EBITDA',     '$9,510,129',  '$14,264,028', '+$4,753,899 (+50.0%)', '✅'),
]
for i, row in enumerate(kpi):
    r = 5+i
    fill_r = mk_fill(C['blue_xl'] if i%2==0 else C['white'])
    lbl, v26, v27, delta, eval_ = row
    bold = lbl in ('COGS율', 'GP율', '영업이익율')
    wc(ws1, r, 2, lbl,   fill=mk_fill(C['gray_lt']), font=mk_font(10, bold), align=al('left','center'))
    wc(ws1, r, 3, v26,   fill=fill_r,                font=mk_font(10),       align=al('right','center'))
    wc(ws1, r, 4, v27,   fill=fill_r,                font=mk_font(10),       align=al('right','center'))
    delta_fill = mk_fill(C['green_lt']) if '+' in delta and '율' not in lbl else \
                 mk_fill(C['green_lt']) if '-' in delta and '율' in lbl else \
                 mk_fill(C['green_lt'])
    if lbl == 'COGS율':
        delta_fill = mk_fill(C['green_lt'])
    wc(ws1, r, 5, delta,  fill=delta_fill, font=mk_font(10, bold=bold, color=C['green1'] if '✅' in eval_ else C['black']), align=al('center','center'))
    wc(ws1, r, 6, eval_,  fill=delta_fill, font=mk_font(10),             align=al('center','center'))

# ── COGS 개선 3대 요인 ─────────────────────────────────────
r_s2 = 5+len(kpi)+2
mc(ws1, r_s2,2, r_s2,6, '② COGS율 -6.48%p 개선의 3대 요인',
   fill=mk_fill(C['blue2']),
   font=mk_font(size=12, bold=True, color=C['white']),
   align=al())
ws1.row_dimensions[r_s2].height = 26

factors = [
    ('① Write-off 소멸',  '-1.61%p',
     '2026년 전기(前期) 재고손실 $681K가 일시 인식됨. 2027년 계획에는 없는 비경상 항목.',
     C['green_lt']),
    ('② 인원 감축 레버리지', '인건비 -$562K',
     '860명(2026 평균) → Jan27 749명 → Dec27 653명. 직접인건비 절감 연간 약 $562K.',
     C['green_lt']),
    ('③ 매출 증가 분모 효과', 'COGM +10.6% < 매출 +18.2%',
     '매출이 원가보다 빠르게 성장하여 고정비 흡수율 향상. 순수 COGM율 75.61%→70.75%.',
     C['green_lt']),
]

hdr_f = ['요인', '효과', '설명']
for j,h in enumerate(hdr_f, 2):
    wc(ws1, r_s2+1, j if j<=3 else j, h,
       fill=mk_fill(C['blue3']),
       font=mk_font(10, bold=True, color=C['white']),
       align=al())
ws1.row_dimensions[r_s2+1].height = 18

for j,h in enumerate(hdr_f, 2):
    wc(ws1, r_s2+1, j, h,
       fill=mk_fill(C['blue3']),
       font=mk_font(10, bold=True, color=C['white']),
       align=al())

for i, (lbl, eff, desc, bg) in enumerate(factors):
    r = r_s2+2+i
    ws1.row_dimensions[r].height = 36
    wc(ws1, r, 2, lbl,  fill=mk_fill(bg), font=mk_font(10, True),  align=al('center','center'))
    wc(ws1, r, 3, eff,  fill=mk_fill(bg), font=mk_font(11, True, color=C['green1']), align=al('center','center'))
    mc(ws1, r, 4, r, 6, desc,
       fill=mk_fill(bg if i%2==0 else C['white']),
       font=mk_font(10),
       align=al('left','center',wrap=True))

# ── 주요 리스크 ────────────────────────────────────────────
r_s3 = r_s2+2+len(factors)+2
mc(ws1, r_s3,2, r_s3,6, '③ 주요 리스크 — 목표 달성 시 해소해야 할 과제',
   fill=mk_fill(C['red1']),
   font=mk_font(size=12, bold=True, color=C['white']),
   align=al())
ws1.row_dimensions[r_s3].height = 26

risks = [
    ('⚠ H1 COGS 73.7%', '상반기 원가율 상승', '신규 SOP 라인 초기 비효율 → 전반기 GP율 압박'),
    ('⚠ LGIT -85% 급감', '고마진 고객 이탈', '삼성 의존도 집중 → 단일 고객 리스크 증가'),
    ('⚠ COGM율 목표 초과', '계획(Rev19) 대비 +11%p', 'Rev19 목표 59.6% vs 실제 계획 70.75% — 근본 원가 개선 필요'),
    ('⚠ Chromate +78%', '재료비율 소폭 악화', '삼성 A38 화성처리 물량 급증 → 재료비 증가'),
]
for i, (risk, cause, desc) in enumerate(risks):
    r = r_s3+1+i
    ws1.row_dimensions[r].height = 28
    bg = mk_fill(C['red_lt'] if i%2==0 else C['yellow'])
    wc(ws1, r, 2, risk,  fill=bg, font=mk_font(10, True, color=C['red1']), align=al('center','center'))
    wc(ws1, r, 3, cause, fill=bg, font=mk_font(10, True), align=al('center','center'))
    mc(ws1, r, 4, r, 6, desc, fill=bg, font=mk_font(10), align=al('left','center',wrap=True))

# ═══════════════════════════════════════════════════════════════════
# 시트 2: 손익 비교
# ═══════════════════════════════════════════════════════════════════
ws2 = wb.create_sheet('손익비교')
no_grid(ws2)
set_col(ws2, {'A':3,'B':22,'C':15,'D':15,'E':15,'F':14,'G':20,'H':3})

mc(ws2, 1,2, 1,7, 'Ⅱ. 손익계산서 비교 (2026 Rev27 vs 2027 Rev2)',
   fill=mk_fill(C['navy']),
   font=mk_font(size=15, bold=True, color=C['white']),
   align=al())
ws2.row_dimensions[1].height = 36

# 연간 IS 비교 테이블
mc(ws2, 3,2, 3,7, '① 연간 손익 비교 (단위: USD)',
   fill=mk_fill(C['blue2']),
   font=mk_font(size=12, bold=True, color=C['white']),
   align=al())
ws2.row_dimensions[3].height = 24

for j,h in enumerate(['항목','2026 Rev27 실적','2027 Rev2 계획','증감액','증감율','비고'],2):
    wc(ws2, 4, j, h, fill=mk_fill(C['blue3']),
       font=mk_font(10, True, color=C['white']), align=al())
ws2.row_dimensions[4].height = 18

# 실제 IS 데이터 (openpyxl 숫자값으로 입력 → 서식 적용)
IS = [
    # (label, v26, v27, is_pct, is_sub, note)
    ('매출',                42339208, 50065917, False, False, ''),
    ('COGM (제조원가)',      32017424, 35420898, False, False, ''),
    ('  └ COGM/매출율',     0.7561,   0.7075,   True,  True,  ''),
    ('Write-off (재고손실)', 681217,   0,         False, False, '2026: 전기 재고손실 일시 인식'),
    ('총 COGS',             32698641, 35420898, False, False, ''),
    ('  └ COGS/매출율',     0.7723,   0.7075,   True,  True,  ''),
    ('매출총이익 (GP)',      9640567,  14645019, False, False, ''),
    ('  └ GP율',            0.2277,   0.2925,   True,  True,  ''),
    ('SG&A',                4541082,  4489948,  False, False, ''),
    ('영업이익',             5099485,  10155071, False, False, ''),
    ('  └ 영업이익율',      0.1204,   0.2028,   True,  True,  ''),
    ('순이익',              3273771,  7256695,  False, False, ''),
    ('  └ 순이익율',        0.0773,   0.1449,   True,  True,  ''),
    ('EBITDA',              9510129,  14264028, False, False, ''),
    ('D&A (감가상각)',       4941609,  None,     False, False, '2027: IS 미집계'),
]

for i, (lbl, v26, v27, is_pct, is_sub, note) in enumerate(IS):
    r = 5+i
    ws2.row_dimensions[r].height = 17
    v27_val = v27 if v27 is not None else ''
    if is_pct:
        delta = (v27-v26) if v27 is not None else None
        better = delta < 0 if 'COGS' in lbl or '율' in lbl and 'GP' not in lbl else (delta > 0 if delta else None)
        if 'GP율' in lbl or '영업이익율' in lbl or '순이익율' in lbl:
            better = delta > 0 if delta else None
        fill_c = mk_fill(C['green_lt']) if (delta and better) else mk_fill(C['red_lt']) if (delta and not better) else mk_fill(C['gray_lt'])
        lbl_fill = mk_fill(C['gray_lt']) if not is_sub else mk_fill(C['gray_lt'])
        wc(ws2, r, 2, lbl, fill=lbl_fill, font=mk_font(10, not is_sub), align=al('left','center'))
        wc(ws2, r, 3, v26, fill=fill_c, font=mk_font(10), align=al('right','center'), fmt='0.00%')
        wc(ws2, r, 4, v27_val, fill=fill_c, font=mk_font(10), align=al('right','center'), fmt='0.00%')
        wc(ws2, r, 5, delta if delta is not None else '', fill=fill_c,
           font=mk_font(10, bold=True, color=C['green1'] if (better and delta) else C['red1']),
           align=al('center','center'), fmt='+0.00%;-0.00%')
        wc(ws2, r, 6, '', fill=fill_c, font=mk_font(10), align=al('center','center'))
    else:
        delta = v27 - v26 if v27 is not None else None
        dpct  = delta/v26 if (delta is not None and v26) else None
        better = delta >= 0 if delta is not None else True
        if lbl == 'Write-off (재고손실)':
            better = delta <= 0
        fill_c = mk_fill(C['green_lt']) if better else mk_fill(C['red_lt'])
        is_total = lbl in ('매출','총 COGS','매출총이익 (GP)','영업이익','순이익','EBITDA')
        lbl_fill = mk_fill(C['gray_md']) if is_total else mk_fill(C['gray_lt'])
        wc(ws2, r, 2, lbl, fill=lbl_fill, font=mk_font(10, is_total), align=al('left','center'))
        wc(ws2, r, 3, v26, fill=fill_c, font=mk_font(10, is_total), align=al('right','center'), fmt='#,##0')
        wc(ws2, r, 4, v27_val, fill=fill_c, font=mk_font(10, is_total), align=al('right','center'), fmt='#,##0')
        wc(ws2, r, 5, delta if delta is not None else '',
           fill=fill_c, font=mk_font(10, True, color=C['green1'] if better else C['red1']),
           align=al('right','center'), fmt='+#,##0;-#,##0')
        wc(ws2, r, 6, dpct if dpct is not None else '',
           fill=fill_c, font=mk_font(10, True),
           align=al('center','center'), fmt='+0.0%;-0.0%')
    wc(ws2, r, 7, note, fill=mk_fill(C['yellow']) if note else mk_fill(C['white']),
       font=mk_font(9, italic=bool(note)), align=al('left','center',wrap=True))

# 월별 COGS율 추이
r_mo = 5+len(IS)+2
mc(ws2, r_mo,2, r_mo,7, '② 월별 COGS율 추이 비교',
   fill=mk_fill(C['blue2']),
   font=mk_font(size=12, bold=True, color=C['white']),
   align=al())
ws2.row_dimensions[r_mo].height = 24
for j,h in enumerate(['월','2026 COGS%','2027 COGS%','개선폭','추세','비고'],2):
    wc(ws2, r_mo+1, j, h, fill=mk_fill(C['blue3']),
       font=mk_font(10, True, color=C['white']), align=al())

monthly = [
    ('1월',  0.7215+0.0561, 0.7343, '2026: Write-off 일부 포함'),
    ('2월',  0.8210,        0.8574, '⚠ 양 연도 최고점'),
    ('3월',  0.7641,        0.7742, ''),
    ('4월',  0.8573,        0.6271, '✅ 2027 급개선 (삼성 물량 증가)'),
    ('5월',  0.7922,        0.6800, '✅'),
    ('6월',  0.7460,        0.7518, ''),
    ('7월',  0.7082,        0.7326, ''),
    ('8월',  0.7114,        0.7180, ''),
    ('9월',  0.7375,        0.6909, '✅'),
    ('10월', 0.7387,        0.6703, '✅'),
    ('11월', 0.7657,        0.6480, '✅'),
    ('12월', 0.7308,        0.6527, '✅'),
    ('연간', 0.7723,        0.7075, '★ 목표: -6.48%p'),
]
for i, (lbl, c26, c27, note) in enumerate(monthly):
    r = r_mo+2+i
    ws2.row_dimensions[r].height = 16
    delta = c27-c26
    improve = delta < 0
    is_yr = lbl == '연간'
    bg = mk_fill(C['blue_lt']) if is_yr else (mk_fill(C['green_lt']) if improve else mk_fill(C['red_lt']))
    trend = '↓ 개선' if improve else '↑ 악화'
    wc(ws2, r,2, lbl,   fill=mk_fill(C['gray_md'] if is_yr else C['gray_lt']), font=mk_font(10, is_yr), align=al())
    wc(ws2, r,3, c26,   fill=bg, font=mk_font(10, is_yr), align=al('right','center'), fmt='0.0%')
    wc(ws2, r,4, c27,   fill=bg, font=mk_font(10, is_yr), align=al('right','center'), fmt='0.0%')
    wc(ws2, r,5, delta, fill=mk_fill(C['green_lt'] if improve else C['red_lt']),
       font=mk_font(10, True, color=C['green1'] if improve else C['red1']),
       align=al(), fmt='+0.0%;-0.0%')
    wc(ws2, r,6, trend, fill=mk_fill(C['green_lt'] if improve else C['red_lt']),
       font=mk_font(10, color=C['green1'] if improve else C['red1']), align=al())
    wc(ws2, r,7, note,  fill=mk_fill(C['yellow']) if '⚠' in note or '★' in note else bg,
       font=mk_font(9), align=al('left','center'))

# ═══════════════════════════════════════════════════════════════════
# 시트 3: COGS 원인 분석
# ═══════════════════════════════════════════════════════════════════
ws3 = wb.create_sheet('COGS원인')
no_grid(ws3)
set_col(ws3, {'A':3,'B':26,'C':14,'D':14,'E':14,'F':24,'G':3})

mc(ws3, 1,2, 1,6, 'Ⅲ. COGS 변동 원인 상세 분석',
   fill=mk_fill(C['navy']),
   font=mk_font(size=15, bold=True, color=C['white']),
   align=al())
ws3.row_dimensions[1].height = 36

# Write-off 분석
mc(ws3, 3,2, 3,6, '① Write-off $681,217 — 2026년 일시 인식 항목',
   fill=mk_fill(C['blue2']),
   font=mk_font(size=12, bold=True, color=C['white']),
   align=al())
ws3.row_dimensions[3].height = 24

for j,h in enumerate(['월','금액 (USD)','비고'],2):
    wc(ws3, 4, j, h, fill=mk_fill(C['blue3']),
       font=mk_font(10, True, color=C['white']), align=al())

woff_mo = [
    ('1월', 204746, '전기 재고 손실 최대 인식'),
    ('2월',  95089, ''),
    ('3월', 112368, ''),
    ('4월',      0, ''),
    ('5월',  33627, ''),
    ('6월',  33627, ''),
    ('7월',  33627, ''),
    ('8월',  33627, ''),
    ('9월',  33627, ''),
    ('10월', 33627, ''),
    ('11월', 33627, ''),
    ('12월', 33627, ''),
    ('합계', 681217, '총 Write-off 연간'),
]
for i, (m, v, n) in enumerate(woff_mo):
    r = 5+i
    ws3.row_dimensions[r].height = 16
    is_tot = m == '합계'
    bg = mk_fill(C['blue_lt']) if is_tot else mk_fill(C['red_lt'] if v>0 else C['gray_lt'])
    wc(ws3, r, 2, m, fill=mk_fill(C['gray_md'] if is_tot else C['gray_lt']),
       font=mk_font(10, is_tot), align=al())
    wc(ws3, r, 3, v, fill=bg, font=mk_font(10, is_tot), align=al('right','center'), fmt='#,##0')
    mc(ws3, r,4, r,6, n, fill=bg, font=mk_font(9), align=al('left','center'))

# 인원·인건비 분석
r_hc = 5+len(woff_mo)+2
mc(ws3, r_hc,2, r_hc,6, '② 인원 감축 현황 (직접인건비 원가 절감)',
   fill=mk_fill(C['blue2']),
   font=mk_font(size=12, bold=True, color=C['white']),
   align=al())
ws3.row_dimensions[r_hc].height = 24

for j,h in enumerate(['구분','2026 Rev27 (평균)','2027 Jan 시작','2027 Dec 목표','효과'],2):
    wc(ws3, r_hc+1, j, h, fill=mk_fill(C['blue3']),
       font=mk_font(10, True, color=C['white']), align=al())

hc_data = [
    ('외국인',              15.3,    15,    16,  '경영진 유지'),
    ('베트남 Staff',        253.8,   237,   219, '간접 감축'),
    ('생산직 근로자',        620.0,   497,   418, '직접인건비 절감 핵심'),
    ('합계',                 860.0,   749,   653, '-207명 감축'),
    ('총 인건비 (USD/년)',   7962078, None,  None,'2027 추정: ~$7.4M (-$562K)'),
]
for i, (lbl, v26, vs, ve, note) in enumerate(hc_data):
    r = r_hc+2+i
    ws3.row_dimensions[r].height = 20
    is_tot = '합계' in lbl or '인건비' in lbl
    bg = mk_fill(C['blue_lt']) if is_tot else mk_fill(C['green_xl'] if i%2==0 else C['white'])
    wc(ws3, r, 2, lbl, fill=mk_fill(C['gray_md'] if is_tot else C['gray_lt']),
       font=mk_font(10, is_tot), align=al('left','center'))
    fmt = '#,##0' if '인건비' in lbl else '0.0'
    wc(ws3, r, 3, v26, fill=bg, font=mk_font(10, is_tot), align=al('right','center'), fmt=fmt)
    wc(ws3, r, 4, vs if vs else '—', fill=mk_fill(C['green_lt']),
       font=mk_font(10, is_tot), align=al('right','center'), fmt=fmt if vs else '@')
    wc(ws3, r, 5, ve if ve else '—', fill=mk_fill(C['green_lt']),
       font=mk_font(10, is_tot), align=al('right','center'), fmt=fmt if ve else '@')
    wc(ws3, r, 6, note, fill=bg, font=mk_font(9), align=al('left','center'))

# COGM율 실질 분해
r_cg = r_hc+2+len(hc_data)+2
mc(ws3, r_cg,2, r_cg,6, '③ COGM율 실질 분해 — 75.61% → 70.75% (-4.86%p)',
   fill=mk_fill(C['blue2']),
   font=mk_font(size=12, bold=True, color=C['white']),
   align=al())
ws3.row_dimensions[r_cg].height = 24

for j,h in enumerate(['구분','2026 비율','2027 비율','기여폭','설명'],2):
    wc(ws3, r_cg+1, j, h, fill=mk_fill(C['blue3']),
       font=mk_font(10, True, color=C['white']), align=al())

decomp = [
    ('순수 COGM율',   0.7561, 0.7075, -0.0486, '재료비+인건비+경비 합산'),
    ('재료비율 기여', None,   None,   -0.0120, 'S36 감소(LGIT 축소) ≒ -1.2%p'),
    ('인건비율 기여', None,   None,   -0.0133, '인원 감축 ≒ -1.3%p'),
    ('분모 레버리지', None,   None,   -0.0233, '매출 +18.2% > COGM +10.6%'),
    ('COGS 총 개선', 0.7723, 0.7075, -0.0648, 'Write-off 소멸 포함 총 개선'),
]
for i, (lbl, v26, v27, d, desc) in enumerate(decomp):
    r = r_cg+2+i
    ws3.row_dimensions[r].height = 20
    is_tot = '총' in lbl
    bg = mk_fill(C['blue_lt']) if is_tot else mk_fill(C['green_xl'] if i%2==0 else C['white'])
    wc(ws3, r, 2, lbl, fill=mk_fill(C['gray_md'] if is_tot else C['gray_lt']),
       font=mk_font(10, is_tot), align=al('left','center'))
    wc(ws3, r, 3, v26 if v26 else '—', fill=bg, font=mk_font(10), align=al('right','center'),
       fmt='0.00%' if v26 else '@')
    wc(ws3, r, 4, v27 if v27 else '—', fill=bg, font=mk_font(10), align=al('right','center'),
       fmt='0.00%' if v27 else '@')
    wc(ws3, r, 5, d, fill=mk_fill(C['green_lt']),
       font=mk_font(10, True, color=C['green1']), align=al(), fmt='+0.00%;-0.00%')
    wc(ws3, r, 6, desc, fill=bg, font=mk_font(9), align=al('left','center'))

# ═══════════════════════════════════════════════════════════════════
# 시트 4: 고객사 분석
# ═══════════════════════════════════════════════════════════════════
ws4 = wb.create_sheet('고객사분석')
no_grid(ws4)
set_col(ws4, {'A':3,'B':24,'C':16,'D':16,'E':14,'F':14,'G':24,'H':3})

mc(ws4, 1,2, 1,7, 'Ⅳ. 고객사별 매출 변동 분석',
   fill=mk_fill(C['navy']),
   font=mk_font(size=15, bold=True, color=C['white']),
   align=al())
ws4.row_dimensions[1].height = 36

mc(ws4, 3,2, 3,7, '① 고객사별 매출 증감 (단위: USD)',
   fill=mk_fill(C['blue2']),
   font=mk_font(size=12, bold=True, color=C['white']),
   align=al())
ws4.row_dimensions[3].height = 24

for j,h in enumerate(['고객사·모델','2026 Rev27','2027 Rev2','증감액','증감율','비고'],2):
    wc(ws4, 4, j, h, fill=mk_fill(C['blue3']),
       font=mk_font(10, True, color=C['white']), align=al())

cust = [
    # (lbl, v26, v27, note, is_sub)
    ('Samsung Bracket (A18·A38 등)', 12243940, 19938149, 'A18 대규모 추가, A38 화성처리 증가', False),
    ('Samsung CNC',                   6451579,  6314820, '단가 $1.14→$1.23/unit, 수량 소폭 감소', False),
    ('Samsung Camera ZN (신규)',              0,  2708558, '★ 2027 신규 추가 모델', False),
    ('Samsung 소계',                 18695520, 28961527, '전체 매출 대비 비중: 44.1%→57.8%', True),
    ('LGIT (GEN3·CL4 등)',            5615490,   845248, '⚠ -84.9%: 대부분 제품 종료 또는 축소', False),
    ('Mando',                          6540485,  7313286, 'JK Housing 추가, NX4/IMEB2 유지', False),
    ('ZF TRW',                         8333549,  8516702, '기존 물량 안정적 유지', False),
    ('Qualcomm',                        693555,  1014591, 'MTP 물량 증가', False),
    ('A사 (ZF계열 Glass Frame)',         177118,   747600, '★ 신규 (+322%)', False),
    ('신규 고객 (No.3)',                 770469,  1404000, '단가 고수준 신규 제품', False),
    ('신규 고객 (No.4)',               1513023,  1262964, '소폭 감소', False),
    ('합계',                          42339208, 50065917, '매출 $50M 목표', True),
]

for i, (lbl, v26, v27, note, is_sub) in enumerate(cust):
    r = 5+i
    ws4.row_dimensions[r].height = 18
    delta = v27-v26
    dpct  = delta/v26 if v26 else None
    inc   = delta >= 0
    is_tot = '합계' in lbl
    bg = mk_fill(C['blue_lt']) if is_tot else \
         mk_fill(C['gray_md']) if is_sub else \
         (mk_fill(C['green_lt']) if inc else mk_fill(C['red_lt']))
    warn = '⚠' in note or 'LGIT' in lbl
    if '신규' in lbl and '★' in note:
        bg = mk_fill(C['green_xl'])
    wc(ws4, r,2, lbl,  fill=mk_fill(C['gray_md'] if (is_tot or is_sub) else C['gray_lt']),
       font=mk_font(10, is_tot or is_sub), align=al('left','center'))
    wc(ws4, r,3, v26,  fill=bg, font=mk_font(10, is_tot), align=al('right','center'), fmt='#,##0')
    wc(ws4, r,4, v27,  fill=bg, font=mk_font(10, is_tot), align=al('right','center'), fmt='#,##0')
    wc(ws4, r,5, delta,fill=bg, font=mk_font(10, True, color=C['green1'] if inc else C['red1']),
       align=al('right','center'), fmt='+#,##0;-#,##0')
    wc(ws4, r,6, dpct if dpct is not None else '',
       fill=bg, font=mk_font(10, True, color=C['green1'] if inc else C['red1']),
       align=al(), fmt='+0.0%;-0.0%')
    wc(ws4, r,7, note, fill=mk_fill(C['yellow']) if warn else bg,
       font=mk_font(9), align=al('left','center',wrap=True))

# 고객 Mix 시사점
r_mix = 5+len(cust)+2
mc(ws4, r_mix,2, r_mix,7, '② 고객 Mix 변화가 COGS에 미치는 영향',
   fill=mk_fill(C['blue2']),
   font=mk_font(size=12, bold=True, color=C['white']),
   align=al())
ws4.row_dimensions[r_mix].height = 24

mix_pts = [
    ('LGIT 축소의 원가 영향', '긍정',
     'LGIT 제품 S36 재료비 감소 → 재료비율 하락 기여 (-64% / 9월 기준)'),
    ('Samsung 집중의 원가 영향', '중립',
     '브라켓 제품 대량 생산으로 고정비 흡수 개선, 단 Chromate 처리비 +78% 발생'),
    ('삼성 단일 의존도 집중 리스크', '주의',
     '2027 매출 57.8%가 Samsung — 발주 변동 시 COGS 흡수율 급락 위험'),
    ('CNC 신규 제품 효과', '긍정',
     'Samsung CNC 단가 $1.14→$1.23 상향, Camera ZN 신규 고마진 품목 추가'),
]

for i, (lbl, tag, desc) in enumerate(mix_pts):
    r = r_mix+1+i
    ws4.row_dimensions[r].height = 28
    tag_fill = mk_fill(C['green_lt']) if tag == '긍정' else \
               (mk_fill(C['red_lt']) if tag == '주의' else mk_fill(C['yellow']))
    wc(ws4, r,2, lbl,  fill=mk_fill(C['gray_lt']), font=mk_font(10,True), align=al('center','center'))
    wc(ws4, r,3, tag,  fill=tag_fill, font=mk_font(10,True), align=al())
    mc(ws4, r,4, r,7, desc, fill=tag_fill, font=mk_font(10), align=al('left','center',wrap=True))

# ═══════════════════════════════════════════════════════════════════
# 시트 5: 원가세부 (재료비·인건비)
# ═══════════════════════════════════════════════════════════════════
ws5 = wb.create_sheet('원가세부')
no_grid(ws5)
set_col(ws5, {'A':3,'B':26,'C':15,'D':15,'E':15,'F':22,'G':3})

mc(ws5, 1,2, 1,6, 'Ⅴ. 재료비·인건비 세부 분석',
   fill=mk_fill(C['navy']),
   font=mk_font(size=15, bold=True, color=C['white']),
   align=al())
ws5.row_dimensions[1].height = 36

mc(ws5, 3,2, 3,6, '① 재료비 세부 비교 — M Plan 9월 단월 기준 (추세 대용)',
   fill=mk_fill(C['blue2']),
   font=mk_font(size=12, bold=True, color=C['white']),
   align=al())
ws5.row_dimensions[3].height = 24

for j,h in enumerate(['항목','2026 Sep (USD)','2027 Sep (USD)','증감','비고'],2):
    wc(ws5, 4, j, h, fill=mk_fill(C['blue3']),
       font=mk_font(10, True, color=C['white']), align=al())

mat = [
    ('ADC12 (주조 알루미늄)',       297571,  304122, 'Samsung 브라켓 볼륨 증가 반영'),
    ('S36 (LGIT 전용 재료)',        233864,   83909, '⚠ LGIT 급감으로 -64% 감소'),
    ('Chromate 화성처리재',          65932,  117489, '⚠ Samsung A38 증가로 +78% 급증'),
    ('A Project (ZF60A 등)',          10766,   18600, '신규 ZF계열 A사 물량'),
    ('기타 재료비',                  210020,  610946, '기타 제품 재료 증가'),
    ('M Plan 합계 (Sep)',            819153, 1135066, '9월 단월 총 재료비'),
    ('Sep 매출 기준 재료비율',     819153/3320220, 1135066/4299226, '24.7% → 26.4% (+1.7%p)'),
]

for i, row in enumerate(mat):
    r = 5+i
    ws5.row_dimensions[r].height = 18
    is_pct = '율' in row[0]
    is_tot = '합계' in row[0]
    lbl, v26, v27, note = row
    delta = v27-v26
    dpct  = delta/v26 if v26 else None
    inc   = delta >= 0
    warn  = '⚠' in note
    bg = mk_fill(C['blue_lt']) if is_tot else \
         (mk_fill(C['red_lt']) if warn else \
         (mk_fill(C['gray_lt']) if is_pct else \
         (mk_fill(C['green_xl'] if not inc else C['white']))))
    wc(ws5, r,2, lbl, fill=mk_fill(C['gray_md'] if is_tot else C['gray_lt']),
       font=mk_font(10, is_tot), align=al('left','center'))
    if is_pct:
        wc(ws5, r,3, v26, fill=bg, font=mk_font(10), align=al('right','center'), fmt='0.0%')
        wc(ws5, r,4, v27, fill=bg, font=mk_font(10), align=al('right','center'), fmt='0.0%')
        wc(ws5, r,5, delta, fill=mk_fill(C['yellow']),
           font=mk_font(10,True), align=al(), fmt='+0.00%;-0.00%')
    else:
        wc(ws5, r,3, v26, fill=bg, font=mk_font(10,is_tot), align=al('right','center'), fmt='#,##0')
        wc(ws5, r,4, v27, fill=bg, font=mk_font(10,is_tot), align=al('right','center'), fmt='#,##0')
        wc(ws5, r,5, dpct if dpct else '', fill=bg,
           font=mk_font(10,True, color=C['green1'] if not inc else C['red1']),
           align=al(), fmt='+0.0%;-0.0%')
    wc(ws5, r,6, note, fill=mk_fill(C['yellow']) if warn else bg,
       font=mk_font(9), align=al('left','center',wrap=True))

# 인건비 추이
r_lc = 5+len(mat)+2
mc(ws5, r_lc,2, r_lc,6, '② 인건비 추이 비교',
   fill=mk_fill(C['blue2']),
   font=mk_font(size=12, bold=True, color=C['white']),
   align=al())
ws5.row_dimensions[r_lc].height = 24

for j,h in enumerate(['구분','2026 Rev27','2027 Rev2 (추정)','절감액','비고'],2):
    wc(ws5, r_lc+1, j, h, fill=mk_fill(C['blue3']),
       font=mk_font(10, True, color=C['white']), align=al())

lc_data = [
    ('총 인건비 (연간)',      7962078, 7400000, '추정 -$562K / 인원 감축 효과'),
    ('SG&A 내 인건비 추정', 4541082, 4489948, '간접비 포함 SG&A -$51K'),
    ('직접인건비 추정 절감', None,    None,    '생산직 207명 × $450/월 × 12 = ~$1,118K'),
]
for i, (lbl, v26, v27, note) in enumerate(lc_data):
    r = r_lc+2+i
    ws5.row_dimensions[r].height = 24
    bg = mk_fill(C['green_xl'])
    wc(ws5, r,2, lbl, fill=mk_fill(C['gray_lt']), font=mk_font(10,True), align=al('left','center'))
    wc(ws5, r,3, v26 if v26 else '—', fill=bg, font=mk_font(10), align=al('right','center'), fmt='#,##0' if v26 else '@')
    wc(ws5, r,4, v27 if v27 else '—', fill=mk_fill(C['green_lt']), font=mk_font(10), align=al('right','center'), fmt='#,##0' if v27 else '@')
    wc(ws5, r,5, (v26-v27) if (v26 and v27) else '', fill=mk_fill(C['green_lt']),
       font=mk_font(10,True,color=C['green1']), align=al('right','center'), fmt='#,##0')
    wc(ws5, r,6, note, fill=mk_fill(C['yellow']), font=mk_font(9), align=al('left','center',wrap=True))

# ═══════════════════════════════════════════════════════════════════
# 시트 6: 종합 진단
# ═══════════════════════════════════════════════════════════════════
ws6 = wb.create_sheet('종합진단')
no_grid(ws6)
set_col(ws6, {'A':3,'B':22,'C':14,'D':36,'E':18,'F':3})

mc(ws6, 1,2, 1,5, 'Ⅵ. 종합 진단 및 시사점',
   fill=mk_fill(C['navy']),
   font=mk_font(size=15, bold=True, color=C['white']),
   align=al())
ws6.row_dimensions[1].height = 36

mc(ws6, 3,2, 3,5, '① 긍정 요인 — 목표 달성의 근거',
   fill=mk_fill(C['green2']),
   font=mk_font(size=12, bold=True, color=C['white']),
   align=al())
ws6.row_dimensions[3].height = 24

for j,h in enumerate(['요인','평가','근거','정량 효과'],2):
    wc(ws6, 4, j, h, fill=mk_fill(C['blue3']),
       font=mk_font(10, True, color=C['white']), align=al())

positives = [
    ('Write-off $681K 소멸',
     '✅ 확정',
     '2026년 비경상 재고손실이 2027년 계획에 없음. 자동 원가율 개선.',
     'COGS율 -1.61%p'),
    ('인원 207명 감축 (860→653)',
     '✅ 달성 중',
     '2027 Jan 749명, Dec 653명 목표. 생산직 중심으로 직접인건비 절감.',
     '~$562K/년 절감'),
    ('매출 +18.2% 고성장',
     '✅ 계획 수립',
     'Samsung 신규 CNC Camera·A18 대규모 물량 추가로 분모 레버리지 효과.',
     'COGM율 -4.86%p'),
    ('Q4 COGS율 65.7% 달성',
     '✅ 계획상 확인',
     '2027 10~12월 COGS율 평균 65.7% — 하반기 수익성 구조 안정화.',
     'GP율 34.3%'),
    ('SG&A 안정 유지',
     '✅ 계획',
     '인원 감축에도 SG&A $4.49M — 전년 대비 소폭 감소(-1.1%).',
     '-$51K'),
]
for i, (lbl, tag, desc, eff) in enumerate(positives):
    r = 5+i
    ws6.row_dimensions[r].height = 28
    bg = mk_fill(C['green_xl'] if i%2==0 else C['white'])
    wc(ws6, r,2, lbl,  fill=mk_fill(C['gray_lt']), font=mk_font(10,True), align=al('center','center',wrap=True))
    wc(ws6, r,3, tag,  fill=mk_fill(C['green_lt']), font=mk_font(10,True,color=C['green1']), align=al())
    wc(ws6, r,4, desc, fill=bg, font=mk_font(10), align=al('left','center',wrap=True))
    wc(ws6, r,5, eff,  fill=mk_fill(C['green_lt']), font=mk_font(10,True,color=C['green1']), align=al())

# 부정 요인
r_neg = 5+len(positives)+2
mc(ws6, r_neg,2, r_neg,5, '② 리스크 요인 — 달성 시 해소해야 할 과제',
   fill=mk_fill(C['red1']),
   font=mk_font(size=12, bold=True, color=C['white']),
   align=al())
ws6.row_dimensions[r_neg].height = 24

for j,h in enumerate(['요인','심각도','상세 내용','관리 방안'],2):
    wc(ws6, r_neg+1, j, h, fill=mk_fill(C['blue3']),
       font=mk_font(10, True, color=C['white']), align=al())

negatives = [
    ('2027 H1 COGS율 73.7%',
     '⚠ 중요',
     '상반기 원가율이 전년 대비 개선 없음. 신규 SOP 라인(A18 등) 초기 비효율.',
     'SOP 안정화 일정 단축, 초기 불량율 집중 관리'),
    ('LGIT 매출 -84.9%',
     '⚠ 중요',
     'GEN3·CL4 등 LGIT 대부분 종료. 삼성 의존도 44.1%→57.8% 집중.',
     '신규 고객 파이프라인 확보, ZF·Qualcomm 물량 확대'),
    ('Rev19 계획 대비 COGS +11%p',
     '❌ 미해소',
     'Rev19 목표 59.6% vs 실제 계획 70.75% — 근본 원가 구조 미개선.',
     '재료 구매가 협상, 생산 효율화, 폐기율 절감'),
    ('Chromate 재료비 +78%',
     '⚠ 확인',
     'Samsung A38 화성처리 물량 급증. 단일 공정 원가 집중.',
     '대체 공정 또는 내재화 검토'),
    ('#REF! 오류 잔존',
     '⚠ 데이터 신뢰성',
     '2027 Rev2 AP Plan 등 일부 시트 #REF! 오류 미수정 → 간접비 합계 불명확.',
     '다음 Rev에서 전수 수정 필요'),
]
for i, (lbl, sev, desc, act) in enumerate(negatives):
    r = r_neg+2+i
    ws6.row_dimensions[r].height = 32
    sev_fill = mk_fill(C['red_lt']) if '❌' in sev else mk_fill(C['yellow'])
    wc(ws6, r,2, lbl,  fill=mk_fill(C['gray_lt']), font=mk_font(10,True), align=al('center','center',wrap=True))
    wc(ws6, r,3, sev,  fill=sev_fill, font=mk_font(10,True,color=C['red1'] if '❌' in sev else C['gray1']), align=al())
    wc(ws6, r,4, desc, fill=mk_fill(C['red_lt'] if i%2==0 else C['yellow']),
       font=mk_font(10), align=al('left','center',wrap=True))
    wc(ws6, r,5, act,  fill=mk_fill(C['blue_xl']), font=mk_font(10), align=al('left','center',wrap=True))

# 최종 결론
r_conc = r_neg+2+len(negatives)+2
mc(ws6, r_conc,2, r_conc,5, '③ 결론 및 권고',
   fill=mk_fill(C['blue1']),
   font=mk_font(size=12, bold=True, color=C['white']),
   align=al())
ws6.row_dimensions[r_conc].height = 24

conclusions = [
    ('핵심 결론',
     '2026 COGS율 77.23%에서 2027 목표 70.75%로 -6.48%p 개선은 달성 가능한 수준. '
     'Write-off 소멸($681K)·인원 감축(207명)·매출 레버리지(+18.2%)의 3중 효과가 구조적으로 확보됨.'),
    ('선결 과제',
     '① H1 원가율 73.7% → 실적 집중 관리 필요 (특히 2~3월 80~86% 구간). '
     '② 삼성 의존도 57.8%에 대한 헷지 전략 수립. '
     '③ #REF! 오류 잔존 시트 Rev3에서 반드시 수정.'),
    ('중장기 과제',
     'Rev19 원 계획 COGS 59.6% 대비 현재 계획이 11%p 이상 높음. '
     '재료 구매가 재협상·공정 효율화·폐기율 절감을 통한 구조적 원가 개선 필요.'),
]
for i, (title, body) in enumerate(conclusions):
    r = r_conc+1+i
    ws6.row_dimensions[r].height = 52
    bg = mk_fill(C['blue_xl'] if i==0 else (C['yellow'] if i==1 else C['red_lt']))
    wc(ws6, r,2, title, fill=mk_fill(C['blue2']),
       font=mk_font(11,True,color=C['white']), align=al())
    mc(ws6, r,3, r,5, body, fill=bg, font=mk_font(10), align=al('left','center',wrap=True))

# ── 저장 ──────────────────────────────────────────────────
wb.save(OUTPUT)
print('저장 완료:', OUTPUT)

from openpyxl import load_workbook as lw
v = lw(OUTPUT)
print('시트:', v.sheetnames)
print('검증 완료.')
