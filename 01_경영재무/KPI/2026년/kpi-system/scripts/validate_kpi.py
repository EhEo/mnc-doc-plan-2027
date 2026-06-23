# KPI JSON 데이터 유효성 검증 모듈

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
        print("Usage: python validate_kpi.py <kpi_data.json>")
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
