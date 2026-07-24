# U9C 카탈로그 Phase 1 구현 계획

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** U9C의 MS SQL Server 스키마 전체(테이블·컬럼·PK/FK·뷰·프로시저·함수·의존관계)를 읽기 전용으로 추출하고, U9C 지식 베이스 규칙으로 시스템 컬럼·부수 테이블을 분류한 뒤, 별도 SQL Server의 `ERP_Catalog` DB에 적재하고, HTML·Excel 데이터 사전을 생성하는 재실행 가능한 CLI 도구를 만든다.

**Architecture:** Python 계층형 파이프라인. `config → db → extractor → noise_classifier → catalog_writer → doc_generator`를 `cli`가 오케스트레이션한다. DB에 접근하는 코드(`db`, `extractor`, `catalog_writer`)는 얇은 경계 뒤에 격리하고, 순수 로직(`noise_classifier`, `doc_generator`, `config`)은 픽스처 데이터로 단위 테스트한다. DB 접근 모듈은 소형 픽스처 DB에 대한 통합 테스트(`integration` 마커)로 검증한다.

**Tech Stack:** Python 3.11+, pyodbc (ODBC Driver 18 for SQL Server), pandas, Jinja2, openpyxl, PyYAML, python-dotenv, pytest.

**참조:** 설계 문서 `docs/superpowers/specs/2026-07-24-u9c-erp-schema-analysis-design.md`, 지식 베이스 `docs/reference/u9c-schema-knowledge-base.md`.

---

## File Structure

Phase 1에서 생성하는 애플리케이션은 리포지터리 하위 `u9c-catalog/`에 둔다.

```
u9c-catalog/
  pyproject.toml                     # 프로젝트/의존성 정의
  .env.example                       # 연결 문자열 템플릿
  config.example.yaml                # 실행 옵션 템플릿
  README.md                          # 실행법
  src/u9c_catalog/
    __init__.py
    models.py            # 메타데이터 dataclass (ColumnMeta/Table/RoutineMeta/DependencyMeta)
    config.py            # .env + yaml 로드 → Settings
    db.py                # pyodbc 연결 팩토리
    queries.py           # 카탈로그 추출용 T-SQL 상수
    extractor.py         # sys 카탈로그 조회 → models
    noise_classifier.py  # 지식 베이스 규칙 → 시스템 컬럼/부수 테이블 태깅
    catalog_schema.sql   # ERP_Catalog DDL
    catalog_writer.py    # 메타데이터 → ERP_Catalog 적재(스냅샷)
    doc_generator.py     # HTML + Excel 데이터 사전 생성
    templates/
      data_dictionary.html.j2
    cli.py               # 오케스트레이션 엔트리포인트
  tests/
    conftest.py
    fixtures/
      sample_metadata.py            # 인메모리 메타데이터 픽스처
    sql/
      create_fixture_db.sql         # 통합 테스트용 소형 U9C-유사 DB
    test_config.py
    test_noise_classifier.py
    test_doc_generator.py
    test_models.py
    test_extractor.py               # @integration
    test_catalog_writer.py          # @integration
```

각 파일은 하나의 책임만 진다. DB 경계를 `db.py`/`extractor.py`/`catalog_writer.py`에 모아, 순수 로직은 DB 없이 테스트한다.

---

## Task 0: 프로젝트 스캐폴드

**Files:**
- Create: `u9c-catalog/pyproject.toml`
- Create: `u9c-catalog/.env.example`
- Create: `u9c-catalog/config.example.yaml`
- Create: `u9c-catalog/README.md`
- Create: `u9c-catalog/src/u9c_catalog/__init__.py`
- Create: `u9c-catalog/tests/conftest.py`

- [ ] **Step 1: pyproject.toml 작성**

```toml
[project]
name = "u9c-catalog"
version = "0.1.0"
description = "U9C ERP 스키마 추출·분류·카탈로그·문서화 도구"
requires-python = ">=3.11"
dependencies = [
    "pyodbc>=5.1",
    "pandas>=2.2",
    "jinja2>=3.1",
    "openpyxl>=3.1",
    "pyyaml>=6.0",
    "python-dotenv>=1.0",
]

[project.optional-dependencies]
dev = ["pytest>=8.0"]

[project.scripts]
u9c-catalog = "u9c_catalog.cli:main"

[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[tool.setuptools.packages.find]
where = ["src"]

[tool.pytest.ini_options]
markers = ["integration: DB가 필요한 통합 테스트 (환경변수 없으면 skip)"]
testpaths = ["tests"]
```

- [ ] **Step 2: .env.example 작성**

```bash
# 운영 U9C (읽기 전용 계정 권장: db_datareader + VIEW DEFINITION + VIEW SERVER STATE)
U9C_SOURCE_CONN="DRIVER={ODBC Driver 18 for SQL Server};SERVER=erp-prod;DATABASE=U9C;UID=readonly;PWD=changeme;Encrypt=yes;TrustServerCertificate=yes"

# 카탈로그 저장소 (UAT 서버의 신규 DB, 쓰기 권한 필요)
CATALOG_CONN="DRIVER={ODBC Driver 18 for SQL Server};SERVER=uat-srv;DATABASE=ERP_Catalog;UID=catalog_writer;PWD=changeme;Encrypt=yes;TrustServerCertificate=yes"

# 통합 테스트용 픽스처 DB (없으면 통합 테스트 skip). CI/로컬 테스트에서만 사용.
U9C_TEST_CONN=""
```

- [ ] **Step 3: config.example.yaml 작성**

```yaml
# 실행 옵션 (실제 사용 시 config.yaml로 복사)
source_schema_filter: []      # 비어있으면 전체 스키마. 예: ["dbo"]
exclude_object_prefixes: []   # 추출 자체에서 제외할 접두어 (보통 비움)
output_dir: "./output"        # 데이터 사전 산출물 경로
snapshot_label: ""            # 비어있으면 실행 시각으로 자동 생성
```

- [ ] **Step 4: README.md 작성**

