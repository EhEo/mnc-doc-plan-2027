<!-- 용우(用友) U9/U9C ERP의 MS SQL Server 스키마 규약을 리버스 엔지니어링 힌트로 정리한 지식 베이스 초안 -->
# U9C 스키마 규약 지식 베이스 (초안)

> 본 문서는 실제 스키마 없이 데이터 주도로 테이블/컬럼 의미를 추정할 때 쓰는 "힌트" 모음이다. 각 항목은 **신뢰도**를 표기했다. `문서화됨` = 용우 공식/벤더 자료, `커뮤니티` = CSDN/博客园/API문서 등 관찰 기반, `추정` = 정황 추론. **확정 사실이 아닌 항목은 반드시 실측 검증 후 사용할 것.**

---

## 1. 전체 아키텍처 (整体架构)

- U9은 완전히 SOA(面向服务 아키텍처) 기반으로 구축된 관리 소프트웨어로 소개된다. `(신뢰도: 문서화됨)` `[출처: https://yonyou.eu/products/u9/]` `[출처: http://www.yonyou.com/global/introduce.html]`
- 지원 DBMS는 **MS SQL Server**가 표준(로컬 DB)이다. `(신뢰도: 문서화됨/커뮤니티)` `[출처: https://blog.csdn.net/weixin_43050480/article/details/143168159]`
- 기술 스택은 **.NET Framework**(3.5 및 4.6) 기반이며, UAP 플랫폼은 C#/VB.NET/F# 등 .NET 언어를 지원한다. `(신뢰도: 커뮤니티)` `[출처: https://blog.csdn.net/weixin_30600197/article/details/99006302]`
- 애플리케이션 기반은 **UAP(用友应用平台, Yonyou Application Platform)** 위의 **UBF(UAP Business Framework)** 로, **메타데이터 주도(metadata-driven)·서비스지향·계층형(데이터/비즈니스/프레젠테이션 분리)** 설계다. `(신뢰도: 문서화됨/커뮤니티)` `[출처: https://www.wenkub.com/doc-21298231.html]` `[출처: https://u9cloud.yonyou.com/news/detailes/news/764]`
- UBF 프로젝트 계층은 **BE(Business Entity, 엔티티)·BF(Business Flow, 오퍼레이션)·SV(Service, 서비스)** 로 나뉜다. 데이터 접근은 **OQL(Object Query Language)** → SQL로 변환되는 ORM 방식이다. `(신뢰도: 커뮤니티)` `[출처: https://jishuzhan.net/article/1804945388239589377]`
- **멀티 조직(多组织, multi-org)** 을 정식 지원한다. U9 V6.6은 SOA 기반 다조직 엔터프라이즈 인터넷 애플리케이션 플랫폼으로 명시된다. 실무적으로 거의 모든 업무 테이블에 `Org` 컬럼이 존재해 조직 단위로 데이터가 분리된다. `(신뢰도: 문서화됨/커뮤니티)` `[출처: https://www.szyonyou.net/a/price/415.html]`
- 메타데이터 파일 위치(설치 환경): `...\UBFV50\U9.VOB.Product.Metadata`. `(신뢰도: 커뮤니티)` `[출처: https://blog.csdn.net/weixin_30617797/article/details/99006340]`

---

## 2. 테이블 명명 규약 (命名规范)

관찰된 규약은 **`모듈접두어_엔티티명`** 형태다. `(신뢰도: 커뮤니티, 관찰 기반)`

