# U9C 카탈로그 Phase 3a 구현 계획 (도메인 매핑 · 문서흐름 관계, 읽기 전용)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 이미 적재된 카탈로그 스냅샷(운영 snapshot_id=2)만으로, 우선순위 테이블을 **6개 업무 도메인(생산실적·입출고·구매·구매요청·비용등록·매출)에 매핑**하고, **문서흐름 관계(`SrcDoc_*` + 헤더-상세 FK-명명 규약)**를 구조적으로 발견해 `catalog.business_map`·`catalog.relations`에 적재하고 **도메인 맵 JSON**을 내보낸다. 전부 읽기 전용(소스 무접촉, 카탈로그 조회·쓰기)이라 즉시 실행 가능. 이 매핑은 "추정(hypothesis)" 신뢰도이며 Phase 3b(복제본 델타 프로빙+XEvents)에서 확정한다.

**Architecture:** 신규 CLI `u9c-catalog-map`이 카탈로그에서 한 스냅샷의 테이블·컬럼(+우선순위)을 읽어 `TableMeta`로 복원(`catalog_reader`) → `domain_mapper`(순수 규칙)로 도메인 할당 → `relation_finder`(구조적)로 문서흐름/헤더-상세 엣지 도출 → `catalog_writer`로 `business_map`·`relations` 적재 → 도메인 맵 JSON 내보내기. 순수 로직은 픽스처로 단위 테스트, 카탈로그 접근은 LocalDB 통합 테스트.

**Tech Stack:** Phase 1·2와 동일. 신규 의존성 없음.

**참조:** 설계 `docs/superpowers/specs/2026-07-24-u9c-erp-schema-analysis-design.md`, 지식베이스(실측+도메인 힌트) `docs/reference/u9c-schema-knowledge-base.md`, Phase 2 계획 `docs/superpowers/plans/2026-07-25-u9c-catalog-phase2.md`.

**실측 전제(운영 snapshot_id=2):** 도메인↔접두어 실증 — 생산실적 `MO_`/`SFC_`, 입출고 `InvTrans_`/`InvDoc_`, 구매 `PM_`/`Complete_Rcv`/`AP_`, 매출 `SM_`, 비용 `CA_`/`GL_`/`IC_`/`AAI_`. 문서흐름 단서 `SrcDoc_SrcDocSubLine_EntityID`·`SrcDocType`·`DocNo`(1,819 SrcDoc* 컬럼). 헤더-상세 FK 컬럼명 = 부모 엔티티명. `UBF_*`는 플랫폼(업무 아님).

---

## File Structure (Phase 3a 신규/수정)

```
u9c-catalog/src/u9c_catalog/
  catalog_reader.py    # (신규) 카탈로그 스냅샷 → TableMeta 리스트 복원
  domain_mapper.py     # (신규) 순수 규칙: 테이블 → 도메인+신뢰도+근거
  relation_finder.py   # (신규) 구조적 문서흐름/헤더-상세 엣지 도출
  mapper_cli.py        # (신규) u9c-catalog-map 엔트리포인트
  catalog_schema.sql   # (수정) catalog.business_map / relations 테이블 추가
  catalog_writer.py    # (수정) write_business_map / write_relations
  models.py            # (수정) DomainAssignment / RelationEdge dataclass
  pyproject.toml       # (수정) u9c-catalog-map 콘솔 스크립트 등록
tests/
  test_domain_mapper.py       # 순수
  test_relation_finder.py     # 순수(픽스처)
  test_catalog_reader.py      # @integration
  test_catalog_writer_p3.py   # @integration
  fixtures/sample_metadata.py # (수정) SrcDoc/헤더-상세 픽스처 보강
```

---

## Task 1: 모델 추가 (DomainAssignment · RelationEdge)

**Files:** Modify `src/u9c_catalog/models.py`; Test `tests/test_models_p3.py`

- [ ] **Step 1: 실패 테스트** — `tests/test_models_p3.py`
```python
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
```

- [ ] **Step 2: 실패 확인** — `python -m pytest tests/test_models_p3.py -v` → ImportError.

