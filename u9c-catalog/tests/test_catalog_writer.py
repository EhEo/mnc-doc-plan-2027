import pytest

from u9c_catalog.catalog_writer import ensure_schema, write_snapshot
from u9c_catalog.extractor import ExtractResult
from tests.fixtures.sample_metadata import make_receivement_table, make_trl_table
from u9c_catalog.noise_classifier import classify_all


@pytest.mark.integration
def test_write_snapshot_persists_objects(test_conn_str):
    ensure_schema(test_conn_str)
    result = ExtractResult(tables=[make_receivement_table(), make_trl_table()])
    classify_all(result.tables)

    snapshot_id = write_snapshot(test_conn_str, result, label="pytest")
    assert isinstance(snapshot_id, int)

    import pyodbc
    with pyodbc.connect(test_conn_str, autocommit=True) as c:
        cur = c.cursor()
        cur.execute(
            "SELECT COUNT(*) FROM catalog.objects WHERE snapshot_id=? AND is_auxiliary=1",
            snapshot_id,
        )
        assert cur.fetchone()[0] == 1  # _Trl 테이블
        cur.execute(
            "SELECT COUNT(*) FROM catalog.columns WHERE snapshot_id=? AND is_system=1",
            snapshot_id,
        )
        assert cur.fetchone()[0] >= 5  # 시스템 컬럼들
