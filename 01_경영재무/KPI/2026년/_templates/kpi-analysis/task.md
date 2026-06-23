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
`tasks/[TASK_ID]/workers/claude-main/result.md`에 아래 형식으로 작성:

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
