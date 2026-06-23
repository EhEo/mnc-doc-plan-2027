# 2026 Rev27 vs 2027 Rev2 비교 분석 xlsx 생성
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import glob as _g

OUTPUT = '../reports/2026vs2027_매출원가_비교분석.xlsx'

# ── 스타일 정의 ──────────────────────────────────────────
BLUE_HDR  = PatternFill('solid', fgColor='1F4E79')
BLUE_SUB  = PatternFill('solid', fgColor='2E75B6')
BLUE_LITE = PatternFill('solid', fgColor='D6E4F0')
RED_LITE  = PatternFill('solid', fgColor='FCE4D6')
RED_MED   = PatternFill('solid', fgColor='F4CCCC')
GREEN_LITE= PatternFill('solid', fgColor='E2EFDA')
GREEN_MED = PatternFill('solid', fgColor='B7E1CD')
YELLOW    = PatternFill('solid', fgColor='FFF2CC')
GRAY_LITE = PatternFill('solid', fgColor='F2F2F2')
GRAY_MED  = PatternFill('solid', fgColor='D9D9D9')
ORANGE    = PatternFill('solid', fgColor='FCE5CD')
WHITE     = PatternFill('solid', fgColor='FFFFFF')

def tb():
    s = Side(border_style='thin', color='BFBFBF')
    return Border(left=s, right=s, top=s, bottom=s)

def hf(sz=10, bold=True, color='FFFFFF'):
    return Font(name='맑은 고딕', size=sz, bold=bold, color=color)

def bf(sz=10, bold=False, color='000000'):
    return Font(name='맑은 고딕', size=sz, bold=bold, color=color)

def ca(): return Alignment(horizontal='center', vertical='center', wrap_text=True)
def la(): return Alignment(horizontal='left',   vertical='center', wrap_text=True)
def ra(): return Alignment(horizontal='right',  vertical='center')

def wc(ws, r, c, v, fill=None, font=None, align=None, fmt=None):
    cell = ws.cell(row=r, column=c, value=v)
    if fill:  cell.fill   = fill
    if font:  cell.font   = font
    if align: cell.alignment = align
    cell.border = tb()
    if fmt:   cell.number_format = fmt
    return cell

def mh(ws, r, c1, c2, v, fill=BLUE_HDR, sz=11):
    ws.merge_cells(start_row=r, start_column=c1, end_row=r, end_column=c2)
    cell = ws.cell(row=r, column=c1, value=v)
    cell.fill=fill; cell.font=hf(sz); cell.alignment=ca(); cell.border=tb()

wb = Workbook()

# ═══════════════════════════════════════════════════════════
# 시트 1: IS 손익 비교
# ═══════════════════════════════════════════════════════════
ws1 = wb.active
ws1.title = '손익 비교'
ws1.sheet_view.showGridLines = False

col_w = [2, 24, 15, 15, 15, 14, 20, 2]
for i,w in enumerate(col_w,1):
    ws1.column_dimensions[get_column_letter(i)].width = w

# 제목
ws1.row_dimensions[2].height = 36
ws1.merge_cells('B2:G2')
c = ws1.cell(row=2, column=2, value='2026 Rev27 vs 2027 Rev2 — 손익 비교')
c.font = Font(name='맑은 고딕', size=16, bold=True, color='1F4E79')
c.alignment = ca()

# ── 섹션 1: 손익 요약 ────────────────────────────────────
ws1.row_dimensions[4].height = 20
mh(ws1, 4, 2, 7, 'I. 손익계산서 주요 지표 비교')

hdr = ['항목', '2026 Rev27 (실적)', '2027 Rev2 (계획)', '증감액', '증감율', '비고']
for j,h in enumerate(hdr,2):
    wc(ws1, 5, j, h, fill=BLUE_SUB, font=hf(10), align=ca())
ws1.row_dimensions[5].height = 18

# 2026 값
s26=42339208; cogs26=32017424; woff26=681217; total_cogs26=32698641
gp26=9640567; sga26=4541082; op26=5099485; ni26=3273771; ebitda26=9510129; da26=4941609
# 2027 값
s27=50065917; cogs27=35420898; woff27=0; total_cogs27=35420898
gp27=14645019; sga27=4489948; op27=10155071; ni27=7256695; ebitda27=14264028

