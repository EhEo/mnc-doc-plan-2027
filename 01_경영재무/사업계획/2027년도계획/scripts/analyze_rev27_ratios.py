# Rev27 비용 예측 방법론 심층 분석 — 비율 패턴 및 계산 방식 역추적
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import glob as _g
from openpyxl import load_workbook

hits = _g.glob('../sources/*Rev27*.xlsx') + _g.glob('../sources/*Rev27*.XLSX')
SRC  = hits[0]
wb   = load_workbook(SRC, data_only=True)

MONTHS = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

def nv(ws, row, col):
    """숫자 값 반환, 없으면 0"""
    v = ws.cell(row, col).value
    return float(v) if isinstance(v, (int, float)) else 0.0

def pct(a, b):
    return f'{a/b*100:.1f}%' if b else 'N/A'

def diff(a, b):
    return f'{(a-b)/b*100:+.1f}%' if b else 'N/A'

# ═══════════════════════════════════════════════════════════
# IS 시트 월별 비율 분석
# IS: B=Jan(col2) ~ M=Dec(col13), N=Total(col14)
# ═══════════════════════════════════════════════════════════
ws_is = wb['10. IS']

print('='*80)
print('【IS 시트】 월별 주요 비율 분석')
print('  실적 확정: Jan(1월), Apr(4월)  /  예측: Feb·Mar·May~Dec')
print('='*80)

# IS 행 정의
IS_ROWS = {
    'Sales':     4,
    'COGM':      5,
    'WriteOff':  6,
    'GrossProfit':8,
    'SGA':       9,
    'OpIncome':  11,
    'Interest':  12,
    'OtherExp':  13,
    'NetIncome': 18,
    'Depr':      20,
    'Amort':     21,
}

# 월별 값 추출 (col2~col13)
data = {}
for k, r in IS_ROWS.items():
    data[k] = [nv(ws_is, r, c) for c in range(2, 14)]

sales = data['Sales']

print(f'\n{"항목":<22}', end='')
for m in MONTHS: print(f'{m:>9}', end='')
print(f'{"연간":>9}')
print('-'*130)

def print_row(label, vals, fmt='$', bold_idx=[0,3]):
    print(f'{label:<22}', end='')
    for i, v in enumerate(vals):
        marker = '★' if i in bold_idx else ' '
        if fmt == '$':
            print(f'{marker}{v/1000:>7.0f}K', end='')
        else:
            print(f'{marker}{v*100:>7.1f}%', end='')
    total = sum(vals)
    print(f' {total/1000:>8.0f}K' if fmt=='$' else f' {(sum(vals)/12)*100:.1f}%avg')

print_row('Sales',      sales)
print_row('COGM',       data['COGM'])
print_row('WriteOff',   data['WriteOff'])
print_row('GrossProfit',data['GrossProfit'])
print_row('SG&A',       data['SGA'])
print_row('OpIncome',   data['OpIncome'])
print_row('Depreciation',data['Depr'])
print_row('Amortization',data['Amort'])

print(f'\n{"비율":<22}', end='')
for m in MONTHS: print(f'{m:>9}', end='')
print()
print('-'*130)

def ratio_row(label, numer, denom, bold_idx=[0,3]):
    vals = [n/d if d else 0 for n, d in zip(numer, denom)]
    print(f'{label:<22}', end='')
    for i, v in enumerate(vals):
        marker = '★' if i in bold_idx else ' '
        print(f'{marker}{v*100:>7.1f}%', end='')
    avg = sum(vals)/len(vals)*100
    print(f' avg={avg:.1f}%')
    return vals

cogm_ratio = ratio_row('COGM/Sales',     data['COGM'],     sales)
sga_ratio  = ratio_row('SG&A/Sales',     data['SGA'],      sales)
gp_ratio   = ratio_row('GP/Sales',       data['GrossProfit'], sales)
op_ratio   = ratio_row('OpInc/Sales',    data['OpIncome'], sales)

# ═══════════════════════════════════════════════════════════
# COGM/Sales 패턴 분석 — 1·4월 실적 vs 예측
# ═══════════════════════════════════════════════════════════
print('\n' + '='*80)
print('【COGM/Sales 비율 패턴】 실적(★) vs 예측')
print('='*80)

