# 컨텍스트 노트 — 결정 사항과 근거

작업 시작: 2026-06-10

## 핵심 설계 결정

### D1. 리서치 엔진 = WebSearch+WebFetch (Gemini 아님)
- **근거**: Gemini CLI(ask-gemini.sh) 실전 테스트 결과, 그럴듯한 수치 + 출처"명"만 반환하고
  검증 가능한 URL을 주지 않음. 웹 grounding 발동 여부도 불확실(로컬 GrepTool fallback 로그).
- 실제 충돌 사례: Auras 액체냉각 비중 — Gemini "2024 Q2 ~20%" vs DigiTimes(WebSearch) "2024년 12%, 2025년 40% 전망".
- **적용**: 보고서의 모든 핵심 수치는 WebFetch로 원문 확인. Gemini는 리드 생성·교차검증 보조용으로만.

### D2. 오케스트레이션 매핑
- 사용자가 묘사한 팀(agy/codex/전략) = Claude 서브에이전트(Agent tool)로 구현.
- 프로젝트 CLAUDE.md 정책: Gemini=researcher, Codex=reviewer는 **메인 세션에서만** 호출(서브에이전트 내 호출 금지).
- 따라서: 서브에이전트는 WebSearch/WebFetch만 사용. Gemini/Codex 호출은 내가 메인에서 수행.

### D3. 작업 순서 (사용자 지정 준수)
- agy + codex 병렬 시작 → codex의 기업-가공품 "매칭"은 agy 목록 수령 후 → 교차검증 → 전략 분석 → 통합.

### D4. 회사 프로필 (전략 섹션 앵커)
- 설비: CNC 밀링/5축, CNC 선반/복합기 (절삭가공 중심. 압출/다이캐스팅/스카이빙 미보유로 추정)
- 소재: 알루미늄, 구리/동합금, SUS/스틸, 티타늄/특수·플라스틱 (광범위)
- 인증: ISO 9001 + IATF 16949 (자동차 품질체계 보유 → 추적성·무결점 역량은 강점)
- 규모: 미응답 → **중소기업(30~100명) 가정**. 보고서에 가정임을 명시.
- 함의: 절삭가공+다소재+IATF는 방열판/콜드플레이트/브라켓/구조부품 진입에 유리. 압출형 히트싱크·다이캐스팅은 약점.

## 교차검증 충돌/확정 기록 (Phase 2)
- (Auras 액냉 비중) Gemini 20% vs DigiTimes 12% → **DigiTimes(원문 URL 존재) 채택**.
- (액냉 침투율) **TrendForce 원문 WebFetch 직접 확정: 2024년 14% → 2025년 33%** (2025-08-21 발행). 콜드플레이트 공급사 Cooler Master/AVC/Boyd/Auras, %점유율은 원문 미공개. → 헤드라인 수치로 확정.
- 약한 출처 2건(보강 필요): Blackwell 5.2M개(TweakTown 403), 콜드플레이트 $293.84M(GM snippet) → codex reconcile에 보강 의뢰.
- (이후 추가)

## Codex 리뷰 결과 (Phase 5)
- 판정 NEEDS-FIX (Blocker 0, Major 4, Minor 2). 6건 전부 반영.
- Major: ①$142.88B vs $187B 정의주석 ②2026 47% 출처보강(TrendForce 2025-11-27 WebSearch 확보) ③BOM "NVIDIA 인정"표현 제거·$88k(GB200)/$49,860(GB300) 분리 ④IATF 벤더등록 "사실상통과"→"강점·가능성↑" 완화.
- Minor: Cooler Master/Foxconn/Quanta 점유 "확정"→"보도".

## 진실성 게이트 — URL 스폿체크 (advisor 지적 후)
- 서브에이전트 인용 ~40건 중 직접검증은 3건뿐이었음 → load-bearing 4건 추가 WebFetch.
- ✅ AVC NT$71.8B(taiwannews 6058452) 원문일치 / ✅ M&M $142.88B→$837.83B 원문일치 / ✅ DigiTimes Rubin(a20260318PD231) "names four cold plate suppliers·AVC" 확인 / ⚠️ CommonWealth 4145 403→GlobalSemiResearch substack로 "CM 50%+·AVC 30~40%" 독립 보강.
- 결론: 특정 article ID 2건이 숫자까지 정확 resolve → 서브에이전트가 실제 fetch함. 게이트 유지.

## 미해결/리스크
- 회사 규모 미확정 → 중소기업 가정. 로드맵에서 규모 의존 항목은 분기 처리.
- "추정 물량"은 공개 데이터가 희소 → top-down(시장규모×단가) 추정 + 가정 명시.
- 분량: 3,357어절/21.5KB/표 14개. 영어 단어수로는 ~6p지만 표 다수로 렌더링 시 더 큼. 사용자에 실측치 보고 + 확장옵션(③ 일본·중국 심화, ④ capex/SOM 추정) 제시.
