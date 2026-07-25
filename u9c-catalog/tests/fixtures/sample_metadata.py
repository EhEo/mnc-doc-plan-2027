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