actual_idx  = [0, 3]   # Jan=0, Apr=3
forecast_idx= [1,2,4,5,6,7,8,9,10,11]  # Feb,Mar,May~Dec

act_ratios  = [cogm_ratio[i] for i in actual_idx]
fc_ratios   = [cogm_ratio[i] for i in forecast_idx]
act_avg = sum(act_ratios)/len(act_ratios)
fc_avg  = sum(fc_ratios)/len(fc_ratios)
fc_min  = min(fc_ratios)
fc_max  = max(fc_ratios)

print(f'  실적 평균 (Jan·Apr):  {act_avg*100:.1f}%  (Jan={cogm_ratio[0]*100:.1f}%, Apr={cogm_ratio[3]*100:.1f}%)')
print(f'  예측 평균 (10개월):   {fc_avg*100:.1f}%  (범위: {fc_min*100:.1f}%~{fc_max*100:.1f}%)')
print(f'  차이:                {(fc_avg-act_avg)*100:+.1f}%p')
print()

# 예측 비율의 일관성 체크 — 매출 연동인지, 고정값인지
print('  [예측 COGM: 월별 산출 방식 추정]')
for i in forecast_idx:
    m  = MONTHS[i]
    s  = sales[i]
    c  = data['COGM'][i]
    r  = c/s if s else 0
    # 인접 실적 월과 비교
    nearest_act = data['COGM'][0] if i < 3 else data['COGM'][3]
    nearest_s   = sales[0] if i < 3 else sales[3]
    act_r = nearest_act/nearest_s if nearest_s else 0
    note = ''
    if abs(r - fc_ratios[0]) < 0.005:
        note = '← 5월 기준 고정 비율 반복'
    elif abs(r - act_r) < 0.01:
        note = '← 인접 실적과 유사'
    print(f'    {m}: COGM={c/1000:.0f}K  Sales={s/1000:.0f}K  비율={r*100:.1f}%  {note}')

# ═══════════════════════════════════════════════════════════
# SG&A 패턴 분석
# ═══════════════════════════════════════════════════════════
print('\n' + '='*80)
print('【SG&A 패턴】 고정비 vs 변동비 성격 분석')
print('='*80)
sga = data['SGA']
print(f'  {"월":<6} {"SG&A($K)":>10} {"매출($K)":>10} {"SG&A/Sales":>12} {"전월대비":>10}')
print(f'  {"-"*52}')
for i, m in enumerate(MONTHS):
    marker = '★실적' if i in [0,3] else '  예측'
    prev_diff = f'{(sga[i]-sga[i-1])/sga[i-1]*100:+.1f}%' if i>0 and sga[i-1] else '—'
    print(f'  {marker} {m:<4} {sga[i]/1000:>9.1f}K  {sales[i]/1000:>9.1f}K  {sga[i]/sales[i]*100:>10.1f}%  {prev_diff:>10}')

# SG&A 고정비 vs 변동비 판정
sga_jan = sga[0]; sga_apr = sga[3]
sga_fc = [sga[i] for i in forecast_idx]
sga_fc_std = (max(sga_fc)-min(sga_fc))/max(sga_fc)*100 if max(sga_fc) else 0
print(f'\n  SG&A 예측 범위 변동폭: {sga_fc_std:.1f}% → {"거의 고정비" if sga_fc_std < 10 else "매출 연동" if sga_fc_std > 20 else "반고정"}')

# ═══════════════════════════════════════════════════════════
# M Plan 재료비 패턴 분석
# IS: COGM = 재료비 + 인건비 + 경비
# M Plan Grand Total(Row73, F~Q) = 재료비 합계
# ═══════════════════════════════════════════════════════════
print('\n' + '='*80)
print('【재료비 패턴】 M Plan Grand Total vs Sales')
print('='*80)
ws_m = wb['5. M Plan']
# Row73: Grand Total, F=Jan(col6)~Q=Dec(col17)
mat_total = [nv(ws_m, 73, c) for c in range(6, 18)]
# Row36: ADC12 금액, Row57: Chromate, Row71: A Project
adc12 = [nv(ws_m, 36, c) for c in range(6, 18)]
chrom = [nv(ws_m, 57, c) for c in range(6, 18)]
aproj = [nv(ws_m, 71, c) for c in range(6, 18)]

