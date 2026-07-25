# 전체 Phase 1 파이프라인을 실행하는 CLI 엔트리포인트
import argparse
import os

from u9c_catalog.catalog_writer import ensure_schema, write_snapshot
from u9c_catalog.config import load_settings
from u9c_catalog.doc_generator import generate_excel, generate_html
from u9c_catalog.extractor import extract_metadata
from u9c_catalog.noise_classifier import classify_all


def run(config_path: str) -> int:
    s = load_settings(config_path)
    label = s.snapshot_label or "snapshot"

    print("[1/5] 스키마 추출 중...")
    result = extract_metadata(s.source_conn, schema_filter=s.source_schema_filter)
    print(f"      테이블/뷰 {len(result.tables)}개, 루틴 {len(result.routines)}개, FK {len(result.dependencies)}개")

    print("[2/5] 노이즈 분류 중...")
    classify_all(result.tables)
    aux = sum(1 for t in result.tables if t.is_auxiliary)
    print(f"      부수 테이블 {aux}개 태깅")

    print("[3/5] 카탈로그 스키마 확인/생성...")
    ensure_schema(s.catalog_conn)

    print("[4/5] 카탈로그 적재 중...")
    snapshot_id = write_snapshot(s.catalog_conn, result, label=label)
    print(f"      snapshot_id={snapshot_id}")

    print("[5/5] 데이터 사전 생성 중...")
    os.makedirs(s.output_dir, exist_ok=True)
    generate_html(result, os.path.join(s.output_dir, "data_dictionary.html"))
    generate_excel(result, os.path.join(s.output_dir, "data_dictionary.xlsx"))
    print(f"      산출물: {s.output_dir}")

    print("완료.")
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(description="U9C 카탈로그 Phase 1 파이프라인")
    parser.add_argument("--config", default="config.yaml", help="설정 파일 경로")
    args = parser.parse_args()
    raise SystemExit(run(args.config))


if __name__ == "__main__":
    main()