is_rows = [
    ('매출',               s26,           s27,           None, None, ''),
    ('COGM (제조원가)',     cogs26,         cogs27,         None, None, ''),
    ('  └ COGM/매출',      cogs26/s26,     cogs27/s27,     None, None, ''),
    ('재고손실 Write-off', woff26,         woff27,         None, None, '⚠ 2026: 전년 재고 일시 인식'),
    ('총 COGS',           total_cogs26,   total_cogs27,   None, None, ''),
    ('  └ 총COGS/매출',   total_cogs26/s26, total_cogs27/s27, None, None, ''),
    ('매출총이익 (GP)',    gp26,           gp27,           None, None, ''),
    ('  └ GP율',          gp26/s26,       gp27/s27,       None, None, ''),
    ('SG&A',              sga26,          sga27,          None, None, ''),
    ('영업이익',          op26,           op27,           None, None, ''),
    ('  └ 영업이익율',    op26/s26,       op27/s27,       None, None, ''),
    ('순이익',            ni26,           ni27,           None, None, ''),
    ('  └ 순이익율',      ni26/s26,       ni27/s27,       None, None, ''),
    ('EBITDA',            ebitda26,       ebitda27,       None, None, ''),
    ('D&A (상각)',         da26,           None,           None, None, '2027: IS 미집계'),
]

for i,(lbl,v26,v27,_,__,note) in enumerate(is_rows):
    r = 6+i
    ws1.row_dimensions[r].height = 16
    is_pct = '율' in lbl or '/' in lbl
    is_sub  = lbl.startswith('  └')
    delta = (v27-v26) if (v27 is not None and v26 is not None) else None
    delta_pct = (delta/v26) if (delta is not None and v26 and not is_pct) else None

    if is_pct:
        better = v27 < v26 if ('COGS' in lbl or '원가' in lbl) else v27 > v26
    else:
        better = delta > 0 if delta is not None else True
    if lbl in ('재고손실 Write-off',):
        better = delta <= 0  # 줄어드는 게 좋음

    row_fill = (GREEN_LITE if better else RED_LITE) if delta is not None else WHITE
    row_fill = GRAY_LITE if is_sub else row_fill
    bold_row = not is_sub

    wc(ws1, r, 2, lbl,   fill=GRAY_LITE if is_sub else GRAY_MED if not is_sub else WHITE,
                          font=bf(10, bold_row), align=la())
    if is_pct:
        wc(ws1, r, 3, v26,  fill=row_fill, font=bf(10,bold_row), align=ra(), fmt='0.00%')
        wc(ws1, r, 4, v27 if v27 is not None else '',
                            fill=row_fill, font=bf(10,bold_row), align=ra(), fmt='0.00%')
        wc(ws1, r, 5, delta if delta is not None else '',
                            fill=row_fill, font=bf(10,bold_row), align=ra(), fmt='+0.00%;-0.00%')
        wc(ws1, r, 6, '',   fill=row_fill, font=bf(), align=ra())
    else:
        wc(ws1, r, 3, v26,  fill=row_fill, font=bf(10,bold_row), align=ra(), fmt='#,##0')
        wc(ws1, r, 4, v27 if v27 is not None else '',
                            fill=row_fill, font=bf(10,bold_row), align=ra(), fmt='#,##0')
        wc(ws1, r, 5, delta if delta is not None else '',
                            fill=row_fill, font=bf(10,bold_row), align=ra(), fmt='+#,##0;-#,##0')
        wc(ws1, r, 6, delta_pct if delta_pct is not None else '',
                            fill=row_fill, font=bf(10,bold_row), align=ra(), fmt='+0.0%;-0.0%')
    wc(ws1, r, 7, note, fill=row_fill, font=bf(9), align=la())

# ── 섹션 2: 월별 COGS% 비교 ──────────────────────────────
r_s2 = 6+len(is_rows)+2
mh(ws1, r_s2, 2, 7, 'II. 월별 COGS% 비교 (2026 Rev27 vs 2027 Rev2)')
ws1.row_dimensions[r_s2].height = 20
r_s2 += 1
mh_row = ['월', '2026 매출', '2026 COGM', '2026 COGS%', '2027 COGS%', '개선폭']
for j,h in enumerate(mh_row,2):
    wc(ws1, r_s2, j, h, fill=BLUE_SUB, font=hf(10), align=ca())

