# CLAUDE.md — HR 인사기록카드 시스템 (pcard)

> AI 에이전트의 **모든 세션에 자동 포함**되는 프로젝트 규약 파일입니다. PRD 전체 대신 이 파일 + 해당 Phase 작업 지시서를 컨텍스트로 사용하세요. 상세는 `docs/PRD.md` 참조.

## 1. 프로젝트 한 줄 요약
전 직원(300~1,000명)의 인사기록카드(기본정보·경력·교육·자격·상벌·계약 이력)·연간 평가·KPI를 관리하는 **온프레미스 사내 웹 시스템**. 외부 연동 없음, 신규 구축, 다국어(한·영·베).

## 2. 기술 스택 고정 (변경 금지 — 추가 시 사전 승인)
- 언어: **TypeScript 5.4+** (프론트·백 공통)
- 프론트: React 18.3, Vite 5, MUI 5, react-i18next, TanStack Query 5, Zustand
- 백엔드: Node.js 20 LTS, NestJS 10.3, Prisma 5
- DB: PostgreSQL 16
- 테스트: Jest(단위/통합), Playwright(E2E), k6(성능)
- 인프라: Docker Compose, Nginx
- 패키지: **pnpm** (`pnpm-lock.yaml` 커밋 필수)

> 목록에 없는 라이브러리가 필요하면 **코드 작성 전** 사유·대안을 보고하고 승인받을 것.

## 3. 디렉토리 구조
```
pcard/
├─ apps/
│  ├─ api/        # NestJS — modules: auth, employee, career, education,
│  │             #   certificate, discipline, contract, evaluation, kpi, audit, common
│  └─ web/        # React SPA — features/, components/, locales/{ko,en,vi}/
├─ packages/shared/   # 공통 타입·상수
├─ prisma/            # schema.prisma, migrations/, seed.ts
├─ docs/              # PRD.md, phase-*.md
├─ CLAUDE.md
└─ docker-compose.yml
```

## 4. 네이밍 & 컨벤션
- 파일: kebab-case / 클래스: PascalCase / 변수·함수: camelCase
- DB 테이블·컬럼: snake_case
- 기능 ID: `F-<모듈>-<번호>` (예: F-EMP-001), 모든 기능은 대응 테스트 보유
- 주석: 한국어 허용, 공개 API/타입은 영문 권장
- 포매팅: ESLint + Prettier (Phase 0 설정, 커밋 전 `pnpm lint` 통과)

## 5. 금지 사항 (Guardrails)
1. 프로덕션 DB 직접 스키마/데이터 변경 금지 → **마이그레이션 파일 경유만**
2. 비밀키·비밀번호·토큰 하드코딩 금지 → `.env`/시크릿
3. 시드·테스트에 **실제 개인정보 금지** → 더미 데이터(주민번호는 체크섬만 유효한 가짜)
4. 테스트 통과 목적의 테스트 삭제·완화 금지 (수정 시 사유 보고)
5. PRD 미정의 기능 임의 추가 금지 (제안 가능, 구현 전 승인)
6. 외부 API·메일 발송 등 부수효과는 개발 환경에서 **mock**

## 6. 보안·개인정보 핵심 규칙
- 암호화 저장(AES-256): 주민/외국인번호, 연락처, 연봉, 상벌 사유
- 비밀번호: bcrypt(cost ≥ 12) / 전송: TLS 1.2+
- 권한: **RBAC + 데이터 범위 필터**(본인/부서/전사) — 6개 역할(EMPLOYEE, MANAGER, HR_STAFF, HR_ADMIN, EXECUTIVE, SYS_ADMIN). 매트릭스는 PRD §8.2
- **모든 생성/수정/삭제는 트랜잭션 내에서 audit_log(이전값→이후값) 기록**
- 권한 없는 사용자에게 민감 필드는 마스킹(예: 주민번호 `******-*******`)
- 로그에 평문 민감정보 금지(마스킹)

## 7. 시간대·다국어
- 저장은 **UTC(TIMESTAMPTZ)**, 표시 시 로캘 변환(KST=UTC+9, ICT=UTC+7)
- i18n: `locales/{ko,en,vi}/*.json`, 기본 한국어. `Accept-Language` 헤더 존중

## 8. 완료 판정 규칙
- Phase 완료 = **자동 테스트 전체 통과 + 사람 검수 통과** 둘 다
- Phase 종료 시 보고: 변경 파일 목록 / 테스트 결과 요약 / 알려진 한계
- 방향 오류 검수 시 해당 Phase 브랜치 폐기·재실행(잘못된 기반 위 누적 금지)

## 9. 자주 쓰는 명령어
```bash
pnpm install              # 의존성 설치
pnpm dev                  # 개발 서버(api+web)
pnpm lint                 # ESLint + Prettier 검사
pnpm test                 # 단위/통합 테스트
pnpm test:e2e             # Playwright E2E
pnpm prisma migrate dev   # 마이그레이션 생성/적용(개발)
pnpm prisma db seed       # 시드 적재
docker compose up -d      # 로컬 스택 기동
```

## 10. 작업 순서 (Phase)
P0 골격 → P1 DB → P2 인증/권한 → P3 직원/인사기록 → P4 이력(경력·교육·자격·상벌·계약) → P5 평가 → P6 KPI → P7 다국어/UX → P8 통합/성능/보안 → P9 배포/운영. 각 Phase 착수 전 해당 Open Question(PRD §24) 해소 확인.
