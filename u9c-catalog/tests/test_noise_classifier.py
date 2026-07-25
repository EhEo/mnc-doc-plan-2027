from u9c_catalog.noise_classifier import classify_columns, classify_table
from tests.fixtures.sample_metadata import make_receivement_table, make_trl_table


def test_system_columns_tagged():
    t = make_receivement_table()
    classify_columns(t)
    by_name = {c.name: c for c in t.columns}
    for sysname in ["ID", "Org", "CreatedBy", "CreatedOn", "ModifiedBy",
                    "ModifiedOn", "SysMlFlag", "Effective_IsEffective",
                    "DescFlexField_PubDescSeg4"]:
        assert by_name[sysname].is_system is True, sysname
    # 업무 컬럼은 시스템으로 잡히면 안 됨
    assert by_name["DocNo"].is_system is False
    assert by_name["BusinessDate"].is_system is False


def test_alt_audit_naming_tagged():
    from u9c_catalog.models import ColumnMeta, TableMeta
    t = TableMeta(schema="dbo", name="ECN_X", object_type="TABLE")
    for n in ["CreateUser", "CreateDate", "ModifyUser", "ModifyTime"]:
        t.columns.append(ColumnMeta(name=n, data_type="nvarchar", is_nullable=True))
    classify_columns(t)
    assert all(c.is_system for c in t.columns)


def test_trl_table_is_auxiliary():
    t = make_trl_table()
    classify_table(t)
    assert t.is_auxiliary is True
    assert "Trl" in (t.auxiliary_reason or "")


def test_business_table_not_auxiliary():
    t = make_receivement_table()
    classify_table(t)
    assert t.is_auxiliary is False