monthly = [
    ('1월',  3649629, 2633554, 0.7215, 0.7343, None),
    ('2월',  3143407, 2581808, 0.8210, 0.8574, None),  # 2026 write-off 포함
    ('3월',  4097111, 3130898, 0.7641, 0.7742, None),
    ('4월',  3295319, 2825043, 0.8573, 0.6271, None),
    ('5월',  3701637, 2932171, 0.7922, 0.6800, None),
    ('6월',  3769218, 2812077, 0.7460, 0.7518, None),
    ('7월',  4064405, 2878140, 0.7082, 0.7326, None),
    ('8월',  3777950, 2687681, 0.7114, 0.7180, None),
    ('9월',  3320220, 2448212, 0.7375, 0.6909, None),
    ('10월', 3200183, 2363793, 0.7387, 0.6703, None),
    ('11월', 3156589, 2417023, 0.7657, 0.6480, None),
    ('12월', 3163539, 2312224, 0.7308, 0.6527, None),
    ('연간', 42339208,32698641, 0.7723, 0.7075, None),
]

# 2026 월별 COGS% 재계산 (COGM/Sales, write-off 포함)
cogs26_mo = [2633554+204746, 2581808+95089, 3130898+112368, 2825043,
             2932171+33627, 2812077+33627, 2878140+33627, 2687681+33627,
             2448212+33627, 2363793+33627, 2417023+33627, 2312224+33627]
sales26_mo = [3649629,3143407,4097111,3295319,3701637,3769218,4064405,3777950,
              3320220,3200183,3156589,3163539]
cogs27_mo_pct = [0.7343,0.8574,0.7742,0.6271,0.6800,0.7518,0.7326,0.7180,
                 0.6909,0.6703,0.6480,0.6527]
mon_lbl = ['1월','2월','3월','4월','5월','6월','7월','8월','9월','10월','11월','12월']

for i,(lbl,s,tc,_,c27,__) in enumerate(monthly):
    r = r_s2+1+i
    ws1.row_dimensions[r].height = 15
    is_yr = lbl == '연간'
    if not is_yr:
        c26_pct = cogs26_mo[i]/sales26_mo[i]
        c27_pct = cogs27_mo_pct[i]
    else:
        c26_pct = 0.7723
        c27_pct = 0.7075

    delta_pct = c27_pct - c26_pct
    improve = delta_pct < 0

    f = BLUE_LITE if is_yr else (GREEN_LITE if improve else RED_LITE)
    bf_bold = bf(10, is_yr)
    wc(ws1, r, 2, lbl,    fill=GRAY_LITE if not is_yr else BLUE_LITE, font=bf_bold, align=ca())
    wc(ws1, r, 3, s if not is_yr else 42339208,
                           fill=f, font=bf_bold, align=ra(), fmt='#,##0')
    wc(ws1, r, 4, tc if not is_yr else 32698641,
                           fill=f, font=bf_bold, align=ra(), fmt='#,##0')
    wc(ws1, r, 5, c26_pct, fill=f, font=bf_bold, align=ra(), fmt='0.0%')
    wc(ws1, r, 6, c27_pct, fill=f, font=bf_bold, align=ra(), fmt='0.0%')
    wc(ws1, r, 7, delta_pct, fill=GREEN_MED if improve else RED_MED,
                              font=bf(10,True), align=ca(), fmt='+0.0%;-0.0%')

# ═══════════════════════════════════════════════════════════
# 시트 2: 고객사별 매출 변동
# ═══════════════════════════════════════════════════════════
ws2 = wb.create_sheet('고객사별 매출 변동')
ws2.sheet_view.showGridLines = False
col_w2 = [2,22,16,16,15,14,22,2]
for i,w in enumerate(col_w2,1):
    ws2.column_dimensions[get_column_letter(i)].width = w

ws2.row_dimensions[2].height = 36
ws2.merge_cells('B2:G2')
c2 = ws2.cell(row=2, column=2, value='고객사별 매출 변동 분석 (2026 Rev27 → 2027 Rev2)')
c2.font = Font(name='맑은 고딕', size=15, bold=True, color='1F4E79')
c2.alignment = ca()

mh(ws2, 4, 2, 7, 'I. 고객사별 매출 변동')
ws2.row_dimensions[4].height = 20
for j,h in enumerate(['고객사','2026 Rev27','2027 Rev2','증감액','증감율','비고'],2):
    wc(ws2, 5, j, h, fill=BLUE_SUB, font=hf(10), align=ca())

