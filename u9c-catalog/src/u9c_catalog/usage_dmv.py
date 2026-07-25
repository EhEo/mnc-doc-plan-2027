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
        if "VIEW SERVER STATE" in str(e) or "permission" in str(e).lower():
            return None
        raise