- [ ] **Step 3: models.py 끝에 추가**
```python
@dataclass
class DomainAssignment:
    schema: str
    name: str
    domain: str                    # 생산실적/입출고/구매/구매요청/비용등록/매출/미분류
    role: str                      # 앵커/상세/연관/코드/미상
    confidence: float              # 0.0~1.0 (3a는 추정, 3b에서 상향)
    evidence: str
    verified_by: str | None = None

    @property
    def full_name(self) -> str:
        return f"{self.schema}.{self.name}"


@dataclass
class RelationEdge:
    from_object: str
    from_column: str
    to_object: str
    kind: str                      # "header-detail" | "master-ref" | "doc-flow"
    evidence: str
```

- [ ] **Step 4: 통과 확인** — `python -m pytest tests/test_models_p3.py -v` → 2 passed.
- [ ] **Step 5: 커밋** — `git add src/u9c_catalog/models.py tests/test_models_p3.py && git commit -m "feat(p3a): 도메인 할당/관계 엣지 모델 추가"`

---

## Task 2: 도메인 매퍼 (순수 규칙)

**Files:** Create `src/u9c_catalog/domain_mapper.py`; Test `tests/test_domain_mapper.py`

- [ ] **Step 1: 실패 테스트** — `tests/test_domain_mapper.py`
```python
from u9c_catalog.domain_mapper import assign_domain
from u9c_catalog.models import TableMeta


def _t(name):
    return TableMeta(schema="dbo", name=name, object_type="TABLE")


def test_production_prefix():
    d = assign_domain(_t("MO_IssueDocLine"))
    assert d.domain == "생산실적"
    assert d.confidence >= 0.5
    assert "MO_" in d.evidence


def test_inventory_prefix():
    assert assign_domain(_t("InvTrans_TransLine")).domain == "입출고"
    assert assign_domain(_t("InvDoc_TransInBin")).domain == "입출고"


def test_sales_and_purchase_and_cost():
    assert assign_domain(_t("SM_SOOrder")).domain == "매출"
    assert assign_domain(_t("PM_Receivement")).domain == "구매"
    assert assign_domain(_t("GL_Entry")).domain == "비용등록"


def test_requisition_keyword_beats_generic_pm():
    # 구매요청은 PM_ 중에서도 Requisition/Apply 키워드로 구분
    d = assign_domain(_t("PM_PurchaseRequisition"))
    assert d.domain == "구매요청"


def test_platform_and_unknown():
    assert assign_domain(_t("UBF_MD_Attribute")).domain == "미분류"
    assert assign_domain(_t("ZZ_Something")).domain == "미분류"
```

- [ ] **Step 2: 실패 확인** — `python -m pytest tests/test_domain_mapper.py -v` → ImportError.

