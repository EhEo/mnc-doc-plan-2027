<!-- agy 가공품·물량 조사와 codex 기업·매출 조사를 매칭·교차검증한 정합성 분석 보고서 -->

# 가공품-기업 매칭 및 물량 vs 매출 교차검증 (codex × agy 통합)

작성: 2026-06. agy의 가공품 8종·물량 anchor와, codex가 조사한 기업 매출·시장규모를 통합 검증한다.
확정 사실과 추정을 구분하고, 새로 fetch한 수치엔 URL을 붙인다.

---

## 임무 1 — 기업-가공품 매칭 표

| # | 가공품 | 주요 공급기업 | 공급망 티어 | 비고 |
|---|---|---|---|---|
| 1 | 방열판/히트싱크 (압출·스카이빙·CNC) | AVC(3017), Auras(3324), Cooler Master, Furukawa | Tier-2/3 | 대만 3사 + 일본 소재. AVC·Auras 내재 가공 |
| 2 | 베이퍼챔버 (스탬핑·소결·확산접합) | AVC, Auras, Furukawa(古河), Fujikura(藤倉) | Tier-2/3 | 일본 2사가 히트파이프·VC 소재/가공 강점(Fujikura 100W HP) |
| 3 | **콜드플레이트/수냉 (CNC·진공브레이징·FSW) — 핵심** | Cooler Master(GB200 1차 50%+), AVC, Boyd, Auras / 中 Shenzhen Cotran | Tier-2(NVIDIA 인증), Tier-3(소재) | AVC·CoolIT가 DLC 콜드플레이트 점유 상위로 거론. Cu-Al 하이브리드 ~35%(2024 물량) |
| 4 | GPU 브라켓·백플레이트 (스탬핑·CNC·다이캐스팅) | 랙 ODM 내재(Foxconn/FII, Quanta, Wiwynn) + 현지 가공사 | Tier-1(통합)/Tier-3(가공) | 구조부품, 특정 브랜드 매핑 약함(미확인 다수) |
| 5 | 서버 섀시·레일 (레이저·벤딩·롤포밍) | Foxconn/FII, Quanta, Wiwynn, Wistron, Inventec | Tier-1 ODM | 랙/시스템 조립사가 섀시 통합 |
| 6 | 소켓·커넥터 접점 (프로그레시브 스탬핑) — 초대량 | Amphenol(Paladin HD 224G), TE Connectivity / QD: CPC·Parker·Danfoss·Staubli | Tier-2 | GPU당 Amphenol 고속 커넥터, 인터페이스별 2~3 벤더 QVL |
| 7 | 반도체 장비 정밀부품 (척·스테이지, EDM·연삭) — 최상난이도 | (AI서버 직접 BOM 아님 — 장비 OEM향 별도 공급망) | 별도 | 본 매핑은 AI서버 부품 중심이라 직접 대응 기업 미식별(미확인) |
| 8 | 케이블 트레이·버스바 (CNC·롤포밍) | 버스바: 랙 ODM 내재 + TE(수냉 버스바 750kW) / 동·알 가공사 | Tier-1(통합)/Tier-2 | NVL72 48V DC 버스바(2.5kA+). TE 수냉 버스바 시연 |

요약: 콜드플레이트·베이퍼챔버·히트싱크는 **대만 3사(Cooler Master·AVC·Auras) + Boyd(미국) + 일본 소재(Furukawa·Fujikura)**, CDU는 **Delta(사이드카)·Vertiv·Boyd(in-row)·CoolIT**, 커넥터/버스바는 **Amphenol·TE Connectivity + QD 4사(CPC·Parker·Danfoss·Staubli)**, 랙/섀시는 **Foxconn·Quanta·Wiwynn**. 7번(반도체 장비 정밀부품)은 AI서버 BOM이 아니라 장비 OEM 공급망이라 본 기업군과 직접 매핑되지 않음.

---

## 임무 2 — 물량 vs 매출 교차검증 (핵심)

