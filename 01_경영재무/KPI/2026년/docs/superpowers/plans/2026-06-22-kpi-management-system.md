# KPI 프로젝트 관리 시스템 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** M&C Electronics Vina의 KPI 수립→확정→월간추적→연말평가 전체 라이프사이클을 관리하는 로컬 대시보드 + 멀티에이전트 분석 시스템 구축

**Architecture:** Excel 기반 데이터 입력(부서별) → Python 처리 엔진(검증·변환·분석) → 정적 HTML 대시보드(브라우저 직접 열기) + 기존 MultiAgent 오케스트레이터(KPI 품질 분석·월간 리뷰)

**Tech Stack:** Python 3 (openpyxl, jinja2, json), HTML5/CSS3/JavaScript (외부 CDN 없음), 기존 claude-main / codex-critic 오케스트레이터 (CLAUDE.md 기준)

---

## 서브시스템 구성

| Phase | 서브시스템 | 산출물 | 선행 조건 |
|-------|-----------|-------|---------|
| A | 폴더 구조 + 프로세스 문서 | 폴더·MD 문서 | 없음 |
| B | Excel KPI 템플릿 | .xlsx 파일 5종 | A |
| C | Python 데이터 엔진 | .py 스크립트 4종 | A, B |
| D | HTML 대시보드 | index.html + dept 페이지 | C |
| E | 멀티에이전트 분석 연동 | 분석 태스크 템플릿 + 스크립트 | C, 기존 오케스트레이터 |

---

## 파일 구조 맵

```
01_경영재무/KPI/2026년/
├── kpi-system/
│   ├── 00_프로세스/
│   │   ├── KPI_전체_라이프사이클.md
│   │   ├── KPI_수립_가이드.md
│   │   ├── 월간보고_절차.md
│   │   └── 연말평가_절차.md
│   ├── 01_KPI수립_2026H2/
│   │   ├── 00_회사전략목표.md
│   │   ├── 관리부문/
│   │   │   ├── KPI_수립서_관리부문.xlsx   ← 부서가 작성
│   │   │   └── kpi_data.json              ← Python 생성
│   │   ├── 생산1부문/   (동일 구조)
│   │   ├── 생산2부문/   (동일 구조)
│   │   ├── 품질부문/    (동일 구조)
│   │   └── 개발영업부문/ (동일 구조)
│   ├── 02_월간추적/
│   │   ├── TEMPLATE_월간실적.xlsx
│   │   ├── 2026-07/
│   │   │   ├── 관리부문_07실적.xlsx
│   │   │   └── [각 부문]/
│   │   └── 2026-08/ … 12/  (폴더만 사전 생성)
│   ├── 03_분기보고/
│   │   ├── Q3_2026/
│   │   └── Q4_2026/
│   ├── 04_연말평가/
│   │   └── 2026_연말평가/
│   ├── dashboard/
│   │   ├── index.html            ← Python 생성
│   │   ├── dept_관리부문.html    ← Python 생성
│   │   ├── dept_생산1부문.html
│   │   ├── dept_생산2부문.html
│   │   ├── dept_품질부문.html
│   │   ├── dept_개발영업부문.html
│   │   ├── css/style.css
│   │   └── js/app.js
│   ├── scripts/
│   │   ├── 01_validate_kpi.py    ← JSON 스키마 검증
│   │   ├── 02_excel_to_json.py   ← Excel → JSON 변환
│   │   ├── 03_generate_dashboard.py ← HTML 대시보드 생성
│   │   └── 04_analyze_kpi_agent.py  ← 멀티에이전트 분석 트리거
│   └── templates/
│       ├── KPI_수립서_TEMPLATE.xlsx
│       ├── 월간실적_TEMPLATE.xlsx
│       └── dashboard_dept.html.j2  ← Jinja2 템플릿
└── tasks/   ← 기존 오케스트레이터 폴더 (건드리지 않음)
```

---

## Phase A: 폴더 구조 + 프로세스 문서

### Task 1: 전체 폴더 구조 생성

**Files:**
- Create: `kpi-system/` 전체 하위 폴더

- [ ] **Step 1: 폴더 생성 스크립트 실행**

```powershell
$base = "D:\Michael\OneDrive - Team Redpanda\ClaudeCowork\01_경영재무\KPI\2026년\kpi-system"
$depts = @("관리부문","생산1부문","생산2부문","품질부문","개발영업부문")
$months = @("2026-07","2026-08","2026-09","2026-10","2026-11","2026-12")

# 메인 폴더
"00_프로세스","01_KPI수립_2026H2","02_월간추적","03_분기보고","04_연말평가","dashboard","dashboard/css","dashboard/js","scripts","templates" | ForEach-Object { New-Item -ItemType Directory -Force "$base\$_" }

# 부문별 폴더
$depts | ForEach-Object { New-Item -ItemType Directory -Force "$base\01_KPI수립_2026H2\$_" }

# 월간 추적 폴더
$months | ForEach-Object { New-Item -ItemType Directory -Force "$base\02_월간추적\$_"; $depts | ForEach-Object { New-Item -ItemType Directory -Force "$base\02_월간추적\$m\$_" -ErrorAction SilentlyContinue } }

# 분기/연말 폴더
"Q3_2026","Q4_2026" | ForEach-Object { New-Item -ItemType Directory -Force "$base\03_분기보고\$_" }
New-Item -ItemType Directory -Force "$base\04_연말평가\2026_연말평가"
```

- [ ] **Step 2: 폴더 생성 확인**

```powershell
Get-ChildItem -Recurse -Directory "D:\Michael\OneDrive - Team Redpanda\ClaudeCowork\01_경영재무\KPI\2026년\kpi-system" | Select-Object FullName
```
Expected: 40+ 폴더 목록 출력

---

### Task 2: KPI 전체 라이프사이클 프로세스 문서 작성

**Files:**
- Create: `kpi-system/00_프로세스/KPI_전체_라이프사이클.md`
- Create: `kpi-system/00_프로세스/KPI_수립_가이드.md`
- Create: `kpi-system/00_프로세스/월간보고_절차.md`
- Create: `kpi-system/00_프로세스/연말평가_절차.md`

- [ ] **Step 1: 라이프사이클 문서 작성**

파일 내용 (`KPI_전체_라이프사이클.md`):

```markdown
# M&C Electronics Vina KPI 관리 전체 프로세스

## 연간 KPI 라이프사이클

```
[6월 말] KPI 수립 → [7월] 확정·공표 → [매월] 실적 입력 → [Q3/Q4] 분기 점검 → [12월] 연말 평가
```

## Phase 1: KPI 수립 (6월~7월)

| 단계 | 담당 | 기한 | 산출물 |
|------|------|------|--------|
| 회사 전략목표 공유 | 경영지원 | 6/25 | 전략목표.md |
| 부문별 KPI 초안 작성 | 각 부문장 | 6/28 | KPI_수립서_[부문].xlsx |
| 내부 검토 회의 | 전 부문장 | 6/30 | 회의록 |
| KPI 확정·서명 | 사장 | 7/5 | 확정본 xlsx |
| 시스템 등록 | 경영지원 | 7/7 | kpi_data.json |

## Phase 2: 월간 추적 (7월~12월)

| 단계 | 담당 | 기한 | 산출물 |
|------|------|------|--------|
| 월간 실적 입력 | 각 부문 담당자 | 익월 5일 | 월간실적_[부문]_MM.xlsx |
| 데이터 처리 | 경영지원 | 익월 6일 | JSON 업데이트, 대시보드 갱신 |
| AI 분석 실행 | 경영지원 | 익월 7일 | 분석 리포트 |
| 월간 보고 | 경영지원→사장 | 익월 10일 | 월간 KPI 보고서 |

## Phase 3: 분기 점검 (9월, 12월)

- Q3 점검: 9월 실적 기준, 10월 초 보고
- Q4 점검: 12월 실적 기준, 연말 평가와 통합

## Phase 4: 연말 평가 (12월)

| 단계 | 담당 | 기한 | 산출물 |
|------|------|------|--------|
| 연간 실적 집계 | 경영지원 | 12/20 | 연말평가서 초안 |
| AI 종합 분석 | 경영지원 | 12/22 | 종합 분석 리포트 |
| 평가 회의 | 전 부문장 | 12/26 | 평가 결과 |
| 최종 보고 | 사장 | 12/31 | 2026 KPI 최종 보고서 |
| 2027 KPI 수립 착수 | 전 부문 | 익년 1/15 | 2027 KPI 초안 |

## 부문 구성

| 부문 | 포함 팀 | 부문장 |
|------|---------|-------|
| 관리부문 | 인사총무, 구매, 공무 | TBD |
| 생산1부문 | 생산1팀 | TBD |
| 생산2부문 | 생산2팀, 금형팀 | TBD |
| 품질부문 | 품질팀 | TBD |
| 개발영업부문 | 개발영업팀 | TBD |

## 파일 관리 원칙

1. **Excel 입력**: 부서 담당자가 지정된 Excel 템플릿에 작성
2. **JSON 변환**: Python 스크립트가 자동 변환 (수동 편집 금지)
3. **대시보드**: Python 스크립트 실행 시 자동 갱신
4. **원본 보존**: 확정된 Excel 파일은 이름 변경 없이 보존
```

