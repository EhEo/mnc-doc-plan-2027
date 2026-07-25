import pytest

from u9c_catalog.extractor import extract_metadata


@pytest.mark.integration
def test_extract_finds_fixture_tables(test_conn_str):
    result = extract_metadata(test_conn_str, schema_filter=["dbo"])
    names = {t.full_name for t in result.tables}
    assert "dbo.PM_Receivement" in names
    assert "dbo.CBO_ItemMaster_Trl" in names

    recv = next(t for t in result.tables if t.name == "PM_Receivement")
    by_name = {c.name: c for c in recv.columns}
    assert by_name["ID"].is_pk is True
    assert recv.row_count == 1
    assert by_name["DocNo"].type_display == "nvarchar(40)"
