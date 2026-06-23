# KPI 데이터 → 멀티에이전트 분석 태스크 자동 생성

import json, sys, argparse
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).parent.parent.parent
TASKS_DIR = BASE_DIR / "tasks"

def create_analysis_task(dept: str, month: str) -> Path:
    task_id = f"kpi-analysis-{dept.replace('부문','')}-{month}"
    task_dir = TASKS_DIR / task_id
    task_dir.mkdir(parents=True, exist_ok=True)
    (task_dir / "workers" / "claude-main").mkdir(parents=True, exist_ok=True)

    kpi_json = BASE_DIR / "kpi-system" / "01_KPI수립_2026H2" / dept / "kpi_data.json"
    if not kpi_json.exists():
        print(f"❌ {dept} kpi_data.json 없음 — Excel 수립서를 먼저 변환하세요.")
        sys.exit(1)
    data = json.loads(kpi_json.read_text(encoding="utf-8"))

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
        print(f"⚠️  {dept} {month} 실적 없음 (monthly_actuals['{month}'] 비어있음)")
        sys.exit(1)

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
            f"| {name} | {v['target']}{v['unit']} | {v['actual']}{v['unit']} "
            f"| {v['pct']}% | {v['weight']}% | {v['owner']} |"
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
        "- target_repo: N/A",
        "- write_scope: none",
    ]
    brief_path = task_dir / "workers" / "claude-main" / "brief.md"
    brief_path.write_text("\n".join(brief_lines), encoding="utf-8")

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
- claude-main 승인 필요 (workers_approved에 추가 후 실행)
- 결과 저장: `tasks/{task_id}/workers/claude-main/result.md`
"""
    (task_dir / "task.md").write_text(task_md, encoding="utf-8")

    print(f"✅ 분석 태스크 생성 완료: tasks/{task_id}/")
    print(f"\n다음 단계:")
    print(f"  1. task.md의 workers_approved에 'claude-main' 추가")
    print(f"  2. Orchestrator가 brief.md 기반으로 claude-main 호출")
    print(f"  3. 결과 확인: tasks/{task_id}/workers/claude-main/result.md")
    return task_dir

def main():
    parser = argparse.ArgumentParser(description="KPI 분석 에이전트 태스크 생성")
    parser.add_argument("--dept", required=True,
                        choices=["관리부문","생산1부문","생산2부문","품질부문","개발영업부문"],
                        help="부문명")
    parser.add_argument("--month", required=True, help="분석 월 (예: 2026-07)")
    create_analysis_task(parser.parse_args().dept, parser.parse_args().month)

if __name__ == "__main__":
    main()
