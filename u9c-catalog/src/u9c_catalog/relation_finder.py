# 카탈로그 메타데이터만으로 구조적 관계를 발견한다: 헤더-상세(FK명=부모엔티티명) + 문서흐름(SrcDoc_*).
from u9c_catalog.models import RelationEdge, TableMeta

_SRCDOC_MARKERS = ("SrcDoc", "SrcDocType")


def find_relations(tables: list[TableMeta]) -> list[RelationEdge]:
    edges: list[RelationEdge] = []
    name_index: dict[str, str] = {t.name: t.full_name for t in tables}

    # 테이블명에서 공통 접두사를 제거한 short name도 인덱싱
    for t in tables:
        parts = t.name.split('_')
        if len(parts) > 1:
            short_name = parts[-1]
            if short_name not in name_index:
                name_index[short_name] = t.full_name

    for t in tables:
        for c in t.columns:
            if c.name in name_index and name_index[c.name] != t.full_name:
                kind = "header-detail" if t.name.endswith(("Line", "L", "SubLine")) else "master-ref"
                edges.append(RelationEdge(
                    from_object=t.full_name, from_column=c.name,
                    to_object=name_index[c.name], kind=kind, evidence="FK명명(컬럼명=부모엔티티명)"))
            elif any(m in c.name for m in _SRCDOC_MARKERS):
                edges.append(RelationEdge(
                    from_object=t.full_name, from_column=c.name,
                    to_object="?", kind="doc-flow", evidence="SrcDoc 계열 컬럼(상류 단거 추적 단서)"))
    return edges
