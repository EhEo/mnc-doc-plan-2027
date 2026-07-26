# 노이즈 분류/문서 생성 테스트용 인메모리 메타데이터 픽스처
from u9c_catalog.models import ColumnMeta, TableMeta


def make_receivement_table() -> TableMeta:
    t = TableMeta(schema="dbo", name="PM_Receivement", object_type="TABLE", row_count=12000)
    cols = [
        ("ID", "bigint", False, True),
        ("Org", "bigint", False, False),
        ("DocNo", "nvarchar", False, False),
        ("CreatedBy", "bigint", True, False),
        ("CreatedOn", "datetime", True, False),
        ("ModifiedBy", "bigint", True, False),
        ("ModifiedOn", "datetime", True, False),
        ("SysMlFlag", "int", True, False),
        ("Effective_IsEffective", "bit", True, False),
        ("DescFlexField_PubDescSeg4", "nvarchar", True, False),
        ("BusinessDate", "datetime", True, False),
    ]
    for i, (n, dt, nul, pk) in enumerate(cols):
        t.columns.append(ColumnMeta(name=n, data_type=dt, is_nullable=nul, is_pk=pk, ordinal=i))
    return t


def make_trl_table() -> TableMeta:
    t = TableMeta(schema="dbo", name="CBO_ItemMaster_Trl", object_type="TABLE", row_count=500)
    t.columns.append(ColumnMeta(name="ID", data_type="bigint", is_nullable=False, is_pk=True))
    t.columns.append(ColumnMeta(name="Name", data_type="nvarchar", is_nullable=True))
    return t


def make_flow_tables() -> list[TableMeta]:
    """헤더-상세 + SrcDoc 문서흐름 픽스처."""
    hdr = TableMeta(schema="dbo", name="PM_Receivement", object_type="TABLE")
    hdr.columns.append(ColumnMeta(name="ID", data_type="bigint", is_nullable=False, is_pk=True))
    hdr.columns.append(ColumnMeta(name="DocNo", data_type="nvarchar", is_nullable=False))
    line = TableMeta(schema="dbo", name="PM_RcvLine", object_type="TABLE")
    line.columns.append(ColumnMeta(name="ID", data_type="bigint", is_nullable=False, is_pk=True))
    line.columns.append(ColumnMeta(name="Receivement", data_type="bigint", is_nullable=False))
    line.columns.append(ColumnMeta(name="SrcDoc_SrcDocSubLine_EntityID", data_type="bigint", is_nullable=True))
    line.columns.append(ColumnMeta(name="SrcDocType", data_type="int", is_nullable=True))
    return [hdr, line]
