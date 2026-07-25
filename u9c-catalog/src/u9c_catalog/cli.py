# 전체 파이프라인(Phase 1+2)을 실행하는 CLI 엔트리포인트
import argparse
import os

from u9c_catalog.activity import collect_activity
from u9c_catalog.catalog_writer import (ensure_schema, write_snapshot,
    write_activity, write_usage, write_priority, write_profiles)
from u9c_catalog.config import load_settings
from u9c_catalog.doc_generator import (generate_html, generate_excel,
    generate_priority_json, filter_priority_tables)
from u9c_catalog.extractor import extract_metadata, ExtractResult
from u9c_catalog.noise_classifier import classify_all
from u9c_catalog.prioritizer import score_tables
from u9c_catalog.profiler import profile_tables
from u9c_catalog.usage_dmv import collect_dmv_usage


def run(config_path: str) -> int:
    s = load_settings(config_path)
    label = s.snapshot_label or "snapshot"

    print("[1/8] 스키마 추출 중...")
    result = extract_metadata(s.source_conn, schema_filter=s.source_schema_filter)
    print(f"      테이블/뷰 {len(result.tables)}개, 루틴 {len(result.routines)}개, FK {len(result.dependencies)}개")

    print("[2/8] 노이즈 분류 중...")
    classify_all(result.tables)
    aux = sum(1 for t in result.tables if t.is_auxiliary)
    print(f"      부수 테이블 {aux}개 태깅")

    print("[3/8] 카탈로그 스키마 확인/생성...")
    ensure_schema(s.catalog_conn)

    print("[4/8] 카탈로그 적재 중...")
    snapshot_id = write_snapshot(s.catalog_conn, result, label=label)
    print(f"      snapshot_id={snapshot_id}")

    print("[5/8] 활성도 수집 중...")
    activities = collect_activity(s.source_conn, result.tables)
    write_activity(s.catalog_conn, snapshot_id, activities)

    print("[6/8] DMV 사용량 수집 시도...")
    dmv = collect_dmv_usage(s.source_conn)
    if dmv is None:
        print("      DMV 권한 없음 → 건너뜀(데이터 기반 신호만 사용)")
    else:
        write_usage(s.catalog_conn, snapshot_id, dmv)
        print(f"      DMV 사용량 {len(dmv)}개 테이블")

    print("[7/8] 우선순위 산정 + 프로파일링 중...")
    act_map = {a.full_name: a for a in activities}
    priorities = score_tables(result.tables, act_map, dmv, top_n=s.profile_top_n)
    write_priority(s.catalog_conn, snapshot_id, priorities)
    pri_tables = filter_priority_tables(result.tables, priorities)
    print(f"      우선순위 상위 {len(pri_tables)}개 선별")
    all_profiles = profile_tables(s.source_conn, pri_tables)
    write_profiles(s.catalog_conn, snapshot_id, all_profiles)
    print(f"      프로파일 {len(all_profiles)}개 컬럼")

    print("[8/8] 산출물 생성 중...")
    os.makedirs(s.output_dir, exist_ok=True)
    pri_result = ExtractResult(tables=pri_tables, routines=result.routines, dependencies=result.dependencies)
    generate_html(pri_result, os.path.join(s.output_dir, "data_dictionary_priority.html"))
    generate_excel(pri_result, os.path.join(s.output_dir, "data_dictionary_priority.xlsx"))
    generate_priority_json(priorities, os.path.join(s.output_dir, "priority_map.json"))
    print(f"      산출물: {s.output_dir}")

    print("완료.")
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(description="U9C 카탈로그 파이프라인 (Phase 1+2)")
    parser.add_argument("--config", default="config.yaml", help="설정 파일 경로")
    args = parser.parse_args()
    raise SystemExit(run(args.config))


if __name__ == "__main__":
    main()