- [ ] **Step 2: KPI 수립 가이드 작성**

파일 내용 (`KPI_수립_가이드.md`):

```markdown
# KPI 수립 가이드 — 부문별 작성 지침

## SMART 기준

| 기준 | 설명 | 예시 (좋음) | 예시 (나쁨) |
|------|------|------------|------------|
| **S**pecific | 구체적 목표 | 불량률 0.5% 이하 | 품질 향상 |
| **M**easurable | 측정 가능 | 월간 측정, 수식 명확 | 노력하겠음 |
| **A**chievable | 달성 가능 | 전년 대비 20% 개선 | 전년 대비 200% |
| **R**elevant | 회사 목표 연결 | AS9100D 인증 지원 | 개인 스킬 향상 |
| **T**ime-bound | 기한 명확 | 2026-12-31 | 연내 |

## 부문별 KPI 유형 가이드

### 관리부문 (인사총무·구매·공무)
- 교육이수율 (인사)
- 채용 계획 충족률 (인사)
- 구매 납기 준수율 (구매)
- 원자재 재고 회전율 (구매)
- 설비 가동률 (공무)
- 에너지 원단위 절감률 (공무)

### 생산1부문
- 생산 계획 달성률
- 공정 불량률
- OEE(종합설비효율)
- 납기 준수율
- 1인당 생산량

### 생산2부문 / 금형
- 생산 계획 달성률
- 공정 불량률
- 금형 수명 달성률
- 금형 납기 준수율

### 품질부문
- 출하 불량률 (PPM)
- 고객 불만 건수
- 내부심사 지적 사항 처리율
- AS9100D 인증 유지

### 개발영업부문
- 매출 목표 달성률
- 신규 고객 확보 건수
- 견적→수주 전환율
- 고객 만족도 점수

## 가중치 배분 원칙

- 부문별 총 가중치 합계 = 100%
- KPI 항목 수: 5~8개 권장 (10개 초과 금지)
- 핵심 지표(Core): 가중치 20~30%
- 보조 지표(Support): 가중치 10~15%

## Excel 작성 방법

1. `templates/KPI_수립서_TEMPLATE.xlsx` 파일을 본인 부문 폴더에 복사
2. 파일명 변경: `KPI_수립서_[부문명].xlsx`
3. "KPI 목록" 시트 작성 (목표치·측정방법·담당자 필수)
4. "실행계획" 시트 작성 (분기별 마일스톤)
5. 경영지원팀에 제출 → 시스템 등록
```

- [ ] **Step 3: 월간보고 절차 문서 작성**

파일 내용 (`월간보고_절차.md`):

```markdown
# 월간 KPI 보고 절차

## 정기 일정 (매월)

| 일정 | 담당 | 작업 |
|------|------|------|
| 익월 1~5일 | 각 부문 담당자 | 실적 Excel 작성 후 제출 |
| 익월 6일 | 경영지원 | Python 데이터 처리 실행 |
| 익월 7일 | 경영지원 | AI 분석 실행, 이슈 확인 |
| 익월 10일 | 경영지원 | 사장 보고 |

## 실적 입력 방법 (부문 담당자)

1. `02_월간추적/TEMPLATE_월간실적.xlsx` 를 해당 월 폴더에 복사
2. 파일명: `[부문명]_MM실적.xlsx` (예: `관리부문_07실적.xlsx`)
3. 실제 달성 수치 입력
4. 특이사항·원인 분석 입력
5. 경영지원팀 이메일 또는 OneDrive 공유

## 데이터 처리 방법 (경영지원)

```powershell
# 1. 해당 월 실적 처리
cd "D:\Michael\OneDrive - Team Redpanda\ClaudeCowork\01_경영재무\KPI\2026년\kpi-system\scripts"
python 02_excel_to_json.py --month 2026-07

# 2. 대시보드 갱신
python 03_generate_dashboard.py

# 3. AI 분석 (선택 — 이슈 있을 때)
python 04_analyze_kpi_agent.py --month 2026-07
```

## 보고서 포함 항목

1. 부문별 KPI 달성 현황 (목표 대비 실적 %)
2. 전월 대비 변동 사항
3. 목표 미달 항목 및 원인 분석
4. 다음 달 개선 계획
5. AI 분석 결과 요약 (이슈 있는 항목)
```

- [ ] **Step 4: 연말평가 절차 문서 작성**

파일 내용 (`연말평가_절차.md`):

```markdown
# 연말 KPI 평가 절차

## 평가 일정

| 일정 | 담당 | 작업 |
|------|------|------|
| 12/20 | 경영지원 | 연간 실적 집계 및 최종 JSON 생성 |
| 12/22 | 경영지원 | AI 종합 분석 실행 |
| 12/26 | 전 부문장 | 평가 회의 |
| 12/28 | 각 부문 | 2027 KPI 초안 제출 |
| 12/31 | 경영지원→사장 | 2026 최종 KPI 보고서 |

## 평가 기준

| 등급 | 달성률 | 설명 |
|------|--------|------|
| S | 110% 이상 | 목표 초과 달성 |
| A | 100~110% | 목표 달성 |
| B | 90~100% | 목표 근접 |
| C | 80~90% | 부분 달성 |
| D | 80% 미만 | 미달 |

## 평가 회의 안건

1. 부문별 연간 KPI 달성률 발표 (부문장)
2. 미달 항목 원인 분석 및 교훈
3. AS9100D 연계 성과 검토
4. 2027 KPI 방향 논의
5. 부문 간 협업 이슈 해소

## 최종 보고서 구성

1. 회사 전체 KPI 달성 요약
2. 부문별 상세 달성 현황
3. 우수 사례 및 Best Practice
4. 개선 필요 영역 및 2027 과제
5. AI 분석 종합 인사이트
```

- [ ] **Step 5: 완료 확인**

```powershell
Get-ChildItem "D:\Michael\OneDrive - Team Redpanda\ClaudeCowork\01_경영재무\KPI\2026년\kpi-system\00_프로세스"
```
Expected: 4개 .md 파일 목록

---

### Task 3: 회사 전략 목표 문서 작성

**Files:**
- Create: `kpi-system/01_KPI수립_2026H2/00_회사전략목표.md`

- [ ] **Step 1: 회사 전략 목표 초안 작성**

파일 내용 (`00_회사전략목표.md`):

```markdown
# M&C Electronics Vina — 2026 하반기 / 2027 전략 목표

> **작성일**: 2026-06-22  **버전**: v0.1 (내부 검토용 — 확정 전)

## 경영 방향

M&C Electronics Vina는 2026 하반기부터 다음 세 축을 중심으로 성장한다:

1. **품질 경쟁력 확보** — AS9100D 인증 취득 및 유지, 불량률 최소화
2. **생산성 향상** — OEE 개선, 원가 절감을 통한 수익성 강화
3. **고객 기반 확대** — 신규 고객 확보, 기존 고객 만족도 향상

## 2026 하반기 핵심 목표 (회사 전체)

| # | 목표 | 지표 | 목표치 |
|---|------|------|--------|
| 1 | 매출 달성 | 하반기 매출 | [금액 TBD] |
| 2 | 수익성 | 영업이익률 | [% TBD] |
| 3 | 품질 | 출하 불량률 | [PPM TBD] |
| 4 | 납기 | 납기 준수율 | 95% 이상 |
| 5 | 인증 | AS9100D 인증 | 2026년 내 취득 |

## 2027 중기 목표 (방향)

- 매출 [전년 대비 X%] 성장
- 원가 절감 [X%]
- 고객 만족도 [점수 TBD]
- 신규 고객 [건수 TBD]

> **참고**: 위 수치는 경영진 회의 후 확정 예정. 각 부문 KPI 수립 시 이 방향과 정렬할 것.

## 부문별 전략 연계 포인트

| 부문 | 전략 목표 기여 |
|------|--------------|
| 관리부문 | 인프라 안정화, 원자재 원가 절감, 인재 확보 |
| 생산1부문 | OEE 향상, 납기 준수, 불량률 감소 |
| 생산2부문 | 생산 유연성, 금형 품질·납기 |
| 품질부문 | AS9100D 인증, 출하 불량 Zero 지향 |
| 개발영업부문 | 매출 성장, 신규 고객, 고객 만족 |
```

- [ ] **Step 2: 확인**

```powershell
Test-Path "D:\Michael\OneDrive - Team Redpanda\ClaudeCowork\01_경영재무\KPI\2026년\kpi-system\01_KPI수립_2026H2\00_회사전략목표.md"
```
Expected: True

---

## Phase B: Excel KPI 템플릿

### Task 4: KPI 수립서 Excel 템플릿 생성

**Files:**
- Create: `kpi-system/templates/KPI_수립서_TEMPLATE.xlsx`
- Test: `tests/test_excel_template.py`

- [ ] **Step 1: 테스트 파일 작성**