# S36 금액: Row17 금액 (Product Material Amount)
s36_amt = [nv(ws_m, 17, c) for c in range(6, 18)]

print(f'  {"월":<6} {"재료비($K)":>10} {"매출($K)":>10} {"재료비/매출":>12} {"ADC12$K":>9} {"S36$K":>8} {"Chrom$K":>9}')
print(f'  {"-"*68}')
for i, m in enumerate(MONTHS):
    marker = '★실적' if i in [0,3] else '  예측'
    mat_r = mat_total[i]/sales[i]*100 if sales[i] else 0
    print(f'  {marker} {m:<4} {mat_total[i]/1000:>9.1f}K  {sales[i]/1000:>9.1f}K  {mat_r:>10.1f}%  {adc12[i]/1000:>8.0f}K  {s36_amt[i]/1000:>7.0f}K  {chrom[i]/1000:>8.0f}K')

# ═══════════════════════════════════════════════════════════
# S Plan 수량 기반 단가 적용 검증
# ═══════════════════════════════════════════════════════════
print('\n' + '='*80)
print('【S Plan】 수량×단가=금액 검증 (실적월 vs 예측월 단가 일관성)')
print('='*80)
ws_s = wb['2. S Plan']
# Row 4 헤더: L=Jan.26(col12), M=Feb.26(col13)...W=Dec.26(col23), X=Total(col24)
# Col: L=12, M=13, N=14, O=15, P=16, Q=17, R=18, S=19, T=20, U=21, V=22, W=23

# 주요 모델 단가(G열=col7) vs 월별 매출
# Row6: A15/17, Row7: A36, Row9: A18(추정), ...
model_rows = []
for r in range(5, 105):
    f_val  = ws_s.cell(r, 6).value   # F열 = Model명
    g_val  = ws_s.cell(r, 7).value   # G열 = U/P 단가
    if g_val and isinstance(g_val, (int, float)) and g_val > 0:
        # 월별 수량 L~W = col12~col23
        qty = [ws_s.cell(r, c).value for c in range(12, 24)]
        qty = [float(v) if isinstance(v, (int,float)) else 0 for v in qty]
        total_qty = sum(qty)
        if total_qty > 0 and f_val:
            model_rows.append({'row': r, 'model': str(f_val)[:20],
                                'up': float(g_val), 'qty': qty,
                                'total': total_qty})

print(f'  {"모델":<22} {"단가(U/P)":>10} {"Jan수량":>9} {"Apr수량":>9} {"May수량":>9} {"Jun수량":>9} {"비고":>20}')
print(f'  {"-"*82}')
for mr in model_rows[:20]:
    q = mr['qty']
    # 5월 이후 수량이 일정한지 체크
    fc_qty = q[4:]  # May~Dec
    fc_nonzero = [v for v in fc_qty if v > 0]
    if not fc_nonzero: continue
    fc_range = (max(fc_nonzero)-min(fc_nonzero))/max(fc_nonzero)*100 if max(fc_nonzero) else 0
    note = ''
    if fc_range < 5:   note = '예측 수량 거의 일정'
    elif fc_range < 20: note = '완만한 증감'
    else:               note = f'변동폭 {fc_range:.0f}%'
    print(f'  {mr["model"]:<22} {mr["up"]:>10.3f} {q[0]:>9.0f} {q[3]:>9.0f} {q[4]:>9.0f} {q[5]:>9.0f} {note:>20}')

# ═══════════════════════════════════════════════════════════
# L Plan 인건비 월별 구조
# ═══════════════════════════════════════════════════════════
print('\n' + '='*80)
print('【L PLAN a】 인건비 월별 — 고정 vs 인원수 연동')
print('='*80)
ws_la = wb['4. L PLAN a']
# 헤더 Row4: E=ST-Person, F=Jan.25...
# 실제 2026 데이터가 어느 열부터인지 파악
# 헤더를 다시 읽어서 2026 열 위치 확인
hdr_row = {}
for c in range(1, 30):
    v = ws_la.cell(4, c).value
    if v:
        hdr_row[c] = str(v)
print('  헤더(Row4):', {c: v for c, v in hdr_row.items() if '26' in str(v) or '25' in str(v)})