````markdown
# U9C 카탈로그 (Phase 1)

U9C ERP 스키마를 읽기 전용으로 추출 → 노이즈 분류 → ERP_Catalog 적재 → 데이터 사전 생성.

## 설치
```bash
cd u9c-catalog
python -m venv .venv && .venv\Scripts\activate
pip install -e ".[dev]"
```

## 설정
`.env.example` → `.env`, `config.example.yaml` → `config.yaml` 복사 후 값 채우기.

## 실행
```bash
u9c-catalog --config config.yaml
```

## 테스트
```bash
pytest                       # 순수 로직 테스트
$env:U9C_TEST_CONN="..."     # 픽스처 DB 지정 시
pytest -m integration        # 통합 테스트
```
````

- [ ] **Step 5: 빈 패키지·conftest 생성**

`src/u9c_catalog/__init__.py`:
```python
# U9C 스키마 추출·분류·카탈로그·문서화 도구 패키지
```

`tests/conftest.py`:
```python
# pytest 공통 설정: 통합 테스트는 연결 환경변수가 없으면 자동 skip
import os
import pytest


@pytest.fixture
def test_conn_str():
    conn = os.environ.get("U9C_TEST_CONN", "").strip()
    if not conn:
        pytest.skip("U9C_TEST_CONN 미설정 — 통합 테스트 skip")
    return conn
```

- [ ] **Step 6: 설치 및 커밋**

Run: `cd u9c-catalog && pip install -e ".[dev]" && pytest`
Expected: `no tests ran` 또는 0 collected (아직 테스트 없음), 설치 성공.

```bash
git add u9c-catalog/
git commit -m "chore: U9C 카탈로그 프로젝트 스캐폴드"
```

---

## Task 1: 메타데이터 모델 (models.py)

**Files:**
- Create: `u9c-catalog/src/u9c_catalog/models.py`
- Test: `u9c-catalog/tests/test_models.py`

- [ ] **Step 1: 실패하는 테스트 작성**

`tests/test_models.py`:
```python
from u9c_catalog.models import ColumnMeta, TableMeta, RoutineMeta, DependencyMeta


def test_columnmeta_defaults():
    c = ColumnMeta(name="Org", data_type="bigint", is_nullable=False)
    assert c.is_system is False
    assert c.is_pk is False


def test_tablemeta_holds_columns():
    t = TableMeta(schema="dbo", name="PM_Receivement", object_type="TABLE")
    t.columns.append(ColumnMeta(name="ID", data_type="bigint", is_nullable=False, is_pk=True))
    assert t.full_name == "dbo.PM_Receivement"
    assert t.columns[0].is_pk is True


def test_routinemeta_full_name():
    r = RoutineMeta(schema="dbo", name="usp_x", object_type="PROCEDURE", definition="...")
    assert r.full_name == "dbo.usp_x"


def test_dependencymeta():
    d = DependencyMeta(from_object="dbo.A", to_object="dbo.B", kind="FK")
    assert d.kind == "FK"
```

- [ ] **Step 2: 테스트 실패 확인**

Run: `pytest tests/test_models.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'u9c_catalog.models'`

- [ ] **Step 3: models.py 구현**

```python
# 스키마 추출 결과를 담는 메타데이터 dataclass 정의
from dataclasses import dataclass, field


@dataclass
class ColumnMeta:
    name: str
    data_type: str
    is_nullable: bool
    max_length: int | None = None
    is_pk: bool = False
    is_identity: bool = False
    default_definition: str | None = None
    ordinal: int = 0
    is_system: bool = False          # noise_classifier가 채움
    system_reason: str | None = None


@dataclass
class TableMeta:
    schema: str
    name: str
    object_type: str                 # "TABLE" | "VIEW"
    columns: list[ColumnMeta] = field(default_factory=list)
    row_count: int | None = None
    is_auxiliary: bool = False        # noise_classifier가 채움
    auxiliary_reason: str | None = None

    @property
    def full_name(self) -> str:
        return f"{self.schema}.{self.name}"


@dataclass
class RoutineMeta:
    schema: str
    name: str
    object_type: str                 # "PROCEDURE" | "FUNCTION"
    definition: str

    @property
    def full_name(self) -> str:
        return f"{self.schema}.{self.name}"


@dataclass
class DependencyMeta:
    from_object: str
    to_object: str
    kind: str                        # "FK" | "REFERENCE"
    detail: str | None = None
```

- [ ] **Step 4: 테스트 통과 확인**

Run: `pytest tests/test_models.py -v`
Expected: PASS (4 passed)

- [ ] **Step 5: 커밋**

```bash
git add src/u9c_catalog/models.py tests/test_models.py
git commit -m "feat: 메타데이터 모델 dataclass 추가"
```

---

## Task 2: 설정 로더 (config.py)

**Files:**
- Create: `u9c-catalog/src/u9c_catalog/config.py`
- Test: `u9c-catalog/tests/test_config.py`

- [ ] **Step 1: 실패하는 테스트 작성**

`tests/test_config.py`:
```python
from u9c_catalog.config import load_settings


def test_load_settings_reads_yaml_and_env(tmp_path, monkeypatch):
    cfg = tmp_path / "config.yaml"
    cfg.write_text(
        "source_schema_filter: [dbo]\noutput_dir: ./out\nsnapshot_label: test\n",
        encoding="utf-8",
    )
    monkeypatch.setenv("U9C_SOURCE_CONN", "SRC")
    monkeypatch.setenv("CATALOG_CONN", "CAT")

    s = load_settings(str(cfg))

    assert s.source_conn == "SRC"
    assert s.catalog_conn == "CAT"
    assert s.source_schema_filter == ["dbo"]
    assert s.output_dir == "./out"
    assert s.snapshot_label == "test"


def test_missing_conn_raises(tmp_path, monkeypatch):
    cfg = tmp_path / "config.yaml"
    cfg.write_text("output_dir: ./out\n", encoding="utf-8")
    monkeypatch.delenv("U9C_SOURCE_CONN", raising=False)
    monkeypatch.setenv("CATALOG_CONN", "CAT")

    import pytest
    with pytest.raises(ValueError, match="U9C_SOURCE_CONN"):
        load_settings(str(cfg))
```