- [ ] **Step 3: domain_mapper.py 구현**
```python
# 테이블명(접두어+키워드) 규칙으로 6개 업무 도메인을 추정 할당한다 (순수 로직, 추정 신뢰도).
from u9c_catalog.models import DomainAssignment, TableMeta

# 규칙 우선순위 순서 중요: 더 구체적인 규칙(구매요청)을 일반(구매)보다 앞에 둔다.
# (도메인, [접두어...], [키워드...], 기본신뢰도)
_RULES = [
    ("구매요청", ["PR_"], ["Requisition", "Requisiton", "Apply", "Request", "请购", "请购单"], 0.55),
    ("생산실적", ["MO_", "SFC_"], ["Issue", "Dispatch", "Complete", "OpTransfer", "WIP", "MO"], 0.6),
    ("입출고", ["InvTrans_", "InvDoc_"], ["TransIn", "TransOut", "MiscShip", "Receipt", "Bin"], 0.6),
    ("구매", ["PM_", "PPR_", "AP_", "Complete_Rcv"], ["Purchase", "PO", "Rcv", "Receivement", "APPosted"], 0.55),
    ("매출", ["SM_", "AR_"], ["SOOrder", "Sales", "Ship", "Invoice", "ARPosted"], 0.55),
    ("비용등록", ["CA_", "GL_", "IC_", "AAI_", "FA_"], ["Cost", "Expense", "Fee", "Entry", "Element"], 0.5),
]

# 플랫폼/기반 접두어는 업무 아님 → 미분류 강제
_PLATFORM_PREFIXES = ("UBF_", "Base_")


def _keyword_hit(name: str, keywords: list[str]) -> str | None:
    low = name.lower()
    for k in keywords:
        if k.lower() in low:
            return k
    return None


def _role_of(name: str) -> str:
    return "상세" if name.endswith(("Line", "L", "SubLine", "Detail")) else "앵커"


def assign_domain(table: TableMeta) -> DomainAssignment:
    name = table.name
    # 1) 플랫폼/기반 테이블 → 업무 아님
    for p in _PLATFORM_PREFIXES:
        if name.startswith(p):
            return DomainAssignment(table.schema, name, "미분류", "미상", 0.0, f"플랫폼 접두어 {p}")
    # 2) 구매요청 키워드 선점 (PM_ 등 어느 접두어든 Requisition/请购 계열이면 구매요청)
    req_kw = _keyword_hit(name, ["Requisition", "Requisiton", "请购", "PurApply", "PurRequest"])
    if req_kw:
        return DomainAssignment(table.schema, name, "구매요청", _role_of(name), 0.6, f"키워드 {req_kw}")
    # 3) 접두어(+키워드) 규칙
    for domain, prefixes, keywords, base in _RULES:
        pref = next((p for p in prefixes if name.startswith(p)), None)
        if pref is None:
            continue
        kw = _keyword_hit(name, keywords)
        conf = min(base + 0.15, 0.8) if kw else base
        ev = f"접두어 {pref}" + (f" + 키워드 {kw}" if kw else "")
        return DomainAssignment(table.schema, name, domain, _role_of(name), conf, ev)
    return DomainAssignment(table.schema, name, "미분류", "미상", 0.0, "규칙 미매칭")


def assign_domains(tables: list[TableMeta]) -> list[DomainAssignment]:
    return [assign_domain(t) for t in tables]
```
> `_RULES`의 `구매요청`(PR_ 접두어) 항목은 접두어가 실제 PR_인 테이블용이고, PM_ 안에 섞인 구매요청은 위 2)의 키워드 선점으로 처리한다.

- [ ] **Step 4: 통과 확인** — `python -m pytest tests/test_domain_mapper.py -v` → 5 passed. 이어서 `python -m pytest -q` 전체 순수 회귀.
- [ ] **Step 5: 커밋** — `git add src/u9c_catalog/domain_mapper.py tests/test_domain_mapper.py && git commit -m "feat(p3a): 도메인 매퍼(접두어+키워드 규칙) 추가"`

---

## Task 3: 관계 발견기 (구조적: 문서흐름 · 헤더-상세)

**Files:** Create `src/u9c_catalog/relation_finder.py`; Modify `tests/fixtures/sample_metadata.py`; Test `tests/test_relation_finder.py`

- [ ] **Step 1: 픽스처 보강** — `tests/fixtures/sample_metadata.py`에 함수 추가(기존 유지)
```python
def make_flow_tables():
    """헤더-상세 + SrcDoc 문서흐름 픽스처."""
    from u9c_catalog.models import ColumnMeta, TableMeta
    hdr = TableMeta(schema="dbo", name="PM_Receivement", object_type="TABLE")
    hdr.columns.append(ColumnMeta(name="ID", data_type="bigint", is_nullable=False, is_pk=True))
    hdr.columns.append(ColumnMeta(name="DocNo", data_type="nvarchar", is_nullable=False))
    line = TableMeta(schema="dbo", name="PM_RcvLine", object_type="TABLE")
    line.columns.append(ColumnMeta(name="ID", data_type="bigint", is_nullable=False, is_pk=True))
    line.columns.append(ColumnMeta(name="Receivement", data_type="bigint", is_nullable=False))  # 헤더-상세 FK명=부모엔티티명
    line.columns.append(ColumnMeta(name="SrcDoc_SrcDocSubLine_EntityID", data_type="bigint", is_nullable=True))
    line.columns.append(ColumnMeta(name="SrcDocType", data_type="int", is_nullable=True))
    return [hdr, line]
```

- [ ] **Step 2: 실패 테스트** — `tests/test_relation_finder.py`
```python
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
    # SrcDoc_* 컬럼 보유 → 문서흐름 참여 엣지(대상 미상은 to_object="?")
    assert any(e.from_object == "dbo.PM_RcvLine" and "SrcDoc" in e.from_column for e in df)
```

- [ ] **Step 3: 실패 확인** — `python -m pytest tests/test_relation_finder.py -v` → ImportError.