# 2026 데이터 열 찾기
jan26_col = None
for c, v in hdr_row.items():
    if 'Jan.26' in v or 'Jan 26' in v or 'Jan.2026' in v:
        jan26_col = c
        break
if not jan26_col:
    # Jan.25 이후 12+1=13번째 열이 Jan.26일 수 있음
    for c, v in hdr_row.items():
        if 'Jan.25' in v or 'Jan 25' in v:
            jan26_col = c + 12
            print(f'  → Jan.26 추정 열: {jan26_col} ({ws_la.cell(4, jan26_col).value})')
            break

if jan26_col:
    print(f'  Jan.26 열: {jan26_col}')
    # 총 인건비 합계행 탐색
    for r in range(1, 130):
        a = ws_la.cell(r, 1).value
        b = ws_la.cell(r, 2).value
        label = f'{a} {b}'.strip()
        if any(kw in str(label).upper() for kw in ['GRAND TOTAL','TOTAL LABOR','합계','TOTAL SALARY','ALL TOTAL']):
            vals = [nv(ws_la, r, jan26_col+i) for i in range(12)]
            if any(v > 0 for v in vals):
                print(f'\n  Row{r} {label[:40]}:')
                for i, (m, v) in enumerate(zip(MONTHS, vals)):
                    marker = '★실적' if i in [0,3] else '  예측'
                    print(f'    {marker} {m}: ${v/1000:.1f}K', end='  ')
                    if (i+1)%4==0: print()
                print()

    # 인원수 합계 탐색
    for r in range(1, 130):
        a = ws_la.cell(r, 1).value
        b = ws_la.cell(r, 2).value
        label = f'{a} {b}'.strip()
        if any(kw in str(label).upper() for kw in ['GRAND TOTAL','TOTAL PERSON']):
            e_val = nv(ws_la, r, 5)  # E열 ST-Person
            if e_val > 0:
                vals = [nv(ws_la, r, jan26_col+i) for i in range(12)]
                if any(v > 0 for v in vals):
                    print(f'\n  Row{r} 인원 {label[:40]}:')
                    for i, (m, v) in enumerate(zip(MONTHS, vals)):
                        marker = '★실적' if i in [0,3] else '  예측'
                        print(f'    {marker} {m}: {v:.0f}명', end='  ')
                        if (i+1)%4==0: print()
                    print()
                    break
else:
    print('  Jan.26 열 찾기 실패 — 전체 헤더:', hdr_row)
    # 그냥 주요 행을 출력
    for r in range(1, 130):
        a = ws_la.cell(r, 1).value
        if a and any(kw in str(a).upper() for kw in ['TOTAL','GRAND']):
            nums = {c: round(ws_la.cell(r,c).value,0)
                    for c in range(2,30)
                    if isinstance(ws_la.cell(r,c).value,(int,float))}
            if nums:
                print(f'  Row{r} {str(a)[:40]}: {dict(list(nums.items())[:14])}')

# ═══════════════════════════════════════════════════════════
# AP Plan 간접비 패턴
# ═══════════════════════════════════════════════════════════
print('\n' + '='*80)
print('【AP Plan】 간접비 (SG&A 구성) 월별 패턴')
print('='*80)
if 'AP Plan' in wb.sheetnames:
    ws_ap = wb['AP Plan']
    # 헤더 확인
    hdr_ap = {}
    for r in range(1,6):
        for c in range(1, 20):
            v = ws_ap.cell(r, c).value
            if v and ('26' in str(v) or 'Jan' in str(v) or 'Total' in str(v)):
                hdr_ap[f'R{r}C{c}'] = str(v)[:20]
    print('  컬럼 헤더(26 포함):', hdr_ap)
    print()
    for r in range(1, 80):
        a = ws_ap.cell(r, 1).value
        if a and str(a).strip():
            nums = {}
            for c in range(2, 18):
                v = ws_ap.cell(r, c).value
                if isinstance(v, (int, float)):
                    nums[ws_ap.cell(r, c).column_letter] = round(v, 0)
            if len(nums) >= 4:
                print(f'  Row{r:3d} {str(a)[:35]:35s} | {dict(list(nums.items())[:13])}')

print('\n===== 분석 완료 =====')
