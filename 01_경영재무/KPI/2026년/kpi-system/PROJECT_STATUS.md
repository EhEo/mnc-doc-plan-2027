# M&C Electronics Vina — KPI 관리 시스템 진행 현황

> 최종 업데이트: 2026-06-22
> 담당: 경영지원팀 (jhlim@mistop.org)

---

## 시스템 개요

| 항목 | 내용 |
|------|------|
| 목적 | KPI 수립→월간추적→분기점검→연말평가 전체 라이프사이클 관리 |
| 대상 | 관리부문 · 생산1부문 · 생산2부문 · 품질부문 · 개발영업부문 (5개 부문) |
| 기반 경로 | `01_경영재무/KPI/2026년/kpi-system/` |
| 테스트 | `python -m pytest tests/ -v` → **9 passed** |

---

## Phase별 완료 현황

### Phase A — 폴더 구조 + 프로세스 문서 ✅

| 산출물 | 경로 | 크기 | 완료일 |
|--------|------|------|--------|
| 전체 폴더 구조 | `kpi-system/` 하위 40+ 폴더 | — | 2026-06-22 |
| KPI 전체 라이프사이클 | `00_프로세스/KPI_전체_라이프사이클.md` | 2,540 bytes | 2026-06-22 |
| KPI 수립 가이드 | `00_프로세스/KPI_수립_가이드.md` | 2,701 bytes | 2026-06-22 |
| 월간보고 절차 | `00_프로세스/월간보고_절차.md` | 1,914 bytes | 2026-06-22 |
| 연말평가 절차 | `00_프로세스/연말평가_절차.md` | 1,884 bytes | 2026-06-22 |
| 통합 운영지침 | `00_프로세스/KPI_통합_운영지침.md` | 14,373 bytes | 2026-06-22 |
| 회사 전략목표 | `01_KPI수립_2026H2/00_회사전략목표.md` | 3,217 bytes | 2026-06-22 |

### Phase B — Excel 템플릿 + 임직원 브리핑 ✅

| 산출물 | 경로 | 크기 | 완료일 |
|--------|------|------|--------|
| KPI 수립서 템플릿 | `templates/KPI_수립서_TEMPLATE.xlsx` | 8,411 bytes | 2026-06-22 |
| 월간실적 입력 템플릿 | `templates/월간실적_TEMPLATE.xlsx` | 5,946 bytes | 2026-06-22 |
| 임직원 브리핑 HTML | `dashboard/kpi_briefing.html` | 42,445 bytes | 2026-06-22 |
| Excel 생성 스크립트 | `scripts/setup_templates.py` | — | 2026-06-22 |

**브리핑 HTML 특징.**
- 10슬라이드 scroll-snap 방식, 키보드 화살표 네비게이션
- 슬라이드9 Gantt 차트: Intersection Observer 순차 애니메이션
- FAQ 아코디언, 역할별 체크리스트, SMART 예시
- Artifact URL: https://claude.ai/code/artifact/475ddf2a-e9b6-4a53-9ba3-ee51033e4290

### Phase C — Python 데이터 엔진 ✅

| 산출물 | 경로 | 테스트 | 완료일 |
|--------|------|--------|--------|
| JSON 스키마 | `schema/kpi_schema.json` | — | 2026-06-22 |
| KPI 검증 스크립트 | `scripts/01_validate_kpi.py` | 4 passed | 2026-06-22 |
| Excel→JSON 변환 | `scripts/02_excel_to_json.py` | 3 passed | 2026-06-22 |

**검증 로직.**
- 부문명 허용값 확인 (5개 부문)
- KPI 항목 수 범위 (3~10개)
- 가중치 합계 = 100% 확인
- deadline 날짜 형식 (YYYY-MM-DD)
- 필수 필드 누락 감지

### Phase D — HTML 대시보드 ✅

