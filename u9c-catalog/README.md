# U9C 카탈로그 (Phase 1)

U9C ERP 스키마를 읽기 전용으로 추출 → 노이즈 분류 → ERP_Catalog 적재 → 데이터 사전 생성.

## 설치
```bash
cd u9c-catalog
python -m venv .venv && .venv\Scripts\activate
pip install -e ".[dev]"
```

## 설정
`.env.example` → `.env`, `config.example.yaml` → `config.yaml` 복사 후 값 채우기.

## 실행
```bash
u9c-catalog --config config.yaml
```

## 테스트
```bash
pytest                       # 순수 로직 테스트
$env:U9C_TEST_CONN="..."     # 픽스처 DB 지정 시
pytest -m integration        # 통합 테스트
```