- [ ] **Step 4: relation_finder.py 구현**
```python
# 카탈로그 메타데이터만으로 구조적 관계를 발견한다: 헤더-상세(FK명=부모엔티티명) + 문서흐름(SrcDoc_*).
from u9c_catalog.models import RelationEdge, TableMeta

_SRCDOC_MARKERS = ("SrcDoc", "SrcDocType")


def find_relations(tables: list[TableMeta]) -> list[RelationEdge]:
    edges: list[RelationEdge] = []
    # 엔티티명 → full_name 색인 (헤더-상세/마스터참조 판정용). 테이블명이 곧 엔티티명.
    name_index: dict[str, str] = {t.name: t.full_name for t in tables}

    for t in tables:
        for c in t.columns:
            # 1) 헤더-상세/마스터참조: 컬럼명이 다른 테이블명과 정확히 일치 (FK명=부모엔티티명 규약)
            if c.name in name_index and name_index[c.name] != t.full_name:
                kind = "header-detail" if t.name.endswith(("Line", "L", "SubLine")) else "master-ref"
                edges.append(RelationEdge(
                    from_object=t.full_name, from_column=c.name,
                    to_object=name_index[c.name], kind=kind, evidence="FK명명(컬럼명=부모엔티티명)"))
            # 2) 문서흐름: SrcDoc 계열 컬럼 → 상류 단거 참조(대상 테이블은 SrcDocType 값→메타데이터 필요, 여기선 미상)
            elif any(m in c.name for m in _SRCDOC_MARKERS):
                edges.append(RelationEdge(
                    from_object=t.full_name, from_column=c.name,
                    to_object="?", kind="doc-flow", evidence="SrcDoc 계열 컬럼(상류 단거 추적 단서)"))
    return edges
```

- [ ] **Step 5: 통과 확인** — `python -m pytest tests/test_relation_finder.py -v` → 2 passed.
- [ ] **Step 6: 커밋** — `git add src/u9c_catalog/relation_finder.py tests/test_relation_finder.py tests/fixtures/sample_metadata.py && git commit -m "feat(p3a): 구조적 관계 발견기(헤더-상세+SrcDoc 문서흐름) 추가"`

---

## Task 4: 카탈로그 리더 (스냅샷 → TableMeta)

**Files:** Create `src/u9c_catalog/catalog_reader.py`; Test `tests/test_catalog_reader.py`

- [ ] **Step 1: 실패 테스트(@integration)** — `tests/test_catalog_reader.py`
```python
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
    # 컬럼과 is_system 태그가 복원되는지
    cols = {c.name: c for c in by["PM_Receivement"].columns}
    assert cols["Org"].is_system is True
    assert by["CBO_ItemMaster_Trl"].is_auxiliary is True
```

- [ ] **Step 2: 실패 확인** — `python -m pytest tests/test_catalog_reader.py -v` → import 실패.

- [ ] **Step 3: catalog_reader.py 구현**
```python
# 카탈로그의 한 스냅샷에서 테이블·컬럼(+우선순위)을 TableMeta로 복원한다.
from u9c_catalog.db import connect
from u9c_catalog.models import ColumnMeta, TableMeta


def load_snapshot_tables(catalog_conn: str, snapshot_id: int,
                         priority_only: bool = False) -> list[TableMeta]:
    with connect(catalog_conn, readonly=True) as conn:
        cur = conn.cursor()
        obj_sql = ("SELECT o.schema_name, o.object_name, o.object_type, o.row_count, "
                   "o.is_auxiliary, o.aux_reason FROM catalog.objects o ")
        params = [snapshot_id]
        if priority_only:
            obj_sql += ("JOIN catalog.priority p ON p.snapshot_id=o.snapshot_id "
                        "AND p.schema_name=o.schema_name AND p.object_name=o.object_name "
                        "AND p.is_priority=1 ")
        obj_sql += "WHERE o.snapshot_id=?"
        cur.execute(obj_sql, *params)
        tables: dict[str, TableMeta] = {}
        for r in cur.fetchall():
            t = TableMeta(schema=r[0], name=r[1], object_type=r[2], row_count=r[3],
                          is_auxiliary=bool(r[4]), auxiliary_reason=r[5])
            tables[t.full_name] = t

        cur.execute(
            "SELECT schema_name, object_name, column_name, data_type, is_nullable, is_pk, "
            "is_system, system_reason, ordinal FROM catalog.columns WHERE snapshot_id=? "
            "ORDER BY schema_name, object_name, ordinal", snapshot_id)
        for r in cur.fetchall():
            key = f"{r[0]}.{r[1]}"
            t = tables.get(key)
            if t is None:
                continue
            c = ColumnMeta(name=r[2], data_type=r[3], is_nullable=bool(r[4]),
                           is_pk=bool(r[5]), ordinal=r[8])
            c.is_system = bool(r[6]); c.system_reason = r[7]
            t.columns.append(c)
    return list(tables.values())
```

