from u9c_catalog.models import DomainAssignment, RelationEdge


def test_domain_assignment():
    d = DomainAssignment(schema="dbo", name="MO_IssueDocLine", domain="생산실적",
                         role="상세", confidence=0.6, evidence="접두어 MO_")
    assert d.full_name == "dbo.MO_IssueDocLine"
    assert d.verified_by is None


def test_relation_edge():
    e = RelationEdge(from_object="dbo.PM_RcvLine", from_column="Receivement",
                     to_object="dbo.PM_Receivement", kind="header-detail", evidence="FK명명")
    assert e.kind == "header-detail"
