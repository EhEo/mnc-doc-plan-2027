# U9C 카탈로그 Phase 2 구현 계획

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Phase 1 카탈로그에 **활성도 신호(row 수 + 최근 ModifiedOn/CreatedOn)**와 **우선순위 점수**를 더하고, 상위 우선순위 테이블에 **데이터 프로파일링**을 수행하며, "살아있는 실질 업무 테이블"만 담은 **선별 데이터 사전 + 우선순위 JSON**을 생성한다. DMV 사용량은 권한(`VIEW SERVER STATE`)이 있으면 자동 수집, 없으면 건너뛴다.

**Architecture:** Phase 1 파이프라인(추출→분류)에 4개 단계를 잇는다 — 활성도 수집(`activity`) → (선택)DMV 사용량(`usage_dmv`) → 우선순위 점수(`prioritizer`, 순수 로직) → 상위 N개 프로파일링(`profiler`). 결과는 `ERP_Catalog`의 신규 테이블에 적재하고, 선별 문서·JSON을 생성한다. DB 접근 모듈은 LocalDB 픽스처로 통합 테스트, 순수 로직은 픽스처로 단위 테스트.

**Tech Stack:** Phase 1과 동일 (Python 3.11+, pyodbc, jinja2, openpyxl, pytest). 신규 의존성 없음.

**참조:** 설계 `docs/superpowers/specs/2026-07-24-u9c-erp-schema-analysis-design.md`, 지식베이스 `docs/reference/u9c-schema-knowledge-base.md`(실측 검증 절 포함), Phase 1 계획 `docs/superpowers/plans/2026-07-24-u9c-catalog-phase1.md`.

**실측 전제(2026-07-25, 운영 U9CEDB):** 선언 FK 68개뿐 → 구조 중요도는 FK보다 참조 컬럼 수/도메인으로 판단. 감사 컬럼 `CreatedOn`/`ModifiedOn`(및 `CreateDate`/`ModifyDate` 변형) 광범위 존재 → 활성도 신호로 활용. DMV는 현재 권한 부족으로 기본 skip.

---

## File Structure (Phase 2 신규/수정)

```
u9c-catalog/src/u9c_catalog/
  activity.py          # (신규) 테이블별 최근 활동시각 수집: 감사/날짜 컬럼 탐지 + MAX 조회
  usage_dmv.py         # (신규) DMV 사용량 수집 (권한 없으면 graceful skip)
  prioritizer.py       # (신규) 순수 로직: 신호 결합 → 우선순위 점수·랭크
  profiler.py          # (신규) 상위 테이블 데이터 프로파일링 (NULL율/distinct/min-max)
  catalog_schema.sql   # (수정) catalog.activity / usage / priority / profiles 테이블 추가
  catalog_writer.py    # (수정) 위 결과 적재 함수 추가
  doc_generator.py     # (수정) 선별 데이터 사전 + 우선순위 JSON export 추가
  cli.py               # (수정) Phase 2 단계 연결 + 옵션(--profile-top)
  models.py            # (수정) 활성도/우선순위/프로파일 dataclass 추가
tests/
  test_activity.py         # 컬럼 선택 로직 단위 + @integration MAX 조회
  test_prioritizer.py      # 순수 점수 로직
  test_profiler.py         # @integration
  test_catalog_writer_p2.py# @integration (신규 테이블 적재)
  test_doc_generator_p2.py # 선별 문서 + JSON
  sql/create_fixture_db.sql# (수정) 활성도/프로파일 테스트용 데이터 보강
```

---

## Task 1: 모델 확장 (활성도·우선순위·프로파일)

**Files:** Modify `src/u9c_catalog/models.py`; Test `tests/test_models_p2.py`

- [ ] **Step 1: 실패 테스트 작성** — `tests/test_models_p2.py`
```python
from u9c_catalog.models import ActivityMeta, PriorityMeta, ColumnProfile


def test_activity_meta():
    a = ActivityMeta(schema="dbo", name="PM_Receivement", last_activity=None, source="none")
    assert a.full_name == "dbo.PM_Receivement"


def test_priority_meta_defaults():
    p = PriorityMeta(schema="dbo", name="T", score=1.5, rank=1)
    assert p.is_priority is False


def test_column_profile():
    cp = ColumnProfile(schema="dbo", name="T", column_name="C", null_ratio=0.1,
                       distinct_count=5, sample_size=100)
    assert cp.min_value is None
```

- [ ] **Step 2: 실패 확인** — `python -m pytest tests/test_models_p2.py -v` → ImportError.

