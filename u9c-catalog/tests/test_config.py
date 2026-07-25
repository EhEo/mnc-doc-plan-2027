from u9c_catalog.config import load_settings


def test_load_settings_reads_yaml_and_env(tmp_path, monkeypatch):
    # 실제 .env가 있어도 테스트가 흔들리지 않게 load_dotenv를 무력화(테스트 격리)
    monkeypatch.setattr("u9c_catalog.config.load_dotenv", lambda *a, **k: None)
    cfg = tmp_path / "config.yaml"
    cfg.write_text(
        "source_schema_filter: [dbo]\noutput_dir: ./out\nsnapshot_label: test\n",
        encoding="utf-8",
    )
    monkeypatch.setenv("U9C_SOURCE_CONN", "SRC")
    monkeypatch.setenv("CATALOG_CONN", "CAT")

    s = load_settings(str(cfg))

    assert s.source_conn == "SRC"
    assert s.catalog_conn == "CAT"
    assert s.source_schema_filter == ["dbo"]
    assert s.output_dir == "./out"
    assert s.snapshot_label == "test"


def test_missing_conn_raises(tmp_path, monkeypatch):
    # 실제 .env가 있어도 테스트가 흔들리지 않게 load_dotenv를 무력화(테스트 격리)
    monkeypatch.setattr("u9c_catalog.config.load_dotenv", lambda *a, **k: None)
    cfg = tmp_path / "config.yaml"
    cfg.write_text("output_dir: ./out\n", encoding="utf-8")
    monkeypatch.delenv("U9C_SOURCE_CONN", raising=False)
    monkeypatch.setenv("CATALOG_CONN", "CAT")

    import pytest
    with pytest.raises(ValueError, match="U9C_SOURCE_CONN"):
        load_settings(str(cfg))