| 접두어 | 의미(추정) | 예시 테이블 |
|--------|-----------|------------|
| `CBO_` | 공공기초객체(公共基础对象, Common Base Object) — 마스터/기초 데이터 | `CBO_ItemMaster`, `CBO_Organization`, `CBO_Department`, `CBO_Supplier`, `CBO_Customer`, `CBO_Wh`, `CBO_Category`, `CBO_ItemStatus`, `CBO_BOMMaster` |
| `Base_` | 시스템 기초 데이터 | `Base_Currency`, `Base_Organization_Trl` |
| `PM_` | 구매관리(采购, Purchase Management) | `PM_PurchaseOrder`, `PM_POLine`, `PM_POShipLine`, `PM_Receivement`, `PM_RcvLine` |
| `PPR_` | 구매가격(采购价格, Purchase Price 추정) | `PPR_PurPriceList`, `PPR_PurPriceLine` |
| `SM_` | 판매관리(销售, Sales Management) | `SM_SOOrder` |
| `InvDoc_` | 재고 단거(库存单据, Inventory Document) | `InvDoc_MiscShip`, `InvDoc_MiscShipL`, `InvDoc_TransferIn`, `InvDoc_TransInLine`, `InvDoc_TransInSubLine` |
| `IC_` | 재고/원가(库存成本, Inventory Cost 추정) | `IC_ItemCost` |

`[출처: https://www.cnblogs.com/friend/p/18349234]` `[출처: https://blog.csdn.net/u014287572/article/details/135689794]`

### 2-1. 헤더(主表)-상세(子表) 명명 패턴
- 헤더 엔티티명 + `Line` / `L` 접미어로 상세 테이블을 만든다. 예: `PM_Receivement`(헤더) ↔ `PM_RcvLine`(상세), `PM_PurchaseOrder` ↔ `PM_POLine`, `InvDoc_MiscShip` ↔ `InvDoc_MiscShipL`. `(신뢰도: 커뮤니티)`
- **3단 계층**도 존재한다. 예: `InvDoc_TransferIn`(헤더) → `InvDoc_TransInLine`(행) → `InvDoc_TransInSubLine`(서브행). `(신뢰도: 커뮤니티)` `[출처: https://blog.csdn.net/u014287572/article/details/135689794]`

### 2-2. 다국어(翻译) 테이블
- 다국어 명칭은 별도 **`_Trl`** 접미어 테이블에 분리 저장한다(Translation). 예: `CBO_ItemMaster_Trl`, `CBO_Wh_Trl`, `CBO_Supplier_Trl`, `CBO_Department_Trl`, `CBO_Operators_Trl`. `(신뢰도: 커뮤니티)` `[출처: https://www.cnblogs.com/friend/p/18349234]`

### 2-3. 스키마(schema) 구분
- SQL Server `schema`(예: dbo 외 별도 스키마) 단위 구분 방식은 **공개 자료 부족**. 관찰된 테이블은 모두 접두어로 모듈을 구분하며, 스키마명이 아닌 테이블명 접두어가 사실상의 네임스페이스 역할로 보인다. `(신뢰도: 추정)`

---

## 3. 공통 시스템/감사 컬럼 (系统字段/公共字段) — 노이즈 필터링 핵심

`CBO_ItemMaster` 실측 컬럼 및 여러 SQL 예제에서 반복 확인된 공통 컬럼이다. `(신뢰도: 커뮤니티, 실제 SQL 관찰)`

| 컬럼명 | 의미 | 비고 |
|--------|------|------|
| `ID` | 기본키(대리키) | 숫자형 서러게이트 키 (아래 4장) |
| `Org` | 소속 조직(组织) | 멀티조직 필터링 핵심. 대부분 업무 테이블에 존재 |
| `MasterOrg` | 통제/주 조직(控制组织) | 마스터 데이터 공유 범위 |
| `Code` | 코드(编码) | 업무 키 |
| `Name` | 명칭 | (다국어는 `_Trl`) |
| `CreatedBy` | 생성자(创建人) | 감사 |
| `CreatedOn` | 생성일시(创建时间) | 감사 |
| `ModifiedBy` | 최종 수정자(修改人) | 감사 |
| `ModifiedOn` | 최종 수정일시(修改时间) | 감사 / 낙관적 동시성 후보 |
| `SysMlFlag` | 시스템 다국어 플래그(多语言标志) | 다국어 처리 |
| `State` | 승인 상태 | 0=开立(개설/대기), 1=审核中(승인중), 2=已核准(승인완료) |
| `Status` | 업무 상태 코드 | `CBO_ItemStatus` 등 코드 테이블 참조 |
| `Effective_IsEffective` | 유효 여부(有效性) | **삭제/비활성 플래그 역할** — 노이즈 필터링에 중요 |
| `Effective_EffectiveDate` | 유효 시작일 | |
| `Effective_DisableDate` | 유효 종료일(비활성일) | |