```python
# tests/test_excel_template.py
# KPI 수립서 Excel 템플릿 구조 검증

import openpyxl
import pytest
from pathlib import Path

TEMPLATE_PATH = Path("kpi-system/templates/KPI_수립서_TEMPLATE.xlsx")

def test_template_exists():
    assert TEMPLATE_PATH.exists(), "템플릿 파일이 없음"

def test_required_sheets():
    wb = openpyxl.load_workbook(TEMPLATE_PATH)
    assert "KPI목록" in wb.sheetnames
    assert "실행계획" in wb.sheetnames
    assert "작성가이드" in wb.sheetnames

def test_kpi_sheet_headers():
    wb = openpyxl.load_workbook(TEMPLATE_PATH)
    ws = wb["KPI목록"]
    headers = [ws.cell(1, c).value for c in range(1, 10)]
    required = ["KPI_ID", "분류", "KPI명", "목표치", "단위", "가중치", "측정방법", "담당자", "기한"]
    for h in required:
        assert h in headers, f"헤더 누락: {h}"
```

- [ ] **Step 2: 테스트 실행 (실패 확인)**

```powershell
cd "D:\Michael\OneDrive - Team Redpanda\ClaudeCowork\01_경영재무\KPI\2026년\kpi-system"
python -m pytest ..\tests\test_excel_template.py -v
```
Expected: FAIL (템플릿 파일 없음)

- [ ] **Step 3: 템플릿 생성 스크립트 실행**

```python
# scripts/setup_templates.py (1회 실행용)
# KPI 수립서 Excel 템플릿 생성

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.styles.numbers import FORMAT_PERCENTAGE
from pathlib import Path

def create_kpi_template():
    wb = Workbook()

    # ── 시트 1: KPI목록 ──────────────────────────────
    ws1 = wb.active
    ws1.title = "KPI목록"

    headers = ["KPI_ID","분류","KPI명","목표치","단위","가중치(%)","측정방법","담당자","기한","비고"]
    col_widths = [10, 12, 25, 10, 8, 10, 35, 12, 12, 20]

    header_fill = PatternFill("solid", fgColor="1F4E79")
    header_font = Font(name="맑은 고딕", bold=True, color="FFFFFF", size=11)
    body_font = Font(name="맑은 고딕", size=10)
    border = Border(
        left=Side(style="thin"), right=Side(style="thin"),
        top=Side(style="thin"), bottom=Side(style="thin")
    )

    # 제목 행
    ws1.merge_cells("A1:J1")
    ws1["A1"] = "M&C Electronics Vina — KPI 수립서"
    ws1["A1"].font = Font(name="맑은 고딕", bold=True, size=14, color="1F4E79")
    ws1["A1"].alignment = Alignment(horizontal="center", vertical="center")
    ws1.row_dimensions[1].height = 30

    # 부문 정보 행
    ws1["A2"] = "부문명"
    ws1["B2"] = ""  # 입력 칸
    ws1["D2"] = "작성자"
    ws1["E2"] = ""
    ws1["G2"] = "작성일"
    ws1["H2"] = ""
    ws1["J2"] = "버전"
    for cell in [ws1["A2"], ws1["D2"], ws1["G2"], ws1["J2"]]:
        cell.font = Font(name="맑은 고딕", bold=True, size=10)
        cell.fill = PatternFill("solid", fgColor="D6E4F0")

    # 헤더 행 (3행)
    for col, (h, w) in enumerate(zip(headers, col_widths), 1):
        cell = ws1.cell(3, col, h)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = border
        ws1.column_dimensions[cell.column_letter].width = w
    ws1.row_dimensions[3].height = 25

    # 샘플 데이터 행 (4~11행, 8개 KPI 슬롯)
    example_data = [
        ["MGT-001", "인사", "교육이수율", 95, "%", 15, "교육 이수자/대상자×100", "인사총무팀", "2026-12-31", ""],
        ["MGT-002", "구매", "납기준수율", 95, "%", 15, "납기 준수 건/전체 발주 건×100", "구매팀", "2026-12-31", ""],
        ["", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", ""],
    ]
    alt_fill = PatternFill("solid", fgColor="EBF3FB")
    for r_idx, row_data in enumerate(example_data, 4):
        fill = alt_fill if r_idx % 2 == 0 else PatternFill("solid", fgColor="FFFFFF")
        for c_idx, val in enumerate(row_data, 1):
            cell = ws1.cell(r_idx, c_idx, val)
            cell.font = body_font
            cell.border = border
            cell.fill = fill
            cell.alignment = Alignment(vertical="center", wrap_text=True)

    # 합계 행
    ws1.cell(12, 1, "합계").font = Font(name="맑은 고딕", bold=True, size=10)
    ws1.cell(12, 6, "=SUM(F4:F11)").font = Font(name="맑은 고딕", bold=True, size=10)
    ws1.cell(12, 6).fill = PatternFill("solid", fgColor="FFF2CC")
    for c in range(1, 11):
        ws1.cell(12, c).border = border

    ws1.freeze_panes = "A4"

    # ── 시트 2: 실행계획 ──────────────────────────────
    ws2 = wb.create_sheet("실행계획")
    ws2.merge_cells("A1:H1")
    ws2["A1"] = "KPI 실행계획 (분기별 마일스톤)"
    ws2["A1"].font = Font(name="맑은 고딕", bold=True, size=13, color="1F4E79")
    ws2["A1"].alignment = Alignment(horizontal="center")

    plan_headers = ["KPI_ID", "KPI명", "Q3 목표\n(7~9월)", "Q3 실행과제", "Q4 목표\n(10~12월)", "Q4 실행과제", "담당자", "비고"]
    for c, h in enumerate(plan_headers, 1):
        cell = ws2.cell(2, c, h)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = border
    ws2.row_dimensions[2].height = 35
    for c in [1,2,3,5,7,8]:
        ws2.column_dimensions[ws2.cell(2,c).column_letter].width = [10,25,12,30,12,30,12,15][c-1]

    for r in range(3, 11):
        for c in range(1, 9):
            ws2.cell(r, c).border = border
            ws2.cell(r, c).font = body_font
        ws2.row_dimensions[r].height = 40

    # ── 시트 3: 작성가이드 ──────────────────────────────
    ws3 = wb.create_sheet("작성가이드")
    guide_lines = [
        ("KPI 수립서 작성 가이드", True, 14),
        ("", False, 10),
        ("■ SMART 기준", True, 11),
        ("  S (Specific) : 구체적 목표 — 예) 불량률 0.5% 이하", False, 10),
        ("  M (Measurable) : 측정 가능 — 수식·데이터 출처 명확히", False, 10),
        ("  A (Achievable) : 달성 가능 — 전년 실적 기준 현실적", False, 10),
        ("  R (Relevant) : 회사 목표 연결 — AS9100D·매출·원가와 연계", False, 10),
        ("  T (Time-bound) : 기한 명확 — YYYY-MM-DD 형식", False, 10),
        ("", False, 10),
        ("■ KPI_ID 명명 규칙", True, 11),
        ("  관리부문: MGT-001, MGT-002 ...", False, 10),
        ("  생산1부문: PR1-001, PR1-002 ...", False, 10),
        ("  생산2부문: PR2-001, PR2-002 ...", False, 10),
        ("  품질부문: QUA-001, QUA-002 ...", False, 10),
        ("  개발영업부문: SLS-001, SLS-002 ...", False, 10),
        ("", False, 10),
        ("■ 가중치 합계 = 100% (F12 셀 확인)", True, 11),
        ("■ KPI 항목 수: 5~8개 권장 (최대 8개)", True, 11),
        ("■ 완성 후 경영지원팀 이메일 제출", True, 11),
    ]
    for r, (text, bold, size) in enumerate(guide_lines, 1):
        cell = ws3.cell(r, 1, text)
        cell.font = Font(name="맑은 고딕", bold=bold, size=size)
    ws3.column_dimensions["A"].width = 70

    out_path = Path("kpi-system/templates/KPI_수립서_TEMPLATE.xlsx")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    wb.save(out_path)
    print(f"저장 완료: {out_path}")

if __name__ == "__main__":
    create_kpi_template()
```

실행:
```powershell
cd "D:\Michael\OneDrive - Team Redpanda\ClaudeCowork\01_경영재무\KPI\2026년"
python kpi-system\scripts\setup_templates.py
```

- [ ] **Step 4: 테스트 재실행 (성공 확인)**

```powershell
python -m pytest tests\test_excel_template.py -v
```
Expected: 3 passed

- [ ] **Step 5: Commit**

```powershell
git add kpi-system/templates/KPI_수립서_TEMPLATE.xlsx tests/test_excel_template.py kpi-system/scripts/setup_templates.py
git commit -m "feat: KPI 수립서 Excel 템플릿 및 테스트 추가"
```

---

### Task 5: 월간 실적 입력 Excel 템플릿

**Files:**
- Create: `kpi-system/templates/월간실적_TEMPLATE.xlsx`

- [ ] **Step 1: 월간 실적 템플릿 생성 스크립트 작성**

