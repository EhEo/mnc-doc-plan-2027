import pytest

from u9c_catalog.catalog_writer import ensure_schema, write_activity, write_usage, write_priority, write_profiles
from u9c_catalog.models import ActivityMeta, PriorityMeta, ColumnProfile


@pytest.mark.integration
def test_write_phase2(test_conn_str):
    ensure_schema(test_conn_str)
    sid = 900001
    write_activity(test_conn_str, sid, [ActivityMeta("dbo", "T", "2026-07-01", "ModifiedOn")])
    write_usage(test_conn_str, sid, {"dbo.T": {"seeks": 5, "scans": 1, "lookups": 0, "updates": 2}})
    write_priority(test_conn_str, sid, [PriorityMeta("dbo", "T", 3.2, 1, True, "활성+2")])
    write_profiles(test_conn_str, sid, [ColumnProfile("dbo", "T", "C", 0.0, 3, 10, "a", "z")])

    import pyodbc
    with pyodbc.connect(test_conn_str, autocommit=True) as c:
        cur = c.cursor()
        for tbl in ["activity", "usage", "priority", "profiles"]:
            cur.execute(f"SELECT COUNT(*) FROM catalog.{tbl} WHERE snapshot_id=?", sid)
            assert cur.fetchone()[0] == 1, tbl
        write_activity(test_conn_str, sid, [ActivityMeta("dbo", "T", "2026-07-02", "ModifiedOn")])
        cur.execute("SELECT COUNT(*) FROM catalog.activity WHERE snapshot_id=?", sid)
        assert cur.fetchone()[0] == 1
