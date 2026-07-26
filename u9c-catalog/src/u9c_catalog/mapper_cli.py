# 카탈로그 스냅샷에서 도메인 매핑 + 관계를 계산해 카탈로그에 적재하고 도메인 맵을 내보낸다.
import argparse
import os
from collections import Counter

from u9c_catalog.catalog_reader import load_snapshot_tables
from u9c_catalog.catalog_writer import ensure_schema, write_business_map, write_relations
from u9c_catalog.config import load_settings
from u9c_catalog.db import connect
from u9c_catalog.doc_generator import generate_domain_map_json
from u9c_catalog.domain_mapper import assign_domains
from u9c_catalog.relation_finder import find_relations


def _latest_snapshot(catalog_conn: str) -> int:
    with connect(catalog_conn, readonly=True) as c:
        cur = c.cursor()
        cur.execute("SELECT MAX(snapshot_id) FROM catalog.snapshots")
        row = cur.fetchone()
    if row is None or row[0] is None:
        raise ValueError("카탈로그에 스냅샷이 없습니다. 먼저 u9c-catalog로 추출을 실행하세요.")
    return int(row[0])


def run(config_path: str, snapshot_id: int | None, priority_only: bool) -> int:
    s = load_settings(config_path)
    ensure_schema(s.catalog_conn)
    sid = snapshot_id or _latest_snapshot(s.catalog_conn)
    print(f"[map] snapshot_id={sid} 대상")

    tables = load_snapshot_tables(s.catalog_conn, sid, priority_only=priority_only)
    print(f"[map] 테이블 {len(tables)}개 로드 (priority_only={priority_only})")

    assignments = assign_domains(tables)
    write_business_map(s.catalog_conn, sid, assignments)
    dist = Counter(a.domain for a in assignments)
    print(f"[map] 도메인 분포: {dict(dist)}")

    edges = find_relations(tables)
    write_relations(s.catalog_conn, sid, edges)
    print(f"[map] 관계 엣지 {len(edges)}개")

    os.makedirs(s.output_dir, exist_ok=True)
    out = os.path.join(s.output_dir, "domain_map.json")
    generate_domain_map_json(assignments, edges, out)
    print(f"[map] 도메인 맵: {out}")
    print("완료.")
    return 0


def main() -> None:
    p = argparse.ArgumentParser(description="U9C 도메인 매핑 (Phase 3a)")
    p.add_argument("--config", default="config.yaml")
    p.add_argument("--snapshot", type=int, default=None, help="대상 snapshot_id (기본: 최신)")
    p.add_argument("--priority-only", action="store_true", help="우선순위 테이블만 매핑")
    a = p.parse_args()
    raise SystemExit(run(a.config, a.snapshot, a.priority_only))


if __name__ == "__main__":
    main()