`scripts/setup_templates.py`에 함수 추가:

```python
def create_monthly_template():
    wb = Workbook()
    ws = wb.active
    ws.title = "월간실적"

    header_fill = PatternFill("solid", fgColor="1F4E79")
    header_font = Font(name="맑은 고딕", bold=True, color="FFFFFF", size=11)
    body_font = Font(name="맑은 고딕", size=10)
    border = Border(
        left=Side(style="thin"), right=Side(style="thin"),
        top=Side(style="thin"), bottom=Side(style="thin")
    )
    red_font = Font(name="맑은 고딕", color="FF0000", size=10)
    green_font = Font(name="맑은 고딕", color="00B050", size=10)

    # 제목
    ws.merge_cells("A1:J1")
    ws["A1"] = "M&C Electronics Vina — 월간 KPI 실적 보고"
    ws["A1"].font = Font(name="맑은 고딕", bold=True, size=14, color="1F4E79")
    ws["A1"].alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[1].height = 30

    # 메타 정보
    meta = [("부문명",""), ("보고월","YYYY-MM"), ("작성자",""), ("작성일","")]
    for i, (label, val) in enumerate(meta):
        col = i * 2 + 1
        ws.cell(2, col, label).font = Font(name="맑은 고딕", bold=True, size=10, color="1F4E79")
        ws.cell(2, col+1, val).font = body_font

    # 헤더
    headers = ["KPI_ID","KPI명","단위","연간목표","월목표","실적","달성률(%)","전월대비","이슈/원인","개선계획"]
    widths =   [10,       25,    8,    10,       10,    10,     12,        12,       30,         30]
    for c, (h, w) in enumerate(zip(headers, widths), 1):
        cell = ws.cell(3, c, h)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = border
        ws.column_dimensions[cell.column_letter].width = w
    ws.row_dimensions[3].height = 25

    # 데이터 행 (8개)
    alt_fill = PatternFill("solid", fgColor="EBF3FB")
    for r in range(4, 12):
        fill = alt_fill if r % 2 == 0 else PatternFill("solid", fgColor="FFFFFF")
        for c in range(1, 11):
            cell = ws.cell(r, c)
            cell.border = border
            cell.font = body_font
            cell.fill = fill
            cell.alignment = Alignment(vertical="center", wrap_text=True)
        # 달성률 수식
        ws.cell(r, 7, f"=IF(E{r}=0,\"\",F{r}/E{r})")
        ws.cell(r, 7).number_format = "0.0%"

    ws.freeze_panes = "A4"

    out_path = Path("kpi-system/templates/월간실적_TEMPLATE.xlsx")
    wb.save(out_path)
    print(f"저장 완료: {out_path}")
```

- [ ] **Step 2: 실행**

```powershell
python kpi-system\scripts\setup_templates.py --monthly
```

- [ ] **Step 3: 파일 확인**

```powershell
Test-Path "D:\Michael\OneDrive - Team Redpanda\ClaudeCowork\01_경영재무\KPI\2026년\kpi-system\templates\월간실적_TEMPLATE.xlsx"
```
Expected: True

---

## Phase C: Python 데이터 엔진

### Task 6: KPI JSON 스키마 정의 + 검증 스크립트

**Files:**
- Create: `kpi-system/scripts/01_validate_kpi.py`
- Create: `kpi-system/schema/kpi_schema.json`
- Test: `tests/test_validate_kpi.py`

- [ ] **Step 1: JSON 스키마 정의**

`kpi-system/schema/kpi_schema.json`:
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "KPI 데이터 스키마",
  "type": "object",
  "required": ["dept", "year", "half", "version", "kpis"],
  "properties": {
    "dept": {"type": "string", "enum": ["관리부문","생산1부문","생산2부문","품질부문","개발영업부문"]},
    "year": {"type": "string", "pattern": "^[0-9]{4}$"},
    "half": {"type": "string", "enum": ["H1","H2","FY"]},
    "version": {"type": "string"},
    "status": {"type": "string", "enum": ["draft","confirmed","active"]},
    "kpis": {
      "type": "array",
      "minItems": 3,
      "maxItems": 10,
      "items": {
        "type": "object",
        "required": ["id","category","name","target","unit","weight","measurement_method","owner","deadline"],
        "properties": {
          "id":                 {"type": "string"},
          "category":          {"type": "string"},
          "name":              {"type": "string"},
          "target":            {"type": "number"},
          "unit":              {"type": "string"},
          "weight":            {"type": "number", "minimum": 5, "maximum": 40},
          "measurement_method":{"type": "string"},
          "owner":             {"type": "string"},
          "deadline":          {"type": "string", "format": "date"},
          "monthly_actuals":   {"type": "object"}
        }
      }
    }
  }
}
```

- [ ] **Step 2: 테스트 작성**

`tests/test_validate_kpi.py`:
```python
# KPI JSON 검증 스크립트 테스트

import json, pytest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "kpi-system" / "scripts"))
from validate_kpi import validate_kpi_file, ValidationError

VALID = {
    "dept": "관리부문", "year": "2026", "half": "H2",
    "version": "v1.0", "status": "draft",
    "kpis": [
        {"id":"MGT-001","category":"인사","name":"교육이수율","target":95,
         "unit":"%","weight":20,"measurement_method":"이수자/대상자×100",
         "owner":"인사총무팀","deadline":"2026-12-31","monthly_actuals":{}},
        {"id":"MGT-002","category":"구매","name":"납기준수율","target":95,
         "unit":"%","weight":20,"measurement_method":"준수건/전체건×100",
         "owner":"구매팀","deadline":"2026-12-31","monthly_actuals":{}},
        {"id":"MGT-003","category":"공무","name":"설비가동률","target":90,
         "unit":"%","weight":20,"measurement_method":"가동시간/총시간×100",
         "owner":"공무팀","deadline":"2026-12-31","monthly_actuals":{}},
    ]
}

def test_valid_data_passes():
    result = validate_kpi_file(VALID)
    assert result["valid"] is True

def test_invalid_dept_fails():
    bad = {**VALID, "dept": "기타부문"}
    result = validate_kpi_file(bad)
    assert result["valid"] is False

def test_weight_sum_must_be_100():
    bad = {**VALID, "kpis": [{**k, "weight": 10} for k in VALID["kpis"]]}
    result = validate_kpi_file(bad)
    assert result["valid"] is False
    assert "가중치" in result["errors"][0]

def test_too_few_kpis_fails():
    bad = {**VALID, "kpis": VALID["kpis"][:1]}
    result = validate_kpi_file(bad)
    assert result["valid"] is False
```

- [ ] **Step 3: 테스트 실행 (실패 확인)**

```powershell
python -m pytest tests\test_validate_kpi.py -v
```
Expected: FAIL (모듈 없음)

- [ ] **Step 4: 검증 스크립트 구현**

`kpi-system/scripts/01_validate_kpi.py`:
```python
# KPI JSON 데이터 유효성 검증 스크립트

import json, sys
from pathlib import Path
from datetime import datetime

VALID_DEPTS = {"관리부문","생산1부문","생산2부문","품질부문","개발영업부문"}
REQUIRED_FIELDS = ["id","category","name","target","unit","weight","measurement_method","owner","deadline"]

def validate_kpi_file(data: dict) -> dict:
    errors = []

    if data.get("dept") not in VALID_DEPTS:
        errors.append(f"부문명 오류: '{data.get('dept')}' — 허용값: {VALID_DEPTS}")

    if not data.get("year","").isdigit():
        errors.append("year 형식 오류 (YYYY)")

    kpis = data.get("kpis", [])
    if len(kpis) < 3:
        errors.append(f"KPI 항목 부족: {len(kpis)}개 (최소 3개)")
    if len(kpis) > 10:
        errors.append(f"KPI 항목 과다: {len(kpis)}개 (최대 10개)")

    total_weight = 0
    for i, kpi in enumerate(kpis, 1):
        for field in REQUIRED_FIELDS:
            if field not in kpi or kpi[field] == "" or kpi[field] is None:
                errors.append(f"KPI[{i}] '{field}' 누락")
        w = kpi.get("weight", 0)
        if not (5 <= w <= 40):
            errors.append(f"KPI[{i}] 가중치 범위 오류: {w} (5~40)")
        total_weight += w
        deadline = kpi.get("deadline","")
        try:
            datetime.strptime(deadline, "%Y-%m-%d")
        except ValueError:
            errors.append(f"KPI[{i}] deadline 형식 오류: '{deadline}' (YYYY-MM-DD)")

    if kpis and abs(total_weight - 100) > 0.1:
        errors.append(f"가중치 합계 오류: {total_weight}% (합계=100% 필요)")

    return {"valid": len(errors) == 0, "errors": errors, "warning_count": 0}