### 새로 확보한 단가 anchor (fetch/검색 확인)
- **GB200 NVL72 콜드플레이트 단가 ≈ US$400/개** (GB300은 CPU/GPU $300, NVSwitch $200). [출처: Tom's Hardware, Morgan Stanley 인용, [tomshardware.com](https://www.tomshardware.com/pc-components/cooling/cooling-system-for-a-single-nvidia-blackwell-ultra-nvl72-rack-costs-a-staggering-usd50-000-set-to-increase-to-usd56-000-with-next-generation-nvl144-racks)]
- **NVL72 랙당 액냉 부품 BOM 합계 ≈ US$49,860** (compute tray 18개 × $2,260 = $40,680 + NVSwitch tray $9,180). [출처: 동일 Tom's Hardware/Morgan Stanley]
  - 직전 codex 보고서의 MS 추정(랙당 액냉 ~$88K)과 차이가 있는데, $49,860은 **GB300/Blackwell Ultra NVL72 기준 산정**으로 범위·구성이 다름. 둘 다 MS 계열이나 본 검증은 더 상세·최신인 $49,860을 채택.

### (A) 콜드플레이트 개수 추정의 정합성 — 5.2M vs 1.08M

먼저 **두 수치는 같은 모집단의 두 추정치가 아니라, 서로 다른 모집단**이다. 이것이 핵심.
- **5.2M개** = 2025년 Blackwell GPU 전수(모든 폼팩터). 대부분은 공냉 HGX·비(非)NVL72로 출하 → "GPU 1개 = 콜드플레이트 1개"는 **느슨한 상한**이며 GB200 랙용 콜드플레이트를 크게 과대계상.
- **1.08M개** = NVL72 한정(Superchip 모듈 36 × 랙 30K). GB200 랙 콜드플레이트 시장과 대응하는 합리적 추정. 단 "모듈당 1개" 가정이며, 다이 단위(랙당 GPU 72 + CPU 36 콜드플레이트)로 세면 더 커진다.

단가 $400을 적용한 환산(추정):

| 추정 | 개수 | × $400 | 함의 |
|---|---|---|---|
| GPU 전수 기준 | 5.2M | **≈ $2.08B** | Blackwell 전체 GPU에 콜드플레이트 가정 — 과대(공냉 다수 포함) |
| NVL72 랙 기준(모듈) | 36 × 30K = 1.08M | **≈ $432M** | GB200 콜드플레이트 시장 대응. 2025 단년 |
| NVL72 랙 기준(다이) | (72+36) × 30K = 3.24M | **≈ $1.30B** | 다이 단위 콜드플레이트 — 상한 근사 |
| MS BOM 교차검증 | $49,860/랙 × 30K | 액냉 전체 **≈ $1.50B**, 콜드플레이트는 그 부분집합(30~40% 가정 시 $0.45~0.6B) | 독립 경로 |

**판정**: 시장규모·매출과 더 잘 맞는 것은 **1.08M개(NVL72 랙 기준, ≈$432M)** 쪽이다. 5.2M개(≈$2.08B)는 GB200 랙 콜드플레이트로 보면 명백히 과대(공냉 GPU 포함). 다만 1.08M(모듈)~3.24M(다이) 사이에 실제값이 있고, MS BOM 경로($0.45~0.6B)와 모듈 기준($432M)이 같은 자릿수로 수렴한다.

### (B)(C) 약한 출처의 모순 적발 및 신뢰도 판정

**적발된 모순: agy의 "콜드플레이트 세그먼트 2024 ≈ $293.84M"(GM Insights snippet)은 거의 확실히 과소계상**이다. 세 가지 독립 경로로 확인:

1. **개별 기업 매출과의 모순(내부 정합성, 검색 불필요)**: AVC 단독 2024 총매출 ≈US$2.0B [Taiwan News, fetch 확인]. 이 중 콜드플레이트/액냉이 15~20%만 차지해도 **AVC 한 곳에서 ~$300~400M** → "전 세계 콜드플레이트 시장 $293.84M"을 단일 중견사가 거의 채우거나 초과. 비현실적.
2. **단가×물량 경로**: 2025 NVL72 한정 콜드플레이트만 모듈 기준 ≈$432M, 다이 기준 ≈$1.30B. 2024→2025 증가를 감안해도 "콜드플레이트 시장 $293.84M"은 한 자릿수 order만큼 낮음.
3. **MS BOM 경로**: 랙당 액냉 $49,860 × 30K랙 ≈ $1.5B(2025, NVL72만). 콜드플레이트가 그 30~40%면 $0.45~0.6B. 역시 $293.84M을 크게 상회.

> 단, $293.84M은 **2024년·"DLC 서버용 콜드플레이트" 등 좁은 정의의 한 리서치사 추정**일 수 있다(연도·범위 차이). 그렇더라도 2025 GB200 단년 물량만으로 이미 초과하므로, **"전체 콜드플레이트 가공 시장" 대용치로 쓰면 안 된다**는 결론은 유지.

**5.2M개(TweakTown 403)**: 원문 접근 불가(403)인 데다 "Blackwell GPU 전수"라 GB200 콜드플레이트 모집단과 불일치. 콜드플레이트 시장 환산용으로는 부적합 → **NVL72 랙 기준(랙 출하 24K~35K [Tom's Hardware] × 모듈 36)으로 대체** 권장.

#### 출처 신뢰 위계 (명시)
```
[높음] 1차/IR·거래소 공시  : AVC NT$71.8B(Taiwan News 기반 실적), Delta IR, Vertiv SEC 8-K
[중간] 리서치사/IB        : Morgan Stanley(콜드플레이트 $400, 랙 BOM $49,860 — Tom's Hardware 매개),
                            TrendForce(침투율 14%→33%), MarketsandMarkets(AI서버 시장)
[낮음] 블로그/snippet     : GM Insights snippet($293.84M), TweakTown(403, GPU 5.2M)
```
- agy의 약한 출처 2건은 모두 위계 최하단. $293.84M은 **MS BOM × 랙수 삼각측량(≈$0.45~0.6B+)으로 하한 보정**, 5.2M은 **NVL72 랙 기준 1.08M(모듈)으로 교체**해 사용.

### 종합 정합성 판정
- agy 물량과 codex 매출/시장규모는 **방향성에서 모순 없음**(액냉·콜드플레이트 급성장, 대만 3사 수혜). 단가·물량 환산($432M~$1.3B/2025 콜드플레이트)이 기업 매출 규모(AVC·Auras 합산 액냉 매출 수억$대)와 **같은 자릿수로 정합**.
- **유일한 실질 모순은 "$293.84M 콜드플레이트 시장(snippet)"** — 세 경로 모두 이를 과소로 판정. 이 수치를 시장 대용치로 쓰지 말 것.
- 5.2M vs 1.08M은 모순이 아니라 **모집단 차이**. 시장규모 정합은 **1.08M(NVL72)** 쪽.

---

## 출처 목록 (이번 검증에서 확인/인용)

- Tom's Hardware (NVL72 콜드플레이트 $400, 액냉 BOM $49,860 / MS 인용): https://www.tomshardware.com/pc-components/cooling/cooling-system-for-a-single-nvidia-blackwell-ultra-nvl72-rack-costs-a-staggering-usd50-000-set-to-increase-to-usd56-000-with-next-generation-nvl144-racks
- IntuitionLabs (GB200 공급망/BOM): https://intuitionlabs.ai/articles/nvidia-gb200-supply-chain
- IntelMarketResearch (DLC 콜드플레이트 시장, AVC·CoolIT 점유 언급): https://www.intelmarketresearch.com/direct-liquid-cooling-cold-plates-for-server-2025-2032-704-6188
- DigiTimes (AVC 히트싱크/액냉 수요): https://www.digitimes.com/news/a20260408PD227/ai-server-liquid-cooling-heat-sink-demand-avc-revenue.html

### codex 직전 보고서에서 승계한 핵심 출처(재인용)
- AVC 2024 실적(Taiwan News): https://www.taiwannews.com.tw/news/6058452
- Auras 2024 실적(Quartr): https://quartr.com/companies/auras-technology-co-ltd_15788
- TrendForce 침투율 14%→33%: https://www.trendforce.com/presscenter/news/20250821-12682.html
- MarketsandMarkets AI 서버 시장: https://www.marketsandmarkets.com/Market-Reports/ai-server-market-141336410.html
- Vertiv SEC 8-K FY2024: https://www.sec.gov/Archives/edgar/data/0001674101/000162828025005006/exhibit991vrt02122025.htm

### agy anchor 중 보강·교체 대상
- (교체) GPU 5.2M개 [TweakTown 403] → NVL72 랙 24K~35K [Tom's Hardware] × 모듈 36 ≈ 1.08M개
- (하한 보정) 콜드플레이트 $293.84M [GM Insights snippet] → MS BOM × 랙수 삼각측량으로 2025 $0.45~1.3B대로 보정
