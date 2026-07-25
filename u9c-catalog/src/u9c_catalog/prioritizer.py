# 활성도·규모·업무성·(선택)DMV 신호를 결합해 테이블 우선순위 점수를 매긴다 (순수 로직).
import math

from u9c_catalog.models import ActivityMeta, PriorityMeta, TableMeta


def _business_col_count(t: TableMeta) -> int:
    return sum(1 for c in t.columns if not c.is_system)


def _score(t: TableMeta, act: ActivityMeta, dmv: dict | None) -> tuple[float, str]:
    reasons = []
    score = 0.0
    if t.is_auxiliary:
        score -= 5.0
        reasons.append("부수(-5)")
    rc = t.row_count or 0
    if rc > 0:
        score += math.log10(rc + 1)
        reasons.append(f"규모+{round(math.log10(rc+1),2)}")
    else:
        score -= 2.0
        reasons.append("빈테이블(-2)")
    bcols = _business_col_count(t)
    score += min(bcols, 30) * 0.1
    reasons.append(f"업무컬럼{bcols}")
    if act.last_activity is not None:
        score += 2.0
        reasons.append("활성+2")
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