def main():
    if len(sys.argv) < 2:
        print("Usage: python 01_validate_kpi.py <kpi_data.json>")
        sys.exit(1)
    path = Path(sys.argv[1])
    data = json.loads(path.read_text(encoding="utf-8"))
    result = validate_kpi_file(data)
    if result["valid"]:
        print(f"✅ 검증 통과: {path.name}")
    else:
        print(f"❌ 검증 실패: {path.name}")
        for e in result["errors"]:
            print(f"   - {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

- [ ] **Step 5: 테스트 재실행 (성공 확인)**

```powershell
python -m pytest tests\test_validate_kpi.py -v
```
Expected: 4 passed

- [ ] **Step 6: Commit**

```powershell
git add kpi-system/scripts/01_validate_kpi.py kpi-system/schema/ tests/test_validate_kpi.py
git commit -m "feat: KPI JSON 검증 스크립트 + 스키마 추가"
```

---

### Task 7: Excel → JSON 변환 스크립트

**Files:**
- Create: `kpi-system/scripts/02_excel_to_json.py`
- Test: `tests/test_excel_to_json.py`

- [ ] **Step 1: 테스트 작성**

`tests/test_excel_to_json.py`:
```python
# Excel → JSON 변환 스크립트 테스트

import json, pytest, openpyxl
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "kpi-system" / "scripts"))
from excel_to_json import parse_kpi_excel, ExcelParseError

def make_test_xlsx(tmp_path, rows):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "KPI목록"
    ws["B2"] = "관리부문"   # 부문명
    headers = ["KPI_ID","분류","KPI명","목표치","단위","가중치(%)","측정방법","담당자","기한","비고"]
    for c, h in enumerate(headers, 1):
        ws.cell(3, c, h)
    for r_idx, row in enumerate(rows, 4):
        for c_idx, val in enumerate(row, 1):
            ws.cell(r_idx, c_idx, val)
    p = tmp_path / "test_kpi.xlsx"
    wb.save(p)
    return p

SAMPLE_ROWS = [
    ["MGT-001","인사","교육이수율",95,"%",20,"이수자/대상자×100","인사총무팀","2026-12-31",""],
    ["MGT-002","구매","납기준수율",95,"%",20,"준수건/전체건×100","구매팀","2026-12-31",""],
    ["MGT-003","공무","설비가동률",90,"%",20,"가동시간/총시간×100","공무팀","2026-12-31",""],
]

def test_parse_returns_dict(tmp_path):
    p = make_test_xlsx(tmp_path, SAMPLE_ROWS)
    result = parse_kpi_excel(p, year="2026", half="H2")
    assert isinstance(result, dict)
    assert result["dept"] == "관리부문"

def test_kpi_count(tmp_path):
    p = make_test_xlsx(tmp_path, SAMPLE_ROWS)
    result = parse_kpi_excel(p, year="2026", half="H2")
    assert len(result["kpis"]) == 3

def test_empty_rows_skipped(tmp_path):
    rows = SAMPLE_ROWS + [["","","","","","","","","",""]]
    p = make_test_xlsx(tmp_path, rows)
    result = parse_kpi_excel(p, year="2026", half="H2")
    assert len(result["kpis"]) == 3
```

- [ ] **Step 2: 변환 스크립트 구현**

`kpi-system/scripts/02_excel_to_json.py`:
```python
# Excel KPI 수립서 → JSON 변환 스크립트

import json, sys, argparse
from pathlib import Path
from datetime import datetime
import openpyxl

class ExcelParseError(Exception):
    pass

DEPT_MAP = {
    "관리부문":"관리부문", "생산1부문":"생산1부문",
    "생산2부문":"생산2부문", "품질부문":"품질부문",
    "개발영업부문":"개발영업부문"
}

def parse_kpi_excel(xlsx_path: Path, year: str = "2026", half: str = "H2") -> dict:
    wb = openpyxl.load_workbook(xlsx_path, data_only=True)
    if "KPI목록" not in wb.sheetnames:
        raise ExcelParseError("'KPI목록' 시트가 없습니다")
    ws = wb["KPI목록"]

    dept_raw = ws["B2"].value or ""
    dept = DEPT_MAP.get(str(dept_raw).strip())
    if not dept:
        raise ExcelParseError(f"부문명 인식 불가: '{dept_raw}'")

    kpis = []
    for row in ws.iter_rows(min_row=4, max_row=13, values_only=True):
        kpi_id, category, name, target, unit, weight, method, owner, deadline, note = (list(row) + [None]*10)[:10]
        if not kpi_id or not name:
            continue
        kpis.append({
            "id": str(kpi_id).strip(),
            "category": str(category or "").strip(),
            "name": str(name).strip(),
            "target": float(target) if target is not None else 0,
            "unit": str(unit or "").strip(),
            "weight": float(weight) if weight is not None else 0,
            "measurement_method": str(method or "").strip(),
            "owner": str(owner or "").strip(),
            "deadline": str(deadline or "").strip(),
            "monthly_actuals": {}
        })

    return {
        "dept": dept, "year": year, "half": half,
        "version": "v1.0", "status": "draft",
        "generated_at": datetime.now().strftime("%Y-%m-%d"),
        "kpis": kpis
    }

def main():
    parser = argparse.ArgumentParser(description="Excel KPI 수립서 → JSON 변환")
    parser.add_argument("xlsx", help="입력 Excel 경로")
    parser.add_argument("--year", default="2026")
    parser.add_argument("--half", default="H2")
    parser.add_argument("--out", help="출력 JSON 경로 (기본: 입력 파일과 같은 폴더)")
    args = parser.parse_args()

    xlsx_path = Path(args.xlsx)
    data = parse_kpi_excel(xlsx_path, args.year, args.half)

    out_path = Path(args.out) if args.out else xlsx_path.parent / "kpi_data.json"
    out_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✅ 변환 완료: {out_path}")

if __name__ == "__main__":
    main()
```

- [ ] **Step 3: 테스트 실행**

```powershell
python -m pytest tests\test_excel_to_json.py -v
```
Expected: 3 passed

- [ ] **Step 4: Commit**

```powershell
git add kpi-system/scripts/02_excel_to_json.py tests/test_excel_to_json.py
git commit -m "feat: Excel → JSON 변환 스크립트 추가"
```

---

## Phase D: HTML 대시보드

### Task 8: 대시보드 CSS + JS 기반 구조

**Files:**
- Create: `kpi-system/dashboard/css/style.css`
- Create: `kpi-system/dashboard/js/app.js`

- [ ] **Step 1: CSS 스타일시트 작성**

`kpi-system/dashboard/css/style.css`:
```css
/* M&C KPI 대시보드 스타일 — 외부 CDN 없음 */
:root {
    --primary: #1F4E79;
    --secondary: #2E75B6;
    --accent: #70AD47;
    --danger: #FF0000;
    --warning: #FFC000;
    --bg: #F5F7FA;
    --card-bg: #FFFFFF;
    --text: #333333;
    --border: #D0D7E2;
    --font: "맑은 고딕", "Malgun Gothic", -apple-system, sans-serif;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: var(--font); background: var(--bg); color: var(--text); font-size: 14px; }

/* 헤더 */
.header { background: var(--primary); color: white; padding: 16px 24px; display: flex; justify-content: space-between; align-items: center; }
.header h1 { font-size: 20px; font-weight: 700; }
.header .subtitle { font-size: 12px; opacity: 0.8; }

/* 네비게이션 */
.nav { background: var(--secondary); padding: 0 24px; display: flex; gap: 4px; }
.nav a { color: white; text-decoration: none; padding: 10px 16px; display: inline-block; font-size: 13px; opacity: 0.85; }
.nav a:hover, .nav a.active { background: rgba(255,255,255,0.2); opacity: 1; }

/* 메인 레이아웃 */
.container { max-width: 1200px; margin: 24px auto; padding: 0 24px; }

/* 요약 카드 */
.summary-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin-bottom: 24px; }
.summary-card { background: var(--card-bg); border-radius: 8px; padding: 20px; border-left: 4px solid var(--secondary); box-shadow: 0 1px 4px rgba(0,0,0,0.08); }
.summary-card .label { font-size: 12px; color: #666; margin-bottom: 8px; }
.summary-card .value { font-size: 28px; font-weight: 700; color: var(--primary); }
.summary-card .sub { font-size: 11px; color: #888; margin-top: 4px; }
.summary-card.green { border-left-color: var(--accent); }
.summary-card.red { border-left-color: var(--danger); }
.summary-card.yellow { border-left-color: var(--warning); }

/* 부문 카드 그리드 */
.dept-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(340px, 1fr)); gap: 20px; margin-bottom: 24px; }
.dept-card { background: var(--card-bg); border-radius: 8px; padding: 20px; box-shadow: 0 1px 4px rgba(0,0,0,0.08); }
.dept-card h3 { font-size: 15px; color: var(--primary); margin-bottom: 16px; padding-bottom: 8px; border-bottom: 2px solid var(--border); }
.dept-card a { text-decoration: none; color: inherit; }

/* KPI 행 */
.kpi-row { display: flex; align-items: center; gap: 10px; padding: 8px 0; border-bottom: 1px solid #F0F0F0; }
.kpi-row:last-child { border-bottom: none; }
.kpi-name { flex: 1; font-size: 13px; }
.kpi-target { font-size: 12px; color: #888; min-width: 60px; text-align: right; }
.kpi-actual { font-size: 13px; font-weight: 600; min-width: 60px; text-align: right; }

/* 진행 바 */
.progress-bar { flex: 2; background: #E8EDF3; border-radius: 4px; height: 8px; overflow: hidden; }
.progress-fill { height: 100%; border-radius: 4px; transition: width 0.4s ease; }
.fill-green { background: var(--accent); }
.fill-yellow { background: var(--warning); }
.fill-red { background: var(--danger); }
.pct-badge { font-size: 12px; font-weight: 600; min-width: 42px; text-align: right; }
.pct-green { color: var(--accent); }
.pct-yellow { color: #B8860B; }
.pct-red { color: var(--danger); }

/* 상태 배지 */
.badge { display: inline-block; font-size: 11px; padding: 2px 8px; border-radius: 10px; font-weight: 600; }
.badge-draft { background: #FFF3CD; color: #856404; }
.badge-confirmed { background: #D1ECF1; color: #0C5460; }
.badge-active { background: #D4EDDA; color: #155724; }

/* 테이블 */
.kpi-table { width: 100%; border-collapse: collapse; margin-top: 16px; }
.kpi-table th { background: var(--primary); color: white; padding: 10px 12px; text-align: left; font-size: 12px; }
.kpi-table td { padding: 9px 12px; border-bottom: 1px solid var(--border); font-size: 13px; }
.kpi-table tr:nth-child(even) { background: #F8FAFC; }
.kpi-table tr:hover { background: #EBF3FB; }

/* 타임라인 */
.timeline { margin-top: 24px; }
.timeline-item { display: flex; gap: 16px; margin-bottom: 16px; }
.timeline-dot { width: 12px; height: 12px; border-radius: 50%; background: var(--secondary); margin-top: 4px; flex-shrink: 0; }
.timeline-dot.done { background: var(--accent); }
.timeline-dot.current { background: var(--warning); box-shadow: 0 0 0 3px rgba(255,192,0,0.3); }

/* 반응형 */
@media (max-width: 768px) {
    .dept-grid { grid-template-columns: 1fr; }
    .summary-grid { grid-template-columns: repeat(2, 1fr); }
    .container { padding: 0 12px; }
}
```

- [ ] **Step 2: JavaScript 작성**

`kpi-system/dashboard/js/app.js`:
```javascript
// KPI 대시보드 공통 유틸리티

function calcPct(actual, target) {
    if (!target || target === 0) return 0;
    return Math.min((actual / target) * 100, 150);
}

function pctClass(pct) {
    if (pct >= 100) return "green";
    if (pct >= 80) return "yellow";
    return "red";
}

function renderProgressBar(container, pct) {
    const cls = pctClass(pct);
    const width = Math.min(pct, 100);
    container.innerHTML = `
        <div class="progress-bar">
            <div class="progress-fill fill-${cls}" style="width:${width}%"></div>
        </div>`;
}

function formatDate(dateStr) {
    if (!dateStr) return "-";
    return dateStr.substring(0, 7);
}

// 마지막 실적 가져오기
function getLatestActual(monthlyActuals) {
    const keys = Object.keys(monthlyActuals || {}).sort().reverse();
    return keys.length > 0 ? { month: keys[0], value: monthlyActuals[keys[0]] } : null;
}
```

---

### Task 9: Python 대시보드 생성기

**Files:**
- Create: `kpi-system/scripts/03_generate_dashboard.py`
- Create: `kpi-system/templates/dashboard_index.html.j2`
- Create: `kpi-system/templates/dashboard_dept.html.j2`
- Test: `tests/test_generate_dashboard.py`

- [ ] **Step 1: 테스트 작성**

`tests/test_generate_dashboard.py`:
```python
import json, pytest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "kpi-system" / "scripts"))
from generate_dashboard import collect_all_kpi_data, render_index_html

SAMPLE_DATA = {
    "dept": "관리부문", "year": "2026", "half": "H2",
    "version": "v1.0", "status": "active",
    "kpis": [
        {"id":"MGT-001","category":"인사","name":"교육이수율","target":95,"unit":"%","weight":20,
         "measurement_method":"이수자/대상자×100","owner":"인사총무팀","deadline":"2026-12-31",
         "monthly_actuals":{"2026-07": 92.5}},
    ]
}

def test_render_produces_html(tmp_path):
    (tmp_path / "kpi_data.json").write_text(
        json.dumps(SAMPLE_DATA, ensure_ascii=False), encoding="utf-8"
    )
    html = render_index_html([SAMPLE_DATA])
    assert "<html" in html
    assert "관리부문" in html
    assert "교육이수율" in html

def test_collect_reads_json_files(tmp_path):
    dept_dir = tmp_path / "관리부문"
    dept_dir.mkdir()
    (dept_dir / "kpi_data.json").write_text(
        json.dumps(SAMPLE_DATA, ensure_ascii=False), encoding="utf-8"
    )
    result = collect_all_kpi_data(tmp_path)
    assert len(result) == 1
    assert result[0]["dept"] == "관리부문"
```

- [ ] **Step 2: 생성기 구현**

`kpi-system/scripts/03_generate_dashboard.py`:
```python
# KPI 대시보드 HTML 생성기 — JSON 데이터를 읽어 정적 HTML 생성

import json, sys
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).parent.parent
DEPT_ORDER = ["관리부문","생산1부문","생산2부문","품질부문","개발영업부문"]

def collect_all_kpi_data(kpi_root: Path) -> list:
    result = []
    for dept in DEPT_ORDER:
        json_path = kpi_root / dept / "kpi_data.json"
        if json_path.exists():
            data = json.loads(json_path.read_text(encoding="utf-8"))
            result.append(data)
    return result

def get_latest_actual(monthly_actuals: dict):
    if not monthly_actuals:
        return None, None
    keys = sorted(monthly_actuals.keys(), reverse=True)
    return keys[0], monthly_actuals[keys[0]]

def calc_pct(actual, target):
    if not target:
        return 0
    return round(min((actual / target) * 100, 150), 1)

def pct_color(pct):
    if pct >= 100: return "#70AD47"
    if pct >= 80:  return "#FFC000"
    return "#FF0000"

def pct_class(pct):
    if pct >= 100: return "green"
    if pct >= 80:  return "yellow"
    return "red"

def render_kpi_row(kpi: dict) -> str:
    month, actual = get_latest_actual(kpi.get("monthly_actuals", {}))
    if actual is not None:
        pct = calc_pct(actual, kpi["target"])
        pct_str = f"{pct:.1f}%"
        actual_str = f"{actual}{kpi['unit']}"
        cls = pct_class(pct)
        width = min(pct, 100)
        bar = f'<div class="progress-bar"><div class="progress-fill fill-{cls}" style="width:{width:.0f}%"></div></div>'
        badge = f'<span class="pct-badge pct-{cls}">{pct_str}</span>'
    else:
        actual_str = "미입력"
        bar = '<div class="progress-bar"><div class="progress-fill fill-yellow" style="width:0%"></div></div>'
        badge = '<span class="pct-badge pct-yellow">-</span>'

    return f"""
    <div class="kpi-row">
        <span class="kpi-name">{kpi['name']}</span>
        <span class="kpi-target">목표: {kpi['target']}{kpi['unit']}</span>
        {bar}
        <span class="kpi-actual">{actual_str}</span>
        {badge}
    </div>"""

def render_dept_card(dept_data: dict) -> str:
    kpi_rows = "".join(render_kpi_row(k) for k in dept_data["kpis"])
    status_badge = f'<span class="badge badge-{dept_data.get("status","draft")}">{dept_data.get("status","draft")}</span>'
    dept_name = dept_data["dept"]
    dept_url = f"dept_{dept_name}.html"
    return f"""
    <div class="dept-card">
        <h3><a href="{dept_url}">{dept_name}</a> {status_badge}</h3>
        {kpi_rows}
    </div>"""

def render_index_html(all_data: list) -> str:
    generated = datetime.now().strftime("%Y-%m-%d %H:%M")
    dept_cards = "\n".join(render_dept_card(d) for d in all_data)

    total_kpis = sum(len(d["kpis"]) for d in all_data)
    depts_active = sum(1 for d in all_data if d.get("status") == "active")

    # 전체 달성률 계산
    achieved, total = 0, 0
    for d in all_data:
        for k in d["kpis"]:
            _, actual = get_latest_actual(k.get("monthly_actuals", {}))
            if actual is not None:
                if calc_pct(actual, k["target"]) >= 100:
                    achieved += 1
                total += 1
    overall_pct = f"{achieved}/{total}" if total else "데이터 없음"

    css_path = "css/style.css"
    js_path = "js/app.js"

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>M&C KPI 대시보드 — 2026</title>
<link rel="stylesheet" href="{css_path}">
</head>
<body>
<div class="header">
    <div>
        <h1>M&amp;C Electronics Vina — KPI 관리 대시보드</h1>
        <div class="subtitle">2026 하반기 / 최종 업데이트: {generated}</div>
    </div>
</div>
<nav class="nav">
    <a href="index.html" class="active">전체 현황</a>
    {"".join(f'<a href="dept_{d["dept"]}.html">{d["dept"]}</a>' for d in all_data)}
</nav>
<div class="container">
    <div class="summary-grid">
        <div class="summary-card">
            <div class="label">등록 부문</div>
            <div class="value">{len(all_data)}</div>
            <div class="sub">/ 5 부문</div>
        </div>
        <div class="summary-card green">
            <div class="label">활성 부문</div>
            <div class="value">{depts_active}</div>
            <div class="sub">실적 입력 완료</div>
        </div>
        <div class="summary-card">
            <div class="label">전체 KPI 수</div>
            <div class="value">{total_kpis}</div>
            <div class="sub">개 지표</div>
        </div>
        <div class="summary-card {'green' if total > 0 else 'yellow'}">
            <div class="label">목표 달성 항목</div>
            <div class="value">{overall_pct}</div>
            <div class="sub">개 달성 (≥100%)</div>
        </div>
    </div>
    <div class="dept-grid">
        {dept_cards if all_data else '<p style="color:#888;padding:24px;">등록된 KPI 데이터가 없습니다. Excel 수립서를 제출하고 변환 스크립트를 실행하세요.</p>'}
    </div>
</div>
<script src="{js_path}"></script>
</body>
</html>"""

def render_dept_html(dept_data: dict, all_depts: list) -> str:
    dept_name = dept_data["dept"]
    generated = datetime.now().strftime("%Y-%m-%d %H:%M")
    nav_links = "\n".join(
        f'<a href="dept_{d["dept"]}.html" {"class=\"active\"" if d["dept"]==dept_name else ""}>{d["dept"]}</a>'
        for d in all_depts
    )
    rows = ""
    for k in dept_data["kpis"]:
        month, actual = get_latest_actual(k.get("monthly_actuals", {}))
        if actual is not None:
            pct = calc_pct(actual, k["target"])
            pct_str = f'{pct:.1f}%'
            cls = pct_class(pct)
            bar = f'<div class="progress-bar" style="width:120px;display:inline-block"><div class="progress-fill fill-{cls}" style="width:{min(pct,100):.0f}%"></div></div>'
        else:
            pct_str, bar = "-", '<span style="color:#888">미입력</span>'
        rows += f"""
        <tr>
            <td>{k['id']}</td>
            <td>{k['category']}</td>
            <td>{k['name']}</td>
            <td>{k['target']}{k['unit']}</td>
            <td>{actual if actual is not None else '-'}{k['unit'] if actual is not None else ''}</td>
            <td>{bar}</td>
            <td><strong>{pct_str}</strong></td>
            <td>{k['weight']}%</td>
            <td>{k['owner']}</td>
        </tr>"""

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<title>{dept_name} — KPI 현황</title>
<link rel="stylesheet" href="css/style.css">
</head>
<body>
<div class="header">
    <div>
        <h1>M&amp;C KPI — {dept_name}</h1>
        <div class="subtitle">2026 하반기 / 업데이트: {generated}</div>
    </div>
</div>
<nav class="nav">
    <a href="index.html">전체 현황</a>
    {nav_links}
</nav>
<div class="container">
    <table class="kpi-table">
        <thead>
            <tr>
                <th>KPI_ID</th><th>분류</th><th>KPI명</th>
                <th>목표</th><th>실적</th><th>진행</th>
                <th>달성률</th><th>가중치</th><th>담당자</th>
            </tr>
        </thead>
        <tbody>{rows}</tbody>
    </table>
</div>
<script src="js/app.js"></script>
</body>
</html>"""

def main():
    kpi_root = BASE_DIR / "01_KPI수립_2026H2"
    dash_dir = BASE_DIR / "dashboard"
    dash_dir.mkdir(parents=True, exist_ok=True)

    all_data = collect_all_kpi_data(kpi_root)

    # index.html 생성
    (dash_dir / "index.html").write_text(render_index_html(all_data), encoding="utf-8")
    print("✅ index.html 생성 완료")

    # 부문별 페이지 생성
    for dept_data in all_data:
        fname = f"dept_{dept_data['dept']}.html"
        (dash_dir / fname).write_text(render_dept_html(dept_data, all_data), encoding="utf-8")
        print(f"✅ {fname} 생성 완료")

    if not all_data:
        print("⚠️ KPI 데이터 없음 — 빈 대시보드 생성됨")
    else:
        print(f"\n대시보드 열기: {dash_dir / 'index.html'}")

if __name__ == "__main__":
    main()
```

- [ ] **Step 3: 테스트 실행**

```powershell
python -m pytest tests\test_generate_dashboard.py -v
```
Expected: 2 passed

- [ ] **Step 4: 대시보드 첫 생성 실행**

```powershell
cd "D:\Michael\OneDrive - Team Redpanda\ClaudeCowork\01_경영재무\KPI\2026년"
python kpi-system\scripts\03_generate_dashboard.py
```
Expected: `index.html 생성 완료` (데이터 없으므로 빈 대시보드)

- [ ] **Step 5: 브라우저에서 열기**

```powershell
Start-Process "D:\Michael\OneDrive - Team Redpanda\ClaudeCowork\01_경영재무\KPI\2026년\kpi-system\dashboard\index.html"
```

- [ ] **Step 6: Commit**

```powershell
git add kpi-system/scripts/03_generate_dashboard.py kpi-system/dashboard/css/ kpi-system/dashboard/js/ tests/test_generate_dashboard.py
git commit -m "feat: KPI HTML 대시보드 생성기 추가"
```

---

## Phase E: 멀티에이전트 분석 연동

### Task 10: KPI 분석 에이전트 태스크 템플릿 생성

**Files:**
- Create: `kpi-system/scripts/04_analyze_kpi_agent.py`
- Create: `_templates/kpi-analysis/task.md`
- Create: `_templates/kpi-analysis/workers/claude-main/brief.md`

- [ ] **Step 1: 오케스트레이터 태스크 템플릿 작성**

`_templates/kpi-analysis/task.md`:
```markdown
---
task: kpi-analysis-[DEPT]-[MONTH]
status: pending
created: [DATE]
workers_approved: []
---

# KPI 분석 태스크 — [DEPT] [MONTH]

## Goal
[DEPT]의 [MONTH] KPI 실적을 분석하여 달성/미달 원인, 개선 방향, 다음달 권고사항을 도출한다.

## Inputs
- KPI 데이터: `kpi-system/01_KPI수립_2026H2/[DEPT]/kpi_data.json`
- 월간 실적: 위 JSON의 `monthly_actuals.[MONTH]` 필드

## Constraints
- 분석은 claude-main이 수행한다
- 결과는 한국어로 작성한다
- 800자 이내 핵심 요약 + 항목별 세부 분석
- 구체적 수치 기반 분석 (정성적 코멘트 최소화)

## Output Format
`tasks/[TASK_ID]/workers/claude-main/result.md`:
```
## 요약 (핵심 3줄)
...

## 항목별 분석
| KPI명 | 목표 | 실적 | 달성률 | 상태 | 원인/비고 |

## 주요 이슈
...

## 다음달 권고사항
...
```
```

- [ ] **Step 2: 분석 스크립트 구현**

`kpi-system/scripts/04_analyze_kpi_agent.py`:
```python
# KPI 데이터 변경 감지 → 멀티에이전트 분석 태스크 자동 생성

import json, sys, argparse, shutil
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).parent.parent.parent
TASKS_DIR = BASE_DIR / "tasks"
TEMPLATES_DIR = BASE_DIR / "_templates" / "kpi-analysis"

def create_analysis_task(dept: str, month: str) -> Path:
    task_id = f"kpi-analysis-{dept.replace('부문','')}-{month}"
    task_dir = TASKS_DIR / task_id
    task_dir.mkdir(parents=True, exist_ok=True)
    (task_dir / "workers" / "claude-main").mkdir(parents=True, exist_ok=True)

    # kpi_data.json 로드
    kpi_json = BASE_DIR / "kpi-system" / "01_KPI수립_2026H2" / dept / "kpi_data.json"
    if not kpi_json.exists():
        print(f"❌ {dept} kpi_data.json 없음")
        sys.exit(1)
    data = json.loads(kpi_json.read_text(encoding="utf-8"))

    # 월간 실적 추출
    actuals = {}
    for kpi in data["kpis"]:
        val = kpi.get("monthly_actuals", {}).get(month)
        if val is not None:
            pct = round((val / kpi["target"]) * 100, 1) if kpi["target"] else 0
            actuals[kpi["name"]] = {
                "target": kpi["target"], "actual": val, "unit": kpi["unit"],
                "pct": pct, "weight": kpi["weight"], "owner": kpi["owner"]
            }

    if not actuals:
        print(f"⚠️ {dept} {month} 실적 데이터 없음 (monthly_actuals가 비어있음)")
        sys.exit(1)

    # brief.md 작성
    brief_lines = [
        f"# claude-main Brief — {dept} {month} KPI 분석",
        "",
        "## 역할",
        "KPI 월간 실적 데이터를 분석하여 달성 현황, 원인, 개선 방향을 한국어로 작성한다.",
        "",
        "## 입력 데이터",
        f"- 부문: {dept}",
        f"- 분석 월: {month}",
        "",
        "### KPI 실적 요약",
        "| KPI명 | 목표 | 실적 | 달성률 | 가중치 | 담당 |",
        "|-------|------|------|--------|--------|------|",
    ]
    for name, v in actuals.items():
        brief_lines.append(
            f"| {name} | {v['target']}{v['unit']} | {v['actual']}{v['unit']} | {v['pct']}% | {v['weight']}% | {v['owner']} |"
        )
    brief_lines += [
        "",
        "## 요청 산출물",
        "```",
        "## 요약 (3줄 이내)",
        "## 항목별 분석 (각 KPI별 달성/미달 원인)",
        "## 주요 이슈 및 리스크",
        "## 다음달 권고사항 (실행 가능한 구체적 조치)",
        "```",
        "",
        "## 제약",
        "- 800자 이내 핵심 요약",
        "- 수치 기반 분석 (정성적 표현 최소화)",
        "- 한국어 작성",
        f"- target_repo: N/A",
        f"- write_scope: none",
    ]
    brief_path = task_dir / "workers" / "claude-main" / "brief.md"
    brief_path.write_text("\n".join(brief_lines), encoding="utf-8")

    # task.md 작성
    task_md = f"""---
task: {task_id}
status: pending
created: {datetime.now().strftime('%Y-%m-%d %H:%M')}
workers_approved: []
---

# KPI 분석 — {dept} {month}

## Goal
{dept}의 {month} KPI 실적 분석 및 개선 권고

## Inputs
- Brief: `tasks/{task_id}/workers/claude-main/brief.md`

## Constraints
- claude-main 승인 필요
- 결과: `tasks/{task_id}/workers/claude-main/result.md`
"""
    (task_dir / "task.md").write_text(task_md, encoding="utf-8")
    print(f"✅ 분석 태스크 생성: {task_dir}")
    print(f"\n다음 단계:")
    print(f"  1. task.md의 workers_approved에 'claude-main' 추가 (승인)")
    print(f"  2. Orchestrator가 claude-main을 호출하여 분석 실행")
    print(f"  3. result.md 확인: {task_dir}/workers/claude-main/result.md")
    return task_dir