- [ ] **Step 3: models.py에 추가**
```python
@dataclass
class ActivityMeta:
    schema: str
    name: str
    last_activity: object | None          # datetime 또는 None
    source: str                            # 활동시각 산출 근거 컬럼명 또는 "none"

    @property
    def full_name(self) -> str:
        return f"{self.schema}.{self.name}"


@dataclass
class PriorityMeta:
    schema: str
    name: str
    score: float
    rank: int
    is_priority: bool = False
    reason: str | None = None

    @property
    def full_name(self) -> str:
        return f"{self.schema}.{self.name}"


@dataclass
class ColumnProfile:
    schema: str
    name: str
    column_name: str
    null_ratio: float
    distinct_count: int
    sample_size: int
    min_value: str | None = None
    max_value: str | None = None
    top_values: str | None = None          # "값:빈도, ..." 요약 문자열
```

- [ ] **Step 4: 통과 확인** — `python -m pytest tests/test_models_p2.py -v` → 3 passed.
- [ ] **Step 5: 커밋** — `git add src/u9c_catalog/models.py tests/test_models_p2.py && git commit -m "feat(p2): 활성도/우선순위/프로파일 모델 추가"`

---

## Task 2: 활성도 컬럼 선택 로직 (순수) + 수집기

테이블마다 "최근 활동시각"을 낼 때 어떤 컬럼을 볼지 고르는 규칙은 순수 로직으로 분리해 단위 테스트한다.

**Files:** Create `src/u9c_catalog/activity.py`; Test `tests/test_activity.py`

- [ ] **Step 1: 실패 테스트(순수 로직)** — `tests/test_activity.py`
```python
from u9c_catalog.activity import pick_activity_column
from u9c_catalog.models import ColumnMeta, TableMeta


def _t(colnames):
    t = TableMeta(schema="dbo", name="T", object_type="TABLE")
    for n in colnames:
        t.columns.append(ColumnMeta(name=n, data_type="datetime", is_nullable=True))
    return t


def test_prefers_modifiedon():
    assert pick_activity_column(_t(["ID", "ModifiedOn", "CreatedOn"])) == "ModifiedOn"


def test_falls_back_to_createdon():
    assert pick_activity_column(_t(["ID", "CreatedOn"])) == "CreatedOn"


def test_alt_naming():
    assert pick_activity_column(_t(["ModifyDate", "CreateDate"])) == "ModifyDate"


def test_none_when_no_audit_col():
    assert pick_activity_column(_t(["ID", "Name"])) is None
```

- [ ] **Step 2: 실패 확인** — `python -m pytest tests/test_activity.py -v` → ImportError.

- [ ] **Step 3: activity.py 구현**
```python
# 테이블별 최근 활동시각을 산출한다 (감사/날짜 컬럼 MAX). 컬럼 선택은 순수 로직으로 분리.
from u9c_catalog.db import connect
from u9c_catalog.models import ActivityMeta, TableMeta

# 우선순위 순서: 수정일시 계열 → 생성일시 계열
_ACTIVITY_PREFERENCE = ["ModifiedOn", "ModifyDate", "ModifyTime",
                        "CreatedOn", "CreateDate", "CreateTime"]


def pick_activity_column(table: TableMeta) -> str | None:
    names = {c.name for c in table.columns}
    for cand in _ACTIVITY_PREFERENCE:
        if cand in names:
            return cand
    return None


def collect_activity(conn_str: str, tables: list[TableMeta]) -> list[ActivityMeta]:
    """각 테이블의 활동시각 = 선택 컬럼의 MAX(...). 뷰/부수/후보없음은 last_activity=None."""
    result: list[ActivityMeta] = []
    with connect(conn_str, readonly=True) as conn:
        cur = conn.cursor()
        for t in tables:
            if t.object_type != "TABLE":
                result.append(ActivityMeta(t.schema, t.name, None, "none"))
                continue
            col = pick_activity_column(t)
            if col is None:
                result.append(ActivityMeta(t.schema, t.name, None, "none"))
                continue
            try:
                cur.execute(f"SELECT MAX([{col}]) FROM [{t.schema}].[{t.name}]")
                val = cur.fetchone()[0]
            except Exception:
                val = None
            result.append(ActivityMeta(t.schema, t.name, val, col if val is not None else "none"))
    return result
```
> 주의: 컬럼/스키마/테이블명은 `sys.*`에서 온 신뢰 식별자이며 `[...]`로 감싼다. 사용자 입력 아님 → 인젝션 표면 없음.

- [ ] **Step 4: 순수 로직 통과 확인** — `python -m pytest tests/test_activity.py -v` → 4 passed.

