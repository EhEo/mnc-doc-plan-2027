# KPI JSON 검증 스크립트 테스트

import json, pytest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "kpi-system" / "scripts"))
from validate_kpi import validate_kpi_file

VALID = {
    "dept": "관리부문", "year": "2026", "half": "H2",
    "version": "v1.0", "status": "draft",
    "kpis": [
        {"id":"MGT-001","category":"인사","name":"교육이수율","target":95,
         "unit":"%","weight":34,"measurement_method":"이수자/대상자×100",
         "owner":"인사총무팀","deadline":"2026-12-31","monthly_actuals":{}},
        {"id":"MGT-002","category":"구매","name":"납기준수율","target":95,
         "unit":"%","weight":33,"measurement_method":"준수건/전체건×100",
         "owner":"구매팀","deadline":"2026-12-31","monthly_actuals":{}},
        {"id":"MGT-003","category":"공무","name":"설비가동률","target":90,
         "unit":"%","weight":33,"measurement_method":"가동시간/총시간×100",
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
