# Rev27 L PLAN + AP Plan 상세 구조 확인
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import glob as _g
from openpyxl import load_workbook

hits = _g.glob('../sources/*Rev27*.xlsx') + _g.glob('../sources/*Rev27*.XLSX')
wb   = load_workbook(hits[0], data_only=True)
MONTHS = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

def nv(ws, row, col):
    v = ws.cell(row, col).value
    return float(v) if isinstance(v, (int, float)) else 0.0

# ═══════════════════════════════════════════════════════════
# 4. L PLAN (별도 시트) — 2026 인건비
# ═══════════════════════════════════════════════════════════
print('='*70)
print('[4. L PLAN] 시트 구조 파악')
print('='*70)
ws_lp = wb['4. L PLAN']

# 헤더 전체 출력 (1~6행)
for r in range(1, 7):
    row = {}
    for c in range(1, 30):
        v = ws_lp.cell(r, c).value
        if v is not None:
            row[ws_lp.cell(r,c).column_letter] = str(v)[:18]
    if row:
        print(f'  Row{r}: ' + ' | '.join(f'{k}={v}' for k,v in list(row.items())[:16]))

print()
# 주요 합계 행 탐색
for r in range(1, 120):
    a = ws_lp.cell(r, 1).value
    b = ws_lp.cell(r, 2).value
    label = f'{a or ""} {b or ""}'.strip()
    if any(kw in str(label).upper() for kw in ['GRAND TOTAL','TOTAL LABOR','합계']):
        nums = {}
        for c in range(1, 25):
            v = ws_lp.cell(r, c).value
            if isinstance(v, (int, float)) and v > 0:
                nums[ws_lp.cell(r, c).column_letter] = round(v, 0)
        if nums:
            print(f'  Row{r:3d} "{label[:40]}" : {dict(list(nums.items())[:16])}')

# ═══════════════════════════════════════════════════════════
# 4. L PLAN a — 실제 2026 데이터 위치 재탐색
# ═══════════════════════════════════════════════════════════
print('\n' + '='*70)
print('[4. L PLAN a] 전체 헤더 및 2026 위치 탐색')
print('='*70)
ws_la = wb['4. L PLAN a']
for r in range(1, 7):
    row = {}
    for c in range(1, 35):
        v = ws_la.cell(r, c).value
        if v is not None:
            row[ws_la.cell(r,c).column_letter] = str(v)[:16]
    if row:
        print(f'  Row{r}: ' + ' | '.join(f'{k}={v}' for k,v in list(row.items())[:18]))

# Grand Total 행의 전체 값
print()
for r in range(80, 130):
    a = ws_la.cell(r, 1).value
    b = ws_la.cell(r, 2).value
    label = f'{a or ""} {b or ""}'.strip()
    if 'GRAND' in str(label).upper() or 'TOTAL' in str(label).upper():
        nums = {}
        for c in range(1, 36):
            v = ws_la.cell(r, c).value
            if isinstance(v, (int, float)) and v > 100:  # 인건비는 100 이상
                nums[ws_la.cell(r, c).column_letter] = round(v/1000, 1)
        if nums:
            print(f'  Row{r:3d} "{label[:40]}" (단위:$K): {dict(list(nums.items())[:18])}')

# ═══════════════════════════════════════════════════════════
# AP Plan — 전체 항목 및 컬럼 구조
# ═══════════════════════════════════════════════════════════
print('\n' + '='*70)
print('[AP Plan] 전체 구조 — 컬럼 헤더 및 항목')
print('='*70)
ws_ap = wb['AP Plan']

# 1~5행 전체 컬럼 출력
for r in range(1, 7):
    row = {}
    for c in range(1, 20):
        v = ws_ap.cell(r, c).value
        if v is not None:
            row[ws_ap.cell(r, c).column_letter] = str(v)[:18]
    if row:
        print(f'  Row{r}: ' + ' | '.join(f'{k}={v}' for k, v in list(row.items())[:16]))

print()
# 전체 항목 + 수치 출력
for r in range(1, 80):
    a = ws_ap.cell(r, 1).value
    if not (a and str(a).strip()): continue
    nums = {}
    for c in range(2, 18):
        v = ws_ap.cell(r, c).value
        if isinstance(v, (int, float)):
            nums[ws_ap.cell(r, c).column_letter] = round(v, 0)
    lbl = str(a).strip()
    if nums:
        print(f'  Row{r:3d} {lbl[:38]:38s} | {dict(list(nums.items())[:14])}')

# ═══════════════════════════════════════════════════════════
# 1. Assumption — 예측 계산의 기준값 확인
# ═══════════════════════════════════════════════════════════
print('\n' + '='*70)
print('[1. Assumption] 예측 기준값 (단가·환율·비율 등)')
print('='*70)
ws_as = wb['1. Assumption']
for r in range(1, 60):
    row = {}
    for c in range(1, 12):
        v = ws_as.cell(r, c).value
        if v is not None:
            row[ws_as.cell(r, c).column_letter] = str(v)[:22]
    if row:
        print(f'  Row{r:2d}: ' + ' | '.join(f'{k}={v}' for k, v in list(row.items())[:10]))

print('\n===== 완료 =====')