def main():
    parser = argparse.ArgumentParser(description="KPI 분석 에이전트 태스크 생성")
    parser.add_argument("--dept", required=True, help="부문명 (예: 관리부문)")
    parser.add_argument("--month", required=True, help="분석 월 (예: 2026-07)")
    args = parser.parse_args()
    create_analysis_task(args.dept, args.month)

if __name__ == "__main__":
    main()
```

- [ ] **Step 3: 사용법 확인 테스트**

```powershell
python kpi-system\scripts\04_analyze_kpi_agent.py --help
```
Expected: 사용법 출력

- [ ] **Step 4: Commit**

```powershell
git add kpi-system/scripts/04_analyze_kpi_agent.py _templates/kpi-analysis/
git commit -m "feat: KPI 멀티에이전트 분석 태스크 생성기 추가"
```

---

### Task 11: 통합 실행 스크립트 (원-커맨드 워크플로)

**Files:**
- Create: `kpi-system/run_monthly.ps1`
- Create: `kpi-system/run_setup.ps1`

- [ ] **Step 1: 초기 셋업 스크립트**

`kpi-system/run_setup.ps1`:
```powershell
# KPI 시스템 초기 셋업 스크립트
# 실행: cd kpi-system && .\run_setup.ps1

$root = Split-Path $PSScriptRoot -Parent
Set-Location $root

