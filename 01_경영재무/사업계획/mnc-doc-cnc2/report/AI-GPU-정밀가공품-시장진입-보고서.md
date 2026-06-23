<!-- AI/GPU 정밀가공품 시장조사 및 우리 가공회사 사업진입 기회분석 통합 보고서 -->

# AI 디바이스·GPU 정밀가공품 시장 조사 및 사업진입 기회분석 보고서

> 작성일 2026-06-10 · 작성 체계 PM(리드) + 3개 조사 조교(agy 가공품, codex 기업·시장, 전략 조교) + 외부 교차검증(Gemini)·리뷰(Codex)
> 조사 기간 자료 2024~2026 · 모든 정량 수치에는 출처를 표기하며, **확정 사실 / 추정·전망 / 미확인**을 구분한다.

**수치 신뢰도 규약.** 본 보고서는 그럴듯한 숫자 날조를 방지하기 위해 다음 위계를 적용했다 — ① 1차/IR·거래소 공시·SEC 파일링(최상) ② 리서치사·투자은행(TrendForce, MarketsandMarkets, Morgan Stanley 등, 중간) ③ 블로그·snippet(최하, 삼각측량으로 보정 후 사용). 위계 최하단 수치 2건(콜드플레이트 시장 $293.84M, Blackwell GPU 5.2M개)은 교차검증에서 부적합·과대/과소로 판정되어 **본문에서 보정·교체**했다(§3.4 참조).

---

## ① 요약 (Executive Summary)

**시장.** AI 서버 시장은 2024년 약 **US$142.88B → 2030년 US$837.83B(CAGR 34.3%)**로 성장한다(MarketsandMarkets). 별도로 TrendForce는 2024년 AI 서버 출하량을 **약 167만 대(+41.5% YoY)**, 시장가치 US$187B(전체 서버시장의 65%)로 집계했다(두 수치는 리서치사·정의 차이로 다르다 — §3.1 주석). GPU TDP가 1,000~1,200W를 넘어서며 공랭의 물리적 한계(랙당 50~100kW)를 초과해, **액체냉각(direct-to-chip)이 NVIDIA GB200 NVL72에서 선택이 아닌 필수 아키텍처**가 되었다. AI 데이터센터 액냉 침투율은 **2024년 14% → 2025년 33% → 2026년 약 47%**로 급증한다(TrendForce, Gemini 교차검증 부합).

