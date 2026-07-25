# 데이터 프로파일러(profile_table) 통합 테스트
import pytest
from u9c_catalog.profiler import profile_table
from u9c_catalog.extractor import extract_metadata


@pytest.mark.integration
def test_profile_table(test_conn_str):
    md = extract_metadata(test_conn_str, schema_filter=["dbo"])
    recv = next(t for t in md.tables if t.name == "PM_Receivement")
    profs = profile_table(test_conn_str, recv, sample_limit=1000)
    by = {p.column_name: p for p in profs}
    assert by["DocNo"].null_ratio == 0.0
    assert by["DocNo"].distinct_count >= 1
    assert profs[0].sample_size >= 1
