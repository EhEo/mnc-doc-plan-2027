# pyodbc 연결을 생성/관리하는 얇은 팩토리 (읽기 전용 소스, 쓰기 카탈로그)
# pyodbc는 컴파일 의존성이므로 함수 내부에서 지연 import한다 (순수 로직 계층과 분리).
from contextlib import contextmanager


@contextmanager
def connect(conn_str: str, readonly: bool = False):
    """연결을 열고 컨텍스트 종료 시 닫는다. readonly=True면 자동커밋(쓰기 없음)."""
    import pyodbc
    conn = pyodbc.connect(conn_str, autocommit=readonly)
    try:
        yield conn
        if not readonly:
            conn.commit()
    except Exception:
        if not readonly:
            conn.rollback()
        raise
    finally:
        conn.close()