`[출처: https://www.cnblogs.com/xychen/p/17961268]` `[출처: https://www.cnblogs.com/friend/p/18349234]`

> ⚠️ **모듈/버전별 변형 주의.** 일부 오래된/타 모듈 테이블(예 BOM·ECN 계열)은 `CreateUser`/`CreateDate`(또는 `CreateTime`)/`ModifyUser`/`ModifyDate`(또는 `ModifyTime`) 형태의 다른 명명을 쓴다는 관찰이 있다. 즉 **`CreatedBy/CreatedOn` 계열과 `CreateUser/CreateDate` 계열이 혼재**할 수 있다. `(신뢰도: 커뮤니티)` `[출처: https://blog.csdn.net/hch271510994/article/details/53953924]`
>
> - **명시적 논리삭제(IsDeleted) 컬럼**의 존재 여부는 **공개 자료 부족**. U9은 물리삭제보다 `Effective_*` / `State`로 라이프사이클을 통제하는 패턴으로 보인다. `(신뢰도: 추정)`

---

## 4. 기본키(PK)/외래키(FK) 전략

- PK는 **`ID`** 라는 단일 **대리키(surrogate key)** 다. `(신뢰도: 커뮤니티)`
- ID 타입은 관찰된 값이 모두 대형 정수(숫자형)이며 GUID(`uniqueidentifier`) 형태가 아니다 → **`bigint`/Int64(long) 서러게이트 키로 추정**. UBF 플랫폼이 전역 OID를 생성하는 구조로 보이나, "bigint" 명시 공식 문서는 확인 못 함. `(신뢰도: 추정, 커뮤니티 관찰 기반)`
- **헤더-상세 연결**: 상세 테이블에 **부모 엔티티명과 동일한 컬럼**을 두어 헤더 `ID`를 참조한다. 예: `PM_RcvLine.Receivement` → `PM_Receivement.ID`. 즉 **FK 컬럼명 = 부모 엔티티명**. `(신뢰도: 커뮤니티, 실제 조인 관찰)` `[출처: https://www.cnblogs.com/shihua513/p/16925235.html]`
- **참조(마스터) FK**: 코드성/마스터 참조도 대상 엔티티명을 컬럼명으로 사용(예: `CostCurrency` → `Base_Currency`, `MainItemCategory` → `CBO_Category`, `Status` → `CBO_ItemStatus`). `(신뢰도: 커뮤니티)`
- **플렉스 필드(Flex Field)**: `DescFlexField_*`(예 `DescFlexField_PubDescSeg4`), `KeyFlexFieldStru`, `NameKeyFlexFieldStru` 형태의 확장/코드구조 컬럼이 존재. 사용자 정의 확장 영역으로 추정. `(신뢰도: 커뮤니티)` `[출처: https://www.cnblogs.com/xychen/p/17961268]`

---

## 5. 단거(单据, 문서) 구조

- 문서번호 컬럼은 **`DocNo`(单据编号)**, 상세 행번호는 **`DocLineNo`(行号)**. `(신뢰도: 커뮤니티)` `[출처: https://www.cnblogs.com/friend/p/18349234]`
- 문서 상태(状态)는 `State`(승인 워크플로: 0=开立, 1=审核中/核准中, 2=已核准 등)와 `Status`(업무 상태, 예 수취 완료=5)로 관리된다. **단, 동일 필드명이라도 단거 유형별로 값의 의미가 다를 수 있음.** `(신뢰도: 커뮤니티)` `[출처: https://blog.csdn.net/qq_39179309/article/details/131539116]`
- 상태 전이는 **DocEngine(문서 엔진)** 이 `setDocState`로 관리하며 단거 라이프사이클 전체 업데이트를 트리거한다. `(신뢰도: 커뮤니티)`
- **문서 흐름(document flow, 단거 연결)**: 상세 행에 원천 단거 참조 컬럼 **`SrcDoc_SrcDocSubLine_EntityID`**(원천 단거 서브행 엔티티 ID)와 **`SrcDocType`**(원천 단거 유형, 예 1=구매주문)을 두어 상류 단거로 추적한다. 예: `PM_RcvLine.SrcDoc_SrcDocSubLine_EntityID` → `PM_POShipLine.ID`. `(신뢰도: 커뮤니티, 실제 조인 관찰)` `[출처: https://www.cnblogs.com/shihua513/p/16925235.html]`

