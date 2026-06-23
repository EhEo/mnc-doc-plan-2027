# Rev27 비용 예측 방법론 분석 — 1·4월(실적) vs 5월 이후(예측)
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import glob as _g
from openpyxl import load_workbook

hits = _g.glob('../sources/*Rev27*.xlsx') + _g.glob('../sources/*Rev27*.XLSX')
if not hits:
    raise FileNotFoundError('Rev27 파일 없음')
SRC = hits[0]
print(f'파일: {SRC}')
wb = load_workbook(SRC, data_only=True)
print(f'시트 목록: {wb.sheetnames}\n')

MONTHS = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

def safe(v):
    if isinstance(v, (int, float)):
        return round(v, 2)
    return v

# ═══════════════════════════════════════════════════════════
# 1. IS 시트 월별 전체 데이터 추출
# ═══════════════════════════════════════════════════════════
print('='*70)
print('[IS 시트] 월별 전체 행 추출')
print('='*70)
ws_is = wb['10. IS']
# 헤더 확인 (1~5행)
for r in range(1, 6):
    row = {c.column_letter: c.value for c in ws_is[r] if c.value is not None}
    if row:
        print(f'  Row{r}: ' + ' | '.join(f'{k}={repr(str(v))[:20]}' for k,v in list(row.items())[:12]))

print()
# 전체 행 (A열 레이블 + B~M 월별 + N 연간)
is_data = {}  # row_num -> {label, months[12], total}
for r in range(1, 80):
    a = ws_is.cell(r, 1).value
    n = ws_is.cell(r, 14).value  # N열
    if a and str(a).strip():
        months_v = []
        for c in range(2, 14):  # B~M
            months_v.append(ws_is.cell(r, c).value)
        is_data[r] = {'label': str(a).strip(), 'months': months_v, 'total': n}
        print(f'  Row{r:2d} {str(a)[:35]:35s} | Jan={safe(months_v[0])} Apr={safe(months_v[3])} May={safe(months_v[4])} | Tot={safe(n)}')

# ═══════════════════════════════════════════════════════════
# 2. M Plan (제조원가) 월별 데이터
# ═══════════════════════════════════════════════════════════
print('\n' + '='*70)
print('[5. M Plan] 월별 전체 행 추출')
print('='*70)
ws_m = wb['5. M Plan']
# 헤더 확인
for r in range(1, 8):
    row = {c.column_letter: c.value for c in ws_m[r] if c.value is not None}
    if row:
        print(f'  Row{r}: ' + ' | '.join(f'{k}={repr(str(v))[:20]}' for k,v in list(row.items())[:14]))

print()
# A열 + 전체 열 파악 (어느 열이 Jan인지)
m_data = {}
for r in range(1, 120):
    a = ws_m.cell(r, 1).value
    if a and str(a).strip():
        row_vals = {ws_m.cell(r, c).column_letter: ws_m.cell(r, c).value
                    for c in range(1, 20) if ws_m.cell(r, c).value is not None}
        m_data[r] = row_vals
        # 숫자값만 모으기
        nums = {k: v for k, v in row_vals.items() if isinstance(v, (int, float))}
        print(f'  Row{r:3d} {str(a)[:35]:35s} | ' +
              ' '.join(f'{k}={round(v,0)}' for k,v in list(nums.items())[:12]))

# ═══════════════════════════════════════════════════════════
# 3. S Plan (매출) 고객사·모델별 수량·단가·금액
# ═══════════════════════════════════════════════════════════
print('\n' + '='*70)
print('[2. S Plan] 월별 수량·단가·금액 구조 파악')
print('='*70)
ws_s = wb['2. S Plan']
# 헤더 (1~5행)
for r in range(1, 8):
    row = {c.column_letter: c.value for c in ws_s[r] if c.value is not None}
    if row:
        print(f'  Row{r}: ' + ' | '.join(f'{k}={repr(str(v))[:18]}' for k,v in list(row.items())[:15]))
print()
# 주요 합계행 추출 (100행 내외에 있을 것)
for r in range(5, 120):
    a = ws_s.cell(r, 1).value
    b = ws_s.cell(r, 2).value
    c3 = ws_s.cell(r, 3).value
    if any(kw in str(a or '').upper()+str(b or '').upper()+str(c3 or '').upper()
           for kw in ['TOTAL','GRAND','SUBTOTAL','합계','소계']):
        nums = {}
        for col in range(1, 30):
            v = ws_s.cell(r, col).value
            if isinstance(v, (int, float)):
                nums[ws_s.cell(r, col).column_letter] = round(v, 0)
        print(f'  Row{r:3d} A={repr(str(a))[:20]} B={repr(str(b))[:15]} C={repr(str(c3))[:15]} | {nums}')

# ═══════════════════════════════════════════════════════════
# 4. L Plan (인건비) 월별 주요행
# ═══════════════════════════════════════════════════════════
print('\n' + '='*70)
print('[4. L PLAN a] 월별 인건비 구조')
print('='*70)
ws_la = wb['4. L PLAN a'] if '4. L PLAN a' in wb.sheetnames else None
if ws_la:
    for r in range(1, 8):
        row = {c.column_letter: c.value for c in ws_la[r] if c.value is not None}
        if row:
            print(f'  Row{r}: ' + ' | '.join(f'{k}={repr(str(v))[:18]}' for k,v in list(row.items())[:14]))
    print()
    for r in range(1, 120):
        a = ws_la.cell(r, 1).value
        if a and str(a).strip():
            nums = {}
            for col in range(2, 20):
                v = ws_la.cell(r, col).value
                if isinstance(v, (int, float)):
                    nums[ws_la.cell(r, col).column_letter] = round(v, 0)
            if nums:
                print(f'  Row{r:3d} {str(a)[:35]:35s} | {dict(list(nums.items())[:12])}')

# ═══════════════════════════════════════════════════════════
# 5. AP Plan (간접비) 월별
# ═══════════════════════════════════════════════════════════
print('\n' + '='*70)
print('[AP Plan] 간접비 월별 구조')
print('='*70)
if 'AP Plan' in wb.sheetnames:
    ws_ap = wb['AP Plan']
    for r in range(1, 6):
        row = {c.column_letter: c.value for c in ws_ap[r] if c.value is not None}
        if row:
            print(f'  Row{r}: ' + ' | '.join(f'{k}={repr(str(v))[:18]}' for k,v in list(row.items())[:14]))
    print()
    for r in range(1, 80):
        a = ws_ap.cell(r, 1).value
        if a and str(a).strip():
            nums = {}
            for col in range(2, 16):
                v = ws_ap.cell(r, col).value
                if isinstance(v, (int, float)):
                    nums[ws_ap.cell(r, col).column_letter] = round(v, 0)
            if nums:
                print(f'  Row{r:3d} {str(a)[:35]:35s} | {dict(list(nums.items())[:12])}')

print('\n===== 완료 =====')