cust_data = [
    ('Samsung Bracket',  12243940, 19938149, None, None, 'A18 대규모 신규 (12.3M units)'),
    ('Samsung CNC',       6451579,  6314820, None, None, '단가 $1.14→$1.23, 수량 소폭 감소'),
    ('Samsung Camera ZN',       0,  2708558, None, None, '★ 2027 신규 추가'),
    ('Samsung 소계',     18695520, 28961527, None, None, ''),
    ('LGIT',              5615490,   845248, None, None, '⚠ -85%: GEN3/CL4 대부분 종료'),
    ('Mando',             6540485,  7313286, None, None, 'JK Housing 추가, NX4/IMEB2 유지'),
    ('ZF TRW',            8333549,  8516702, None, None, '기존 물량 유지 (+2.2%)'),
    ('Qualcomm',           693555,  1014591, None, None, 'MTP 물량 증가'),
    ('A사(ZF계열)',         177118,   747600, None, None, 'Glass Frame 신규'),
    ('신규 고객(3,4번)',   2283492,  2666964, None, None, '고단가 신규 제품'),
    ('합계',             42339208, 50065917, None, None, ''),
]

for i,(cust,v26,v27,_,__,note) in enumerate(cust_data):
    r = 6+i
    ws2.row_dimensions[r].height = 18
    is_total = cust == '합계'
    is_sub   = '소계' in cust
    delta = v27-v26
    dpct  = delta/v26 if v26 else None
    inc   = delta >= 0

    f = BLUE_LITE if is_total else (GRAY_LITE if is_sub else
        (GREEN_LITE if (inc and not is_total) else RED_LITE))
    bold_f = bf(10, is_total or is_sub)
    wc(ws2, r, 2, cust,  fill=GRAY_MED if (is_total or is_sub) else GRAY_LITE,
                          font=bold_f, align=la())
    wc(ws2, r, 3, v26,   fill=f, font=bold_f, align=ra(), fmt='#,##0')
    wc(ws2, r, 4, v27,   fill=f, font=bold_f, align=ra(), fmt='#,##0')
    wc(ws2, r, 5, delta, fill=f, font=bold_f, align=ra(), fmt='+#,##0;-#,##0')
    wc(ws2, r, 6, dpct if dpct is not None else '',
                          fill=f, font=bold_f, align=ra(), fmt='+0.0%;-0.0%')
    wc(ws2, r, 7, note,  fill=f, font=bf(9), align=la())

# ── 섹션 2: 재료비 비교 (M Plan Sep 월 기준) ──────────────
r_m = 6+len(cust_data)+2
mh(ws2, r_m, 2, 7, 'II. 재료비 세부 비교 (M Plan — 9월 기준, 연간 추세 대용)')
ws2.row_dimensions[r_m].height = 20
r_m += 1
for j,h in enumerate(['항목','2026 Sep','2027 Sep','증감','증감율','비고'],2):
    wc(ws2, r_m, j, h, fill=BLUE_SUB, font=hf(10), align=ca())

mat_data = [
    ('ADC12 재료비',    297571,  304122, None, None, '주조 알루미늄 (주력 소재)'),
    ('S36 재료비',      233864,   83909, None, None, '⚠ -64%: LGIT 물량 감소 직접 영향'),
    ('Chromate 처리비',  65932,  117489, None, None, '⚠ +78%: 삼성 A38 화성처리 급증'),
    ('A Project(Block)', 10766,   18600, None, None, '신규 ZF60A 등 A사 추가'),
    ('M Plan 합계',     819153, 1135066, None, None, '9월 단월 기준'),
    ('M Plan/매출(Sep)', 819153/3320220, 1135066/4299226,
                                         None, None, '재료비율: 24.7% → 26.4% (+1.7%p)'),
]

for i,(lbl,v26,v27,_,__,note) in enumerate(mat_data):
    r = r_m+1+i
    ws2.row_dimensions[r].height = 16
    is_pct  = '/' in lbl
    is_total= '합계' in lbl
    if not is_pct:
        delta = v27-v26
        dpct  = delta/v26 if v26 else None
        inc   = delta >= 0
    else:
        delta = v27-v26
        dpct  = None
        inc   = v27 < v26  # 비율은 낮을수록 좋음

    f = GRAY_LITE if is_total else (GREEN_LITE if inc else RED_LITE)
    if lbl.startswith('S36') or lbl.startswith('Chromate'):
        f = ORANGE  # 특이 항목 강조
    bold_f = bf(10, is_total)
    wc(ws2, r, 2, lbl,  fill=GRAY_MED if is_total else GRAY_LITE, font=bold_f, align=la())
    if is_pct:
        wc(ws2, r, 3, v26,  fill=f, font=bold_f, align=ra(), fmt='0.0%')
        wc(ws2, r, 4, v27,  fill=f, font=bold_f, align=ra(), fmt='0.0%')
        wc(ws2, r, 5, delta,fill=f, font=bold_f, align=ra(), fmt='+0.00%;-0.00%')
        wc(ws2, r, 6, '',   fill=f, font=bf(),   align=ra())
    else:
        wc(ws2, r, 3, v26,  fill=f, font=bold_f, align=ra(), fmt='#,##0')
        wc(ws2, r, 4, v27,  fill=f, font=bold_f, align=ra(), fmt='#,##0')
        wc(ws2, r, 5, delta,fill=f, font=bold_f, align=ra(), fmt='+#,##0;-#,##0')
        wc(ws2, r, 6, dpct if dpct else '',
                            fill=f, font=bold_f, align=ra(), fmt='+0.0%;-0.0%')
    wc(ws2, r, 7, note, fill=f, font=bf(9), align=la())