> 힌트: `SrcDoc_*` / `SrcDocType` 계열 컬럼은 **단거 간 계보(주문→출하→입고→매입 등) 재구성의 핵심 단서**다.

---

## 6. 모듈 목록과 테이블군 (알려진 것만)

`(신뢰도: 커뮤니티)` `[출처: https://www.cnblogs.com/friend/p/18349234]` `[출처: https://blog.csdn.net/u014287572/article/details/135689794]`

- **기초/마스터 (CBO_/Base_)**: `CBO_ItemMaster`(품목 주档/마스터) + `CBO_ItemMaster_Trl`, `CBO_Organization`, `CBO_Department`, `CBO_Supplier`, `CBO_Customer`, `CBO_Operators`(업무원), `CBO_Wh`(창고), `CBO_Category`, `CBO_ItemStatus`, `Base_Currency`.
- **구매(采购, PM)**: `PM_PurchaseOrder`/`PM_POLine`/`PM_POShipLine`(주문·행·출하행), `PM_Receivement`/`PM_RcvLine`(입고·행), 가격 `PPR_PurPriceList`/`PPR_PurPriceLine`.
- **구매요청(采购申请/请购)**: 별도 엔티티 존재로 추정되나 **정확한 테이블명 공개 자료 부족**(접두어는 `PM_` 계열로 추정). `(신뢰도: 추정)`
- **판매·매출(销售, SM)**: `SM_SOOrder`(판매주문). 상세/출하 테이블명은 헤더-상세 패턴상 `SM_SO*Line` 형태로 추정되나 미확인. `(신뢰도: 커뮤니티/추정)`
- **재고·입출고(库存, InvDoc_)**: `InvDoc_MiscShip`/`_MiscShipL`(기타 출고), `InvDoc_TransferIn`/`_TransInLine`/`_TransInSubLine`(이동/조정). 창고=`CBO_Wh`. `(신뢰도: 커뮤니티)`
- **생산·제조(生产/制造)**: BOM `CBO_BOMMaster`/`CBO_BOMVersion`/`CBO_BOMComponent`, 공정 `CBO_Routing`/`CBO_Operation`/`CBO_OpResource`. 생산오더(工单)는 별도 엔티티(단거 상태 예시가 生产订单)로 존재하나 **정확한 테이블명 미확인**. `(신뢰도: 커뮤니티/추정)`
- **원가·비용(成本/费用)**: `IC_ItemCost`(품목 원가). 그 외 세부 원가 테이블 **공개 자료 부족**. `(신뢰도: 커뮤니티/추정)`
- **재무(财务: 总账 GL / 应收 AR / 应付 AP)**: 모듈 존재는 문서화됨(총장·응수관리 등)이나, **구체 테이블명(GL_/AR_/AP_ 등) 공개 자료 부족**. `(신뢰도: 추정)` `[출처: https://youyougd.com/hkj/xinwendongtai/1251.html]`

---

## 7. 열거형(枚举/enum)·코드 테이블

