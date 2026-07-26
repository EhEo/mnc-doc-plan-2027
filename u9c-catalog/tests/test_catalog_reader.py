# catalog_reader.load_snapshot_tables 통합 테스트
import pytest
from u9c_catalog.catalog_reader import load_snapshot_tables
from u9c_catalog.catalog_writer import ensure_schema, write_snapshot
from u9c_catalog.extractor import ExtractResult
from u9c_catalog.noise_classifier import classify_all
from tests.fixtures.sample_metadata import make_receivement_table, make_trl_table


@pytest.mark.integration
def test_load_snapshot_tables(test_conn_str):
    ensure_schema(test_conn_str)
    r = ExtractResult(tables=[make_receivement_table(), make_trl_table()])
    classify_all(r.tables)
    sid = write_snapshot(test_conn_str, r, label="p3reader")

    tables = load_snapshot_tables(test_conn_str, sid)
    by = {t.name: t for t in tables}
    assert "PM_Receivement" in by
    cols = {c.name: c for c in by["PM_Receivement"].columns}
    assert cols["Org"].is_system is True
    assert by["CBO_ItemMaster_Trl"].is_auxiliary is True
