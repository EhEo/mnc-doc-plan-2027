# 카탈로그의 한 스냅샷에서 테이블·컬럼(+우선순위)을 TableMeta로 복원한다.
from u9c_catalog.db import connect
from u9c_catalog.models import ColumnMeta, TableMeta


def load_snapshot_tables(catalog_conn: str, snapshot_id: int,
                         priority_only: bool = False) -> list[TableMeta]:
    with connect(catalog_conn, readonly=True) as conn:
        cur = conn.cursor()
        obj_sql = ("SELECT o.schema_name, o.object_name, o.object_type, o.row_count, "
                   "o.is_auxiliary, o.aux_reason FROM catalog.objects o ")
        if priority_only:
            obj_sql += ("JOIN catalog.priority p ON p.snapshot_id=o.snapshot_id "
                        "AND p.schema_name=o.schema_name AND p.object_name=o.object_name "
                        "AND p.is_priority=1 ")
        obj_sql += "WHERE o.snapshot_id=?"
        cur.execute(obj_sql, snapshot_id)
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
            c.is_system = bool(r[6])
            c.system_reason = r[7]
            t.columns.append(c)
    return list(tables.values())