| 산출물 | 경로 | 테스트 | 완료일 |
|--------|------|--------|--------|
| 대시보드 CSS | `dashboard/css/style.css` | — | 2026-06-22 |
| 대시보드 JS | `dashboard/js/app.js` | — | 2026-06-22 |
| 대시보드 생성기 | `scripts/03_generate_dashboard.py` | 2 passed | 2026-06-22 |
| 대시보드 메인 | `dashboard/index.html` | — | 2026-06-22 |

**대시보드 기능.**
- 5개 부문 카드 + 달성률 진행 바
- 요약 카드 (등록 부문, 활성 부문, 전체 KPI 수, 목표 달성 항목)
- 부문별 상세 페이지 (테이블 형식)
- 데이터 없을 때 빈 상태 메시지 표시

### Phase E — 멀티에이전트 분석 연동 ✅

| 산출물 | 경로 | 완료일 |
|--------|------|--------|
| 분석 태스크 생성기 | `scripts/04_analyze_kpi_agent.py` | 2026-06-22 |
| 태스크 템플릿 | `_templates/kpi-analysis/task.md` | 2026-06-22 |
| claude-main 브리프 | `_templates/kpi-analysis/workers/claude-main/brief.md` | 2026-06-22 |
| 초기 셋업 스크립트 | `kpi-system/run_setup.ps1` | 2026-06-22 |
| 월간 처리 스크립트 | `kpi-system/run_monthly.ps1` | 2026-06-22 |

---

## 현재 테스트 상태

```
tests/test_validate_kpi.py      — 4 passed
tests/test_excel_to_json.py     — 3 passed
tests/test_generate_dashboard.py — 2 passed
─────────────────────────────────
합계: 9 passed (2026-06-22 기준)
```

실행 명령: `python -m pytest tests/ -v`

---

## 운영 워크플로

### 최초 1회 셋업

```powershell
cd "D:\Michael\OneDrive - Team Redpanda\ClaudeCowork\01_경영재무\KPI\2026년"
powershell -ExecutionPolicy Bypass -File kpi-system\run_setup.ps1
```

### 매월 5일 — 실적 처리

```powershell
# 부문별 월간실적 Excel 파일을 02_월간추적\YYYY-MM\ 에 넣은 후 실행
.\kpi-system\run_monthly.ps1 -Month 2026-07
```

### KPI 미달 시 — AI 분석 요청

```powershell
python kpi-system\scripts\04_analyze_kpi_agent.py --dept 품질부문 --month 2026-07
# → tasks/ 폴더에 분석 태스크 생성 → Orchestrator가 claude-main 호출
```

### 대시보드 수동 열기

```powershell
Start-Process "D:\Michael\OneDrive - Team Redpanda\ClaudeCowork\01_경영재무\KPI\2026년\kpi-system\dashboard\index.html"
```

---

## KPI_ID 명명 규칙

| 부문 | 접두사 | 예시 |
|------|--------|------|
| 관리부문 (인사총무·구매·공무) | MGT | MGT-001, MGT-002 |
| 생산1부문 | PR1 | PR1-001, PR1-002 |
| 생산2부문 (금형 포함) | PR2 | PR2-001, PR2-002 |
| 품질부문 | QUA | QUA-001, QUA-002 |
| 개발영업부문 | SLS | SLS-001, SLS-002 |

---

## 주요 일정

| 일정 | 내용 | 담당 |
|------|------|------|
| **2026-06-28** | KPI 수립서 제출 기한 | 각 부문장 |
| 2026-07-05 | 시스템 등록 (Excel → JSON 변환) | 경영지원 |
| 매월 5일 | 월간 실적 Excel 제출 | 각 부문 담당자 |
| 매월 6일 | 데이터 처리 + 대시보드 갱신 | 경영지원 |
| 2026-10 초 | Q3 분기 점검 보고 | 경영지원 |
| 2026-12-20 | 연말 집계 시작 | 경영지원 |
| 2026-12-31 | 2026 KPI 최종 보고 | 전 부문 |

---

## 변경 이력

| 날짜 | 내용 | 담당 |
|------|------|------|
| 2026-06-22 | Phase A~E 전체 구축 완료, 테스트 9 passed | Claude + 경영지원 |