- [ ] **Step 5: 통합 테스트 추가(@integration)** — `tests/test_activity.py`에 덧붙임
```python
import pytest
from u9c_catalog.activity import collect_activity


@pytest.mark.integration
def test_collect_activity_integration(test_conn_str):
    from u9c_catalog.extractor import extract_metadata
    md = extract_metadata(test_conn_str, schema_filter=["dbo"])
    acts = {a.full_name: a for a in collect_activity(test_conn_str, md.tables)}
    # 픽스처 PM_Receivement에는 CreatedOn 존재 → source가 CreatedOn 또는 값 유무 확인
    assert "dbo.PM_Receivement" in acts
```

- [ ] **Step 6: 픽스처 보강** — `tests/sql/create_fixture_db.sql`의 `PM_Receivement` INSERT에 `CreatedOn` 값을 넣도록 수정(현재 NULL). 예: `INSERT INTO dbo.PM_Receivement (ID, Org, DocNo, CreatedOn) VALUES (1, 100, 'RCV-0001', '2026-07-01T09:00:00');` 픽스처 DB 재적재:
`sqlcmd -S "(localdb)\MSSQLLocalDB" -d U9C_Fixture -i tests/sql/create_fixture_db.sql`

- [ ] **Step 7: 통합 통과 확인** — `export U9C_TEST_CONN="DRIVER={ODBC Driver 18 for SQL Server};SERVER=(localdb)\\MSSQLLocalDB;DATABASE=U9C_Fixture;Trusted_Connection=yes;Encrypt=no" && python -m pytest tests/test_activity.py -v` → 순수 4 + 통합 1 passed.

- [ ] **Step 8: 커밋** — `git add src/u9c_catalog/activity.py tests/test_activity.py tests/sql/create_fixture_db.sql && git commit -m "feat(p2): 활성도 수집기(최근 ModifiedOn/CreatedOn) 추가"`

---

## Task 3: DMV 사용량 수집 (선택·권한 graceful)

**Files:** Create `src/u9c_catalog/usage_dmv.py`; Test `tests/test_usage_dmv.py`

- [ ] **Step 1: 실패 테스트(@integration)** — `tests/test_usage_dmv.py`
```python
import pytest
from u9c_catalog.usage_dmv import collect_dmv_usage


@pytest.mark.integration
def test_dmv_usage_returns_dict_or_none(test_conn_str):
    # 권한 있으면 dict, 없으면 None. LocalDB(sysadmin)에서는 dict 기대.
    res = collect_dmv_usage(test_conn_str)
    assert res is None or isinstance(res, dict)
```

- [ ] **Step 2: 실패 확인** — `python -m pytest tests/test_usage_dmv.py -v` (통합, 미설정 시 skip) → import 실패 red.

- [ ] **Step 3: usage_dmv.py 구현**
```python
# DMV 인덱스 사용 통계 수집. VIEW SERVER STATE 권한이 없으면 None을 반환(graceful skip).
from u9c_catalog.db import connect

_SQL = """
SELECT s.name AS [schema], o.name AS [name],
       SUM(us.user_seeks) AS seeks, SUM(us.user_scans) AS scans,
       SUM(us.user_lookups) AS lookups, SUM(us.user_updates) AS updates
FROM sys.dm_db_index_usage_stats us
JOIN sys.objects o ON o.object_id = us.object_id
JOIN sys.schemas s ON s.schema_id = o.schema_id
WHERE us.database_id = DB_ID() AND o.type = 'U'
GROUP BY s.name, o.name;
"""


def collect_dmv_usage(conn_str: str) -> dict | None:
    """{ "schema.name": {seeks,scans,lookups,updates} }. 권한 없으면 None."""
    try:
        with connect(conn_str, readonly=True) as conn:
            cur = conn.cursor()
            cur.execute(_SQL)
            out = {}
            for r in cur.fetchall():
                out[f"{r[0]}.{r[1]}"] = {
                    "seeks": int(r[2] or 0), "scans": int(r[3] or 0),
                    "lookups": int(r[4] or 0), "updates": int(r[5] or 0),
                }
            return out
    except Exception as e:
        # VIEW SERVER STATE 거부 등 → 신호 없이 진행
        if "VIEW SERVER STATE" in str(e) or "permission" in str(e).lower():
            return None
        raise
```

- [ ] **Step 4: 통합 통과 확인** — `python -m pytest tests/test_usage_dmv.py -m integration -v` → 1 passed (LocalDB는 권한 있어 dict 반환).

