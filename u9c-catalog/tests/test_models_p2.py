from u9c_catalog.models import ActivityMeta, PriorityMeta, ColumnProfile


def test_activity_meta():
    a = ActivityMeta(schema="dbo", name="PM_Receivement", last_activity=None, source="none")
    assert a.full_name == "dbo.PM_Receivement"


def test_priority_meta_defaults():
    p = PriorityMeta(schema="dbo", name="T", score=1.5, rank=1)
    assert p.is_priority is False


def test_column_profile():
    cp = ColumnProfile(schema="dbo", name="T", column_name="C", null_ratio=0.1,
                       distinct_count=5, sample_size=100)
    assert cp.min_value is None
