import json
from u9c_catalog.doc_generator import generate_priority_json, filter_priority_tables
from u9c_catalog.extractor import ExtractResult
from u9c_catalog.models import PriorityMeta
from tests.fixtures.sample_metadata import make_receivement_table, make_trl_table


def test_generate_priority_json(tmp_path):
    prios = [PriorityMeta("dbo", "PM_Receivement", 5.0, 1, True, "활성+2"),
             PriorityMeta("dbo", "CBO_ItemMaster_Trl", -3.0, 2, False, "부수(-5)")]
    out = tmp_path / "priority.json"
    generate_priority_json(prios, str(out))
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data[0]["object"] == "dbo.PM_Receivement"
    assert data[0]["is_priority"] is True
    assert data[0]["rank"] == 1


def test_filter_priority_tables():
    r = ExtractResult(tables=[make_receivement_table(), make_trl_table()])
    prios = [PriorityMeta("dbo", "PM_Receivement", 5.0, 1, True),
             PriorityMeta("dbo", "CBO_ItemMaster_Trl", -3.0, 2, False)]
    filtered = filter_priority_tables(r.tables, prios)
    assert [t.name for t in filtered] == ["PM_Receivement"]