- [ ] **Step 2: 테스트 실패 확인**

Run: `pytest tests/test_config.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'u9c_catalog.config'`

- [ ] **Step 3: config.py 구현**

```python
# .env와 config.yaml을 읽어 실행 설정(Settings)을 만드는 로더
import os
from dataclasses import dataclass, field

import yaml
from dotenv import load_dotenv


@dataclass
class Settings:
    source_conn: str
    catalog_conn: str
    source_schema_filter: list[str] = field(default_factory=list)
    exclude_object_prefixes: list[str] = field(default_factory=list)
    output_dir: str = "./output"
    snapshot_label: str = ""


def _require_env(name: str) -> str:
    val = os.environ.get(name, "").strip()
    if not val:
        raise ValueError(f"환경변수 {name} 가 비어 있습니다. .env를 확인하세요.")
    return val


def load_settings(config_path: str) -> Settings:
    load_dotenv()
    with open(config_path, encoding="utf-8") as f:
        cfg = yaml.safe_load(f) or {}
    return Settings(
        source_conn=_require_env("U9C_SOURCE_CONN"),
        catalog_conn=_require_env("CATALOG_CONN"),
        source_schema_filter=cfg.get("source_schema_filter") or [],
        exclude_object_prefixes=cfg.get("exclude_object_prefixes") or [],
        output_dir=cfg.get("output_dir") or "./output",
        snapshot_label=cfg.get("snapshot_label") or "",
    )
```

- [ ] **Step 4: 테스트 통과 확인**

Run: `pytest tests/test_config.py -v`
Expected: PASS (2 passed)

- [ ] **Step 5: 커밋**

```bash
git add src/u9c_catalog/config.py tests/test_config.py
git commit -m "feat: 설정 로더(.env + yaml) 추가"
```

---

## Task 3: 노이즈 분류기 (noise_classifier.py)

지식 베이스(§3, §8)의 시스템 컬럼·부수 테이블 규칙을 코드화한다. Phase 1의 핵심 로직이므로 픽스처로 철저히 테스트한다.

**Files:**
- Create: `u9c-catalog/src/u9c_catalog/noise_classifier.py`
- Create: `u9c-catalog/tests/fixtures/sample_metadata.py`
- Test: `u9c-catalog/tests/test_noise_classifier.py`

- [ ] **Step 1: 픽스처 작성**

`tests/fixtures/sample_metadata.py`:
```python
# 노이즈 분류/문서 생성 테스트용 인메모리 메타데이터 픽스처
from u9c_catalog.models import ColumnMeta, TableMeta


def make_receivement_table() -> TableMeta:
    t = TableMeta(schema="dbo", name="PM_Receivement", object_type="TABLE", row_count=12000)
    cols = [
        ("ID", "bigint", False, True),
        ("Org", "bigint", False, False),
        ("DocNo", "nvarchar", False, False),
        ("CreatedBy", "bigint", True, False),
        ("CreatedOn", "datetime", True, False),
        ("ModifiedBy", "bigint", True, False),
        ("ModifiedOn", "datetime", True, False),
        ("SysMlFlag", "int", True, False),
        ("Effective_IsEffective", "bit", True, False),
        ("DescFlexField_PubDescSeg4", "nvarchar", True, False),
        ("BusinessDate", "datetime", True, False),
    ]
    for i, (n, dt, nul, pk) in enumerate(cols):
        t.columns.append(ColumnMeta(name=n, data_type=dt, is_nullable=nul, is_pk=pk, ordinal=i))
    return t


def make_trl_table() -> TableMeta:
    t = TableMeta(schema="dbo", name="CBO_ItemMaster_Trl", object_type="TABLE", row_count=500)
    t.columns.append(ColumnMeta(name="ID", data_type="bigint", is_nullable=False, is_pk=True))
    t.columns.append(ColumnMeta(name="Name", data_type="nvarchar", is_nullable=True))
    return t
```

- [ ] **Step 2: 실패하는 테스트 작성**

`tests/test_noise_classifier.py`:
```python
from u9c_catalog.noise_classifier import classify_columns, classify_table
from tests.fixtures.sample_metadata import make_receivement_table, make_trl_table


def test_system_columns_tagged():
    t = make_receivement_table()
    classify_columns(t)
    by_name = {c.name: c for c in t.columns}
    for sysname in ["ID", "Org", "CreatedBy", "CreatedOn", "ModifiedBy",
                    "ModifiedOn", "SysMlFlag", "Effective_IsEffective",
                    "DescFlexField_PubDescSeg4"]:
        assert by_name[sysname].is_system is True, sysname
    # 업무 컬럼은 시스템으로 잡히면 안 됨
    assert by_name["DocNo"].is_system is False
    assert by_name["BusinessDate"].is_system is False


def test_alt_audit_naming_tagged():
    from u9c_catalog.models import ColumnMeta, TableMeta
    t = TableMeta(schema="dbo", name="ECN_X", object_type="TABLE")
    for n in ["CreateUser", "CreateDate", "ModifyUser", "ModifyTime"]:
        t.columns.append(ColumnMeta(name=n, data_type="nvarchar", is_nullable=True))
    classify_columns(t)
    assert all(c.is_system for c in t.columns)


def test_trl_table_is_auxiliary():
    t = make_trl_table()
    classify_table(t)
    assert t.is_auxiliary is True
    assert "Trl" in (t.auxiliary_reason or "")


def test_business_table_not_auxiliary():
    t = make_receivement_table()
    classify_table(t)
    assert t.is_auxiliary is False
```

- [ ] **Step 3: 테스트 실패 확인**

Run: `pytest tests/test_noise_classifier.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'u9c_catalog.noise_classifier'`

- [ ] **Step 4: noise_classifier.py 구현**