- [ ] **Step 5: 커밋** — `git add src/u9c_catalog/usage_dmv.py tests/test_usage_dmv.py && git commit -m "feat(p2): DMV 사용량 수집(권한 graceful skip) 추가"`

---

## Task 4: 우선순위 점수 (순수 로직)

**Files:** Create `src/u9c_catalog/prioritizer.py`; Test `tests/test_prioritizer.py`

- [ ] **Step 1: 실패 테스트** — `tests/test_prioritizer.py`
```python
from u9c_catalog.prioritizer import score_tables
from u9c_catalog.models import ColumnMeta, TableMeta, ActivityMeta


def _tbl(name, ncols, business_cols, rows, aux=False):
    t = TableMeta(schema="dbo", name=name, object_type="TABLE", row_count=rows, is_auxiliary=aux)
    for i in range(ncols):
        c = ColumnMeta(name=f"c{i}", data_type="int", is_nullable=True)
        c.is_system = i >= business_cols
        t.columns.append(c)
    return t


def test_priority_ranking_order():
    tables = [
        _tbl("Big", 20, 15, 100000),         # 큰 업무 테이블
        _tbl("Empty", 20, 15, 0),            # 빈 테이블
        _tbl("Aux", 5, 0, 5000, aux=True),   # 부수
    ]
    acts = {
        "dbo.Big": ActivityMeta("dbo", "Big", "2026-07-20", "ModifiedOn"),
        "dbo.Empty": ActivityMeta("dbo", "Empty", None, "none"),
        "dbo.Aux": ActivityMeta("dbo", "Aux", "2026-07-20", "ModifiedOn"),
    }
    ranked = score_tables(tables, acts, dmv=None, top_n=2)
    by = {p.name: p for p in ranked}
    # 큰 활성 업무 테이블이 1위, 부수/빈 테이블은 하위
    assert by["Big"].rank == 1
    assert by["Big"].is_priority is True
    assert by["Aux"].score < by["Big"].score
    assert by["Empty"].score < by["Big"].score
    # top_n=2 → 상위 2개만 is_priority
    assert sum(1 for p in ranked if p.is_priority) == 2


def test_empty_and_aux_not_priority_when_topn_small():
    tables = [_tbl("Aux", 5, 0, 5000, aux=True), _tbl("Empty", 10, 8, 0)]
    acts = {"dbo.Aux": ActivityMeta("dbo","Aux",None,"none"),
            "dbo.Empty": ActivityMeta("dbo","Empty",None,"none")}
    ranked = score_tables(tables, acts, dmv=None, top_n=1)
    assert sum(1 for p in ranked if p.is_priority) == 1
```

- [ ] **Step 2: 실패 확인** — `python -m pytest tests/test_prioritizer.py -v` → ImportError.

- [ ] **Step 3: prioritizer.py 구현**
```python
# 활성도·규모·업무성·(선택)DMV 신호를 결합해 테이블 우선순위 점수를 매긴다 (순수 로직).
import math

from u9c_catalog.models import ActivityMeta, PriorityMeta, TableMeta


def _business_col_count(t: TableMeta) -> int:
    return sum(1 for c in t.columns if not c.is_system)


def _score(t: TableMeta, act: ActivityMeta, dmv: dict | None) -> tuple[float, str]:
    reasons = []
    score = 0.0
    # 1) 부수 테이블 강한 감점
    if t.is_auxiliary:
        score -= 5.0
        reasons.append("부수(-5)")
    # 2) 규모: log(row_count)
    rc = t.row_count or 0
    if rc > 0:
        score += math.log10(rc + 1)
        reasons.append(f"규모+{round(math.log10(rc+1),2)}")
    else:
        score -= 2.0
        reasons.append("빈테이블(-2)")
    # 3) 업무 컬럼 수 (많을수록 실질 엔티티)
    bcols = _business_col_count(t)
    score += min(bcols, 30) * 0.1
    reasons.append(f"업무컬럼{bcols}")
    # 4) 활성도: 최근 활동 있으면 가점
    if act.last_activity is not None:
        score += 2.0
        reasons.append("활성+2")
    # 5) DMV: 읽기(seek+scan+lookup) 있으면 가점
    if dmv is not None:
        u = dmv.get(t.full_name)
        if u:
            reads = u["seeks"] + u["scans"] + u["lookups"]
            if reads > 0:
                score += min(math.log10(reads + 1), 3.0)
                reasons.append(f"DMV읽기+{round(min(math.log10(reads+1),3.0),2)}")
    return score, ", ".join(reasons)


def score_tables(tables: list[TableMeta], activities: dict[str, ActivityMeta],
                 dmv: dict | None, top_n: int) -> list[PriorityMeta]:
    none_act = ActivityMeta("", "", None, "none")
    scored = []
    for t in tables:
        act = activities.get(t.full_name, none_act)
        sc, reason = _score(t, act, dmv)
        scored.append(PriorityMeta(schema=t.schema, name=t.name, score=sc, rank=0, reason=reason))
    scored.sort(key=lambda p: p.score, reverse=True)
    for i, p in enumerate(scored, start=1):
        p.rank = i
        p.is_priority = i <= top_n
    return scored
```

