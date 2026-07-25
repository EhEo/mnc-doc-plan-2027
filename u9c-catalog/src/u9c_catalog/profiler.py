# 우선순위 테이블의 컬럼별 NULL율·distinct·min/max를 샘플로 프로파일링한다.
from u9c_catalog.db import connect
from u9c_catalog.models import ColumnProfile, TableMeta


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
                # 비교 불가 타입(text/image/xml 등)은 스킵
                continue
            null_ratio = (int(nulls or 0) / n) if n else 0.0
            profs.append(ColumnProfile(
                schema=table.schema, name=table.name, column_name=c.name,
                null_ratio=round(null_ratio, 4), distinct_count=int(distinct or 0),
                sample_size=n, min_value=mn, max_value=mx,
            ))
    return profs
