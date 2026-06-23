# 체크리스트 — AI 디바이스/GPU 정밀가공품 시장조사 & 진입전략 보고서

## Phase 0 — 환경·설계 (완료)
- [x] Gemini/Codex CLI 가동 확인 (ask-gemini.sh, ask-codex.sh)
- [x] 리서치 엔진 검증: Gemini는 출처명만 반환(검증 불가) → WebSearch+WebFetch가 실제 URL 반환 확인
- [x] 회사 프로필 확보: CNC 밀링/5축 + 선반/복합기, 소재(알루미늄·구리·SUS·티타늄/특수·플라스틱), 인증 ISO9001+IATF16949
- [x] 아키텍처 확정: 검증=WebSearch/WebFetch, 팀=Claude 서브에이전트, 교차검증=Gemini, 최종리뷰=Codex

## Phase 1 — 병렬 조사 (Round 1)
- [x] **agy**: 가공품 8종 전수조사 → 표, 13개 출처 (agy-machining.md)
- [x] **codex(리서치)**: 기업 13곳·매출·티어·시장규모·한국현황, 28개 출처 (codex-market.md)

## Phase 2 — 매칭 & 교차검증 (Round 2)
- [x] agy 가공품 목록 → codex 전달, 기업-가공품 매칭 (codex-reconcile.md)
- [x] 물량 vs 매출 reconcile: $293.84M 콜드플레이트 시장 과소계상 적발(3경로), 5.2M vs 1.08M 모집단 차이 정리, $400/개 단가 anchor 확보
- [x] Gemini 교차검증: 3개 헤드라인 수치 통념 부합 + 2026 침투율 ~47% 추가
- [x] WebFetch 직접 확정: 액냉 침투율 14%→33% (TrendForce 원문)

## Phase 3 — 전략 분석 (Round 3)
- [x] **전략 조교**: 진입난이도 분류·필요설비/인증·진입경로·리스크 (strategy-analysis.md)
- [x] 회사 프로필 앵커링 + NVIDIA RVL·Rubin 조달·NADCAP 절차 신규 조사

## Phase 4 — 통합 보고서 (Round 4, 리드=나)
- [x] ① 요약 ② 가공품·가공기 총람 ③ 시장현황 ④ 진입기회·로드맵 ⑤ 출처목록 (5개 섹션 전부)
- [x] 21,476자/표 14개 — 렌더링 시 10~15페이지 범위
- [x] 핵심 수치 실제 URL 역추적 가능 (진실성 게이트)

## Phase 5 — 검토
- [x] Codex 최종 리뷰 → **NEEDS-FIX** (Blocker 0, Major 4, Minor 2)
- [x] 6건 전부 사용자 보고 후 반영: 시장정의 주석, 2026 47% 출처보강(TrendForce 2025-11-27), BOM 표현/수치 분리, IATF 단정 완화, Cooler Master/Foxconn/Quanta 라벨 보도화
- [x] NEED RESEARCH(2026 47%) → WebSearch로 TrendForce 1차 출처 확보
- [x] 최종 verdict + 로그 경로 보고

## Phase 6 — 확장 (사용자 요청: ③·④ 추가)
- [x] jpcn 조교: 일본(Furukawa/Fujikura)·중국(Envicool/Yinlun/Feirongda/中石/高澜) 심화 → §3.6
- [x] capex 조교: 설비·인증 단가 + SOM 3시나리오 bottom-up → §4.6·§4.7
- [x] 스폿체크: Furukawa ¥1,201.8B·Yinlun 127.02억元 원문확인, Fujikura 403(2차출처), SOM 산수 재검산 일치
- [x] §3.6/§4.6/§4.7 + ①요약 + 출처 + 부록 통합. 분량 30KB/표 18개 → 10~15p 충족
- [x] Codex 추가섹션 재검토 → **SHIP** (Blocker/Major/Minor 0건, 단위·SOM산수·라벨·정합성 통과)