- [ ] **Step 4: 통과 확인** — `python -m pytest tests/test_prioritizer.py -v` → 2 passed.
- [ ] **Step 5: 커밋** — `git add src/u9c_catalog/prioritizer.py tests/test_prioritizer.py && git commit -m "feat(p2): 우선순위 점수 로직 추가"`

---

## Task 5: 데이터 프로파일러 (상위 테이블)

**Files:** Create `src/u9c_catalog/profiler.py`; Test `tests/test_profiler.py`

- [ ] **Step 1: 실패 테스트(@integration)** — `tests/test_profiler.py`
```python
import pytest
from u9c_catalog.profiler import profile_table
from u9c_catalog.extractor import extract_metadata


@pytest.mark.integration
def test_profile_table(test_conn_str):
    md = extract_metadata(test_conn_str, schema_filter=["dbo"])
    recv = next(t for t in md.tables if t.name == "PM_Receivement")
    profs = profile_table(test_conn_str, recv, sample_limit=1000)
    by = {p.column_name: p for p in profs}
    # DocNo는 NOT NULL이라 null_ratio 0
    assert by["DocNo"].null_ratio == 0.0
    assert by["DocNo"].distinct_count >= 1
    assert profs[0].sample_size >= 1
```

- [ ] **Step 2: 실패 확인** — `python -m pytest tests/test_profiler.py -v` → import 실패.

- [ ] **Step 3: profiler.py 구현**
```python
# 우선순위 테이블의 컬럼별 NULL율·distinct·min/max를 샘플로 프로파일링한다.
from u9c_catalog.db import connect
from u9c_catalog.models import ColumnProfile, TableMeta

# 대용량 방지: 표본 상한. 상한 이하면 전량, 초과면 TOP 표본.
def profile_table(conn_str: str, table: TableMeta, sample_limit: int = 100000) -> list[ColumnProfile]:
    profs: list[ColumnProfile] = []
    with connect(conn_str, readonly=True) as conn:
        cur = conn.cursor()
        src = f"(SELECT TOP {sample_limit} * FROM [{table.schema}].[{table.name}]) AS s"
        cur.execute(f"SELECT COUNT(*) FROM {src}")
        n = int(cur.fetchone()[0])
        for c in table.columns:
            col = f"[{c.name}]"
            try:
                cur.execute(
                    f"SELECT SUM(CASE WHEN {col} IS NULL THEN 1 ELSE 0 END), "
                    f"COUNT(DISTINCT {col}), "
                    f"CONVERT(nvarchar(256), MIN({col})), CONVERT(nvarchar(256), MAX({col})) "
                    f"FROM {src}"
                )
                nulls, distinct, mn, mx = cur.fetchone()
            except Exception:
                # 비교 불가 타입(text/image 등)은 스킵
                continue
            null_ratio = (int(nulls or 0) / n) if n else 0.0
            profs.append(ColumnProfile(
                schema=table.schema, name=table.name, column_name=c.name,
                null_ratio=round(null_ratio, 4), distinct_count=int(distinct or 0),
                sample_size=n, min_value=mn, max_value=mx,
            ))
    return profs
```

- [ ] **Step 4: 통합 통과 확인** — `python -m pytest tests/test_profiler.py -m integration -v` → 1 passed.
- [ ] **Step 5: 커밋** — `git add src/u9c_catalog/profiler.py tests/test_profiler.py && git commit -m "feat(p2): 데이터 프로파일러 추가"`

---

## Task 6: 카탈로그 스키마·적재기 확장

**Files:** Modify `src/u9c_catalog/catalog_schema.sql`, `src/u9c_catalog/catalog_writer.py`; Test `tests/test_catalog_writer_p2.py`