```python
# U9C 지식 베이스 규칙으로 시스템 컬럼/부수 테이블을 태깅하는 분류기
import re

from u9c_catalog.models import TableMeta

# §3: 정확 일치 시스템 컬럼 (표준 명명)
_SYSTEM_COLUMN_EXACT = {
    "ID", "Org", "MasterOrg", "SysMlFlag",
    "CreatedBy", "CreatedOn", "ModifiedBy", "ModifiedOn",
    "Effective_IsEffective", "Effective_EffectiveDate", "Effective_DisableDate",
}

# §3 주의: 감사 컬럼 대체 명명 (CreateUser/CreateDate 계열)
_SYSTEM_COLUMN_ALT = {
    "CreateUser", "CreateDate", "CreateTime",
    "ModifyUser", "ModifyDate", "ModifyTime",
}

# §4/§8: 접두어로 판정하는 시스템/확장 컬럼
_SYSTEM_COLUMN_PREFIXES = ("DescFlexField_", "KeyFlexField", "NameKeyFlexField")

# §2-2/§8: 부수 테이블로 강등할 테이블명 접미어/패턴
_AUX_TABLE_SUFFIXES = ("_Trl",)


def is_system_column(name: str) -> tuple[bool, str | None]:
    if name in _SYSTEM_COLUMN_EXACT:
        return True, "표준 시스템/감사 컬럼"
    if name in _SYSTEM_COLUMN_ALT:
        return True, "대체 명명 감사 컬럼"
    for p in _SYSTEM_COLUMN_PREFIXES:
        if name.startswith(p):
            return True, f"확장 필드 접두어 {p}"
    return False, None


def classify_columns(table: TableMeta) -> None:
    for c in table.columns:
        flag, reason = is_system_column(c.name)
        c.is_system = flag
        c.system_reason = reason


def classify_table(table: TableMeta) -> None:
    for suf in _AUX_TABLE_SUFFIXES:
        if table.name.endswith(suf):
            table.is_auxiliary = True
            table.auxiliary_reason = f"다국어/부수 테이블 접미어 {suf}"
            return
    table.is_auxiliary = False
    table.auxiliary_reason = None


def classify_all(tables: list[TableMeta]) -> None:
    for t in tables:
        classify_columns(t)
        classify_table(t)
```

- [ ] **Step 5: 테스트 통과 확인**

Run: `pytest tests/test_noise_classifier.py -v`
Expected: PASS (4 passed)

- [ ] **Step 6: 커밋**

```bash
git add src/u9c_catalog/noise_classifier.py tests/test_noise_classifier.py tests/fixtures/sample_metadata.py
git commit -m "feat: 지식베이스 규칙 기반 노이즈 분류기 추가"
```

---

## Task 4: DB 연결 팩토리 (db.py)

**Files:**
- Create: `u9c-catalog/src/u9c_catalog/db.py`

- [ ] **Step 1: db.py 구현 (얇은 래퍼, 단위 테스트 대상 아님)**

```python
# pyodbc 연결을 생성/관리하는 얇은 팩토리 (읽기 전용 소스, 쓰기 카탈로그)
from contextlib import contextmanager

import pyodbc


@contextmanager
def connect(conn_str: str, readonly: bool = False):
    """연결을 열고 컨텍스트 종료 시 닫는다. readonly=True면 자동커밋(쓰기 없음)."""
    conn = pyodbc.connect(conn_str, autocommit=readonly)
    try:
        yield conn
        if not readonly:
            conn.commit()
    except Exception:
        if not readonly:
            conn.rollback()
        raise
    finally:
        conn.close()
```

- [ ] **Step 2: import 스모크 확인**

Run: `python -c "from u9c_catalog.db import connect; print('ok')"`
Expected: `ok`

- [ ] **Step 3: 커밋**

```bash
git add src/u9c_catalog/db.py
git commit -m "feat: pyodbc 연결 팩토리 추가"
```

---

## Task 5: 추출 쿼리 + 추출기 (queries.py, extractor.py)

**Files:**
- Create: `u9c-catalog/src/u9c_catalog/queries.py`
- Create: `u9c-catalog/src/u9c_catalog/extractor.py`
- Create: `u9c-catalog/tests/sql/create_fixture_db.sql`
- Test: `u9c-catalog/tests/test_extractor.py` (`@integration`)

- [ ] **Step 1: 추출 쿼리 상수 작성**

`src/u9c_catalog/queries.py`:
```python
# 시스템 카탈로그에서 스키마 메타데이터를 뽑는 T-SQL 쿼리 모음
TABLES_AND_VIEWS = """
SELECT s.name AS [schema], o.name AS [name],
       CASE o.type WHEN 'U' THEN 'TABLE' ELSE 'VIEW' END AS object_type
FROM sys.objects o
JOIN sys.schemas s ON s.schema_id = o.schema_id
WHERE o.type IN ('U','V')
ORDER BY s.name, o.name;
"""

COLUMNS = """
SELECT s.name AS [schema], o.name AS [table],
       c.name AS [column], t.name AS data_type,
       c.max_length AS max_length, c.is_nullable AS is_nullable,
       c.is_identity AS is_identity, c.column_id AS ordinal,
       CAST(CASE WHEN pk.column_id IS NOT NULL THEN 1 ELSE 0 END AS bit) AS is_pk,
       dc.definition AS default_definition
FROM sys.columns c
JOIN sys.objects o ON o.object_id = c.object_id
JOIN sys.schemas s ON s.schema_id = o.schema_id
JOIN sys.types t ON t.user_type_id = c.user_type_id
LEFT JOIN sys.default_constraints dc ON dc.object_id = c.default_object_id
LEFT JOIN (
    SELECT ic.object_id, ic.column_id
    FROM sys.indexes i
    JOIN sys.index_columns ic ON ic.object_id = i.object_id AND ic.index_id = i.index_id
    WHERE i.is_primary_key = 1
) pk ON pk.object_id = c.object_id AND pk.column_id = c.column_id
WHERE o.type IN ('U','V')
ORDER BY s.name, o.name, c.column_id;
"""

ROUTINES = """
SELECT s.name AS [schema], o.name AS [name],
       CASE o.type WHEN 'P' THEN 'PROCEDURE' ELSE 'FUNCTION' END AS object_type,
       m.definition AS definition
FROM sys.sql_modules m
JOIN sys.objects o ON o.object_id = m.object_id
JOIN sys.schemas s ON s.schema_id = o.schema_id
WHERE o.type IN ('P','FN','IF','TF')
ORDER BY s.name, o.name;
"""

FOREIGN_KEYS = """
SELECT sp.name + '.' + tp.name AS from_object,
       sr.name + '.' + tr.name AS to_object,
       fk.name AS detail
FROM sys.foreign_keys fk
JOIN sys.tables tp ON tp.object_id = fk.parent_object_id
JOIN sys.schemas sp ON sp.schema_id = tp.schema_id
JOIN sys.tables tr ON tr.object_id = fk.referenced_object_id
JOIN sys.schemas sr ON sr.schema_id = tr.schema_id;
"""

ROW_COUNTS = """
SELECT s.name AS [schema], t.name AS [table], SUM(p.rows) AS row_count
FROM sys.tables t
JOIN sys.schemas s ON s.schema_id = t.schema_id
JOIN sys.partitions p ON p.object_id = t.object_id AND p.index_id IN (0,1)
GROUP BY s.name, t.name;
"""
```

