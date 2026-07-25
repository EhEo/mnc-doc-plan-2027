# U9C 지식 베이스 규칙으로 시스템 컬럼/부수 테이블을 태깅하는 분류기
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