**가공품.** AI/GPU 서버 정밀가공의 핵심은 **콜드플레이트·매니폴드(수냉)**이다. 액냉 부품은 랙 BOM에서 GPU·CPU 모듈 다음으로 높은 단일 부품 비중을 차지한다(GB200 NVL72 기준 랙당 약 US$88,000, BOM의 약 2.9% — Morgan Stanley/IntuitionLabs). 단가 측면에서 콜드플레이트는 약 US$400/개, GB300/Blackwell Ultra NVL72 기준 랙당 액냉 BOM은 약 US$49,860로 추정된다(Morgan Stanley/Tom's Hardware). 8개 조사 품목 중 절삭가공 비중이 높은 것은 콜드플레이트·매니폴드(CNC 밀링/5축), 버스바(CNC 멀티축), GPU 백플레이트(CNC), 반도체 장비 정밀부품(CNC+EDM+연삭)이다.

**경쟁 구도.** 글로벌 공급망은 **대만·미국·일본**이 장악한다. Tier-1 랙 ODM은 Foxconn(~40%)·Quanta(~30%)·Wiwynn, Tier-2 콜드플레이트/모듈은 Cooler Master(GB200 1차 액냉 50%+)·AVC(2024 NT$71.8B)·Boyd·Auras(2024 NT$15.78B), CDU는 Delta·Vertiv·CoolIT, 커넥터는 Amphenol·TE 및 QD 4사(CPC·Parker·Danfoss·Staubli)다. **한국은 GB200급 콜드플레이트/CDU 1차 공급망에 사실상 미진입**이며, 국내는 액침냉각(GST·케이엔솔·SK엔무브) 위주다.

**우리 회사 기회 (CNC 밀링/5축·선반 + ISO9001·IATF16949 보유 중소 가공사 가정).**
- **진입 표면은 "완제품"이 아니라 "콜드플레이트/매니폴드/버스바/백플레이트의 CNC 가공 공정"이다.** 완제품은 진공브레이징·헬륨 누설검사가 필요하나, 그 전 단계인 **채널 바디·유로 절삭은 우리 보유 설비만으로 즉시 가능**하다.
- **단기 1순위 = 콜드플레이트·매니폴드 CNC 바디 가공.** 신규 설비 투자 0, IATF16949 + PPAP로 Tier-2 부품사(AVC/Auras/Cooler Master/Boyd)의 **Tier-3 가공 협력사**로 진입.
- **IATF16949 보유가 결정적 자산.** 대만 ODM·Tier-2는 자동차 고객 영향으로 IATF16949+APQP+PPAP 규율을 협력사에 적용하므로, 우리의 자동차 품질체계는 벤더등록 **품질시스템 사전심사에서 강점이며 통과 가능성을 높인다**(실제 등록은 SAQ·샘플·PPAP 결과에 달림).
- **진입 타이밍이 중요.** NVIDIA는 차세대 Rubin(2H2026)부터 콜드플레이트 조달을 중앙집중화하고 공급사를 소수로 지명하는 중 — **2026~2027년이 신규 진입창**이다.
- **최대 리스크 = 중국·대만 가공사와의 가격경쟁.** 단순 형상(버스바)·범용 바디로 경쟁하면 단가에서 밀린다. **완화 핵심은 IATF16949 추적성을 무기로 무결점·소량·고난이도 콜드플레이트 가공이라는 가격경쟁이 약한 틈새에 집중**하는 것이다.

**권고.** 무투자로 ① 콜드플레이트/매니폴드 CNC 바디 협력 진입(0~12개월) → ② 품목·고객 확대(1~2년) → ③ 진공브레이징로+He 누설검사 투자(완제품 수직상승, 추가 capex ≈ US$0.2M~0.5M)로 2~3년 내 완제품화하는 3단계 로드맵을 채택한다. CNC 바디 가공의 현실적 획득가능시장(SOM)은 **기본 시나리오 연 약 10억 원(보수 3.5억~낙관 31억, 추정)**으로, 중소사가 5축 2~3대 라인으로 감당 가능한 규모다(§4.6~4.7). 경쟁 측면에서 **일본은 소재·광배선 강자(직접 경쟁 약함, 잠재 조달처), 중국은 수출규제로 글로벌 GB200 인증서 구조적 배제(가격 벤치마크로만 압박)**라 대만·미국 Tier-2가 핵심 표적 고객이다(§3.6).

---

## ② 가공품·가공기 총람

### 2.1 물량 추정의 기준 수치 (Anchor)

| 항목 | 값 | 구분 | 출처 |
|---|---|---|---|
| 2024 AI 서버 출하량 | 167만 대(+41.5% YoY), $187B, 서버시장의 65% | 확정 | TrendForce 2024-07-17 |
| 2026 AI 서버 성장 | +28% YoY, GPU형 69.7% / ASIC형 27.8% | 전망 | TrendForce 2026-01-20 |
| 액냉 침투율 | 2024 **14%** → 2025 **33%** → 2026 약 **47%** | 전망(원문 확정) | TrendForce 2025-08-21(14%→33% 직접 확인), TrendForce 2025-11-27(2026 47%) |
| GB200 NVL72 랙 1대 구성 | GPU 72개 / Superchip 모듈 36개 / 120kW / 냉각수 200L | 확정 | Introl |
| 2025 NVL72 캐비닛 출하 | 24K~35K대 (전망 하향 조정) | 전망 | Tom's Hardware (WT·JPM 인용) |
| 콜드플레이트 단가 | ≈ US$400/개 (GB200/GB300 기준) | 추정(IB) | Tom's Hardware / Morgan Stanley |
| NVL72 랙당 액냉 BOM | ≈ US$49,860 (GB300/Blackwell Ultra 기준) | 추정(IB) | Tom's Hardware / Morgan Stanley |

> 콜드플레이트 물량 환산(추정). NVL72 랙 기준 = 모듈 36개 × 캐비닛 30K대 ≈ **108만 개/2025년**(×$400 ≈ $432M). 다이 단위(GPU 72 + CPU 36)로 세면 ≈ 324만 개(≈$1.3B). "Blackwell GPU 전수 5.2M개"는 공랭 HGX·비NVL72를 포함한 **상한**으로, GB200 콜드플레이트 모집단과 다르다(§3.4).

### 2.2 가공품 8종 총람표

| # | 가공품 | 주 가공기 | 소재 | 요구 정밀도/공차 | 추정 물량 규모 | 가공난이도 |
|---|---|---|---|---|---|---|
| 1 | **방열판/히트싱크(공랭)** | 압출 + CNC 후가공 / 스카이빙 / 프레스·브레이징 | AL6063(압출)·구리(C1100) | 일반 ±0.1mm, 베이스 평탄도 ≤0.002 in/in, Ra 관리 | 공랭 잔존 서버 대량(저단가) | 중 |
| 2 | **베이퍼챔버** | 스탬핑(쉘) + 소결(윅) + 확산접합/용접 + 스카이빙(핀) | 구리(동판·동분말) | 박판 성형·기밀 용접면, 모세관 균일성 | 고급 GPU·칩당 1개 | 중상 |
| 3 | **콜드플레이트/수냉 (핵심)** | CNC 밀링/라우팅 + 스카이빙 + 진공브레이징 + FSW | 구리(T2, 391 W/mK)·AL6061·Cu-W | 접촉면 평탄도 ≤0.05mm, Ra ≤0.8μm, 6 bar 내압, He 누설검사 | GPU당 1개 → 2025 약 108만~324만 개 | **상** |
| 4 | **GPU 브라켓·백플레이트·스티프너** | 프레스/스탬핑 + CNC 밀링 + 다이캐스팅 | SUS·알루미늄 | 브라켓 ±0.10mm, CNC 백플레이트 ±0.0005 in | GPU 카드당 1개(연 수백만) | 중 |
| 5 | **서버 섀시·랙 레일·슬레드** | 레이저절단 + 벤딩 + 스탬핑 + 롤포밍 + 용접 | 냉연강판(CRS)·SUS·알루미늄 판재 | 판금 일반공차, 슬라이드 레일 랙깊이 정렬 ±0.005 in | 서버 1대당 1세트(대량) | 중하 |
| 6 | **소켓·커넥터 접점·busbar 접점** | 프로그레시브 프레스/스탬핑 + 일부 CNC | 베릴륨동·인청동·황동(도금) | 버 최소화, 단면 정밀, 압입 공차 | 칩/포트당 수백~수천 핀(초대량) | 중 |
| 7 | **반도체 장비용 정밀부품(척·스테이지·진공/EFEM)** | CNC 정밀밀링 + 와이어 EDM + 연삭/폴리싱 | Al₂O₃·AlN·SiC 세라믹 + 알루미늄·SUS(316L/17-4PH)·Ti·인바 | 평탄도 <1μm/300mm, Ra <0.1μm, 홀위치 ±2μm, UHV 무아웃가싱 | (미확인 — WFE capex 연동, GPU 출하 무관) | **최상** |
| 8 | **케이블 트레이·버스바(전력)** | CNC 멀티축(드릴·밀링·프로파일) + 스탬핑 + 롤포밍 | 구리(연동)·알루미늄·강판 | 접촉점·체결홀 타이트 공차 | 랙당 다수(고전류화로 구리 중량 급증) | 중 |

### 2.3 품목별 핵심 해설

- **콜드플레이트(핵심).** 고열밀도(GB200 모듈 ~2.7kW)로 direct-to-chip이 표준화되며 AI 서버 정밀가공의 최대 고부가 품목이 되었다. 마이크로채널 CNC 가공 + 진공 브레이징 + 헬륨 누설검사가 결합된 고난이도 부품으로, 접촉면 평탄도·내압·누설이 신뢰성의 생명이다.
- **베이퍼챔버.** 절삭보다 스탬핑·소결·진공충진·확산접합 비중이 높아 절삭가공사에는 적합도가 낮다.
- **반도체 장비 정밀부품(최상 난이도).** ㎛급 평탄도·위치공차와 플라즈마/UHV/극온 내성을 요구해 CNC+EDM+연삭+폴리싱 다공정이 필요하다. 단, 물량 분모가 GPU 출하가 아닌 반도체 전공정 장비(WFE) capex라 별도 시장이다.
- **소켓·커넥터.** 고속 프로그레시브 스탬핑이 주력이며 핀 수가 칩당 수천 개라 총 물량은 최대급이지만, 절삭가공사의 진입 표면은 작다.

---

## ③ 국가별·기업별 시장 현황과 매출 규모

### 3.1 시장 규모

| 시장 | 규모/전망 | CAGR | 발행처 | 출처 |
|---|---|---|---|---|
| AI 서버(전체) | 2024 US$142.88B → 2030 US$837.83B | 34.3% (2024–2030) | MarketsandMarkets | M&M AI Server |
| 데이터센터 액체냉각(전체) | 2025 US$6.65B → 2033 US$29.46B | 20.1% (2026–2033) | Grand View Research | GVR |
| 데이터센터 액체냉각(전체) | 2026 US$4.07B → 2033 US$27.65B | 31.5% (2026–2033) | MarketsandMarkets | M&M DC Liquid Cooling |
| AI DC 액체냉각 | 2025–2030 +US$2.48B | 31.7% (2025–2030) | Technavio | Technavio |

> 리서치사별 액체냉각 시장규모 편차가 큰 것은 기준연도·범위·방법론 차이 때문이다. 동일선상 비교를 지양하고 발행처·기준연도를 함께 본다.
> **AI 서버 시장 규모 주석.** 2024년 AI 서버 시장을 MarketsandMarkets는 US$142.88B, TrendForce는 US$187B로 제시한다. 두 값은 모순이 아니라 **리서치사별 정의·범위 차이**(서버 본체만 vs 가속기·스토리지·네트워킹 포함 여부, AI 서버 분류 기준)에서 비롯된다. 본 보고서는 성장률·구조 분석에는 M&M(CAGR 34.3%)을, 출하량·물량 환산에는 TrendForce(167만 대·$187B)를 사용하며 혼용하지 않는다.

### 3.2 국가별 주요 기업 (매출·AI서버 비중·티어)

| 기업 | 국가 | 주력 품목 | 2024 매출 | AI서버 비중 | 공급망 티어 | 구분/출처 |
|---|---|---|---|---|---|---|
| **AVC**(3017) | 대만 | 방열판·히트파이프·베이퍼챔버·콜드플레이트·매니폴드·냉각모듈 | NT$71.8B(≈US$2.0B), +21.2%, 순이익 +54% | 세그먼트 비공개(미확인) | Tier-2 (콜드플레이트·매니폴드 NVIDIA 인증) | 확정/Taiwan News |
| **Auras**(3324) | 대만 | 방열판·히트파이프·베이퍼챔버·콜드플레이트·액냉모듈 | NT$15.78B, +24%, 순이익 +54% | 액냉 2024 약 **12%** → 2025 40%+ 목표 / 서버비중 2024 41%→2025 51% 전망 | Tier-2/3 | 확정+전망/Quartr·DigiTimes |
| **Cooler Master** | 대만(비상장) | 액냉 시스템·콜드플레이트 | 비공개(미확인) | GB200 1차 랙 액냉 **50%+**(보도) | Tier-1/2 (GB200·GB300 선도) | 보도(점유)/CommonWealth |
| **Delta**(2308) | 대만 | 전원·사이드카 CDU(최대 1.5MW)·팬 | NT$421.1B(≈US$13B), +5% | 쿨링 2026 매출 약 10% 전망 | Tier-1/2 (사이드카 CDU 선도) | 확정+전망/Delta IR·CommonWealth |
| **Vertiv**(VRT) | 미국 | in-row CDU·열관리·랙·전원 | US$8,011.8M, 2025 가이던스 $9.1~9.3B | 액냉 세그먼트 비공개(미확인) | Tier-1 (열관리 시스템) | 확정/SEC 8-K |
| **Boyd** | 미국(비상장) | 콜드플레이트·in-row CDU | 비공개(미확인) | 미확인 | Tier-1/2 (GB200 RVL 검증) | 확정(RVL)/Boyd |
| **CoolIT** | 캐나다(비상장) | CDU·콜드플레이트 | 비공개(미확인) | 미확인 | Tier-1/2 (NVIDIA 코이노베이션) | 확정/CoolIT |
| **Furukawa·Fujikura** | 일본 | 베이퍼챔버·히트파이프(최대 100W) | 미확인 | 미확인 | Tier-3 (소재/열부품) | 확정(품목)/각사 |
| **Foxconn/FII** | 대만/중국 | GB200 랙 시스템 조립 ODM | 그룹 전체 별도(미확인) | GB200 랙 점유 약 **40%**(보도) | Tier-1 직납 ODM | 보도(점유)/TweakTown |
| **Quanta** | 대만 | GB200 랙 ODM | 미확인 | GB200 랙 점유 약 **30%**(보도) | Tier-1 직납 ODM | 보도(점유)/TweakTown |
| **Wiwynn·Wistron·Inventec** | 대만 | NVL72/NVL36 랙 ODM | 미확인 | NVL36 분담 | Tier-1 직납 ODM | 확정(역할)/Wiwynn |
| **Amphenol·TE Connectivity** | 미국 | 고속 커넥터·수냉 버스바(750kW) | 미확인 | 미확인 | Tier-2 커넥터 | 확정(품목) |
| **CPC·Parker·Danfoss·Staubli** | 미국·유럽 | 퀵디스커넥트(QD) 커넥터 | 미확인 | 미확인 | Tier-2 (GB200 인증 선점) | 확정(역할)/TrendForce |
| **Envicool·Nidec·Shenzhen Cotran** | 중국 | CDU·Cu-Al 하이브리드 콜드플레이트 | 미확인 | 미확인(대중 규제 영향) | Tier-1/2(내수)·Tier-3(가공) | 확정(역할)/Valuates |

> 환산 주의. AVC US$ 환산은 기사 본문 표기(≈US$2.0B) 기준, Delta US$ 환산(~US$13B)은 개략치다. "순이익 +54%"는 AVC·Auras가 우연히 일치(2024 AI 호황 공통)하며 순이익 증가율(EPS 증가율 아님)이다.

### 3.3 NVIDIA/AMD 공급망 티어 구조

```
NVIDIA (GPU/플랫폼) ── 레퍼런스 설계, 부품 인증(RVL: Recommended Vendor List)
        │
[Tier-1 직납 ODM / 시스템·랙 모듈]
   Foxconn/FII(~40%), Quanta(~30%), Wiwynn, Wistron, Inventec   → GB200 NVL72/36 랙·시스템 조립
   Vertiv, Delta, Boyd, CoolIT, Cooler Master                   → CDU / 액냉 시스템 모듈
        │
[Tier-2 부품/모듈]
   콜드플레이트·매니폴드 : Cooler Master(GB200 1차 50%+), AVC, Boyd, Auras
   CDU                  : Delta(사이드카 선도), Vertiv·Boyd(in-row), CoolIT, Asetek
   QD 커넥터            : CPC, Parker Hannifin, Danfoss, Staubli
        │
[Tier-3 소재/가공]  ← ★ 우리 회사의 현실적 진입점
   베이퍼챔버·히트파이프 소재 : Furukawa, Fujikura
   Cu-Al 하이브리드 콜드플레이트 가공 : Shenzhen Cotran 등(2024 물량 ~35% 점유), AVC·Auras 일부 내재화
```

핵심 사실.
- GB200 NVL72는 **액체냉각이 필수 아키텍처**다. NVL72당 CDU 용량 150~200kW.
- 랙 1대(BOM ≈ US$3M)에서 액냉 부품 가치는 GPU·CPU 모듈 다음으로 높은 단일 부품 비중이다(Morgan Stanley/IntuitionLabs).
- **AMD MI300/MI350은 별도 콜드플레이트 벤더군**(Motivair, Jetcool, Alloy Enterprises)이 두드러진다. NVIDIA 외 제2 진영으로, 단일고객 의존 완화에 활용 가능하다.
- **NVIDIA는 차세대 Rubin(2H2026)부터 콜드플레이트 조달을 중앙집중화하고 공급사를 소수(공개분에서 AVC 등 4곳)로 지명**하는 중이다 → 신규 진입창이 좁아지기 전 선진입이 중요하다.

### 3.4 교차검증 — 적발된 모순과 채택 근거

본 보고서가 신뢰성을 위해 수행한 핵심 검증이다(agy 물량 × codex 매출 정합성).

1. **콜드플레이트 시장 "$293.84M(2024)" → 과소계상으로 기각.** 세 경로로 입증 — (a) **내부 정합성**: AVC 단독 총매출 ≈US$2.0B 중 콜드플레이트/액냉이 15~20%만 차지해도 ~$300~400M으로, 단일 중견사가 "전 세계 시장 전체"를 채우거나 초과하므로 비현실적. (b) **단가×물량**: 2025 NVL72 한정 콜드플레이트만 모듈 기준 ≈$432M, 다이 기준 ≈$1.3B. (c) **BOM 경로**: 랙당 액냉 $49,860 × 30K랙 ≈ $1.5B(2025, NVL72만), 콜드플레이트는 그 30~40%면 $0.45~0.6B. → 세 경로 모두 $293.84M을 크게 상회하므로 **전체 콜드플레이트 가공 시장 대용치로 사용하지 않음.**
2. **"Blackwell GPU 5.2M개(2025)" → 모집단 차이로 교체.** 이는 공랭 HGX·비NVL72를 포함한 전수로, GB200 콜드플레이트 모집단(NVL72 한정 ≈108만 개)과 다르다. 콜드플레이트 환산에는 NVL72 랙 기준을 채택했다.
3. **신뢰 위계 적용 결과** — 1차/공시(AVC 실적, Vertiv SEC 8-K) > 리서치사/IB(Morgan Stanley 단가, TrendForce 침투율) > 블로그/snippet(기각·보정 대상).

방향성에서 agy 물량과 codex 매출은 **모순 없음**(액냉·콜드플레이트 급성장, 대만 3사 수혜). 단가·물량 환산($432M~$1.3B/2025 콜드플레이트)이 기업 매출 규모와 같은 자릿수로 정합한다.

### 3.5 한국 기업 참여 현황

**핵심 결론 — 한국은 GB200급 글로벌 콜드플레이트/CDU 1차 공급망(대만·미국 중심)에 사실상 미진입이다.** 국내는 주로 액침냉각(immersion)과 반도체 장비 냉각 전용(轉用) 단계에 있다.

| 기업 | 현황 | 출처 |
|---|---|---|
| **GST**(083450) | 반도체 장비 냉각 기반 국내 액침냉각 1위 평가. 2025-05 LG유플러스에 단상형 액침냉각 첫 상업 납품. Vertiv·NVIDIA 밸류체인 편입 기대 단계 | thebell |
| **케이엔솔** | 글로벌 액침냉각 1위 Submer와 협력해 국내 진출(설계·구축·운영) | thebell |
| **SK엔무브** | 2022 GRC 전략투자로 국내 최초 액침냉각 진출, DC용 플루이드 개발·SKT DC 상용화(2023) | 에너지뉴스 |
| LS전선·LS일렉트릭·LG전자 | DC그리드·HVAC 참여. **열관리 정밀가공 부품(콜드플레이트/베이퍼챔버) 직접 가공 메이저는 미확인** | (테마 분류, 미확인) |

- 한국 DC 냉각 시장: 2025 US$176.67M → 2031 US$454.12M, CAGR 17.04%(소형 시장).
- **함의 — 국내 경쟁자 공백이 곧 기회다.** "콜드플레이트/베이퍼챔버 정밀가공 직납 메이저 미확인"은, IATF16949 보유 절삭사에게 "한국발 검증된 콜드플레이트 CNC 가공 파트너"라는 빈 포지션을 의미한다. 국내 AI DC 투자 본격화(2026~2027 전망)와 타이밍도 일치한다.

### 3.6 일본·중국 기업 심화

#### 일본 — 완제 콜드플레이트보다 소재·광배선 강자

| 기업 | 티커 | 주력 | 최근 매출(FY24, ~2025-03) | AI/열관리 노출 | 위치 | 출처 |
|---|---|---|---|---|---|---|
| **Furukawa Electric**(古河電工) | 5801.T | 전선·광섬유 + 베이퍼챔버·히트파이프·3D VC | 연결 **¥1,201.8B(≈US$8.0B)**, 영업익 ¥47.1B(원문 확인) | 열관리는 Electronics/Functional 세그먼트 내 소규모 라인. **세그먼트 매출 비공개(미확인)** | Tier-3 소재/열부품 | Furukawa IR |
| **Fujikura**(藤倉) | 5803.T | 광섬유·광커넥터(WTC/SWR) + 고성능 히트파이프·VC | 연결 **¥979.4B(≈US$6.5B, +22.5%)**, 순이익 ¥91.1B | AI DC 노출 본체는 열부품 아닌 **광배선**(초고밀도 광케이블). VC·히트파이프 별도 라인(미확인) | Tier-2/3 광배선+열부품 | QUICK/MarketScreener |

> 일본세는 완제 콜드플레이트/CDU보다 **소재(구리·동박·VC 시트)와 광배선** 강자다. 우리 가공사 관점에서 직접 경쟁자라기보다 향후 VC·히트파이프 소재 조달처 또는 일본 OEM의 가공 외주 가능성으로 본다.

#### 중국 — 거대 방어 내수, 수출규제로 글로벌 GB200 인증서 구조적 배제

| 기업 | 티커 | 주력 | 2024 매출 | DC/AI 비중 | 위치 | 출처 |
|---|---|---|---|---|---|---|
| **Envicool**(英维克) | 002837.SZ | DC 정밀온도제어·CDU·Coolinside 액냉 | 45.89억元(+30%, ≈US$6.4억) | 기房온도제어 24.41억元(53%), Coolinside 누적 1.2GW(검색요약 기준) | 중국 액냉 1위권, 내수 중심 | sina/futunn |
| **Yinlun**(银轮股份) | 002126.SZ | 자동차 열관리 + DC 액냉/콜드플레이트(제3곡선) | **127.02억元(+15.28%, ≈US$17.6억)**(원문 확인) | 디지털·에너지 10.27억元(매출 8.08%, +47.44%) | Tier-2 콜드플레이트(자동차 횡전개) | sina |
| **Feirongda**(飞荣达) | 300602.SZ | EMI 차폐·열관리(TIM·VC·히트파이프·콜드플레이트) | 50.31억元(+15.76%, ≈US$7.0억) | AI서버 액냉 양산 진입, 세부비중 비공개(미확인) | Tier-2/3 (화웨이 방열 공급) | cnstock/cninfo |
| **中石科技**(Sinomags) | 300684.SZ | 열관리 소재(TIM·그라파이트·VC·히트파이프) | 15.66억元(≈US$2.2억) | AI단말·AI DC 신성장축, 세부 비공개(미확인) | Tier-3 소재 | 163/eastmoney |
| **高澜股份** | 300499.SZ | 순수수 냉각·DC 액냉(콜드플레이트/Manifold/CDU) | 6.91억元(+20.58%, ≈US$0.96억), 귀모순이익 적자 | 액냉 선행이나 규모 작고 적자, 비중 비공개(미확인) | Tier-2 액냉 | sina/cninfo |

> **단위 주의.** 중국 매출은 億元(=1억 RMB) 단위다. 예: Yinlun 127.02억元 ≈ RMB 12.7B ≈ US$17.6억("127 billion"이 아님). 영문 검색요약의 "billion yuan" 오역에 주의. USD 환산은 7.2 RMB/USD 개략치.

> **수출규제 함의.** 2025-04 美 H20(중국전용 칩) 수출 라이선스 의무화 → NVIDIA FY26 1Q 약 US$45억 충당금, 中 당국 국산 대체 지시. 중국 액냉사의 AI DC 수요는 NVIDIA GB200급이 아니라 **국산 가속기(화웨이 Ascend 등)·ESS·전력**에 묶여, 글로벌 GB200 NVL72 메인 콜드플레이트 인증 경쟁에서 구조적으로 배제되는 경향이다. 반대로 "东数西算"·국산화 정책이 방어된 거대 내수를 보장한다. → **우리 가공사 함의**: 글로벌(대만·미국) 공급망에서 중국은 직접 경쟁자가 아니나 가격 벤치마크로 압박한다. 중국 내수 시장은 현지화·정책 장벽이 높아 현실적 표적이 아니다.

---

## ④ 우리 회사 진입 기회와 실행 로드맵

> **회사 프로필(전제).** 보유 설비 = CNC 밀링/5축, CNC 선반/복합기(절삭 중심). 미보유(가정) = 압출·다이캐스팅·대형 프레스/스탬핑·스카이빙 전용설비·롤포밍·진공브레이징·소결. 주력 소재 = 알루미늄·구리/동합금·SUS/스틸·티타늄/특수합금·플라스틱. 인증 = ISO 9001 + **IATF 16949**. 규모 = **중소기업(직원 30~100명, 연매출 50~300억) 가정**(미응답에 따른 가정).

### 4.1 핵심 전략 통찰 — "완제품"이 아니라 "공정"으로 진입한다

8개 완제품 단위로 보면 콜드플레이트조차 진공브레이징·헬륨 누설검사가 필요해 단기 진입이 불가능하다. 그러나 **공정 단계로 분해하면** 콜드플레이트/매니폴드의 **CNC 가공 공정(마이크로채널 바디·유로 절삭, 브레이징 전 단계까지)은 우리 보유 설비만으로 즉시 가능**하다. 이 "가공 공정 분리"가 현실적 진입점이다. 또한 **IATF16949의 추적성·PPAP·무결점 체계는 누설·내압·접촉면 무결점이 생명인 콜드플레이트 가공에서 직접 가치로 환산**된다(일반 절삭사 대비 차별점).

### 4.2 진입 난이도별 가공품 분류

**단기 진입 가능 (신규 설비 0, 기존 CNC + IATF16949로 즉시 대응)**

| 우리가 맡는 공정 단위 | 역량 매칭 | 근거 |
|---|---|---|
| **콜드플레이트·매니폴드 CNC 바디 가공** (채널 바디 밀링/라우팅, 매니폴드 5축 유로 절삭 — 브레이징 전 단계까지) | 구리(T2)·AL6061 절삭 + 5축. 평탄도 ≤0.05mm·Ra ≤0.8μm는 정밀밀링 영역 | **단기 1순위.** 시장 핵심·고성장. Tier-2에 CNC 바디만 납품, 브레이징·누설검사·조립은 고객 수행. *스코프 가드: CNC 밀링/라우팅 가능한 채널에 한정. 초미세·고세장비 핀은 스카이빙(미보유) 영역이라 중기로 분류* |
| **고전류 리지드 버스바** (CNC 드릴·밀링·프로파일) | 구리 멀티축 절삭 | 단기 2순위. 고전류화로 수요↑. 단 형상 단순 → 가격경쟁 노출 큼 |
| **GPU 백플레이트·스티프너 CNC 가공분** | 알루미늄 절삭, CNC 시 ±0.0005 in | 순수 CNC 백플레이트(소량·고강성)에 한정. 대량 다이캐스팅품은 미스매치 |
| **반도체 장비 정밀부품 중 절삭+EDM 비중 부품** (스테이지·플레이트·진공/EFEM 메탈) | CNC 5축 + SUS/Ti/인바 다소재 | 단기~중기 경계. 세라믹 ESC 본체는 부적합 |

**중기 설비투자 필요 (1~3년)**

| 품목 | 추가 필요 | 근거 |
|---|---|---|
| **콜드플레이트 완제품(밀폐·검증)** | 진공브레이징로 + 헬륨 누설검사기 + 특수공정 인증 | CNC 바디 → 완제품으로 **수직상승**. 단가 ≈$400/개, 부가가치 최대 |
| **반도체 장비 정밀부품 풀세트** | 와이어 EDM·정밀연삭·폴리싱·㎛급 CMM | ㎛급 평탄도 요구. 물량은 WFE capex 연동 |
| 소켓/커넥터 CNC 보완 가공 | (스탬핑 본체 외주) | 본체는 프로그레시브 스탬핑이 주력 → 진입 매력 낮음 |

**장기·부적합 (설비 본질이 다름 — 비권장):** 압출 핀 히트싱크(압출설비), 베이퍼챔버(소결·확산접합), 스카이빙 핀 히트싱크(전용설비), 서버 섀시·레일(판금·롤포밍), 커넥터 접점 본체(프로그레시브 스탬핑), ESC 세라믹 본체(세라믹 소결).

### 4.3 필요 설비·인증 및 벤더등록 절차

| 진입 후보 | 추가 설비 | 추가 인증/절차 |
|---|---|---|
| 콜드플레이트 CNC 바디(단기) | **없음**(기존 5축·밀링) | IATF16949/ISO9001로 충분. 고객 PPAP·초도품 승인(ISIR) |
| 콜드플레이트 완제품(중기) | **진공브레이징로**, **헬륨 누설검사기**, 미세채널 가공능력 | **NADCAP 브레이징** 검토 — 단 NADCAP은 AS9100(또는 동등) **선(先)인증** 전제. 데이터센터향이면 고객 자체 특수공정 승인으로 대체 가능성(고객 요구 확인 필요) |
| 반도체 장비 정밀부품(중기) | 와이어 EDM·정밀연삭·㎛급 CMM·클린룸/세정 | 장비 OEM 벤더승인, UHV 무아웃가싱 검증, 청정도 등급 |
| 버스바(단기) | 없음 | IATF16949. 접촉저항·도금 사양 관리 |

> 헬륨 누설검사기·진공브레이징로가 콜드플레이트 **완제품** 경로의 결정적 게이트다. 단기 경로(CNC 바디 납품)는 이 둘이 **불필요**하므로 무투자 진입이 성립한다 — 이것이 단기/중기를 가르는 실선이다.

**공급망 벤더등록 절차(신규 조사).**
- NVIDIA는 열솔루션을 **RVL(Recommended Vendor List)** 체계로 관리하며(Boyd·Eaton이 GB200 NVL72 RVL 검증 획득), GB200 모듈 1200W 방열·냉각수 입구 30~45°C·열저항 ≤0.03°C/W 등 정량 사양을 전제한다. **RVL은 Tier-1/2 모듈·시스템 공급사 대상이며, Tier-3 가공사는 NVIDIA 직접 등재가 아니라 RVL 등재사(AVC/Boyd/Auras)의 협력사로 편입되는 경로**다.
- **대만 ODM(Foxconn·Quanta·Wiwynn)은 자동차 고객 영향으로 EMS 공급사에 IATF16949+APQP+PPAP 규율을 적용**한다 → **우리의 IATF16949 보유는 벤더등록 품질시스템 사전심사에서 강점이며 통과 가능성을 높인다**. 단 실제 등록은 SAQ·샘플·PPAP 결과에 달려 있으므로 인증 보유가 곧 등록 보장은 아니다.
- 표준 절차: NDA → 공급사 설문(SAQ)·품질시스템 심사(IATF 인증서 제출) → 견적·샘플 → **PPAP/초도품(ISIR) 승인** → 소량 양산 후 물량 확대. 우리는 PPAP 단계가 강점이다.

### 4.4 실행 로드맵 (티어 구조상 현실적 진입점)

```
[0단계 — 현재] IATF16949 보유 절삭사. 콜드플레이트 BOM·도면 이해 확보.
        │
[1단계 — 진입(0~12개월)] Tier-2 부품사(AVC/Auras/Cooler Master/Boyd)의
        콜드플레이트/매니폴드 "CNC 바디 가공" 협력사로 등록.
        브레이징·누설검사·조립은 고객(Tier-2)이 수행, 우리는 절삭만.
        → 무투자. IATF16949 + PPAP로 벤더등록 사전심사 통과 가능성↑. 소량 시작.
        ▷ 검증: 초도품 승인(ISIR)·PPAP 통과, 반복 발주 확보
        │
[2단계 — 확대(1~2년)] 동일 고객에 매니폴드·백플레이트·버스바로 품목 확대 +
        2nd Tier-2 고객 추가(단일고객 의존 완화) + 한국 內 Tier-1 ODM 직접 가공 병행.
        ▷ 검증: 고객 2곳 이상, 품목 3종 이상
        │
[3단계 — 수직상승(2~3년)] 진공브레이징로 + He 누설검사기 투자 →
        콜드플레이트 "완제품(밀폐·검증)" 공급으로 부가가치 상승(단가 ≈$400/개).
        선택적으로 NADCAP/AS9100 또는 고객 특수공정 승인 확보.
        ▷ 검증: 완제품 단가 수주, RVL 등재사 협력사 지위
```

**진입 타이밍.** NVIDIA Rubin(2H2026)부터 콜드플레이트 조달 중앙집중·공급사 소수 지명으로 진입창이 좁아진다 → **2026~2027년 Tier-2 가공 협력사 선진입**이 관건이다.

### 4.5 리스크 및 완화방안

| 리스크 | 내용·근거 | 완화방안 |
|---|---|---|
| **중국·대만 가격경쟁 (최대 리스크)** | Tier-3 가공은 Shenzhen Cotran 등과 단가 경쟁(Cu-Al 하이브리드 ~35% 점유). 단순 형상일수록 노출 큼 | 가격이 아닌 **IATF16949 추적성·무결점·소량 정밀**으로 차별화. **고난이도 콜드플레이트 마이크로채널에 집중**, 단순 버스바는 보조로만 |
| **물량 변동성** | NVL72 캐비닛 2025 전망 24K~35K로 하향 조정. 발주 급변 | 다품목·다고객 분산. AI 외 IATF 본업(자동차) 병행으로 변동 흡수 |
| **단일고객 의존** | Tier-2 1곳 시작 시 종속·협상력 약화 | 2단계에서 고객 2곳 이상. NVIDIA+AMD(Motivair/Jetcool) 양 진영 분산 |
| **기술·인증 진입장벽** | 완제품화에 진공브레이징·He누설·(NADCAP 시 AS9100 선행) 자본·시간 | 1단계 무투자 진입으로 현금흐름·레퍼런스 확보 후 단계적 투자. AS9100은 고객 특수공정 승인으로 대체 검토 |
| **공급사 고착·진입창 축소** | Rubin부터 조달 중앙집중·공급사 4곳 지명 | **2026~2027 진입 타이밍 확보.** RVL 등재 Tier-2의 협력사로 우회 편입 |
| **환율** | 콜드플레이트 단가 USD 표시, 원/달러 변동이 마진 직타 | USD 결제 비중 관리·단순 선물환 헤지 |

### 4.6 중기 설비투자 Capex (완제품 수직상승 시)

콜드플레이트를 절삭 바디가 아닌 **완제품(브레이징·누설검사 포함)**으로 공급하려면 기존 CNC에 더해 아래 설비·인증이 필요하다. 단가는 단일가 단정 대신 **범위**로 제시한다(확정/추정/통념 라벨).

| 항목 | 가격대(USD) | 라벨 | 비고 |
|---|---|---|---|
| 진공브레이징로(소형·시작품) | $20K~$80K | 통념/추정 | 진공로 시장가 $4K~$300K로 광범위, 시작품용은 하단 |
| 진공브레이징로(중형·양산, Al cold plate급) | $150K~$300K+ | 통념/추정 | hot zone·진공도·온도균일도·NADCAP 대응이 가격 주도. 단일 최대 항목 |
| 헬륨 누설검사기(질량분석형) | 신품 $30K~$80K / 중고 $1K~$5K | 추정/확정 | Inficon UL3000·Pfeiffer ASM 등 |
| CMM(㎛급 브리지형) | $65K~$130K / 고정밀 $150K+ | 확정(범위) | 연 교정·유지비 별도 |
| 5축 CNC(증설 시·참고) | 엔트리 $80K~$150K / 정밀 $200K~$500K | 확정(범위) | 기보유 가정, 증설 시만 |
| 마이크로채널 미세 툴링(소모성) | 개당 $20~$150+ | 통념/추정 | 월 수백~수천 달러 누적 운영비 |
| **AS9100 인증** | 총 $10K~$50K | 확정(범위) | **ISO9001 보유 → 약 4개월로 단축** |
| **NADCAP 브레이징** | 총 $10K~$30K+ (심사 $4.85K~$7.15K + 연유지 $3K~$5K) | 확정(범위) | **AS9100(또는 동등 QMS) 선행 필수**, 약 1년 준비 |

**완제품 진입 설비 Capex 총액(추정).** 신규 추가분 합산.

| 시나리오 | 합계(추정) |
|---|---|
| 최소(시작품·소형로) | ≈ **US$200K** (약 2.7억 원) |
| 본격(중형 양산로) | ≈ **US$490K** (약 6.6억 원) |
| 고사양(대형로+고정밀 CMM+5축 1대 증설) | ≈ **US$990K** (약 13.4억 원) |

> 진공브레이징로가 단일 최대 항목. 인증은 ISO9001 보유로 AS9100 단축이 가능해 비용 비중이 상대적으로 작다. **단기 경로(CNC 바디 납품)는 이 capex가 전부 불필요**하므로 무투자 진입이 성립한다.

### 4.7 획득가능시장(SOM) 산정 — TAM → SAM → SOM

> **본 SOM은 검증된 anchor의 산수 + 명시 가정에 기반한 추정**이다. 단일 숫자 단정이 아니며 가정에 따라 크게 변한다.

```
TAM = 2025 GB200 NVL72 콜드플레이트 완제품 시장 (검증 anchor)
      모듈 기준 ≈ $432M (=108만 개 × $400)  ← 기본 채택
      다이 기준 ≈ $1.3B (=324만 개 × $400)  ← 상한(민감도)
      ※ GB200 NVL72 단년 한정 → 실제 전체 액냉 TAM은 더 큼(본 SOM은 보수적 대용치)
  ▼ × 가공임 비중(완제품가 중 CNC 절삭) — 기본 30% 가정
SAM = 전 세계 'CNC 바디 절삭' 빌러블 시장 ≈ $432M × 30% ≈ $130M (모듈 기준)
  ▼ × 신규진입 중소사 현실적 점유율 %(시나리오 변수)
SOM = 1~3년 내 현실적 획득 매출
```

구조 가정(TAM=모듈, 가공임=30%)은 **고정**하고 3시나리오는 **점유율 %만** 차등한다(모든 극단 동시 곱셈으로 인한 시나리오 폭주 방지).

| 시나리오 | 점유율 | 근거 | **SOM(연, 추정)** |
|---|---|---|---|
| **보수** | 0.2% | 한국발 Tier-3 신규진입, 대만 3사·Boyd·중국 장악 구도, 트라이얼 물량만 | ≈ **US$0.26M (약 3.5억 원)** |
| **기본** | 0.6% | 1~2개 2차 협력사 QVL 진입, 일부 품번 안정 공급 | ≈ **US$0.78M (약 10억 원)** |
| **낙관** | 1.8% | 복수 품번 + 침투율 33%→47%·AI서버 CAGR 34.3% 상방 흡수 | ≈ **US$2.3M (약 31억 원)** |

> 환율 ₩1,350/$ 가정. 점유율 %는 검색값이 아니라 경쟁구도 기반 판단값이다.

**Capacity 교차검증(현실성).** 5축 1대 ≈ 연 3,000개(사이클 2hr/개, 가동 6,000hr) × 가공단가 $120/개($400×30%) ≈ 대당 연 매출 상한 ≈ $360K. → 기본 SOM $0.78M ≈ 5축 **2~3대** 풀가동, 낙관 $2.3M ≈ 6~7대. 기본 시나리오는 중소사가 라인 증설로 감당 가능한 "현실적" 수준과 정합한다.

**민감도.** ① **점유율 %가 지배적** — 0.2% vs 1.8%로 9배 차이(QVL 진입·품번 수에 좌우). ② TAM basis(모듈→다이 시 ×3)·가공임 비중(20~40% 시 ±33%)을 동시 낙관 시 SOM이 추가로 ~4배 부풀 수 있어, 본 표는 의도적으로 모듈·30% 기본값에 고정했다.

---

## ⑤ 출처 목록

### 시장·물량 (확정/리서치사)
- TrendForce 2024-07-17 — AI 서버 2024 167만 대(+41.5%), $187B, 서버시장 65% — https://www.trendforce.com/presscenter/news/20240717-12227.html
- TrendForce 2025-07-24 — Blackwell GPU 80%+, 액냉 표준화 — https://www.trendforce.com/presscenter/news/20250724-12653.html
- TrendForce 2026-01-20 — 2026 AI 서버 +28%, GPU형 69.7%/ASIC 27.8% — https://www.trendforce.com/presscenter/news/20260120-12887.html
- TrendForce 2025-08-21 — **액냉 침투율 14%→33%(원문 직접 확인)**, 콜드플레이트/CDU/QD 공급사 — https://www.trendforce.com/presscenter/news/20250821-12682.html
- TrendForce 2025-11-27 — **2026 AI 서버 +20%↑, 액냉 침투율 47% 전망** — https://www.trendforce.com/presscenter/news/20251127-12805.html
- TrendForce via BusinessWire 2024-09-23 — 2025 침투율 20%+ 전망 — https://www.businesswire.com/news/home/20240923760832/en/NVIDIA-Blackwell-Platform-and-ASIC-Chip-Upgrades-to-Boost-Liquid-Cooling-Penetration-to-Over-20-in-2025-Says-TrendForce
- Introl — GB200 NVL72 구성(GPU 72/모듈 36/120kW/200L) — https://introl.com/blog/gb200-nvl72-deployment-72-gpu-liquid-cooled
- Tom's Hardware — NVL72 캐비닛 24K~35K 전망 하향 — https://www.tomshardware.com/tech-industry/artificial-intelligence/analysts-halve-nvidia-gb200-blackwell-shipment-forecasts-for-2025-prediction-contrasts-ai-boom
- Tom's Hardware / Morgan Stanley — 콜드플레이트 단가 ≈$400, NVL72 랙 액냉 BOM ≈$49,860 — https://www.tomshardware.com/pc-components/cooling/cooling-system-for-a-single-nvidia-blackwell-ultra-nvl72-rack-costs-a-staggering-usd50-000-set-to-increase-to-usd56-000-with-next-generation-nvl144-racks
- IntuitionLabs — GB200 공급망/BOM(액냉 부품 가치) — https://intuitionlabs.ai/articles/nvidia-gb200-supply-chain
- MarketsandMarkets — AI 서버 시장 2024 $142.88B→2030 $837.83B(34.3%) — https://www.marketsandmarkets.com/Market-Reports/ai-server-market-141336410.html
- MarketsandMarkets — DC 액체냉각 2026 $4.07B→2033 $27.65B(31.5%) — https://www.marketsandmarkets.com/Market-Reports/data-center-liquid-cooling-market-84374345.html
- Grand View Research — DC 액체냉각 2025 $6.65B→2033 $29.46B(20.1%) — https://www.grandviewresearch.com/industry-analysis/data-center-liquid-cooling-market-report
- Technavio — AI DC 액냉 31.7% — https://www.technavio.com/report/liquid-cooling-for-ai-data-centers-market-industry-analysis

### 기업 (실적·공시)
- Taiwan News — AVC 2024 NT$71.8B(+21.2%) — https://www.taiwannews.com.tw/news/6058452
- Quartr — Auras 3324 Q4 2024 실적 — https://quartr.com/companies/auras-technology-co-ltd_15788
- DigiTimes — Auras 액냉 2024 12%→2025 40%+ — https://www.digitimes.com/news/a20250516PD231/auras-liquid-cooling-ai-server-revenue-2025.html
- CommonWealth — Cooler Master GB200 1차 액냉 50%+ — https://english.cw.com.tw/article/article.action?id=4145 (원문 403, 보강: GlobalSemiResearch "CM 50%+·AVC 30~40%" https://globalsemiresearch.substack.com/p/nvidia-liquid-cooling-analysis-from )
- Delta IR — 2024 실적/배당 공시 — https://www.deltaww.com/en-us/news/39602
- CommonWealth — Delta AI서버 전원/냉각 — https://english.cw.com.tw/article/article.action?id=3691
- Vertiv SEC 8-K FY2024 (2025-02-12) — US$8,011.8M — https://www.sec.gov/Archives/edgar/data/0001674101/000162828025005006/exhibit991vrt02122025.htm
- Boyd — NVIDIA GB200 협력 / NVL72 RVL 검증 — https://www.boydcorp.com/boyds-collaboration-with-nvidia.html , https://www.boydcorp.com/thermal/boyd-validated-for-nvidia-gb200-nvl72-recommended-vendor-list.html
- Eaton — GB200 NVL72 RVL 검증 — https://www.eaton.com/us/en-us/markets/data-centers/ai-machine-learning/eaton-validated-for-nvidia-gb200-nvl72-recommended-vendor-list.html
- CoolIT — NVIDIA 코이노베이션 — https://www.coolitsystems.com/capabilities/co-innovation/nvidia/
- Furukawa Thermal — https://www.furukawaelectric.com/thermal/en/furukawa/
- Fujikura Thermal — https://www.fujikura.co.jp/en/lp/thermal/ja/
- TweakTown — Foxconn 40%/Quanta 30% (GB200 랙) — https://www.tweaktown.com/news/98852/nvidias-new-gb200-ai-servers-led-by-foxconn-with-40-and-quanta-30-ships-in-q3-2024/index.html
- Wiwynn GTC 2024 — NVL72 시연 — https://www.wiwynn.com/news/wiwynn-showcases-innovations-on-nvidia-gb200-nvl72-at-gtc-2024
- Valuates — CDU 시장/중국 벤더 — https://reports.valuates.com/market-reports/QYRE-Auto-30N17857/global-data-center-cdu
- Motivair — AMD MI300 콜드플레이트 — https://www.motivaircorp.com/products/amd-instinct-MI300-cold-plate/
- Supermicro — AMD Instinct 액냉 시스템 — https://www.supermicro.com/en/accelerators/amd
- IntelMarketResearch — DLC 콜드플레이트 시장(AVC·CoolIT 점유) — https://www.intelmarketresearch.com/direct-liquid-cooling-cold-plates-for-server-2025-2032-704-6188
- DigiTimes — Rubin 액냉 표준화·콜드플레이트 조달 중앙집중·공급사 4곳 지명 — https://www.digitimes.com/news/a20260318PD231/nvidia-rubin-liquid-cooling-ai-server-launch.html

### 가공공정·사양·인증 절차
- Ecotherm — 히트싱크 공정(스카이빙 0.1mm핀, 평탄도 0.002 in/in, He 누설) — https://ecothermgroup.com/how-heat-sinks-are-made/
- ToneCooling — 콜드플레이트 T2동 391 W/mK, 평탄도 ≤0.05mm, GB200 사양(1200W·30~45°C·≤0.03°C/W) — https://tonecooling.com/nvidia-gb200-nvl72-cooling-requirements/
- Fountyl — ESC 평탄도 <1μm/300mm, EDM 냉각유로 — https://www.fountyltech.com/news/electrostatic-chuck-2/
- Gazfull — 반도체 정밀가공 소재·공차 — https://www.gazfull.com/cnc-machining-for-semiconductors/
- Cadrex / Dahlstrom — 섀시·레일 ±0.005 in 롤포밍 — https://www.cadrex.com/custom-sheet-metal-server-rack-hardware
- PMi2 / NVIDIA dev — 버스바 구리 사용량, 800VDC 전환 — https://pmi2sc.com/blog/copper-machining-for-ai-data-centers , https://developer.nvidia.com/blog/nvidia-800-v-hvdc-architecture-will-power-the-next-generation-of-ai-factories/
- Greenconn — 커넥터 스탬핑·동합금 — https://www.greenconn.com/en/news-detail102.html
- PRI — NADCAP 브레이징 특수공정 인증(AC7110/1 Rev I) — https://www.p-r-i.org/nadcap/accreditation
- MSI — NADCAP 전 AS9100 품질시스템 선행 요구 — https://www.msi-aqr.com/post/nadcap-special-processes
- 대만 ODM IATF16949+APQP+PPAP 규율 — https://techstock01.substack.com/p/ai-servers-the-big-system-designers , https://teeptrak.com/en/electronics-ems-foxconn-pegatron-flex-jabil-2027/

### 일본·중국 기업 (§3.6 보강)
- Furukawa Electric IR(연결 매출 ¥1,201.8B·영업익 ¥47.1B, 원문 확인) — https://www.furukawaelectric.com/en/ir/achievements/sales.html
- Fujikura FY2025-03 실적(¥979.4B·순이익 ¥91.1B) — https://corporate.quick.co.jp/en/japanmarketsview/equity/fujikura-5803-expands-performance-driven-by-growing-data-center-demand/ , https://www.marketscreener.com/news/fujikura-ltd-reports-earnings-results-for-the-full-year-ended-march-31-2025-ce7c5fdedd8cff21
- Envicool(英维克) 2024 연보(45.89억元) — http://money.finance.sina.com.cn/corp/view/vCB_AllBulletinDetail.php?stockid=002837&id=10922596
- Yinlun(银轮股份) 2024 실적(127.02억元·제3곡선 10.27억元, 원문 확인) — https://finance.sina.com.cn/tech/roll/2025-04-21/doc-inetwvhf6539308.shtml
- Feirongda(飞荣达) 2024 연보(50.31억元) — https://paper.cnstock.com/html/2025-04/16/content_2049483.htm
- 中石科技 2024 연보(15.66억元) — https://www.163.com/dy/article/JTTAUFVO0534A4SC.html
- 高澜股份 2024 연보(6.91억元) — http://file.finance.sina.com.cn/211.154.219.97:9494/MRGG/CNSESZ_STOCK/2025/2025-4/2025-04-25/10972594.PDF
- H20 수출규제(NVIDIA $45억 충당금) — https://www.npr.org/2025/04/16/nx-s1-5366665/nvidia-china-h20-chips-exports , https://www.sec.gov/Archives/edgar/data/0001045810/000104581025000115/q1fy26pr.htm , https://www.cnbc.com/2025/08/22/nvidia-halt-h20-chip-production-china-cracks-down.html

### 설비·인증 단가 (§4.6 보강)
- 진공브레이징로 가격대 — https://www.vacfurnace.com/vacuum-furnace-news/vacuum-brazing-furnace-price/ , https://www.bnrtherm.com/the-latest-prices-of-vacuum-furnaces.html
- 헬륨 누설검사기 — https://www.inficon.com/en/products/leak-detectors/ul3000-fab-series , https://www.idealvac.com/en-us/Leak-Detection-and-RGA-Pfeiffer-Adixen-ASM-Series-Helium-Leak-Detectors/pl/18-372
- 5축 CNC 가격대 — https://us.dmgmori.com/products/machines/milling/5-axis-milling , https://rosnokmachine.com/cnc-machine-price/
- CMM 가격대 — https://www.cmm-compass.com/about/price.html , https://hexagon.com/products/product-groups/measurement-inspection-hardware/coordinate-measuring-machines/bridge-cmms/entry-level-cmms
- AS9100 비용·기간 — https://www.theqmscollective.com/post/how-much-does-as9100-certification-cost-for-a-small-shop , https://ksqa.org/blog/as9100-certification-process-cost/
- NADCAP 비용·AS9100 선행 — https://aqmauditing.com/cost-timeframe-for-gaining-nadcap-certification/ , https://www.p-r-i.org/nadcap/accreditation

### 한국 현황
- thebell — GST 액침냉각·밸류체인 — https://www.thebell.co.kr/free/content/ArticleView.asp?key=202509191433437760102540
- thebell — 케이엔솔-Submer — https://www.thebell.co.kr/free/content/ArticleView.asp?key=202509251747366960104418
- 에너지뉴스 — SK엔무브 액침냉각 — https://www.energy-news.co.kr/news/articleView.html?idxno=219128
- W.Media — 한국 DC 냉각 시장 2025 $176.67M→2031 $454.12M — https://w.media/ambitious-ai-goals-making-south-korea-embrace-liquid-cooling/
- 한양경제 — 한국 액침냉각 경쟁 — https://www.hanyangeconomy.com/article/view/hye202511120013

---

### 부록 — 미확인·보정 항목 (투명성 고지)
- **콜드플레이트 시장 $293.84M(GM Insights snippet)**: 과소계상으로 판정·기각(§3.4). 대용치로 사용하지 않음.
- **Blackwell GPU 5.2M개(TweakTown, 원문 403)**: GB200 콜드플레이트 모집단과 불일치 → NVL72 랙 기준(108만 개)으로 교체.
- **AVC·Vertiv 등 AI서버 매출 비중**: 기업이 세그먼트를 분리 공시하지 않아 다수 "미확인". 회사 전체 매출·정성 코멘트로 갈음.
- **반도체 장비 정밀부품 물량**: WFE capex 연동으로 GPU 출하 역산 불가 → 별도 시장, 본 보고서 범위 밖(미확인).
- **회사 규모**: 사용자 미응답으로 중소기업(30~100명) 가정. 로드맵의 규모 의존 항목(설비투자 시점)은 실제 규모 확정 시 재조정 필요.
- **일본·중국 매출(§3.6)**: Furukawa ¥1,201.8B·Yinlun 127.02억元은 원문 직접 확인. Fujikura ¥979.4B는 원문 403로 QUICK/MarketScreener 2차 출처 기준, Envicool 45.89억元은 PDF 미파싱으로 검색요약 기준(타사는 HTML 원문 교차확인). 일본·중국 각사의 열관리/AI 세부 매출 비중은 대부분 비공개(미확인).
- **설비 단가(§4.6)**: 진공브레이징로·헬륨검사기·CMM 신품 정가는 벤더 비공개가 많아 "통념/추정 범위". 정확 견적은 실제 RFQ 필요.
- **SOM(§4.7)**: 검증된 anchor의 산수 + 명시 가정에 기반한 추정. 점유율 %는 검색값이 아닌 경쟁구도 판단값이며, 이 가정이 결과를 가장 크게 좌우(보수~낙관 9배).
