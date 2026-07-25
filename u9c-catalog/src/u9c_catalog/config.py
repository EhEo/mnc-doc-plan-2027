# .env와 config.yaml을 읽어 실행 설정(Settings)을 만드는 로더
import os
from dataclasses import dataclass, field

import yaml
from dotenv import load_dotenv


@dataclass
class Settings:
    source_conn: str
    catalog_conn: str
    source_schema_filter: list[str] = field(default_factory=list)
    exclude_object_prefixes: list[str] = field(default_factory=list)
    output_dir: str = "./output"
    snapshot_label: str = ""


def _require_env(name: str) -> str:
    val = os.environ.get(name, "").strip()
    if not val:
        raise ValueError(f"환경변수 {name} 가 비어 있습니다. .env를 확인하세요.")
    return val


def load_settings(config_path: str) -> Settings:
    load_dotenv()
    with open(config_path, encoding="utf-8") as f:
        cfg = yaml.safe_load(f) or {}
    return Settings(
        source_conn=_require_env("U9C_SOURCE_CONN"),
        catalog_conn=_require_env("CATALOG_CONN"),
        source_schema_filter=cfg.get("source_schema_filter") or [],
        exclude_object_prefixes=cfg.get("exclude_object_prefixes") or [],
        output_dir=cfg.get("output_dir") or "./output",
        snapshot_label=cfg.get("snapshot_label") or "",
    )
