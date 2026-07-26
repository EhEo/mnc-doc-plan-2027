# business_map/relations 적재 함수 통합 테스트
import pytest
from u9c_catalog.catalog_writer import ensure_schema, write_business_map, write_relations
from u9c_catalog.models import DomainAssignment, RelationEdge


@pytest.mark.integration
def test_write_p3(test_conn_str):
    ensure_schema(test_conn_str)
    sid = 900777
    write_business_map(test_conn_str, sid, [
        DomainAssignment("dbo", "MO_IssueDocLine", "생산실적", "상세", 0.6, "접두어 MO_")])
    write_relations(test_conn_str, sid, [
        RelationEdge("dbo.PM_RcvLine", "Receivement", "dbo.PM_Receivement", "header-detail", "FK명명")])
    import pyodbc
    with pyodbc.connect(test_conn_str, autocommit=True) as c:
        cur = c.cursor()
        cur.execute("SELECT domain FROM catalog.business_map WHERE snapshot_id=? AND object_name='MO_IssueDocLine'", sid)
        assert cur.fetchone()[0] == "생산실적"
        cur.execute("SELECT COUNT(*) FROM catalog.relations WHERE snapshot_id=?", sid)
        assert cur.fetchone()[0] == 1
        write_business_map(test_conn_str, sid, [
            DomainAssignment("dbo", "MO_IssueDocLine", "생산실적", "상세", 0.7, "재적재")])
        cur.execute("SELECT COUNT(*) FROM catalog.business_map WHERE snapshot_id=?", sid)
        assert cur.fetchone()[0] == 1