- [ ] **Step 1: catalog_schema.sql에 신규 테이블 추가** (기존 GO 블록들 뒤, 각 `IF OBJECT_ID(...) IS NULL` 패턴 유지)
```sql
IF OBJECT_ID('catalog.activity','U') IS NULL
CREATE TABLE catalog.activity (
    snapshot_id int NOT NULL, schema_name nvarchar(128) NOT NULL,
    object_name nvarchar(256) NOT NULL, last_activity datetime2 NULL,
    source nvarchar(64) NULL,
    CONSTRAINT PK_catalog_activity PRIMARY KEY (snapshot_id, schema_name, object_name)
);
GO
IF OBJECT_ID('catalog.usage','U') IS NULL
CREATE TABLE catalog.usage (
    snapshot_id int NOT NULL, schema_name nvarchar(128) NOT NULL,
    object_name nvarchar(256) NOT NULL,
    seeks bigint NULL, scans bigint NULL, lookups bigint NULL, updates bigint NULL,
    CONSTRAINT PK_catalog_usage PRIMARY KEY (snapshot_id, schema_name, object_name)
);
GO
IF OBJECT_ID('catalog.priority','U') IS NULL
CREATE TABLE catalog.priority (
    snapshot_id int NOT NULL, schema_name nvarchar(128) NOT NULL,
    object_name nvarchar(256) NOT NULL, score float NOT NULL, rank int NOT NULL,
    is_priority bit NOT NULL DEFAULT 0, reason nvarchar(400) NULL,
    CONSTRAINT PK_catalog_priority PRIMARY KEY (snapshot_id, schema_name, object_name)
);
GO
IF OBJECT_ID('catalog.profiles','U') IS NULL
CREATE TABLE catalog.profiles (
    snapshot_id int NOT NULL, schema_name nvarchar(128) NOT NULL,
    object_name nvarchar(256) NOT NULL, column_name nvarchar(128) NOT NULL,
    null_ratio float NULL, distinct_count bigint NULL, sample_size bigint NULL,
    min_value nvarchar(256) NULL, max_value nvarchar(256) NULL, top_values nvarchar(max) NULL,
    CONSTRAINT PK_catalog_profiles PRIMARY KEY (snapshot_id, schema_name, object_name, column_name)
);
GO
```

- [ ] **Step 2: 실패 테스트(@integration)** — `tests/test_catalog_writer_p2.py`
```python
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
        # 재적재 idempotent 확인(같은 sid 재실행 시 중복 PK 오류 안 나게 delete-then-insert)
        write_activity(test_conn_str, sid, [ActivityMeta("dbo", "T", "2026-07-02", "ModifiedOn")])
        cur.execute("SELECT COUNT(*) FROM catalog.activity WHERE snapshot_id=?", sid)
        assert cur.fetchone()[0] == 1
```

- [ ] **Step 3: 실패 확인** — `python -m pytest tests/test_catalog_writer_p2.py -v` → import 실패.

- [ ] **Step 4: catalog_writer.py에 함수 추가** (기존 import·connect 재사용)
```python
def _replace(cur, table, snapshot_id, rows_sql, params_list):
    cur.execute(f"DELETE FROM catalog.{table} WHERE snapshot_id=?", snapshot_id)
    for p in params_list:
        cur.execute(rows_sql, *p)


def write_activity(catalog_conn, snapshot_id, activities):
    with connect(catalog_conn) as conn:
        cur = conn.cursor()
        _replace(cur, "activity", snapshot_id,
                 "INSERT INTO catalog.activity(snapshot_id,schema_name,object_name,last_activity,source) VALUES (?,?,?,?,?)",
                 [(snapshot_id, a.schema, a.name, a.last_activity, a.source) for a in activities])


def write_usage(catalog_conn, snapshot_id, dmv):
    if not dmv:
        return
    rows = []
    for key, u in dmv.items():
        sch, name = key.split(".", 1)
        rows.append((snapshot_id, sch, name, u["seeks"], u["scans"], u["lookups"], u["updates"]))
    with connect(catalog_conn) as conn:
        cur = conn.cursor()
        _replace(cur, "usage", snapshot_id,
                 "INSERT INTO catalog.usage(snapshot_id,schema_name,object_name,seeks,scans,lookups,updates) VALUES (?,?,?,?,?,?,?)",
                 rows)


def write_priority(catalog_conn, snapshot_id, priorities):
    with connect(catalog_conn) as conn:
        cur = conn.cursor()
        _replace(cur, "priority", snapshot_id,
                 "INSERT INTO catalog.priority(snapshot_id,schema_name,object_name,score,rank,is_priority,reason) VALUES (?,?,?,?,?,?,?)",
                 [(snapshot_id, p.schema, p.name, p.score, p.rank, 1 if p.is_priority else 0, p.reason) for p in priorities])


def write_profiles(catalog_conn, snapshot_id, profiles):
    with connect(catalog_conn) as conn:
        cur = conn.cursor()
        _replace(cur, "profiles", snapshot_id,
                 "INSERT INTO catalog.profiles(snapshot_id,schema_name,object_name,column_name,null_ratio,distinct_count,sample_size,min_value,max_value,top_values) VALUES (?,?,?,?,?,?,?,?,?,?)",
                 [(snapshot_id, p.schema, p.name, p.column_name, p.null_ratio, p.distinct_count, p.sample_size, p.min_value, p.max_value, p.top_values) for p in profiles])
```

