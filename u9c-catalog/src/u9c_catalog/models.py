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
    precision: int | None = None
    scale: int | None = None
    type_display: str | None = None
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


_LEN_TYPES = {"char", "varchar", "binary", "varbinary"}
_NLEN_TYPES = {"nchar", "nvarchar"}
_PREC_TYPES = {"decimal", "numeric"}


def format_type(data_type: str, max_length: int | None,
                precision: int | None, scale: int | None) -> str:
    """SQL Server 컬럼을 사람이 읽는 타입 표기로 변환한다 (예: nvarchar(40), decimal(18,2))."""
    dt = data_type.lower()
    if dt in _NLEN_TYPES:
        if max_length == -1:
            return f"{data_type}(MAX)"
        if max_length is None:
            return data_type
        return f"{data_type}({max_length // 2})"  # nchar/nvarchar는 byte 길이 → 문자수
    if dt in _LEN_TYPES:
        if max_length == -1:
            return f"{data_type}(MAX)"
        if max_length is None:
            return data_type
        return f"{data_type}({max_length})"
    if dt in _PREC_TYPES and precision is not None:
        return f"{data_type}({precision},{scale})"
    return data_type


@dataclass
class ActivityMeta:
    schema: str
    name: str
    last_activity: object | None          # datetime 또는 None
    source: str                            # 활동시각 산출 근거 컬럼명 또는 "none"

    @property
    def full_name(self) -> str:
        return f"{self.schema}.{self.name}"


@dataclass
class PriorityMeta:
    schema: str
    name: str
    score: float
    rank: int
    is_priority: bool = False
    reason: str | None = None

    @property
    def full_name(self) -> str:
        return f"{self.schema}.{self.name}"


@dataclass
class ColumnProfile:
    schema: str
    name: str
    column_name: str
    null_ratio: float
    distinct_count: int
    sample_size: int
    min_value: str | None = None
    max_value: str | None = None
    top_values: str | None = None          # "값:빈도, ..." 요약 문자열


@dataclass
class DomainAssignment:
    schema: str
    name: str
    domain: str                    # 생산실적/입출고/구매/구매요청/비용등록/매출/미분류
    role: str                      # 앵커/상세/연관/코드/미상
    confidence: float              # 0.0~1.0 (3a는 추정, 3b에서 상향)
    evidence: str
    verified_by: str | None = None

    @property
    def full_name(self) -> str:
        return f"{self.schema}.{self.name}"


@dataclass
class RelationEdge:
    from_object: str
    from_column: str
    to_object: str
    kind: str                      # "header-detail" | "master-ref" | "doc-flow"
    evidence: str