- [ ] **Step 4: 통합 통과 확인** — 픽스처 catalog 재생성(Phase 1 절차) 후 `python -m pytest tests/test_catalog_reader.py -m integration -v` → 1 passed.
- [ ] **Step 5: 커밋** — `git add src/u9c_catalog/catalog_reader.py tests/test_catalog_reader.py && git commit -m "feat(p3a): 카탈로그 스냅샷 → TableMeta 리더 추가"`

---

## Task 5: 카탈로그 스키마·적재기 확장 (business_map · relations)

**Files:** Modify `src/u9c_catalog/catalog_schema.sql`, `src/u9c_catalog/catalog_writer.py`; Test `tests/test_catalog_writer_p3.py`

- [ ] **Step 1: catalog_schema.sql에 테이블 추가 (파일 끝, 기존 GO 패턴)**
```sql
IF OBJECT_ID('catalog.business_map','U') IS NULL
CREATE TABLE catalog.business_map (
    snapshot_id int NOT NULL, schema_name nvarchar(128) NOT NULL, object_name nvarchar(256) NOT NULL,
    domain nvarchar(40) NOT NULL, role nvarchar(20) NULL, confidence float NOT NULL,
    evidence nvarchar(400) NULL, verified_by nvarchar(64) NULL,
    CONSTRAINT PK_catalog_business_map PRIMARY KEY (snapshot_id, schema_name, object_name)
);
GO
IF OBJECT_ID('catalog.relations','U') IS NULL
CREATE TABLE catalog.relations (
    snapshot_id int NOT NULL, from_object nvarchar(384) NOT NULL, from_column nvarchar(128) NOT NULL,
    to_object nvarchar(384) NULL, kind nvarchar(20) NOT NULL, evidence nvarchar(400) NULL
);
GO
```

- [ ] **Step 2: 실패 테스트(@integration)** — `tests/test_catalog_writer_p3.py`
```python
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
        # 재적재 멱등
        write_business_map(test_conn_str, sid, [
            DomainAssignment("dbo", "MO_IssueDocLine", "생산실적", "상세", 0.7, "재적재")])
        cur.execute("SELECT COUNT(*) FROM catalog.business_map WHERE snapshot_id=?", sid)
        assert cur.fetchone()[0] == 1
```

- [ ] **Step 3: 실패 확인** — `python -m pytest tests/test_catalog_writer_p3.py -v` → import 실패.

- [ ] **Step 4: catalog_writer.py에 함수 추가 (기존 `_replace` 재사용)**
```python
def write_business_map(catalog_conn, snapshot_id, assignments):
    with connect(catalog_conn) as conn:
        cur = conn.cursor()
        _replace(cur, "business_map", snapshot_id,
                 "INSERT INTO catalog.business_map(snapshot_id,schema_name,object_name,domain,role,confidence,evidence,verified_by) VALUES (?,?,?,?,?,?,?,?)",
                 [(snapshot_id, a.schema, a.name, a.domain, a.role, a.confidence, a.evidence, a.verified_by) for a in assignments])


def write_relations(catalog_conn, snapshot_id, edges):
    with connect(catalog_conn) as conn:
        cur = conn.cursor()
        _replace(cur, "relations", snapshot_id,
                 "INSERT INTO catalog.relations(snapshot_id,from_object,from_column,to_object,kind,evidence) VALUES (?,?,?,?,?,?)",
                 [(snapshot_id, e.from_object, e.from_column, e.to_object, e.kind, e.evidence) for e in edges])
```
> 주의: `catalog.relations`는 PK가 없어 `_replace`의 DELETE→INSERT가 그대로 동작(스냅샷 단위 재적재). `business_map`은 PK로 멱등.