# ═══════════════════════════════════════════════════════════
# 시트 3: COGS 원인 분석
# ═══════════════════════════════════════════════════════════
ws3 = wb.create_sheet('COGS 원인 분석')
ws3.sheet_view.showGridLines = False
col_w3 = [2,26,14,14,16,18,2]
for i,w in enumerate(col_w3,1):
    ws3.column_dimensions[get_column_letter(i)].width = w

ws3.row_dimensions[2].height = 36
ws3.merge_cells('B2:F2')
c3 = ws3.cell(row=2,column=2,value='COGS 변동 원인 분석')
c3.font = Font(name='맑은 고딕', size=15, bold=True, color='1F4E79')
c3.alignment = ca()

# ── 원가율 요약 ───────────────────────────────────────────
mh(ws3, 4, 2, 6, 'I. COGS율 변동 분해 (77.23% → 70.75%)')
ws3.row_dimensions[4].height = 20
for j,h in enumerate(['변동 요인','2026 기여도','2027 기여도','개선폭','설명'],2):
    wc(ws3, 5, j, h, fill=BLUE_SUB, font=hf(10), align=ca())

factor_data = [
    ('총 COGS율',          0.7723, 0.7075, None, '기준선'),
    ('  ① Write-off 효과',  0.0161, 0.0000, None, '2026: 전년 재고손실 $681K 일시 인식'),
    ('  ② COGM 실질 개선',  0.7562, 0.7075, None, 'Write-off 제거 후 순수 제조원가율'),
    ('  ③ 재료비 Mix 변화', None,   None,   None, 'LGIT(고재료비 S36) 감소, Samsung 증가'),
    ('  ④ 인건비 절감',     None,   None,   None, '인원 860→749명(-111명) 직접인건비 감소'),
    ('  ⑤ H1 vs H2 격차',  None,   None,   None, '2027 H1 73.7% vs H2 68.5% — 전반기 고비용'),
]

for i,(lbl,v26,v27,_,note) in enumerate(factor_data):
    r = 6+i
    ws3.row_dimensions[r].height = 18
    is_base = lbl == '총 COGS율'
    is_sub  = lbl.startswith('  ')
    if v26 is not None and v27 is not None:
        delta = v27-v26
        improve = delta < 0
        f = BLUE_LITE if is_base else (GREEN_LITE if improve else RED_LITE)
    else:
        f = YELLOW
        delta = None
    bold_f = bf(10, is_base)
    wc(ws3, r, 2, lbl,  fill=GRAY_MED if is_base else GRAY_LITE, font=bold_f, align=la())
    wc(ws3, r, 3, v26 if v26 is not None else '—',
                         fill=f, font=bold_f, align=ra(),
                         fmt='0.00%' if v26 is not None else '@')
    wc(ws3, r, 4, v27 if v27 is not None else '—',
                         fill=f, font=bold_f, align=ra(),
                         fmt='0.00%' if v27 is not None else '@')
    wc(ws3, r, 5, delta if delta is not None else '—',
                         fill=GREEN_MED if (delta is not None and delta<0) else
                              (RED_MED if (delta is not None and delta>0) else YELLOW),
                         font=bf(10,True), align=ca(),
                         fmt='+0.00%;-0.00%' if delta is not None else '@')
    wc(ws3, r, 6, note,  fill=f, font=bf(9), align=la())

# ── 인원 비교 ─────────────────────────────────────────────
r_hc = 6+len(factor_data)+2
mh(ws3, r_hc, 2, 6, 'II. 인원 변동 (인건비 원가 영향)')
ws3.row_dimensions[r_hc].height = 20
r_hc += 1
for j,h in enumerate(['구분','2026 Rev27','2027 Jan','2027 Dec','비고'],2):
    wc(ws3, r_hc, j, h, fill=BLUE_SUB, font=hf(10), align=ca())

