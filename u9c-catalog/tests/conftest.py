# pytest 공통 설정: 통합 테스트는 연결 환경변수가 없으면 자동 skip
import os
import pytest


@pytest.fixture
def test_conn_str():
    conn = os.environ.get("U9C_TEST_CONN", "").strip()
    if not conn:
        pytest.skip("U9C_TEST_CONN 미설정 — 통합 테스트 skip")
    return conn
