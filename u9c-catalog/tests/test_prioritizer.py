from u9c_catalog.prioritizer import score_tables
from u9c_catalog.models import ColumnMeta, TableMeta, ActivityMeta


def _tbl(name, ncols, business_cols, rows, aux=False):
    t = TableMeta(schema="dbo", name=name, object_type="TABLE", row_count=rows, is_auxiliary=aux)
    for i in range(ncols):
        c = ColumnMeta(name=f"c{i}", data_type="int", is_nullable=True)
        c.is_system = i >= business_cols
        t.columns.append(c)
    return t


def test_priority_ranking_order():
    tables = [
        _tbl("Big", 20, 15, 100000),
        _tbl("Empty", 20, 15, 0),
        _tbl("Aux", 5, 0, 5000, aux=True),
    ]
    acts = {
        "dbo.Big": ActivityMeta("dbo", "Big", "2026-07-20", "ModifiedOn"),
        "dbo.Empty": ActivityMeta("dbo", "Empty", None, "none"),
        "dbo.Aux": ActivityMeta("dbo", "Aux", "2026-07-20", "ModifiedOn"),
    }
    ranked = score_tables(tables, acts, dmv=None, top_n=2)
    by = {p.name: p for p in ranked}
    assert by["Big"].rank == 1
    assert by["Big"].is_priority is True
    assert by["Aux"].score < by["Big"].score
    assert by["Empty"].score < by["Big"].score
    assert sum(1 for p in ranked if p.is_priority) == 2


def test_empty_and_aux_not_priority_when_topn_small():
    tables = [_tbl("Aux", 5, 0, 5000, aux=True), _tbl("Empty", 10, 8, 0)]
    acts = {"dbo.Aux": ActivityMeta("dbo","Aux",None,"none"),
            "dbo.Empty": ActivityMeta("dbo","Empty",None,"none")}
    ranked = score_tables(tables, acts, dmv=None, top_n=1)
    assert sum(1 for p in ranked if p.is_priority) == 1
