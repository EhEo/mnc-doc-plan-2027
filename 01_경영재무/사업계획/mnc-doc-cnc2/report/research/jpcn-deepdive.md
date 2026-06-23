<!-- AI 서버 열관리 부품 일본·중국 기업 심화 조사 (대만·미국 보고서 보완용) -->

# 일본·중국 열관리 부품 기업 심화 조사

조사 시점: 2026-06. 2024~2026년 자료 우선. 모든 매출·비중에 fetch/검색으로 확인한 출처를 표기한다. 확인 못 한 항목은 "(미확인)" 또는 "(검색요약 기준, 원문 미파싱)"으로 명시한다. 중국 매출 단위 주의: 중국 매체의 **"亿元"(억 위안 = 1억 RMB)**을 영문 검색요약이 "billion yuan"으로 오역하는 사례가 많아, 본 보고서는 원문 단위(亿元)를 기준으로 표기했다. 환율 환산(1 USD ≈ 7.2 RMB, 1 USD ≈ 150 JPY)은 개략 추정이며 환산임을 명시한다.

---

## 1. 일본 기업 표

| 기업 | 티커 | 주력품목 | 최근 매출(전사) | 열관리/AI 비중 | 공급망 위치 | 출처 |
|---|---|---|---|---|---|---|
| Furukawa Electric (古河電工) | 5801.T | 전선·광섬유·반도체용 소재 / 베이퍼챔버·히트파이프·3D VC·열확산 | FY2024(2025-03 종료) 연결 매출 **¥1,201.8B**(≈US$8.0B), 영업이익 ¥47.1B. 전년 ¥1,056.5B·영업익 ¥11.2B 대비 대폭 개선 | 열관리는 "Electronics" / "Functional Products" 세그먼트 내 소규모 라인. **세그먼트별 열관리 매출 비공개(미확인).** AI/하이퍼스케일 대상 VC·히트파이프·액냉 솔루션을 공식 마케팅 | Tier-3 소재/열부품(VC·히트파이프 등 컴포넌트 공급) | [Furukawa IR 매출/이익](https://www.furukawaelectric.com/en/ir/achievements/sales.html), [Furukawa Thermal](https://www.furukawaelectric.com/thermal/en/) |
| Fujikura (藤倉) | 5803.T | 광섬유·광케이블(WTC/SWR)·광커넥터·전력케이블 / 고성능 히트파이프·VC | FY2024(2025-03 종료) **연결 매출 ¥979,375M(≈¥979.4B, ≈US$6.5B), +22.5% YoY, 순이익 ¥91,123M.** 기중 상향 가이던스(¥880B)를 실적이 상회 | 데이터센터 수요는 주로 **광통신(Telecommunications Systems) 세그먼트**가 견인(생성형 AI DC향 광섬유·케이블). 히트파이프·VC는 별도 열관리 라인이나 **세그먼트 매출 비공개(미확인)**. AI 노출의 본체는 열부품이 아니라 광배선 | Tier-2/3: AI DC **광배선 강자**(WTC/SWR 초고밀도 광케이블) + 열부품(히트파이프·VC) | [QUICK 5803 실적](https://corporate.quick.co.jp/en/japanmarketsview/equity/fujikura-5803-expands-performance-driven-by-growing-data-center-demand/), [MarketScreener FY2025-03 실적](https://www.marketscreener.com/news/fujikura-ltd-reports-earnings-results-for-the-full-year-ended-march-31-2025-ce7c5fdedd8cff21), [Fujikura Heat Pipe(DC)](https://www.businesswire.com/news/home/20221011005626/en/Fujikura-Development-of-High-performance-Heat-Pipe-for-Data-Center-Cooling) |

**그 외 일본사:** 중석과학(中石科技)의 검색 과정에서 확인된 바, 일본 히트파이프 공급망에는 Furukawa·Fujikura 외에 Mitsubishi Materials(구리 베이퍼챔버 소재), Furukawa 계열 외 OEM이 존재하나, **AI 서버 직접 노출에 대한 공시 수치는 본 조사에서 확인하지 못함(미확인)**. 일본세는 전반적으로 "완제 콜드플레이트/CDU"보다 **소재(구리·동박·VC 시트)와 광배선** 쪽 강자다.

---

## 2. 중국 기업 표

| 기업 | 티커 | 주력품목 | 최근 매출(2024) | 열관리/AI·DC 비중 | 공급망 위치 | 출처 |
|---|---|---|---|---|---|---|
| Envicool (英维克) | 002837.SZ | 데이터센터/기지국 정밀 온도제어·CDU·Coolinside 전(全)링크 액냉 | **45.89억元(+30.04%, ≈US$6.4억), 순이익 4.53억元(+31.59%)** (검색요약 기준; 원문 PDF 미파싱) | 기房온도제어(DC) 24.41억元/매출 53.19%, 캐비닛온도제어 17.15억元(주로 ESS). DC 액냉이 핵심 성장축, **Coolinside 솔루션 인텔·NVIDIA 인증·누적 1.2GW 인도** | Tier-1/2 액냉/CDU 시스템 — 중국 액냉 1위권, 주로 내수 | [Envicool 2024 연보摘要(sina)](http://money.finance.sina.com.cn/corp/view/vCB_AllBulletinDetail.php?stockid=002837&id=10922596), [futunn 분석](https://news.futunn.com/post/46552593/shenzhen-envicool-technology-002837-datacenter-business-is-impressive-liquid-cooling) |
| Yinlun (银轮股份) | 002126.SZ | 자동차 열관리(본업) + 제3곡선 "디지털·에너지"(DC 액냉/콜드플레이트/침지) | **127.02억元(+15.28%, ≈US$17.6억), 순이익 7.84억元(+28%)** | 디지털·에너지(제3곡선) 10.27억元 = **매출 8.08%, +47.44%.** DC BTB 액냉·콜드플레이트 모듈·서버 침지 장비. NVIDIA向 콜드플레이트·QD 공급 보도(연보 원문엔 NVIDIA 직접언급 없음) | Tier-2 콜드플레이트/액냉(자동차 열관리 기반 횡전개) | [Yinlun 2024 실적(sina)](https://finance.sina.com.cn/tech/roll/2025-04-21/doc-inetwvhf6539308.shtml) |
| Feirongda (飞荣达) | 300602.SZ | EMI 차폐·열관리 소재/부품(TIM·그라파이트·VC·히트파이프·콜드플레이트·3D-VC·팬) | **50.31억元(503,078.64만元, +15.76%, ≈US$7.0억), 순이익 1.89억元(18,889만元, +83.01%)** | AI서버 액냉 사업 "순조"·배치 주문 양산 진입. 단상/2상 액냉모듈·3D-VC·열사이펀·특수방열기 R&D. **AI/액냉 세부 매출 비중 비공개(미확인)** | Tier-2/3 열관리 소재·모듈(화웨이 방열 핵심 공급사) | [Feirongda 2024 연보摘要(cnstock)](https://paper.cnstock.com/html/2025-04/16/content_2049483.htm) |
| Sinomags / 中石科技 | 300684.SZ | 열관리 소재 솔루션(TIM·그라파이트·히트파이프·VC·방열모듈) | **15.66억元(≈US$2.2억), 순이익 2.01억元, 모이익률 30.95%** | 소비전자 회복 + 북미 고객 비폰 단말 + AI 신열솔루션 수요가 성장 견인. AI단말·AI DC를 신성장축으로 명시. **DC/AI 세부 매출 비중 비공개(미확인)** | Tier-3 열관리 소재/부품(20년+ TIM·히트파이프·VC) | [中石科技 2024 연보(163 미러)](https://www.163.com/dy/article/JTTAUFVO0534A4SC.html), [eastmoney](https://finance.eastmoney.com/a/202504243386869793.html) |
| High & Low (高澜股份) | 300499.SZ | 순수수 냉각·전력전자 액냉 + DC 콜드플레이트/침지/CDU/Manifold | **6.91억元(69,126.40만元, +20.58%, ≈US$0.96억), 귀모순이익 -5,032만元(적자)** | 특고압직류·ESS·DC 액냉 전링크(서버 액냉판·커넥터·Manifold·CDU·TANK). 액냉 선행주자지만 **규모 작고 적자, AI DC 매출 비중 비공개(미확인)** | Tier-2 액냉 시스템(전력전자 기반, DC 확장 중) | [高澜股份 2024 연보(sina/cninfo)](http://file.finance.sina.com.cn/211.154.219.97:9494/MRGG/CNSESZ_STOCK/2025/2025-4/2025-04-25/10972594.PDF) |

> 단위·환산 주의: 중국 매출은 모두 **억元(=1억 RMB)** 단위다(예: Yinlun 127.02억元 ≈ RMB 12.7B ≈ US$17.6억, "127 billion"이 아님). USD 환산은 7.2 RMB/USD 개략치. Feirongda·Envicool·Yinlun·中石·高澜 5사 헤드라인 매출/순이익은 HTML 원문(cnstock/sina/163)으로 교차 확인했고, Envicool만 PDF 미파싱으로 검색요약 기준임을 명시.

---

## 3. 해설 — 중국 공급망의 특수성(대중 수출규제)

- **2025-04-09, 美 정부가 NVIDIA H20(중국전용 칩) 수출에 라이선스 의무 부과** → NVIDIA는 FY2026 1Q에 H20 재고 관련 약 **$45억 충당금**을 인식, 中 고객 주문 취소. 이후 中 사이버공간관리국(CAC)이 자국 기업의 NVIDIA 칩 구매를 사실상 금지하고 **국산 대체를 지시**. 2025-07 트럼프 행정부가 H20 재개를 일부 허용하나, 2025-08 中이 다시 구매 자제 압박 → NVIDIA가 H20 생산 중단 검토. [NPR 2025-04-16](https://www.npr.org/2025/04/16/nx-s1-5366665/nvidia-china-h20-chips-exports), [NVIDIA Q1 FY26 8-K](https://www.sec.gov/Archives/edgar/data/0001045810/000104581025000115/q1fy26pr.htm), [CNBC 2025-08-22](https://www.cnbc.com/2025/08/22/nvidia-halt-h20-chip-production-china-cracks-down.html)
- **콜드플레이트사에 대한 함의:** (1) 중국 액냉사(Envicool·Yinlun·Feirongda·高澜)의 AI DC 수요는 **NVIDIA GB200/H100급이 아니라 국산 가속기(화웨이 Ascend 등) + H20급 잔여 물량 + ESS·전력**에 묶인다. 즉 글로벌 NVIDIA 레퍼런스 랙(GB200 NVL72) 메인 콜드플레이트 인증 경쟁에서 구조적으로 배제되는 경향. (2) Envicool이 "NVIDIA 인증"을 내세우지만 미·중 갈등 상 글로벌 하이퍼스케일러 직납보다 **중국 내수 + 일대일로/동남아 위주**. (3) 반대로 내수 AI 투자·"东数西算"·국산화 정책이 이들에게 **방어된 거대 내수 시장**을 보장 → 규모는 빠르게 크지만 글로벌 진입은 제약.

---

## 4. 출처 목록(주요)

- Furukawa Electric IR 매출/이익: https://www.furukawaelectric.com/en/ir/achievements/sales.html
- Furukawa Thermal Solutions: https://www.furukawaelectric.com/thermal/en/
- Fujikura 5803 실적(QUICK): https://corporate.quick.co.jp/en/japanmarketsview/equity/fujikura-5803-expands-performance-driven-by-growing-data-center-demand/
- Fujikura FY2025-03 실적(MarketScreener): https://www.marketscreener.com/news/fujikura-ltd-reports-earnings-results-for-the-full-year-ended-march-31-2025-ce7c5fdedd8cff21
- Fujikura DC 히트파이프(BusinessWire): https://www.businesswire.com/news/home/20221011005626/en/Fujikura-Development-of-High-performance-Heat-Pipe-for-Data-Center-Cooling
- Envicool 2024 연보摘要(sina): http://money.finance.sina.com.cn/corp/view/vCB_AllBulletinDetail.php?stockid=002837&id=10922596
- Yinlun 2024 실적(sina): https://finance.sina.com.cn/tech/roll/2025-04-21/doc-inetwvhf6539308.shtml
- Feirongda 2024 연보摘要(cnstock): https://paper.cnstock.com/html/2025-04/16/content_2049483.htm ; cninfo PDF: https://static.cninfo.com.cn/finalpage/2025-04-16/1223100742.PDF
- 中石科技 2024 연보(163/eastmoney): https://www.163.com/dy/article/JTTAUFVO0534A4SC.html
- 高澜股份 2024 연보(sina/cninfo): http://file.finance.sina.com.cn/211.154.219.97:9494/MRGG/CNSESZ_STOCK/2025/2025-4/2025-04-25/10972594.PDF
- H20 수출규제: NPR 2025-04-16 / NVIDIA Q1 FY26 8-K / CNBC 2025-08-22 (상기 링크)