Write-Host "=== M&C KPI 시스템 초기 셋업 ===" -ForegroundColor Cyan

# 의존성 확인
python -c "import openpyxl, jinja2" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "openpyxl, jinja2 설치 중..." -ForegroundColor Yellow
    pip install openpyxl jinja2 -q
}

# 폴더 생성
python kpi-system\scripts\setup_templates.py
Write-Host "✅ 폴더 구조 + 템플릿 생성 완료" -ForegroundColor Green

# 빈 대시보드 생성
python kpi-system\scripts\03_generate_dashboard.py
Write-Host "✅ 대시보드 초기 생성 완료" -ForegroundColor Green

Write-Host ""
Write-Host "다음 단계:" -ForegroundColor Yellow
Write-Host "  1. kpi-system\templates\KPI_수립서_TEMPLATE.xlsx 를 각 부문 폴더에 복사"
Write-Host "  2. 각 부문이 Excel 수립서 작성 후 제출"
Write-Host "  3. run_monthly.ps1 로 데이터 처리 실행"
Write-Host ""
Write-Host "대시보드 열기:" -ForegroundColor Cyan
Write-Host "  Start-Process '$root\kpi-system\dashboard\index.html'"
```

- [ ] **Step 2: 월간 처리 스크립트**

`kpi-system/run_monthly.ps1`:
```powershell
# 월간 KPI 실적 처리 스크립트
# 실행: cd kpi-system && .\run_monthly.ps1 -Month 2026-07

