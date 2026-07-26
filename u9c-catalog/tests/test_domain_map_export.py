# 도메인 맵 JSON export 테스트
import json

from u9c_catalog.doc_generator import generate_domain_map_json
from u9c_catalog.models import DomainAssignment, RelationEdge


def test_domain_map_json(tmp_path):
    assigns = [DomainAssignment("dbo", "MO_IssueDocLine", "생산실적", "상세", 0.6, "접두어 MO_"),
               DomainAssignment("dbo", "SM_SOOrder", "매출", "앵커", 0.55, "접두어 SM_")]
    edges = [RelationEdge("dbo.MO_IssueDocLine", "MO", "dbo.MO_MO", "header-detail", "FK명명")]
    out = tmp_path / "domain_map.json"
    generate_domain_map_json(assigns, edges, str(out))
    data = json.loads(out.read_text(encoding="utf-8"))
    assert "생산실적" in data["domains"]
    assert any(t["object"] == "dbo.MO_IssueDocLine" for t in data["domains"]["생산실적"]["tables"])
    assert len(data["relations"]) == 1


def test_domain_map_json_excludes_unclassified(tmp_path):
    assigns = [DomainAssignment("dbo", "UBF_MD_Attribute", "미분류", "미상", 0.0, "플랫폼 접두어 UBF_")]
    out = tmp_path / "domain_map.json"
    generate_domain_map_json(assigns, [], str(out))
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["domains"] == {}