- [ ] **Step 2: 통합 테스트용 픽스처 DB 스크립트 작성**

`tests/sql/create_fixture_db.sql`:
```sql
-- 통합 테스트용 소형 U9C-유사 스키마 (idempotent)
IF OBJECT_ID('dbo.PM_Receivement', 'U') IS NOT NULL DROP TABLE dbo.PM_Receivement;
IF OBJECT_ID('dbo.CBO_ItemMaster_Trl', 'U') IS NOT NULL DROP TABLE dbo.CBO_ItemMaster_Trl;
GO
CREATE TABLE dbo.PM_Receivement (
    ID bigint NOT NULL PRIMARY KEY,
    Org bigint NOT NULL,
    DocNo nvarchar(40) NOT NULL,
    CreatedOn datetime NULL,
    SysMlFlag int NULL
);
GO
CREATE TABLE dbo.CBO_ItemMaster_Trl (
    ID bigint NOT NULL PRIMARY KEY,
    Name nvarchar(200) NULL
);
GO
INSERT INTO dbo.PM_Receivement (ID, Org, DocNo) VALUES (1, 100, 'RCV-0001');
INSERT INTO dbo.CBO_ItemMaster_Trl (ID, Name) VALUES (1, N'품목A');
GO
```

- [ ] **Step 3: 실패하는 통합 테스트 작성**

`tests/test_extractor.py`:
```python
import pytest

from u9c_catalog.extractor import extract_metadata


@pytest.mark.integration
def test_extract_finds_fixture_tables(test_conn_str):
    result = extract_metadata(test_conn_str, schema_filter=["dbo"])
    names = {t.full_name for t in result.tables}
    assert "dbo.PM_Receivement" in names
    assert "dbo.CBO_ItemMaster_Trl" in names

    recv = next(t for t in result.tables if t.name == "PM_Receivement")
    by_name = {c.name: c for c in recv.columns}
    assert by_name["ID"].is_pk is True
    assert recv.row_count == 1
```

- [ ] **Step 4: 테스트가 skip되는지 확인 (연결 미설정 시)**

Run: `pytest tests/test_extractor.py -v`
Expected: SKIPPED ("U9C_TEST_CONN 미설정")

- [ ] **Step 5: extractor.py 구현**

```python
# 시스템 카탈로그를 조회해 메타데이터 모델로 변환하는 추출기
from dataclasses import dataclass, field

from u9c_catalog import queries
from u9c_catalog.db import connect
from u9c_catalog.models import ColumnMeta, DependencyMeta, RoutineMeta, TableMeta


@dataclass
class ExtractResult:
    tables: list[TableMeta] = field(default_factory=list)
    routines: list[RoutineMeta] = field(default_factory=list)
    dependencies: list[DependencyMeta] = field(default_factory=list)


def _rows(cursor, sql):
    cursor.execute(sql)
    cols = [d[0] for d in cursor.description]
    return [dict(zip(cols, r)) for r in cursor.fetchall()]


def extract_metadata(conn_str: str, schema_filter: list[str] | None = None) -> ExtractResult:
    schema_filter = schema_filter or []
    result = ExtractResult()
    with connect(conn_str, readonly=True) as conn:
        cur = conn.cursor()

        tables: dict[str, TableMeta] = {}
        for r in _rows(cur, queries.TABLES_AND_VIEWS):
            if schema_filter and r["schema"] not in schema_filter:
                continue
            t = TableMeta(schema=r["schema"], name=r["name"], object_type=r["object_type"])
            tables[t.full_name] = t

        for r in _rows(cur, queries.COLUMNS):
            key = f'{r["schema"]}.{r["table"]}'
            t = tables.get(key)
            if t is None:
                continue
            t.columns.append(ColumnMeta(
                name=r["column"], data_type=r["data_type"],
                is_nullable=bool(r["is_nullable"]), max_length=r["max_length"],
                is_pk=bool(r["is_pk"]), is_identity=bool(r["is_identity"]),
                default_definition=r["default_definition"], ordinal=r["ordinal"],
            ))

        for r in _rows(cur, queries.ROW_COUNTS):
            key = f'{r["schema"]}.{r["table"]}'
            if key in tables:
                tables[key].row_count = int(r["row_count"]) if r["row_count"] is not None else None

        result.tables = list(tables.values())

        for r in _rows(cur, queries.ROUTINES):
            if schema_filter and r["schema"] not in schema_filter:
                continue
            result.routines.append(RoutineMeta(
                schema=r["schema"], name=r["name"],
                object_type=r["object_type"], definition=r["definition"] or "",
            ))

        for r in _rows(cur, queries.FOREIGN_KEYS):
            result.dependencies.append(DependencyMeta(
                from_object=r["from_object"], to_object=r["to_object"],
                kind="FK", detail=r["detail"],
            ))

    return result
```

