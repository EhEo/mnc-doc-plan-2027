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
