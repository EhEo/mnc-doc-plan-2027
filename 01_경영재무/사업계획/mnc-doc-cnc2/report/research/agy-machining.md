<!-- AI/GPU 서버 하드웨어용 정밀가공품 8종의 가공공정·소재·공차·물량 전수 조사 (agy 조교) -->

# AI/GPU 서버 정밀가공품 전수 조사 — 가공공정 매핑

> 조사일 2026-06-10 · 대상 NVIDIA/AMD GPU·AI 가속기 서버
> 물량은 top-down 추정이며, 정량 수치에는 출처 URL을 명시한다. 미확인 수치는 (미확인/업계 추정)으로 표기.

## 물량 추정의 기준 수치 (anchor)

- **2024 AI 서버 출하량 1.67M대 (+41.5% YoY)**, 시장가치 $187B, 전체 서버 시장의 65% [출처: TrendForce, 2024-07-17, https://www.trendforce.com/presscenter/news/20240717-12227.html]
- **2025 Blackwell GPU = NVIDIA 고급 GPU 출하의 80%+** [출처: TrendForce, 2025-07-24, https://www.trendforce.com/presscenter/news/20250724-12653.html]
- **2025 Blackwell GPU 출하 약 5.2M개** (JP Morgan 추정, 애널리스트 노트 재인용 — 원문 fetch 차단(403)으로 snippet 기반, 업계 추정) [출처: TweakTown, 2026, https://www.tweaktown.com/news/106116/]
- **GB200 NVL72 랙 1대 = GPU 72개 / Grace-Blackwell Superchip 모듈 36개 / NVLink 동축 케이블 144개 / 광케이블 288개 / 120kW / 냉각수 200L** [출처: Introl, 2025, https://introl.com/blog/gb200-nvl72-deployment-72-gpu-liquid-cooled]
- **2025 GB200 NVL72 캐비닛 출하 24K~35K대** (애널리스트 전망, 하향 조정됨; snippet 기반 업계 추정) [출처: Tom's Hardware / WT·JPM 인용, 2025, https://www.tomshardware.com/tech-industry/artificial-intelligence/analysts-halve-nvidia-gb200-blackwell-shipment-forecasts-for-2025-prediction-contrasts-ai-boom]
- **2026 AI 서버 출하 +28% YoY, GPU형 69.7% / ASIC형 27.8%** [출처: TrendForce, 2026-01-20, https://www.trendforce.com/presscenter/news/20260120-12887.html]

> 핵심 환산 체인: Blackwell GPU 5.2M개(2025) → GPU 1개당 콜드플레이트 1개 → 콜드플레이트 약 5.2M개 / Superchip 모듈(2 GPU) 기준 약 2.6M모듈. NVL72 랙 30K대 기준이면 랙당 콜드플레이트 36개 × 30K = 약 1.08M개. (GPU-단위 추정과 랙-단위 추정의 차이는 비(非)NVL72 폼팩터·HGX 보드 포함 여부 때문.)

---

## 1. 방열판 / 히트싱크 (공랭)

| 가공품 | 사용 가공기 | 소재 | 요구 정밀도/공차 | 추정 물량 규모 |
|---|---|---|---|---|
| 압출 핀 히트싱크 | 압출(extrusion) + CNC 후가공 | AL6063 (압출용), 일부 AL6061 | 일반 ±0.1mm, 베이스 평탄도 중간 | 공랭 잔존 서버 다수 (저단가·대량) |
| 스카이빙 핀 히트싱크 | 스카이빙(skiving), CNC 블레이드 | 구리(C1100), 알루미늄 | 핀 두께 0.1mm·피치 0.2mm, 핀-베이스 일체(계면 열저항 0) | GPU·CPU 보드용, AI 서버 GPU 수 비례 |
| 지퍼핀/폴디드핀 + 베이스 | 프레스/스탬핑(핀), 솔더링/브레이징(결합), CNC(베이스) | 구리, 알루미늄 | 베이스 접촉면 평탄도 ≤0.002 in/in, Ra 관리 | 고성능 공랭 GPU |

해설. 공랭 히트싱크의 핵심 난이도는 **칩 접촉 베이스의 평탄도/조도**(CNC 정밀 밀링)와 **고종횡비 핀 형성**(스카이빙)이다. 스카이빙은 핀과 베이스가 한 덩어리라 계면 열저항이 없어 고열밀도 GPU에 유리하나 평행핀만 가능하다. AI 서버 고열밀도화로 순수 공랭 비중은 줄지만, 저전력 노드·엣지·일반 서버에서 여전히 최대 물량.

---

## 2. 베이퍼챔버 (vapor chamber)

| 가공품 | 사용 가공기 | 소재 | 요구 정밀도/공차 | 추정 물량 규모 |
|---|---|---|---|---|
| 베이퍼챔버 쉘(상·하판) | 프레스/스탬핑 | 구리(동박/동판) | 박판 성형, 기밀 용접면 정밀도 | 고급 GPU·서버 칩당 1개 |
| 윅(wick) 소결 | 소결(sintering, 가공기 아님) | 구리 분말 | 모세관 구조 균일성 | 챔버 내부 |
| 핀 부착 면 | 스카이빙/CNC | 구리 | 챔버 2차 벽 핀 형성 | 챔버+핀 일체형 |

해설. 베이퍼챔버는 절삭보다 **스탬핑·소결·진공 충진·확산접합/용접** 공정 비중이 높다. 정밀가공 관점에서는 쉘 스탬핑 금형과 핀 스카이빙이 가공 포인트. 균열·누설이 신뢰성 리스크(과거 RTX 사례). 물량은 고급 GPU·일부 콜드플레이트 하이브리드에 한정.

---

## 3. 콜드플레이트 / 수냉 (direct-to-chip)

| 가공품 | 사용 가공기 | 소재 | 요구 정밀도/공차 | 추정 물량 규모 |
|---|---|---|---|---|
| 마이크로채널 콜드플레이트 | CNC 밀링/라우팅, 스카이빙, 진공 브레이징, FSW | 구리(T2 자동, 391 W/mK), 일부 AL6061, Cu-W | 접촉면 평탄도 ≤0.05mm, Ra ≤0.8μm, 6 bar 내압, He 누설검사 | GPU 1개당 1개 |
| 매니폴드/분배 블록 | CNC 5축, 브레이징 | 구리, 알루미늄, SUS | 유로 정밀도, 기밀 | 랙당 다수 |

해설. **현재 AI 서버 정밀가공의 핵심 품목.** 고열밀도(GB200 모듈 ~2.7kW)로 direct-to-chip이 표준화. 마이크로채널 CNC + 진공 브레이징 + 헬륨 누설검사가 결합된 고난이도·고부가 부품. 물량: Blackwell GPU 약 5.2M개(2025) → 콜드플레이트 수 GPU 수에 비례하여 **연 수백만 개 규모**. NVL72 랙 1대당 모듈 36개(콜드플레이트 36개 상당), 랙 24~35K대 기준 랙 채널만 약 0.9~1.3M개. 콜드플레이트 세그먼트 시장 2024년 약 $293.84M (snippet 기반, 업계 추정) [출처: GM Insights/Tweaktown snippet, https://www.gminsights.com/industry-analysis/data-center-liquid-cooling-market].

---

## 4. GPU 브라켓 · 백플레이트 · 스티프너

| 가공품 | 사용 가공기 | 소재 | 요구 정밀도/공차 | 추정 물량 규모 |
|---|---|---|---|---|
| PCIe 브라켓 | 프레스/스탬핑, 일부 CNC | SUS(스테인리스), 알루미늄 | ±0.10mm, 아노다이징 | 카드 1장당 1개 (대량) |
| 백플레이트 | CNC 밀링, 스탬핑, 다이캐스팅 | 알루미늄(강성·열질량) | CNC 시 ±0.0005 in 가능, 다이캐스팅은 후가공 필요 | GPU 카드당 1개 |
| 스티프너/보강 프레임 | CNC, 다이캐스팅 | 알루미늄 | 평탄도·체결 위치 | 대형 GPU 비중 증가 |

해설. 난이도는 중간. **대량 스탬핑(브라켓)** 과 **다이캐스팅+CNC 후가공(백플레이트/스티프너)** 조합. 다이캐스팅은 복잡형상·고생산성이나 다공성으로 임계부 2차 가공 필요. 물량은 GPU 카드 출하량에 1:1 비례(연 수백만~).

---

## 5. 서버 섀시 · 랙 레일 · 슬레드

| 가공품 | 사용 가공기 | 소재 | 요구 정밀도/공차 | 추정 물량 규모 |
|---|---|---|---|---|
| 섀시/인클로저 | 레이저 절단 + CNC 벤딩 + 스탬핑 + 용접 | 냉연강판(CRS), SUS, 알루미늄 판재 | 판금 일반 공차, 조립 정합성 | 서버 1대당 1세트 |
| 슬라이드 레일 | 롤포밍(roll-forming), 스탬핑 | 강판 | 랙 전체 깊이 정렬 ±0.005" (±0.13mm) | 서버 1대당 1쌍 |
| 드라이브 슬레드·팬 케이지 | 스탬핑 | 강판, 알루미늄 | 반복 정밀도 | 다수/서버 |

해설. 정밀절삭보다 **판금(레이저·벤딩·스탬핑)·롤포밍** 중심. 핵심 정밀도는 슬라이드 레일의 랙 깊이 정렬(±0.005")로, 미스얼라인 시 커넥터 손상·다운타임 유발. 물량은 서버 출하량(2024 AI 서버 1.67M대 + 일반 서버) 비례로 대량.

---

## 6. 소켓 · 커넥터 부품 (busbar 접점 포함)

| 가공품 | 사용 가공기 | 소재 | 요구 정밀도/공차 | 추정 물량 규모 |
|---|---|---|---|---|
| 소켓/터미널 접점 | 프로그레시브 프레스/스탬핑, 일부 CNC | 베릴륨동, 인청동, 황동 | 버burr 최소화, 단면 정밀, 고1차수율 | 칩/포트당 수백~수천 핀 (초대량) |
| 프레스핏 터미널 | 스탬핑 | 동합금(도금) | 압입 공차 | 보드당 다수 |
| 고전류 busbar 접점/링크 | 스탬핑 + CNC(드릴·밀링) | 구리 | 접촉면·체결홀 정밀도 | 전력경로당 |

해설. **고속 프로그레시브 스탬핑**이 주력(코일 → 다단 전단·벤딩). 소재가 동합금·베릴륨동으로 도금까지 포함. 핀 수가 칩당 수천 개라 단위가 작아도 **총 물량은 최대급**. AMD/NVIDIA 소켓, NVLink 커넥터, 전원 커넥터 전 영역.

---

## 7. 반도체 제조장비용 정밀부품 (척·스테이지·진공/EFEM)

| 가공품 | 사용 가공기 | 소재 | 요구 정밀도/공차 | 추정 물량 규모 |
|---|---|---|---|---|
| 정전척(ESC) | CNC 정밀밀링 + 와이어 EDM(냉각유로) + 연삭/폴리싱 | Al₂O₃·AlN·SiC 세라믹 + 알루미늄/몰리브덴 베이스 | 평탄도 <1μm/300mm, Ra <0.1μm | (미확인/업계 추정) |
| 웨이퍼 스테이지/플레이트 | CNC 5축, EDM, 연삭 | 알루미늄, SUS(316L/17-4PH), Ti, 세라믹, 인바 | 평탄도 1~5μm, 홀 위치 ±2μm, 평행도 <2μm | (미확인/업계 추정) |
| 진공챔버·EFEM 부품 | CNC, 용접 | SUS, 알루미늄, Ti | UHV(10⁻⁹ mbar) 무아웃가싱 | (미확인/업계 추정) |

해설. **8개 품목 중 가공난이도 최고.** ㎛급 평탄도·위치공차, 플라즈마/UHV/극온 내성 요구로 CNC+EDM+연삭+폴리싱 다공정. 단, 이 품목의 물량은 GPU/서버 출하량이 아니라 **WFE(반도체 전공정 장비) capex에 연동**되는 다른 분모이므로 GPU 기반 역산 불가 → 물량은 (미확인/업계 추정). 별도 ESC/WFE 시장 데이터 확보 필요.

---

## 8. 케이블 트레이 · 버스바 (power delivery)

| 가공품 | 사용 가공기 | 소재 | 요구 정밀도/공차 | 추정 물량 규모 |
|---|---|---|---|---|
| 리지드 버스바 | CNC 멀티축(드릴·밀링·프로파일), 일부 스탬핑 | 구리(연동), 일부 알루미늄 | 접촉점·체결홀 타이트 공차 | 랙당 다수 (대형 캐비닛 다량) |
| 적층/절연 버스바 | 스탬핑 + 적층 + 절연 | 구리 + 절연재 | 도체 단면 정밀 | 전력셸프·PDU당 |
| 케이블 트레이 | 판금(스탬핑·벤딩), 롤포밍 | 강판, 알루미늄 | 일반 판금 공차 | 데이터홀당 대량 |

해설. 버스바는 **CNC 가공(연동은 "끈적"해 절삭 난이도 있음)+스탬핑** 조합. AI 랙 고전류화(40~60kW→200kW+)로 구리 사용량 급증 — 54VDC 1MW 랙은 버스바만 최대 200kg 구리. NVIDIA 800VDC 전환(2027~)이 변수. 물량은 랙 수·전력밀도 비례로 구리 중량 기준 급성장.

---

## 가공품 목록 요약 (codex 기업 매칭용)

1. 방열판/히트싱크 — 압출·스카이빙·CNC·스탬핑 — AL6063/구리 — 난이도 중
2. 베이퍼챔버 — 스탬핑·소결·확산접합·스카이빙 — 구리 — 난이도 중상
3. 콜드플레이트/수냉 — CNC밀링·스카이빙·진공브레이징·FSW — 구리(T2)/AL6061 — 난이도 상 (핵심 품목)
4. GPU 브라켓·백플레이트 — 스탬핑·CNC·다이캐스팅 — SUS/알루미늄 — 난이도 중
5. 서버 섀시·레일 — 레이저절단·벤딩·스탬핑·롤포밍 — 냉연강판/SUS/알루미늄 — 난이도 중하
6. 소켓·커넥터 접점 — 프로그레시브 스탬핑·CNC — 베릴륨동/인청동/황동 — 난이도 중 (초대량)
7. 반도체 장비 정밀부품 — CNC·와이어EDM·연삭·폴리싱 — 세라믹(Al₂O₃/AlN/SiC)/알루미늄/SUS/Ti — 난이도 최상
8. 케이블 트레이·버스바 — CNC멀티축·스탬핑·롤포밍 — 구리/알루미늄/강판 — 난이도 중

---

## 출처 목록

- TrendForce 2024-07-17 (AI 서버 1.67M대, +41.5%, $187B) — https://www.trendforce.com/presscenter/news/20240717-12227.html
- TrendForce 2025-07-24 (Blackwell 80%+, 액냉 표준화) — https://www.trendforce.com/presscenter/news/20250724-12653.html
- TrendForce 2026-01-20 (2026 +28%, GPU 69.7%/ASIC 27.8%) — https://www.trendforce.com/presscenter/news/20260120-12887.html
- Introl (GB200 NVL72 BOM: GPU 72/모듈 36/NVLink 동축 144/120kW/200L) — https://introl.com/blog/gb200-nvl72-deployment-72-gpu-liquid-cooled
- Tom's Hardware (NVL72 캐비닛 24~35K 전망 하향) — https://www.tomshardware.com/tech-industry/artificial-intelligence/analysts-halve-nvidia-gb200-blackwell-shipment-forecasts-for-2025-prediction-contrasts-ai-boom
- TweakTown (Blackwell 5.2M/2025, JPM 추정; 원문 403) — https://www.tweaktown.com/news/106116/
- Ecotherm (히트싱크 공정: 스카이빙 0.1mm핀, CNC 0.002in/in, 콜드플레이트 He누설) — https://ecothermgroup.com/how-heat-sinks-are-made/
- Gazfull (반도체 정밀가공: 소재·공차) — https://www.gazfull.com/cnc-machining-for-semiconductors/
- Fountyl (ESC 평탄도 <1μm/300mm, EDM 냉각유로) — https://www.fountyltech.com/news/electrostatic-chuck-2/
- PMi2 / MSS / NVIDIA dev (버스바 동 200kg, 800VDC 전환) — https://pmi2sc.com/blog/copper-machining-for-ai-data-centers , https://developer.nvidia.com/blog/nvidia-800-v-hvdc-architecture-will-power-the-next-generation-of-ai-factories/
- ToneCooling (콜드플레이트 T2동 391W/mK, 평탄도 ≤0.05mm) — https://tonecooling.com/nvidia-gb200-nvl72-cooling-requirements/
- Cadrex / Dahlstrom (섀시·레일 ±0.005" 롤포밍) — https://www.cadrex.com/custom-sheet-metal-server-rack-hardware
- Greenconn / ConnectorSupplier (커넥터 스탬핑·동합금) — https://www.greenconn.com/en/news-detail102.html