- 열거형 값은 **정수(integer)로 저장**된다(예 `State` 0/1/2, `SrcDocType` 1). `(신뢰도: 커뮤니티, 관찰)` `[출처: https://blog.csdn.net/qq_39179309/article/details/131539116]`
- enum 정의 자체는 DB가 아니라 **UBF 메타데이터(枚举)** 에 정의되며, 데이터 권한 등도 열거값으로 배정된다. 따라서 정수코드→의미 매핑은 DB만으로는 알 수 없고 메타데이터/문서가 필요하다. `(신뢰도: 커뮤니티)` `[출처: https://blog.csdn.net/aoroushe7628/article/details/101361021]`
- 코드성(참조) 데이터는 `CBO_`(예 `CBO_ItemStatus`, `CBO_Category`) 등 마스터 테이블에 정의되고 FK로 참조된다. `(신뢰도: 커뮤니티)`

---

## 8. 동시성/부수 데이터 (세션/잠금/임시/로그)

- **낙관적 동시성**: `ModifiedOn`(수정일시)이 변경 감지/충돌 판단에 쓰이는 것으로 추정되나, 전용 `RowVersion`/`timestamp`/`SysVersion` 컬럼의 표준 여부는 **공개 자료 부족**. `(신뢰도: 추정)`
- 세션/잠금/임시/로그성 전용 테이블·컬럼 패턴(수십 명 동시 사용 환경에서 생기는 것)은 **공개 자료 부족**. 다만 U9은 UBF 플랫폼/DocEngine이 트랜잭션·잠금을 애플리케이션 계층에서 관리하는 구조라, 물리 잠금 테이블보다 **감사 컬럼(`ModifiedBy/ModifiedOn`) + 상태(`State`)** 로 흐름을 통제하는 것으로 보인다. `(신뢰도: 추정)`
- 노이즈 필터링 실무 힌트(추정): `_Trl`(다국어), `DescFlexField_*`/`KeyFlexField*`(확장 필드), `SysMlFlag`, 미사용 플래그 컬럼(`Is*Enable`)은 데이터 분석 시 부수 데이터일 가능성이 크다.

---

## 9. 공개 데이터 사전/리소스

`(신뢰도: 커뮤니티)`
- U9 SQL 쿼리·테이블 종합 정리(博客园): `[출처: https://www.cnblogs.com/friend/p/18349234]`
- 품목(料品) 전체 컬럼 SQL(博客园 미러): `[출처: https://www.cnblogs.com/xychen/p/17961268]`
- U9 구매/입고 SQL 리포트 예제(단거 연결·상태값): `[출처: https://www.cnblogs.com/shihua513/p/16925235.html]`
- U9 Cloud(U9C) DB 동기화 SQL·조직 테이블: `[출처: https://blog.csdn.net/u014287572/article/details/135689794]`
- U9/U9C 학습 리소스 모음(CSDN): `[출처: https://blog.csdn.net/2302_77974636/article/details/130495544]`
- "U9 데이터字典.zip" 다운로드형 자료 언급(CSDN, 원본 접근성 낮음): `[출처: https://blog.csdn.net/mm2286088551/article/details/129839984]`
- **실무 권장**: U9은 DB 갱신이 잦아 정적 데이터 사전이 뒤처지므로, **UBF의 BE(엔티티) 쿼리/실체 조회 리포트를 살아있는 데이터 사전으로 사용**하라는 커뮤니티 조언이 반복된다. `[출처: https://blog.csdn.net/yanyulong0/article/details/139785415]`

---

## ✅ 확정 검증이 필요한 항목 (실측 필수)

1. **`ID` 타입** — `bigint`/Int64 여부(GUID 아님은 강한 추정이나 컬럼 타입 실측 요).
2. **논리삭제 컬럼** — 별도 `IsDeleted` 유무 vs `Effective_IsEffective` 대체 여부.
3. **동시성 컬럼** — `RowVersion`/`timestamp`/`SysVersion` 등 전용 컬럼 존재 여부.
4. **감사 컬럼 명명 혼재** — `CreatedBy/CreatedOn` vs `CreateUser/CreateDate` 어느 규약이 어느 모듈/버전에 쓰이는지.
5. **판매(SM)·생산(工单)·재무(GL/AR/AP) 실제 테이블명** — 접두어·헤더/상세 명명 실측.
6. **enum 정수코드 → 의미 매핑표** — DB로는 불가, 메타데이터/문서 확보 필요(단거 유형별로 값 의미 상이).
7. **schema 구분** — dbo 단일 vs 다중 스키마 여부.
8. **`Org`/`MasterOrg` 실제 유효 조직 범위** — 멀티조직 데이터 파티셔닝 규칙.
9. **U9(온프레) vs U9C(클라우드) 스키마 차이** — 본 초안은 두 자료를 혼합했으므로 버전 간 컬럼 차이 검증 필요.