- [ ] **Step 6: 통합 테스트 통과 확인 (픽스처 DB 준비 후)**

먼저 픽스처 DB를 만든다 (LocalDB 또는 테스트 SQL Server):
```bash
sqlcmd -S "(localdb)\MSSQLLocalDB" -Q "IF DB_ID('U9C_Fixture') IS NULL CREATE DATABASE U9C_Fixture;"
sqlcmd -S "(localdb)\MSSQLLocalDB" -d U9C_Fixture -i tests/sql/create_fixture_db.sql
```
그다음 환경변수 지정 후 실행:
```bash
$env:U9C_TEST_CONN="DRIVER={ODBC Driver 18 for SQL Server};SERVER=(localdb)\MSSQLLocalDB;DATABASE=U9C_Fixture;Trusted_Connection=yes;Encrypt=no"
pytest tests/test_extractor.py -m integration -v
```
Expected: PASS (1 passed)

- [ ] **Step 7: 커밋**

```bash
git add src/u9c_catalog/queries.py src/u9c_catalog/extractor.py tests/test_extractor.py tests/sql/create_fixture_db.sql
git commit -m "feat: 시스템 카탈로그 스키마 추출기 추가"
```

---

## Task 6: 카탈로그 스키마 + 적재기 (catalog_schema.sql, catalog_writer.py)

**Files:**
- Create: `u9c-catalog/src/u9c_catalog/catalog_schema.sql`
- Create: `u9c-catalog/src/u9c_catalog/catalog_writer.py`
- Test: `u9c-catalog/tests/test_catalog_writer.py` (`@integration`)

- [ ] **Step 1: 카탈로그 DDL 작성**

`src/u9c_catalog/catalog_schema.sql`:
```sql
-- ERP_Catalog: U9C 메타데이터 스냅샷 저장 스키마 (idempotent 생성)
IF SCHEMA_ID('catalog') IS NULL EXEC('CREATE SCHEMA catalog');
GO
IF OBJECT_ID('catalog.snapshots','U') IS NULL
CREATE TABLE catalog.snapshots (
    snapshot_id   int IDENTITY(1,1) PRIMARY KEY,
    label         nvarchar(100) NOT NULL,
    created_on    datetime2 NOT NULL DEFAULT SYSUTCDATETIME()
);
GO
IF OBJECT_ID('catalog.objects','U') IS NULL
CREATE TABLE catalog.objects (
    snapshot_id   int NOT NULL,
    schema_name   nvarchar(128) NOT NULL,
    object_name   nvarchar(256) NOT NULL,
    object_type   nvarchar(20) NOT NULL,
    row_count     bigint NULL,
    is_auxiliary  bit NOT NULL DEFAULT 0,
    aux_reason    nvarchar(200) NULL,
    CONSTRAINT PK_catalog_objects PRIMARY KEY (snapshot_id, schema_name, object_name)
);
GO
IF OBJECT_ID('catalog.columns','U') IS NULL
CREATE TABLE catalog.columns (
    snapshot_id   int NOT NULL,
    schema_name   nvarchar(128) NOT NULL,
    object_name   nvarchar(256) NOT NULL,
    column_name   nvarchar(128) NOT NULL,
    data_type     nvarchar(64) NOT NULL,
    is_nullable   bit NOT NULL,
    is_pk         bit NOT NULL,
    is_system     bit NOT NULL DEFAULT 0,
    system_reason nvarchar(200) NULL,
    ordinal       int NOT NULL,
    CONSTRAINT PK_catalog_columns PRIMARY KEY (snapshot_id, schema_name, object_name, column_name)
);
GO
IF OBJECT_ID('catalog.dependencies','U') IS NULL
CREATE TABLE catalog.dependencies (
    snapshot_id   int NOT NULL,
    from_object   nvarchar(384) NOT NULL,
    to_object     nvarchar(384) NOT NULL,
    kind          nvarchar(20) NOT NULL,
    detail        nvarchar(256) NULL
);
GO
IF OBJECT_ID('catalog.routines','U') IS NULL
CREATE TABLE catalog.routines (
    snapshot_id   int NOT NULL,
    schema_name   nvarchar(128) NOT NULL,
    object_name   nvarchar(256) NOT NULL,
    object_type   nvarchar(20) NOT NULL,
    definition    nvarchar(max) NULL,
    CONSTRAINT PK_catalog_routines PRIMARY KEY (snapshot_id, schema_name, object_name)
);
GO
```

- [ ] **Step 2: 실패하는 통합 테스트 작성**

`tests/test_catalog_writer.py`:
```python
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
```

- [ ] **Step 3: 테스트 skip 확인**

Run: `pytest tests/test_catalog_writer.py -v`
Expected: SKIPPED

- [ ] **Step 4: catalog_writer.py 구현**

