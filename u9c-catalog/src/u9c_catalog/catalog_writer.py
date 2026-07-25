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
