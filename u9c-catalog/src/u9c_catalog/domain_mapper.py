# 테이블명(접두어+키워드) 규칙으로 6개 업무 도메인을 추정 할당한다 (순수 로직, 추정 신뢰도).
from u9c_catalog.models import DomainAssignment, TableMeta

# 규칙 우선순위 순서 중요. (도메인, [접두어...], [키워드...], 기본신뢰도)
_RULES = [
    ("구매요청", ["PR_"], ["Requisition", "Requisiton", "Apply", "Request", "请购", "请购单"], 0.55),
    ("생산실적", ["MO_", "SFC_"], ["Issue", "Dispatch", "Complete", "OpTransfer", "WIP", "MO"], 0.6),
    ("입출고", ["InvTrans_", "InvDoc_"], ["TransIn", "TransOut", "MiscShip", "Receipt", "Bin"], 0.6),
    ("구매", ["PM_", "PPR_", "AP_", "Complete_Rcv"], ["Purchase", "PO", "Rcv", "Receivement", "APPosted"], 0.55),
    ("매출", ["SM_", "AR_"], ["SOOrder", "Sales", "Ship", "Invoice", "ARPosted"], 0.55),
    ("비용등록", ["CA_", "GL_", "IC_", "AAI_", "FA_"], ["Cost", "Expense", "Fee", "Entry", "Element"], 0.5),
]

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
    for p in _PLATFORM_PREFIXES:
        if name.startswith(p):
            return DomainAssignment(table.schema, name, "미분류", "미상", 0.0, f"플랫폼 접두어 {p}")
    req_kw = _keyword_hit(name, ["Requisition", "Requisiton", "请购", "PurApply", "PurRequest"])
    if req_kw:
        return DomainAssignment(table.schema, name, "구매요청", _role_of(name), 0.6, f"키워드 {req_kw}")
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
