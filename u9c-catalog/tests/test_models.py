from u9c_catalog.models import ColumnMeta, TableMeta, RoutineMeta, DependencyMeta


def test_columnmeta_defaults():
    c = ColumnMeta(name="Org", data_type="bigint", is_nullable=False)
    assert c.is_system is False
    assert c.is_pk is False


def test_tablemeta_holds_columns():
    t = TableMeta(schema="dbo", name="PM_Receivement", object_type="TABLE")
    t.columns.append(ColumnMeta(name="ID", data_type="bigint", is_nullable=False, is_pk=True))
    assert t.full_name == "dbo.PM_Receivement"
    assert t.columns[0].is_pk is True


def test_routinemeta_full_name():
    r = RoutineMeta(schema="dbo", name="usp_x", object_type="PROCEDURE", definition="...")
    assert r.full_name == "dbo.usp_x"


def test_dependencymeta():
    d = DependencyMeta(from_object="dbo.A", to_object="dbo.B", kind="FK")
    assert d.kind == "FK"
