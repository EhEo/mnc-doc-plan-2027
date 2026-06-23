# Phase 1 작업 지시서 — DB 스키마 + 마이그레이션 + 시드

> 대상: AI 에이전트 / 선행: Phase 0(골격·CI) 완료, **Open Question Q3(개인정보 보존정책·베트남 규제) 해소 필수**. 함께 참조: `CLAUDE.md`, `docs/PRD.md` §6.

## 1. 목표
PostgreSQL 16 + Prisma 5로 인사기록카드 시스템의 전체 데이터 모델을 정의하고, 마이그레이션과 시드(가상 데이터)를 구성한다. 이후 모든 Phase가 이 스키마 위에서 동작한다.

## 2. 범위 (산출물)
- `prisma/schema.prisma` — 전체 엔티티
- `prisma/migrations/` — 초기 마이그레이션
- `prisma/seed.ts` — 공통코드 + 가상 직원/이력 데이터
- `apps/api/test/schema.spec.ts` — 스키마·제약 검증 테스트

## 3. 엔티티 정의 (전체)

### 3.1 department (부서)
| 컬럼 | 타입 | NULL | 제약 | 설명 |
|------|------|------|------|------|
| id | BIGSERIAL | N | PK | |
| code | VARCHAR(20) | N | UNIQUE | 부서코드 |
| name_ko | VARCHAR(100) | N | | 부서명(한) |
| name_en | VARCHAR(100) | Y | | 부서명(영) |
| name_vi | VARCHAR(100) | Y | | 부서명(베) |
| parent_id | BIGINT | Y | FK→department | 상위부서 |
| created_at/updated_at/deleted_at | TIMESTAMPTZ | | | 공통 |

### 3.2 employee (직원/인사기록카드 마스터)
PRD §6.2 employee 표 전체 적용. 핵심 제약: `emp_no` UNIQUE, `rrn_enc`/`phone_enc` BYTEA(AES-256), `status` CHECK(ACTIVE/LEAVE/RESIGNED), `employment_type` CHECK(REGULAR/CONTRACT/DISPATCH), `dept_id` FK→department, `grade_code` FK→code.

### 3.3 이력 테이블 (공통 패턴: id PK, employee_id FK, created_at/updated_at/deleted_at)
- **career**: company_name, dept, position, duty, start_date, end_date(NULL=재직중)
- **education**: title, institution, type CHECK(INTERNAL/EXTERNAL/MANDATORY), completed_date, hours(≥0), is_completed
- **certificate**: name, issuer, acquired_date, expiry_date(Y), cert_no
- **discipline**: type CHECK(REWARD/PENALTY), reason(암호화), date, doc_ref, action_detail — **변경 시 reason 필수**
- **contract**: type CHECK(REGULAR/CONTRACT/ANNUAL), start_date, end_date, salary(암호화), work_place, file_path

### 3.4 인증/권한
- **user_account**: id, login_id(UNIQUE), password_hash(bcrypt), employee_id FK(UNIQUE), is_locked, failed_count, last_login_at
- **role**: id, code(UNIQUE: EMPLOYEE/MANAGER/HR_STAFF/HR_ADMIN/EXECUTIVE/SYS_ADMIN), name
- **user_role**: user_id FK, role_id FK (복합 PK)

### 3.5 평가
- **evaluation_cycle**: id, year, type CHECK(ANNUAL/HALF), grade_scale(JSONB), period_start, period_end, status
- **evaluation**: id, cycle_id FK, employee_id FK, stage CHECK(FIRST/SECOND), score_json(JSONB), total_score, grade, comment, status CHECK(DRAFT/CONFIRMED), evaluator_id FK, UNIQUE(cycle_id, employee_id, stage)

### 3.6 KPI
- **kpi_def**: id, name, description, unit, target_value, weight, year, scope CHECK(COMPANY/DEPT/INDIVIDUAL)
- **kpi_target**: id, kpi_def_id FK, employee_id FK(Y), dept_id FK(Y), target_value, weight — 배정 단위별 가중치 합=100% 검증(앱 레벨)
- **kpi_result**: id, kpi_target_id FK, period, actual_value, achievement_rate, confirmed_at

### 3.7 감사/공통
- **audit_log**: PRD §6.2 audit_log 표 전체(actor_user_id, action, entity, entity_id, before_json, after_json, reason, created_at)
- **code**: group_code, code, name_ko/en/vi, sort_order — 공통코드(직급·자격종류 등)

## 4. 인덱스
PRD §6.2 인덱스 + 각 이력 테이블 `(employee_id, deleted_at)` 복합 인덱스, `kpi_target(employee_id, year)`, `user_account(login_id)` UNIQUE.

## 5. 시드 데이터 규칙
- 공통코드(부서 10개, 직급 6개, 고용형태, 자격종류) 적재
- 6개 역할 적재
- **가상 직원 30명 + 각 직원 이력 2~3건** — 실제 개인정보 사용 금지. 이름은 더미, 주민번호는 체크섬만 유효한 가짜, 연락처/연봉은 더미값. 베트남 직원 일부 포함(name_vi, nationality=VN)
- SYS_ADMIN·HR_ADMIN 테스트 계정 각 1개

## 6. 완료 판정 기준 (기계 검증)
- [ ] `pnpm prisma migrate dev` 성공, `pnpm prisma migrate status` clean
- [ ] `pnpm prisma db seed` 성공 — 30명 + 공통코드 + 6역할 적재 확인
- [ ] `apps/api/test/schema.spec.ts` 통과: ① 전 테이블 존재 ② FK·UNIQUE·CHECK 제약 동작(중복 emp_no INSERT 실패, 잘못된 status 거부) ③ 암호화 컬럼 BYTEA 타입 ④ TIMESTAMPTZ 확인
- [ ] 시드 데이터에 실제 개인정보·평문 민감정보 없음(검증 스크립트)

## 7. 사람 검수 항목
- ERD가 PRD §6.2와 일치하는지
- 암호화 대상 컬럼(주민번호·연락처·연봉·상벌사유)이 BYTEA/암호화 처리되었는지
- 보존정책(Q3) 반영: 퇴사자·법정 보존기간 관련 컬럼(resign_date, 보관 플래그) 적절성
- 시드 가상 데이터에 실제 개인정보 미포함 확인

## 8. 롤백 단위
Git 브랜치 `phase/1`. 문제 시 브랜치 폐기 후 재실행. 마이그레이션 down 스크립트 보유.

## 9. 의존 Open Questions
- **Q3(개인정보 보존기간·베트남 규제) — 본 Phase 블로킹.** 보존기간/파기·마스킹 정책이 스키마(보관 컬럼·정책)에 영향. 미해소 시 착수 금지.