hc_data = [
    ('외국인',             15.3, 15,  16,  ''),
    ('베트남 직원(Staff)', 253.8,237, 219, ''),
    ('생산직 근로자',      620.0,497, 418, ''),
    ('전체 합계',          860.0,749, 653, '2026연평균→2027 Jan/Dec'),
    ('총 인건비(USD)',      7962078, None, None, '2026: $7.96M / 2027: 추정 ~$7.4M'),
]

for i,(lbl,v26,v27s,v27e,note) in enumerate(hc_data):
    r = r_hc+1+i
    ws3.row_dimensions[r].height = 16
    is_total = '합계' in lbl or '인건비' in lbl
    bold_f = bf(10, is_total)
    f = BLUE_LITE if is_total else GRAY_LITE
    wc(ws3, r, 2, lbl,  fill=GRAY_MED if is_total else GRAY_LITE, font=bold_f, align=la())
    if '인건비' in lbl:
        wc(ws3, r, 3, v26,  fill=f, font=bold_f, align=ra(), fmt='#,##0')
        wc(ws3, r, 4, '',   fill=f, font=bold_f, align=ra())
        wc(ws3, r, 5, '',   fill=f, font=bold_f, align=ra())
    else:
        wc(ws3, r, 3, v26,  fill=f, font=bold_f, align=ra(), fmt='0.0')
        wc(ws3, r, 4, v27s if v27s else '',
                            fill=GREEN_LITE, font=bold_f, align=ra(), fmt='0')
        wc(ws3, r, 5, v27e if v27e else '',
                            fill=GREEN_MED,  font=bold_f, align=ra(), fmt='0')
    wc(ws3, r, 6, note, fill=f, font=bf(9), align=la())

# ── 종합 진단 ─────────────────────────────────────────────
r_diag = r_hc+1+len(hc_data)+2
mh(ws3, r_diag, 2, 6, 'III. 종합 진단 및 시사점')
ws3.row_dimensions[r_diag].height = 20
r_diag += 1
for j,h in enumerate(['구분','내용','판정'],2):
    wc(ws3, r_diag, j, h, fill=BLUE_SUB, font=hf(10), align=ca())
ws3.column_dimensions['C'].width = 45

diag_data = [
    ('긍정 요인 ①',
     'Write-off $681K 소멸 → 2027 COGS율 -1.6%p 자동 개선',
     '✅ 확정'),
    ('긍정 요인 ②',
     '인원 860→653명(-207명) 감축 → 직접인건비 절감 효과',
     '✅ 확정'),
    ('긍정 요인 ③',
     'Q4(10~12월) COGS% 65.7% — 하반기 안정화 확인',
     '✅ 추세'),
    ('부정 요인 ①',
     'LGIT $5.6M→$0.85M(-85%) — 고마진 Mix 이탈, S36 재료비 감소 상쇄',
     '⚠ 중요'),
    ('부정 요인 ②',
     'Chromate 처리비 +78% — 삼성 A38 화성처리 증가, 재료비율 악화',
     '⚠ 확인'),
    ('부정 요인 ③',
     '2027 H1 COGS% 73.7% — 신규 SOP 라인 초기 비효율',
     '⚠ 구조적'),
    ('핵심 과제',
     'COGM 실질율 75.6%(2026)→70.8%(2027)이나 계획 목표(59.6%) 대비 여전히 11%p 초과',
     '❌ 미해소'),
]

for i,(cat,cont,verdict) in enumerate(diag_data):
    r = r_diag+1+i
    ws3.row_dimensions[r].height = 22
    f = GREEN_LITE if '✅' in verdict else (RED_LITE if '❌' in verdict else YELLOW)
    wc(ws3, r, 2, cat,     fill=GRAY_LITE, font=bf(10,True), align=ca())
    ws3.merge_cells(start_row=r, start_column=3, end_row=r, end_column=5)
    wc(ws3, r, 3, cont,    fill=f, font=bf(10), align=la())
    wc(ws3, r, 6, verdict, fill=f, font=bf(10,True), align=ca())

wb.save(OUTPUT)
print('저장 완료: ' + OUTPUT)
from openpyxl import load_workbook as lw
v = lw(OUTPUT)
print('시트: ' + str(v.sheetnames))
print('검증 완료.')