## ✅ 실측 검증 결과 (운영 `U9CEDB` @192.168.100.10, 서버명 U9CDB, 2026-07-25, snapshot_id=1)

Phase 1 도구로 **실제 운영 U9C**를 스캔해 아래 가정을 검증함(별도 U9C UAT는 없음. 192.168.110.8은 카탈로그 저장 서버).

- **규모**: 테이블 7,086 + 뷰 130 + 루틴 3,016 = 10,232 객체, 컬럼 279,445개.
- **선언 FK는 68개뿐** → 관계가 선언 FK가 아닌 값/코드 공유로 흐른다는 판단 강하게 확증. 값 기반 관계 발견 필수.
- **노이즈**: `_Trl` 등 부수 테이블 2,120개(29%), 시스템 컬럼 142,518개(전체 51%). 노이즈 분리 접근 유효.
- **ID 타입(§4)**: `bigint` 6,857개로 다수 확증. 단 예외 존재 — `uniqueidentifier` 40, `int` 15, 문자형 3. "전부 bigint" 단정 금지.
- **명명 접두어(§2)**: `CBO_`(1137), `SM_`(369), `InvDoc_`(281), `PM_`(205), `Base_`(194) 확인. 추가 확인 접두어 — `MO_`(251, 생산오더 유력), `MRP_`(197), `InvTrans_`(185), `CS_`(230), `HI_`(169), `CA_`(165), `PPB_`(152), `EAM_`(147, 설비), `FA_`(140, 자산), `UBF_`(212, 플랫폼).
- **문서 흐름(§5)**: `DocNo` 447개 테이블, `SrcDocType` 95개, `SrcDoc_SrcDocSubLine_EntityID` 17개, `SrcDoc*` 계열 컬럼 총 1,819개 실재 → Phase 3 코드 추적 근거 확보.
- **도메인 앵커 힌트**: 생산실적→`MO_`, 매출→`SM_`, 입출고→`InvDoc_`/`InvTrans_`, 구매/구매요청→`PM_`, 비용→`CA_`/`FA_` 계열부터 조사 시작 권장(실측 델타 프로빙으로 확정).

## 참고 링크 (전체)

- https://yonyou.eu/products/u9/ (문서화됨, SOA)
- http://www.yonyou.com/global/introduce.html (문서화됨)
- https://u9cloud.yonyou.com/news/detailes/news/764 (문서화됨, UAP)
- https://www.wenkub.com/doc-21298231.html (UBF 개발 매뉴얼)
- https://www.cnblogs.com/friend/p/18349234 (핵심 테이블/SQL)
- https://www.cnblogs.com/xychen/p/17961268 (ItemMaster 전체 컬럼)
- https://www.cnblogs.com/shihua513/p/16925235.html (단거 연결/상태)
- https://blog.csdn.net/u014287572/article/details/135689794 (U9C 조직/동기화)
- https://blog.csdn.net/qq_39179309/article/details/131539116 (SQL 종합/상태값)
- https://blog.csdn.net/hch271510994/article/details/53953924 (감사 컬럼 변형)
- https://blog.csdn.net/aoroushe7628/article/details/101361021 (열거값/권한)
- https://blog.csdn.net/yanyulong0/article/details/139785415 (BE 엔티티=데이터 사전)
- https://blog.csdn.net/weixin_43050480/article/details/143168159 (설치/SQL Server)
- https://blog.csdn.net/weixin_30600197/article/details/99006302 (.NET 배포)