```python
# 추출·분류된 메타데이터를 ERP_Catalog에 스냅샷으로 적재하는 모듈
from importlib import resources

from u9c_catalog.db import connect
from u9c_catalog.extractor import ExtractResult


def _split_batches(ddl: str) -> list[str]:
    return [b.strip() for b in ddl.replace("\r\n", "\n").split("\nGO") if b.strip()]


def ensure_schema(catalog_conn: str) -> None:
    ddl = resources.files("u9c_catalog").joinpath("catalog_schema.sql").read_text(encoding="utf-8")
    with connect(catalog_conn) as conn:
        cur = conn.cursor()
        for batch in _split_batches(ddl):
            cur.execute(batch)


def write_snapshot(catalog_conn: str, result: ExtractResult, label: str) -> int:
    with connect(catalog_conn) as conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO catalog.snapshots(label) OUTPUT INSERTED.snapshot_id VALUES (?)", label)
        snapshot_id = int(cur.fetchone()[0])

        for t in result.tables:
            cur.execute(
                "INSERT INTO catalog.objects(snapshot_id,schema_name,object_name,object_type,row_count,is_auxiliary,aux_reason) VALUES (?,?,?,?,?,?,?)",
                snapshot_id, t.schema, t.name, t.object_type, t.row_count,
                1 if t.is_auxiliary else 0, t.auxiliary_reason,
            )
            for c in t.columns:
                cur.execute(
                    "INSERT INTO catalog.columns(snapshot_id,schema_name,object_name,column_name,data_type,is_nullable,is_pk,is_system,system_reason,ordinal) VALUES (?,?,?,?,?,?,?,?,?,?)",
                    snapshot_id, t.schema, t.name, c.name, c.data_type,
                    1 if c.is_nullable else 0, 1 if c.is_pk else 0,
                    1 if c.is_system else 0, c.system_reason, c.ordinal,
                )

        for r in result.routines:
            cur.execute(
                "INSERT INTO catalog.routines(snapshot_id,schema_name,object_name,object_type,definition) VALUES (?,?,?,?,?)",
                snapshot_id, r.schema, r.name, r.object_type, r.definition,
            )

        for d in result.dependencies:
            cur.execute(
                "INSERT INTO catalog.dependencies(snapshot_id,from_object,to_object,kind,detail) VALUES (?,?,?,?,?)",
                snapshot_id, d.from_object, d.to_object, d.kind, d.detail,
            )

    return snapshot_id
```

- [ ] **Step 5: 통합 테스트 통과 확인 (카탈로그 픽스처 DB 사용)**

카탈로그 테스트는 동일 픽스처 DB에 `catalog` 스키마를 만들어 검증한다. `U9C_TEST_CONN`을 재사용한다.
Run:
```bash
pytest tests/test_catalog_writer.py -m integration -v
```
Expected: PASS (1 passed)

- [ ] **Step 6: 커밋**

```bash
git add src/u9c_catalog/catalog_schema.sql src/u9c_catalog/catalog_writer.py tests/test_catalog_writer.py
git commit -m "feat: ERP_Catalog 스키마 및 스냅샷 적재기 추가"
```

---

## Task 7: 데이터 사전 생성기 (doc_generator.py + 템플릿)

**Files:**
- Create: `u9c-catalog/src/u9c_catalog/templates/data_dictionary.html.j2`
- Create: `u9c-catalog/src/u9c_catalog/doc_generator.py`
- Test: `u9c-catalog/tests/test_doc_generator.py`

- [ ] **Step 1: 실패하는 테스트 작성**

`tests/test_doc_generator.py`:
```python
from pathlib import Path

from u9c_catalog.doc_generator import generate_html, generate_excel
from u9c_catalog.extractor import ExtractResult
from u9c_catalog.noise_classifier import classify_all
from tests.fixtures.sample_metadata import make_receivement_table, make_trl_table


def _result():
    r = ExtractResult(tables=[make_receivement_table(), make_trl_table()])
    classify_all(r.tables)
    return r


def test_generate_html(tmp_path):
    out = tmp_path / "dd.html"
    generate_html(_result(), str(out))
    html = out.read_text(encoding="utf-8")
    assert "PM_Receivement" in html
    assert "DocNo" in html
    # 시스템 컬럼은 표시하되 구분 표기가 있어야 함
    assert "시스템" in html
    # 부수 테이블 표기
    assert "부수" in html


def test_generate_excel(tmp_path):
    out = tmp_path / "dd.xlsx"
    generate_excel(_result(), str(out))
    assert Path(out).exists()
    from openpyxl import load_workbook
    wb = load_workbook(out)
    assert "Objects" in wb.sheetnames
    assert "Columns" in wb.sheetnames
```

- [ ] **Step 2: 테스트 실패 확인**

Run: `pytest tests/test_doc_generator.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'u9c_catalog.doc_generator'`

- [ ] **Step 3: HTML 템플릿 작성**

`src/u9c_catalog/templates/data_dictionary.html.j2`:
```html
<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<title>U9C 데이터 사전</title>
<style>
 body { font-family: 'Malgun Gothic','맑은 고딕',sans-serif; margin: 24px; }
 h2 { border-bottom: 2px solid #333; padding-bottom: 4px; }
 table { border-collapse: collapse; width: 100%; margin-bottom: 24px; }
 th, td { border: 1px solid #ccc; padding: 4px 8px; font-size: 13px; }
 th { background: #f0f0f0; }
 .sys { color: #999; }
 .aux { background: #fff4e5; }
</style>
</head>
<body>
<h1>U9C 데이터 사전</h1>
{% for t in tables %}
<h2 class="{{ 'aux' if t.is_auxiliary else '' }}">
  {{ t.full_name }} ({{ t.object_type }})
  {% if t.is_auxiliary %}<small>[부수: {{ t.auxiliary_reason }}]</small>{% endif %}
  {% if t.row_count is not none %}<small>rows={{ t.row_count }}</small>{% endif %}
</h2>
<table>
<tr><th>#</th><th>컬럼</th><th>타입</th><th>NULL</th><th>PK</th><th>구분</th></tr>
{% for c in t.columns %}
<tr class="{{ 'sys' if c.is_system else '' }}">
  <td>{{ c.ordinal }}</td><td>{{ c.name }}</td><td>{{ c.data_type }}</td>
  <td>{{ 'Y' if c.is_nullable else 'N' }}</td>
  <td>{{ 'PK' if c.is_pk else '' }}</td>
  <td>{{ ('시스템: ' + c.system_reason) if c.is_system else '업무' }}</td>
</tr>
{% endfor %}
</table>
{% endfor %}
</body>
</html>
```

- [ ] **Step 4: doc_generator.py 구현**