param([string]$Month = (Get-Date -Format "yyyy-MM"))

$root = Split-Path $PSScriptRoot -Parent
Set-Location $root

Write-Host "=== M&C KPI 월간 처리: $Month ===" -ForegroundColor Cyan

$depts = @("관리부문","생산1부문","생산2부문","품질부문","개발영업부문")

# Step 1: Excel → JSON 변환
foreach ($dept in $depts) {
    $xlsxPath = "kpi-system\02_월간추적\$Month\${dept}_$(($Month -split '-')[1])실적.xlsx"
    $jsonOut   = "kpi-system\01_KPI수립_2026H2\$dept\kpi_data.json"
    if (Test-Path $xlsxPath) {
        Write-Host "  변환 중: $dept" -ForegroundColor Gray
        python kpi-system\scripts\02_excel_to_json.py $xlsxPath --out $jsonOut
    } else {
        Write-Host "  ⚠️ 실적 파일 없음: $xlsxPath" -ForegroundColor Yellow
    }
}

# Step 2: 검증
Write-Host "`n검증 중..." -ForegroundColor Cyan
foreach ($dept in $depts) {
    $jsonPath = "kpi-system\01_KPI수립_2026H2\$dept\kpi_data.json"
    if (Test-Path $jsonPath) {
        python kpi-system\scripts\01_validate_kpi.py $jsonPath
    }
}

# Step 3: 대시보드 갱신
Write-Host "`n대시보드 갱신..." -ForegroundColor Cyan
python kpi-system\scripts\03_generate_dashboard.py
Write-Host "✅ 대시보드 갱신 완료" -ForegroundColor Green

# Step 4: 브라우저 열기
$dashPath = "$root\kpi-system\dashboard\index.html"
Write-Host "`n대시보드 열기: $dashPath" -ForegroundColor Cyan
Start-Process $dashPath
```

- [ ] **Step 3: 스크립트 실행 테스트**

```powershell
cd "D:\Michael\OneDrive - Team Redpanda\ClaudeCowork\01_경영재무\KPI\2026년"
powershell -ExecutionPolicy Bypass -File kpi-system\run_setup.ps1
```
Expected: 오류 없이 완료, 대시보드 파일 생성

- [ ] **Step 4: Commit**

```powershell
git add kpi-system/run_monthly.ps1 kpi-system/run_setup.ps1
git commit -m "feat: 통합 실행 스크립트 (셋업 + 월간 처리) 추가"
```

---

## 자가 검토

### Spec 커버리지 확인

| 요구사항 | 구현 태스크 | 상태 |
|---------|-----------|------|
| 회사 방향 연계 핵심 목표 | Task 3 (회사전략목표.md) | ✅ |
| 측정 가능한 KPI (수치 기준) | Task 4 (Excel 템플릿 + 스키마) | ✅ |
| 목표/실행계획/담당자/일정 | Task 4, 5 (Excel 시트 구조) | ✅ |
| 부서별 개선 과제 | Task 2 (KPI 수립 가이드) | ✅ |
| 멀티에이전트 리뷰·분석 | Task 10, 11 (분석 스크립트) | ✅ |
| 웹 대시보드 | Task 8, 9 | ✅ |
| 월간 보고 프로세스 | Task 2 (프로세스 문서) + run_monthly.ps1 | ✅ |
| 연말 평가 프로세스 | Task 2 (연말평가_절차.md) | ✅ |
| 5부문 구조 | Task 1 (폴더 구조), 전 태스크 | ✅ |
| KPI 데이터 추가 시 자동 분석 | Task 10 + 11 | ✅ |

### 실행 순서 (6월 말까지)

```
Phase A (Task 1~3) → Phase B (Task 4~5) → Phase C (Task 6~7)
→ Phase D (Task 8~9) → Phase E (Task 10~11)
예상 소요: 약 3~4시간 (병렬 실행 가능 항목 多)
```

---

*계획 작성: 2026-06-22 | 대상: M&C Electronics Vina KPI 관리 시스템*