- [ ] **Step 5: 스키마 재생성 후 통합 통과** — 픽스처 catalog 드롭·재생성(Phase 1 절차에 business_map/relations 드롭 추가) 후 `python -m pytest tests/test_catalog_writer_p3.py -m integration -v` → 1 passed.
- [ ] **Step 6: 커밋** — `git add src/u9c_catalog/catalog_schema.sql src/u9c_catalog/catalog_writer.py tests/test_catalog_writer_p3.py && git commit -m "feat(p3a): business_map/relations 스키마 및 적재 추가"`

---

## Task 6: 매핑 CLI + 도메인 맵 export

**Files:** Create `src/u9c_catalog/mapper_cli.py`; Modify `src/u9c_catalog/doc_generator.py`, `pyproject.toml`; Test `tests/test_domain_map_export.py`

- [ ] **Step 1: doc_generator.py에 도메인 맵 export 추가 + 실패 테스트**
`tests/test_domain_map_export.py`:
```python
import json
from u9c_catalog.doc_generator import generate_domain_map_json
from u9c_catalog.models import DomainAssignment, RelationEdge


def test_domain_map_json(tmp_path):
    assigns = [DomainAssignment("dbo","MO_IssueDocLine","생산실적","상세",0.6,"접두어 MO_"),
               DomainAssignment("dbo","SM_SOOrder","매출","앵커",0.55,"접두어 SM_")]
    edges = [RelationEdge("dbo.MO_IssueDocLine","MO","dbo.MO_MO","header-detail","FK명명")]
    out = tmp_path / "domain_map.json"
    generate_domain_map_json(assigns, edges, str(out))
    data = json.loads(out.read_text(encoding="utf-8"))
    assert "생산실적" in data["domains"]
    assert any(t["object"] == "dbo.MO_IssueDocLine" for t in data["domains"]["생산실적"]["tables"])
    assert len(data["relations"]) == 1
```
`doc_generator.py`에 추가(파일 끝, `import json`은 이미 있음):
```python
def generate_domain_map_json(assignments, edges, out_path):
    """도메인별 테이블 + 관계 엣지를 MES/대시보드용 JSON으로 내보낸다."""
    domains: dict = {}
    for a in assignments:
        if a.domain == "미분류":
            continue
        d = domains.setdefault(a.domain, {"tables": []})
        d["tables"].append({"object": a.full_name, "role": a.role,
                            "confidence": round(a.confidence, 2), "evidence": a.evidence,
                            "verified_by": a.verified_by})
    rels = [{"from": e.from_object, "column": e.from_column, "to": e.to_object,
             "kind": e.kind, "evidence": e.evidence} for e in edges]
    data = {"domains": domains, "relations": rels}
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
```

- [ ] **Step 2: 실패 확인 → 구현 → 통과** — `python -m pytest tests/test_domain_map_export.py -v` → 1 passed.

