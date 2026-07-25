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
    """각 테이블의 활동시각 = 선택 컬럼의 MAX(...). 뷰/후보없음은 last_activity=None."""
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
