from u9c_catalog.activity import pick_activity_column
from u9c_catalog.models import ColumnMeta, TableMeta


def _t(colnames):
    t = TableMeta(schema="dbo", name="T", object_type="TABLE")
    for n in colnames:
        t.columns.append(ColumnMeta(name=n, data_type="datetime", is_nullable=True))
    return t


def test_prefers_modifiedon():
    assert pick_activity_column(_t(["ID", "ModifiedOn", "CreatedOn"])) == "ModifiedOn"


def test_falls_back_to_createdon():
    assert pick_activity_column(_t(["ID", "CreatedOn"])) == "CreatedOn"


def test_alt_naming():
    assert pick_activity_column(_t(["ModifyDate", "CreateDate"])) == "ModifyDate"


def test_none_when_no_audit_col():
    assert pick_activity_column(_t(["ID", "Name"])) is None


def test_ignores_non_date_typed_audit_column():
    from u9c_catalog.models import ColumnMeta, TableMeta
    t = TableMeta(schema="dbo", name="T", object_type="TABLE")
    t.columns.append(ColumnMeta(name="CreateDate", data_type="int", is_nullable=True))
    assert pick_activity_column(t) is None


import pytest
from u9c_catalog.activity import collect_activity


@pytest.mark.integration
def test_collect_activity_integration(test_conn_str):
    from u9c_catalog.extractor import extract_metadata
    md = extract_metadata(test_conn_str, schema_filter=["dbo"])
    acts = {a.full_name: a for a in collect_activity(test_conn_str, md.tables)}
    assert "dbo.PM_Receivement" in acts
