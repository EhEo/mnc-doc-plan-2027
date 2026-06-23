# Rev2 상세 데이터 추출 — 인원절감·매출구성·COGS 분석용
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from openpyxl import load_workbook
from openpyxl.chartsheet import Chartsheet

wb = load_workbook('../working/20260615-2027Y BIZ Plan_Rev2.xlsx', data_only=True)

# ── 1. L PLAN a 전체 (인원 절감 섹션 포함) ───────────────────
print('===== L PLAN a 전체 =====')
ws = wb['4. L PLAN a']
for r in range(1, 70):
    row_data = {c.column_letter: c.value for c in ws[r] if c.value is not None}
    if row_data:
        line = ' | '.join(f'{k}={repr(str(v))[:35]}' for k, v in sorted(row_data.items())[:8])
        print(f'  Row{r:3d}: {line}')

# ── 2. L PLAN 주요행 F~Q열 (Jan.27~Dec.27 인원 월별) ──────────
print('\n===== L PLAN 월별 인원 (Row13 외국인, Row25 VN, Row40 합계) =====')
ws_l = wb['4. L PLAN']
# Row 4가 헤더
hdr = {c.column_letter: c.value for c in ws_l[4] if c.value is not None}
print('  헤더:', {k: v for k, v in hdr.items() if k >= 'E' and k <= 'R'})

for r in [13, 25, 29, 36, 40, 53, 66, 79, 90]:
    row_data = {c.column_letter: c.value for c in ws_l[r] if c.value is not None}
    label = row_data.get('A', row_data.get('B', ''))
    # F~Q = Jan~Dec 2027
    monthly = {k: round(v, 1) if isinstance(v, float) else v
               for k, v in row_data.items() if 'F' <= k <= 'Q'}
    e = row_data.get('E', '')
    print(f'\n  Row{r} [{label}]:')
    print(f'    E(ST)={e}')
    print(f'    월별: {monthly}')

# ── 3. S Plan 매출금액 전체 (Row110 이후) ────────────────────
print('\n===== S Plan 매출금액 전체 (Row110+) =====')
ws_s = wb['2. S Plan']
for r in range(110, 220):
    row_data = {c.column_letter: c.value for c in ws_s[r] if c.value is not None}
    if not row_data:
        continue
    a = row_data.get('A', '')
    b = row_data.get('B', '')
    c_v = row_data.get('C', '')
    f = row_data.get('F', '')
    g = row_data.get('G', '')
    x = row_data.get('X', '')
    if x or a or c_v:
        print(f'  Row{r}: A={repr(str(a))[:20]} C={repr(str(c_v))[:15]} F={repr(str(f))[:20]} G={g} X={x}')

# ── 4. IS 월별 매출·COGS (B~N열) ────────────────────────────
print('\n===== IS 월별 매출·COGS (B~N) =====')
ws_is = wb['10. IS']
for r in [4, 5, 8, 9, 11, 18, 19]:
    row_data = {c.column_letter: c.value for c in ws_is[r] if c.value is not None}
    label = row_data.get('A', '')
    monthly = {}
    for col in 'BCDEFGHIJKLMN':
        v = row_data.get(col)
        if v is not None:
            monthly[col] = round(v, 0) if isinstance(v, float) else v
    print(f'  Row{r} [{label}]: {monthly}')

# ── 5. 인원 절감 월별 비용 영향 (L PLAN Row79 = Grand Total 급여) ─
print('\n===== L PLAN Row79 Grand Total 급여 월별 =====')
ws_l2 = wb['4. L PLAN']
r79 = {c.column_letter: c.value for c in ws_l2[79] if c.value is not None}
label = r79.get('A', '')
print(f'  [{label}]')
for col in 'FGHIJKLMNOQ':  # F=Jan.27 ~ Q=Dec.27 (approx)
    v = r79.get(col)
    if v is not None:
        print(f'    {col}: {round(v,0) if isinstance(v,float) else v}')

# ── 6. Sub-L plan 시트 존재 시 ─────────────────────────────
print('\n===== Sub-L plan 확인 =====')
if 'Sub-L plan' in wb.sheetnames:
    ws_sub = wb['Sub-L plan']
    for r in range(1, 40):
        row_data = {c.column_letter: c.value for c in ws_sub[r] if c.value is not None}
        if row_data:
            line = ' | '.join(f'{k}={repr(str(v))[:30]}' for k,v in list(row_data.items())[:6])
            print(f'  Row{r:3d}: {line}')

# ── 7. 요약 시트 ──────────────────────────────────────────
print('\n===== 요약 시트 =====')
if '요약' in wb.sheetnames:
    ws_sum = wb['요약']
    for r in range(1, 60):
        row_data = {c.column_letter: c.value for c in ws_sum[r] if c.value is not None}
        if row_data:
            line = ' | '.join(f'{k}={repr(str(v))[:35]}' for k,v in list(row_data.items())[:6])
            print(f'  Row{r:3d}: {line}')