- [ ] **Step 5: 스키마 재생성 후 통합 통과** — 픽스처 catalog 재생성(Phase 1 절차) 후 `python -m pytest tests/test_catalog_writer_p2.py -m integration -v` → 1 passed.
- [ ] **Step 6: 커밋** — `git add src/u9c_catalog/catalog_schema.sql src/u9c_catalog/catalog_writer.py tests/test_catalog_writer_p2.py && git commit -m "feat(p2): 카탈로그 활성도/사용량/우선순위/프로파일 적재 추가"`

---

## Task 7: 선별 데이터 사전 + 우선순위 JSON

**Files:** Modify `src/u9c_catalog/doc_generator.py`; Test `tests/test_doc_generator_p2.py`

- [ ] **Step 1: 실패 테스트** — `tests/test_doc_generator_p2.py`
```python
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
```

- [ ] **Step 2: 실패 확인** — `python -m pytest tests/test_doc_generator_p2.py -v` → ImportError.

- [ ] **Step 3: doc_generator.py에 추가**
```python
import json


def filter_priority_tables(tables, priorities):
    """is_priority=True인 테이블만 원래 순서로 반환."""
    pri = {(p.schema, p.name) for p in priorities if p.is_priority}
    return [t for t in tables if (t.schema, t.name) in pri]


def generate_priority_json(priorities, out_path):
    """우선순위 랭킹을 다운스트림(MES/대시보드)용 JSON으로 출력 (rank 오름차순)."""
    data = [
        {"object": f"{p.schema}.{p.name}", "rank": p.rank, "score": round(p.score, 3),
         "is_priority": p.is_priority, "reason": p.reason}
        for p in sorted(priorities, key=lambda x: x.rank)
    ]
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
```

- [ ] **Step 4: 통과 확인** — `python -m pytest tests/test_doc_generator_p2.py -v` → 2 passed.
- [ ] **Step 5: 커밋** — `git add src/u9c_catalog/doc_generator.py tests/test_doc_generator_p2.py && git commit -m "feat(p2): 선별 테이블 필터 + 우선순위 JSON export 추가"`

---

## Task 8: CLI에 Phase 2 단계 연결

**Files:** Modify `src/u9c_catalog/cli.py`; Modify `config.example.yaml`

- [ ] **Step 1: config.example.yaml에 옵션 추가**
```yaml
profile_top_n: 200            # 우선순위 상위 N개 테이블만 프로파일링·선별사전 대상
```

- [ ] **Step 2: cli.py의 run()에 Phase 2 단계 추가** — 기존 `[5/5]` 문서 생성 앞에 삽입하고 단계 번호를 갱신. 신규 import와 로직:
```python
from u9c_catalog.activity import collect_activity
from u9c_catalog.usage_dmv import collect_dmv_usage
from u9c_catalog.prioritizer import score_tables
from u9c_catalog.profiler import profile_table
from u9c_catalog.catalog_writer import (ensure_schema, write_snapshot,
    write_activity, write_usage, write_priority, write_profiles)
from u9c_catalog.doc_generator import (generate_html, generate_excel,
    generate_priority_json, filter_priority_tables)
```
run() 본문에서 카탈로그 적재(snapshot_id 확보) 이후, 문서 생성 이전에 아래를 추가한다. `top_n`은 `getattr(s, "profile_top_n", 200)` 사용을 위해 config.py의 Settings에 `profile_top_n: int = 200`도 추가하고 load_settings에서 `cfg.get("profile_top_n") or 200`으로 읽는다(이 변경 포함).
```python
    print("[활성도] 최근 활동시각 수집 중...")
    activities = collect_activity(s.source_conn, result.tables)
    write_activity(s.catalog_conn, snapshot_id, activities)

    print("[사용량] DMV 수집 시도...")
    dmv = collect_dmv_usage(s.source_conn)
    if dmv is None:
        print("      DMV 권한 없음 → 건너뜀(데이터 기반 신호만 사용)")
    else:
        write_usage(s.catalog_conn, snapshot_id, dmv)
        print(f"      DMV 사용량 {len(dmv)}개 테이블")

    print("[우선순위] 점수 산정 중...")
    act_map = {a.full_name: a for a in activities}
    priorities = score_tables(result.tables, act_map, dmv, top_n=s.profile_top_n)
    write_priority(s.catalog_conn, snapshot_id, priorities)
    pri_tables = filter_priority_tables(result.tables, priorities)
    print(f"      우선순위 상위 {len(pri_tables)}개 선별")

    print("[프로파일] 상위 테이블 프로파일링 중...")
    all_profiles = []
    for t in pri_tables:
        all_profiles.extend(profile_table(s.source_conn, t))
    write_profiles(s.catalog_conn, snapshot_id, all_profiles)
    print(f"      프로파일 {len(all_profiles)}개 컬럼")
```
그리고 문서 생성 단계에서, 전체 대신 **선별 테이블**로 데이터 사전을 만들고 우선순위 JSON도 출력한다.
```python
    os.makedirs(s.output_dir, exist_ok=True)
    from u9c_catalog.extractor import ExtractResult
    pri_result = ExtractResult(tables=pri_tables, routines=result.routines, dependencies=result.dependencies)
    generate_html(pri_result, os.path.join(s.output_dir, "data_dictionary_priority.html"))
    generate_excel(pri_result, os.path.join(s.output_dir, "data_dictionary_priority.xlsx"))
    generate_priority_json(priorities, os.path.join(s.output_dir, "priority_map.json"))
```

