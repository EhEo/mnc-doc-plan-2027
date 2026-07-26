# 관계 발견기 테스트
from u9c_catalog.relation_finder import find_relations
from tests.fixtures.sample_metadata import make_flow_tables


def test_header_detail_edge():
    edges = find_relations(make_flow_tables())
    hd = [e for e in edges if e.kind == "header-detail"]
    assert any(e.from_object == "dbo.PM_RcvLine" and e.from_column == "Receivement"
               and e.to_object == "dbo.PM_Receivement" for e in hd)


def test_doc_flow_edge_marked():
    edges = find_relations(make_flow_tables())
    df = [e for e in edges if e.kind == "doc-flow"]
    assert any(e.from_object == "dbo.PM_RcvLine" and "SrcDoc" in e.from_column for e in df)