```python
# 메타데이터로 HTML/Excel 데이터 사전을 생성 (한글 폰트 맑은 고딕)
from jinja2 import Environment, PackageLoader, select_autoescape
from openpyxl import Workbook
from openpyxl.styles import Font

from u9c_catalog.extractor import ExtractResult

_env = Environment(
    loader=PackageLoader("u9c_catalog", "templates"),
    autoescape=select_autoescape(["html"]),
)


def generate_html(result: ExtractResult, out_path: str) -> None:
    tmpl = _env.get_template("data_dictionary.html.j2")
    html = tmpl.render(tables=result.tables)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)


def generate_excel(result: ExtractResult, out_path: str) -> None:
    wb = Workbook()
    ws_obj = wb.active
    ws_obj.title = "Objects"
    ws_obj.append(["schema", "object", "type", "row_count", "is_auxiliary", "aux_reason"])
    for t in result.tables:
        ws_obj.append([t.schema, t.name, t.object_type, t.row_count,
                       "Y" if t.is_auxiliary else "N", t.auxiliary_reason or ""])

    ws_col = wb.create_sheet("Columns")
    ws_col.append(["schema", "object", "column", "type", "nullable", "pk", "is_system", "system_reason"])
    for t in result.tables:
        for c in t.columns:
            ws_col.append([t.schema, t.name, c.name, c.data_type,
                           "Y" if c.is_nullable else "N", "PK" if c.is_pk else "",
                           "Y" if c.is_system else "N", c.system_reason or ""])

    for ws in (ws_obj, ws_col):
        for cell in ws[1]:
            cell.font = Font(name="맑은 고딕", bold=True)

    wb.save(out_path)
```

- [ ] **Step 5: 테스트 통과 확인**

Run: `pytest tests/test_doc_generator.py -v`
Expected: PASS (2 passed)

- [ ] **Step 6: 커밋**

```bash
git add src/u9c_catalog/templates/data_dictionary.html.j2 src/u9c_catalog/doc_generator.py tests/test_doc_generator.py
git commit -m "feat: HTML/Excel 데이터 사전 생성기 추가"
```

---

## Task 8: 오케스트레이션 CLI (cli.py)

**Files:**
- Create: `u9c-catalog/src/u9c_catalog/cli.py`

- [ ] **Step 1: cli.py 구현**

```python
# 전체 Phase 1 파이프라인을 실행하는 CLI 엔트리포인트
import argparse
import os

from u9c_catalog.catalog_writer import ensure_schema, write_snapshot
from u9c_catalog.config import load_settings
from u9c_catalog.doc_generator import generate_excel, generate_html
from u9c_catalog.extractor import extract_metadata
from u9c_catalog.noise_classifier import classify_all


def run(config_path: str) -> int:
    s = load_settings(config_path)
    label = s.snapshot_label or "snapshot"

    print("[1/5] 스키마 추출 중...")
    result = extract_metadata(s.source_conn, schema_filter=s.source_schema_filter)
    print(f"      테이블/뷰 {len(result.tables)}개, 루틴 {len(result.routines)}개, FK {len(result.dependencies)}개")

    print("[2/5] 노이즈 분류 중...")
    classify_all(result.tables)
    aux = sum(1 for t in result.tables if t.is_auxiliary)
    print(f"      부수 테이블 {aux}개 태깅")

    print("[3/5] 카탈로그 스키마 확인/생성...")
    ensure_schema(s.catalog_conn)

    print("[4/5] 카탈로그 적재 중...")
    snapshot_id = write_snapshot(s.catalog_conn, result, label=label)
    print(f"      snapshot_id={snapshot_id}")

    print("[5/5] 데이터 사전 생성 중...")
    os.makedirs(s.output_dir, exist_ok=True)
    generate_html(result, os.path.join(s.output_dir, "data_dictionary.html"))
    generate_excel(result, os.path.join(s.output_dir, "data_dictionary.xlsx"))
    print(f"      산출물: {s.output_dir}")

    print("완료.")
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(description="U9C 카탈로그 Phase 1 파이프라인")
    parser.add_argument("--config", default="config.yaml", help="설정 파일 경로")
    args = parser.parse_args()
    raise SystemExit(run(args.config))


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: import 스모크 확인**

Run: `python -c "from u9c_catalog.cli import run, main; print('ok')"`
Expected: `ok`

- [ ] **Step 3: 전체 테스트 실행**

Run: `pytest -v`
Expected: 순수 로직 테스트 PASS, 통합 테스트는 `U9C_TEST_CONN` 없으면 SKIP.

- [ ] **Step 4: (환경 준비 시) 엔드투엔드 스모크**

픽스처 DB를 소스·카탈로그로 함께 사용해 실제 파이프라인을 돌린다.
```bash
# config.yaml, .env를 픽스처 DB로 채운 뒤
u9c-catalog --config config.yaml
```
Expected: `[1/5]~[5/5]` 출력, `output/data_dictionary.html`·`.xlsx` 생성, 카탈로그에 snapshot 적재.

- [ ] **Step 5: 커밋**

```bash
git add src/u9c_catalog/cli.py
git commit -m "feat: Phase 1 파이프라인 오케스트레이션 CLI 추가"
```

---

## Phase 1 완료 기준

- [ ] `pytest` 순수 로직 테스트 전부 통과 (config, models, noise_classifier, doc_generator).
- [ ] 픽스처 DB로 통합 테스트(extractor, catalog_writer) 통과.
- [ ] CLI 엔드투엔드로 데이터 사전(HTML/Excel) 생성 + 카탈로그 스냅샷 적재 확인.
- [ ] 한글이 HTML/Excel에 정상 표시(맑은 고딕).

## 다음 Phase 예고 (별도 계획으로 작성)

- **Phase 2** — 사용량 수집(DMV/Query Store) + 우선순위 점수 + 데이터 프로파일링.
- **Phase 3** — 델타 프로빙 + XEvents + 값 기반 관계·코드 추적(`SrcDoc_*`) + 6개 도메인 매핑.
- **Phase 4** — 운영 대조 검증 + 대시보드/MES 연동 JSON export + 주기 재실행.