- [ ] **Step 3: mapper_cli.py 구현**
```python
# 카탈로그 스냅샷에서 도메인 매핑 + 관계를 계산해 카탈로그에 적재하고 도메인 맵을 내보낸다.
import argparse
import os

from u9c_catalog.catalog_reader import load_snapshot_tables
from u9c_catalog.catalog_writer import ensure_schema, write_business_map, write_relations
from u9c_catalog.config import load_settings
from u9c_catalog.doc_generator import generate_domain_map_json
from u9c_catalog.domain_mapper import assign_domains
from u9c_catalog.relation_finder import find_relations
from u9c_catalog.db import connect


def _latest_snapshot(catalog_conn: str) -> int:
    with connect(catalog_conn, readonly=True) as c:
        cur = c.cursor()
        cur.execute("SELECT MAX(snapshot_id) FROM catalog.snapshots")
        return int(cur.fetchone()[0])


def run(config_path: str, snapshot_id: int | None, priority_only: bool) -> int:
    s = load_settings(config_path)
    ensure_schema(s.catalog_conn)
    sid = snapshot_id or _latest_snapshot(s.catalog_conn)
    print(f"[map] snapshot_id={sid} 대상")

    tables = load_snapshot_tables(s.catalog_conn, sid, priority_only=priority_only)
    print(f"[map] 테이블 {len(tables)}개 로드 (priority_only={priority_only})")

    assignments = assign_domains(tables)
    write_business_map(s.catalog_conn, sid, assignments)
    from collections import Counter
    dist = Counter(a.domain for a in assignments)
    print(f"[map] 도메인 분포: {dict(dist)}")

    edges = find_relations(tables)
    write_relations(s.catalog_conn, sid, edges)
    print(f"[map] 관계 엣지 {len(edges)}개")

    os.makedirs(s.output_dir, exist_ok=True)
    out = os.path.join(s.output_dir, "domain_map.json")
    generate_domain_map_json(assignments, edges, out)
    print(f"[map] 도메인 맵: {out}")
    print("완료.")
    return 0


def main() -> None:
    p = argparse.ArgumentParser(description="U9C 도메인 매핑 (Phase 3a)")
    p.add_argument("--config", default="config.yaml")
    p.add_argument("--snapshot", type=int, default=None, help="대상 snapshot_id (기본: 최신)")
    p.add_argument("--priority-only", action="store_true", help="우선순위 테이블만 매핑")
    a = p.parse_args()
    raise SystemExit(run(a.config, a.snapshot, a.priority_only))


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: pyproject.toml 콘솔 스크립트 등록** — `[project.scripts]`에 추가:
```toml
u9c-catalog-map = "u9c_catalog.mapper_cli:main"
```
재설치: `pip install -e ".[dev]"` (엔트리포인트 갱신).

- [ ] **Step 5: import 스모크 + 전체 순수 테스트** — `python -c "from u9c_catalog.mapper_cli import run; print('ok')"` → ok. `python -m pytest -q` → 순수 전부 통과.

- [ ] **Step 6: E2E (LocalDB 픽스처 카탈로그)** — 픽스처 catalog에 스냅샷이 있어야 하므로, 먼저 Phase 1 파이프라인을 픽스처에 한 번 돌려 snapshot 생성(또는 기존 사용) 후:
`python -m u9c_catalog.mapper_cli --config <임시config> --priority-only`
기대: `[map]` 로그, 도메인 분포 출력, `output/domain_map.json` 생성, `catalog.business_map`·`catalog.relations`에 행 적재. PM_Receivement→구매, PM_RcvLine→구매(상세), 헤더-상세 엣지 존재 확인.

- [ ] **Step 7: 커밋** — `git add src/u9c_catalog/mapper_cli.py src/u9c_catalog/doc_generator.py tests/test_domain_map_export.py pyproject.toml && git commit -m "feat(p3a): 도메인 매핑 CLI + 도메인 맵 export"`

---

## Phase 3a 완료 기준

- [ ] 순수 테스트(models_p3, domain_mapper, relation_finder, domain_map_export) 통과.
- [ ] 통합 테스트(catalog_reader, catalog_writer_p3) LocalDB로 통과.
- [ ] `u9c-catalog-map`으로 운영 snapshot_id=2에 대해 도메인 매핑 실행 → `catalog.business_map` 적재 + `domain_map.json` 생성, 6개 도메인 분포 확인.

## 운영 적용 메모

- 운영 매핑은 소스 무접촉(카탈로그만 조회·쓰기). `--priority-only`로 상위 200개만 매핑하면 노이즈 적고 검수 쉬움.
- 결과는 "추정" 신뢰도(0.5~0.8). `verified_by`는 비워두고 Phase 3b 델타 프로빙에서 채운다.
- 도메인 규칙(`domain_mapper._RULES`)은 실측으로 계속 보정. 미분류 상위 테이블을 검토해 규칙 추가.

## Phase 3b 예고 (다음 계획 — 운영 복제본 + XEvents 필요)

- 운영 백업을 UAT에 복원해 **쓰기 가능한 프로빙 U9C** 구성.
- `delta_prober` — 업무 1건 수행 전후 row수·MAX(ID) 스냅샷 diff → 변경 테이블 = 그 업무의 테이블.
- `xevents_capture` — 프로빙 구간 SQL 캡처·파싱 → 컬럼 단위 확정.
- `value_link_finder` — 후보 코드/문서번호 컬럼의 값 공유로 암묵 관계·`SrcDocType`→대상테이블 해소.
- 위 근거로 `business_map.confidence` 상향 + `verified_by` 기록, `relations`의 `doc-flow to_object="?"` 실제 테이블로 확정.
