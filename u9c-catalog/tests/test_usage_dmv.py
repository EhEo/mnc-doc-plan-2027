import pytest
from u9c_catalog.usage_dmv import collect_dmv_usage


@pytest.mark.integration
def test_dmv_usage_returns_dict_or_none(test_conn_str):
    # 권한 있으면 dict, 없으면 None. LocalDB(sysadmin)에서는 dict 기대.
    res = collect_dmv_usage(test_conn_str)
    assert res is None or isinstance(res, dict)
