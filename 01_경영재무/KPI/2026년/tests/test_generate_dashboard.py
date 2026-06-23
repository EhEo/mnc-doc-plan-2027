# 대시보드 생성기 테스트

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