- [ ] **Step 3: config.py Settings 확장** — `Settings`에 `profile_top_n: int = 200` 필드 추가, `load_settings`에 `profile_top_n=cfg.get("profile_top_n") or 200` 추가. 기존 `tests/test_config.py`가 깨지지 않는지 확인(`python -m pytest tests/test_config.py -v`).

- [ ] **Step 4: import 스모크 + 전체 순수 테스트** — `python -c "from u9c_catalog.cli import run; print('ok')"` 후 `python -m pytest -q`(순수 전부 통과).

- [ ] **Step 5: E2E (LocalDB 픽스처, 소스=카탈로그)** — Phase 1과 동일 방식으로 config/env 지정 후 `python -m u9c_catalog.cli --config <임시config>` 실행. 기대: 활성도/DMV(LocalDB는 권한 있음)/우선순위/프로파일 단계 출력, `output/`에 `data_dictionary_priority.html`·`priority_map.json` 생성, 카탈로그 `catalog.activity/usage/priority/profiles`에 행 존재. `priority_map.json`의 1위가 PM_Receivement(활성·업무 컬럼 보유)인지 확인.

- [ ] **Step 6: 커밋** — `git add src/u9c_catalog/cli.py src/u9c_catalog/config.py config.example.yaml && git commit -m "feat(p2): CLI에 활성도/DMV/우선순위/프로파일 단계 + 선별 산출물 연결"`

---

## Phase 2 완료 기준

- [ ] 순수 로직 테스트(models_p2, activity 순수, prioritizer, doc_generator_p2) 통과.
- [ ] 통합 테스트(activity, usage_dmv, profiler, catalog_writer_p2) LocalDB 픽스처로 통과.
- [ ] E2E로 선별 데이터 사전 + `priority_map.json` 생성 + 카탈로그 Phase 2 테이블 적재 확인.
- [ ] DMV 권한 없을 때 graceful skip 동작(운영에서 검증: 실제로 skip 출력).

## 운영 적용 메모

- 운영 실행 시 `collect_activity`가 테이블마다 `MAX(ModifiedOn)`을 조회 → 7천 테이블에 대해 다수 쿼리 발생. 부수 테이블·뷰는 건너뛰므로 실질 5천 미만. 필요 시 `profile_top_n`을 낮게 시작(예 100)해 프로파일 부하 조절.
- `VIEW SERVER STATE` 권한이 부여되면 `collect_dmv_usage`가 자동으로 dict를 반환해 DMV 신호가 점수에 반영된다(코드 변경 불필요).
- 프로파일링은 우선순위 상위만 대상이므로 대량 스캔을 피한다. 대용량 테이블은 `profile_table(sample_limit=...)` 상한으로 TOP 표본만.

## 다음 Phase 예고

- **Phase 3** — QA/테스트 U9C 델타 프로빙 + XEvents + 값 기반 관계·코드 추적(`SrcDoc_*`) + 6개 도메인 매핑.
- **Phase 4** — 대시보드/MES 연동 JSON 맵 확장 + 주기 재실행·스냅샷 diff.
