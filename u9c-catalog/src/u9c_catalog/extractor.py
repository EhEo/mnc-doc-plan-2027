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
