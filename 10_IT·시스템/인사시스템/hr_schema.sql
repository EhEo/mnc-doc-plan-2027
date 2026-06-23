-- =============================================================================
--  M&C ELECTRONICS VINA — 인사시스템 (HR System)
--  파일명  : hr_schema.sql
--  기준    : 인사카드_양식_베트남법인.xlsx (6개 시트)
--  DB      : MySQL 8.0+ / MariaDB 10.6+
--  문자셋  : utf8mb4 (한국어·베트남어·이모지 지원)
--  작성일  : 2026-06-16
--
--  시트 → 테이블 매핑
--  ─────────────────────────────────────────────────────
--  [기준 테이블]
--    ref_departments       부서 코드표
--    ref_positions         직위 코드표
--    ref_salary_grades     급여등급 코드표
--    ref_employment_types  고용형태 코드표
--  [시트②] employees         직원 기본 인사카드
--  [시트③] promotion_history  진급 이력
--  [시트③] assignment_history 발령·전보 이력
--  [시트④] certifications     자격증·인증 목록
--  [시트⑤] performance_reviews  인사평가 (HR 전용)
--  [시트⑥] salary_grade_history 급여등급 변경 이력 (HR 전용)
-- =============================================================================

-- ─────────────────────────────────────────────────────
--  데이터베이스 생성
-- ─────────────────────────────────────────────────────
CREATE DATABASE IF NOT EXISTS hr_db
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_unicode_ci;

USE hr_db;

-- ─────────────────────────────────────────────────────
--  0-1. 부서 코드표  (ref_departments)
-- ─────────────────────────────────────────────────────
CREATE TABLE ref_departments (
  dept_code     VARCHAR(10)   NOT NULL COMMENT '부서 코드 (예: PROD, QC, HR)',
  dept_name_ko  VARCHAR(100)  NOT NULL COMMENT '부서명 (한국어)',
  dept_name_vn  VARCHAR(100)  NOT NULL COMMENT '부서명 (베트남어)',
  dept_name_en  VARCHAR(100)      NULL COMMENT '부서명 (영어)',
  parent_code   VARCHAR(10)       NULL COMMENT '상위 부서 코드 (NULL=최상위)',
  is_active     TINYINT(1)    NOT NULL DEFAULT 1 COMMENT '사용 여부 (1=활성)',
  created_at    DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at    DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (dept_code),
  FOREIGN KEY fk_dept_parent (parent_code)
    REFERENCES ref_departments (dept_code)
    ON UPDATE CASCADE ON DELETE SET NULL
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci
  COMMENT='부서 코드표 — Danh mục phòng ban';

-- 샘플 데이터
INSERT INTO ref_departments (dept_code, dept_name_ko, dept_name_vn, dept_name_en) VALUES
  ('MGMT',  '경영진',       'Ban Giám Đốc',           'Management'),
  ('HR',    '인사총무',      'Phòng Nhân Sự',          'Human Resources'),
  ('FIN',   '재무회계',      'Phòng Tài Chính',        'Finance & Accounting'),
  ('PROD',  '생산부',        'Phòng Sản Xuất',         'Production'),
  ('QC',    '품질관리',      'Phòng Quản Lý Chất Lượng','Quality Control'),
  ('MAINT', '설비유지보수',   'Phòng Bảo Trì',         'Maintenance'),
  ('PURCH', '구매',          'Phòng Mua Hàng',         'Purchasing'),
  ('SALES', '영업',          'Phòng Kinh Doanh',       'Sales'),
  ('IT',    'IT·시스템',     'Phòng Công Nghệ Thông Tin','IT & Systems'),
  ('LOG',   '물류창고',      'Phòng Kho Vận',          'Logistics');


-- ─────────────────────────────────────────────────────
--  0-2. 직위·직급 코드표  (ref_positions)
-- ─────────────────────────────────────────────────────
CREATE TABLE ref_positions (
  pos_code     VARCHAR(10)   NOT NULL COMMENT '직위 코드 (예: MGR, SUP, STAFF)',
  pos_name_ko  VARCHAR(80)   NOT NULL COMMENT '직위명 (한국어)',
  pos_name_vn  VARCHAR(80)   NOT NULL COMMENT '직위명 (베트남어)',
  pos_level    TINYINT       NOT NULL COMMENT '직급 레벨 (1=임원, 높을수록 하위)',
  is_active    TINYINT(1)    NOT NULL DEFAULT 1,
  PRIMARY KEY (pos_code)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci
  COMMENT='직위·직급 코드표';

INSERT INTO ref_positions (pos_code, pos_name_ko, pos_name_vn, pos_level) VALUES
  ('DIR',    '이사 / 법인장',     'Giám Đốc',                 1),
  ('VDIR',   '부이사',            'Phó Giám Đốc',             2),
  ('MGR',    '팀장 / 매니저',     'Trưởng Phòng',             3),
  ('VMGR',   '부팀장',            'Phó Phòng',                4),
  ('SUP',    '감독·주임',         'Trưởng Ca / Tổ Trưởng',    5),
  ('STAFF',  '사원',              'Nhân Viên',                6),
  ('WORKER', '생산직 (기능직)',    'Công Nhân Sản Xuất',       7),
  ('TEMP',   '계약직·임시직',     'Nhân Viên Hợp Đồng',       8);


-- ─────────────────────────────────────────────────────
--  0-3. 급여등급 코드표  (ref_salary_grades)
-- ─────────────────────────────────────────────────────
CREATE TABLE ref_salary_grades (
  grade_code    VARCHAR(10)   NOT NULL COMMENT '급여등급 코드 (예: G1, G2 … G10)',
  grade_desc_ko VARCHAR(100)  NOT NULL COMMENT '등급 설명 (한국어)',
  grade_desc_vn VARCHAR(100)  NOT NULL COMMENT '등급 설명 (베트남어)',
  effective_from DATE         NOT NULL COMMENT '적용 시작일',
  effective_to   DATE             NULL COMMENT '적용 종료일 (NULL=현행)',
  is_active      TINYINT(1)   NOT NULL DEFAULT 1,
  PRIMARY KEY (grade_code, effective_from)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci
  COMMENT='급여등급 코드표 — Bảng bậc lương (코드만 관리, 실수령액 미저장)';

INSERT INTO ref_salary_grades (grade_code, grade_desc_ko, grade_desc_vn, effective_from) VALUES
  ('G1',  '1등급 — 임원',           'Bậc 1 — Giám đốc',      '2024-01-01'),
  ('G2',  '2등급 — 부이사·팀장',    'Bậc 2 — Phó GĐ / TP',   '2024-01-01'),
  ('G3',  '3등급 — 선임팀장',       'Bậc 3 — Trưởng phòng',  '2024-01-01'),
  ('G4',  '4등급 — 주임·감독',      'Bậc 4 — Tổ trưởng',     '2024-01-01'),
  ('G5',  '5등급 — 선임사원',       'Bậc 5 — NV cấp cao',    '2024-01-01'),
  ('G6',  '6등급 — 사원',           'Bậc 6 — Nhân viên',     '2024-01-01'),
  ('G7',  '7등급 — 생산직 숙련',    'Bậc 7 — CN lành nghề',  '2024-01-01'),
  ('G8',  '8등급 — 생산직 일반',    'Bậc 8 — Công nhân',     '2024-01-01'),
  ('G9',  '9등급 — 수습',           'Bậc 9 — Thử việc',      '2024-01-01'),
  ('G10', '10등급 — 인턴',          'Bậc 10 — Thực tập sinh','2024-01-01');


-- ─────────────────────────────────────────────────────
--  0-4. 고용형태 코드표  (ref_employment_types)
-- ─────────────────────────────────────────────────────
CREATE TABLE ref_employment_types (
  emp_type_code VARCHAR(10)  NOT NULL COMMENT '고용형태 코드',
  name_ko       VARCHAR(80)  NOT NULL,
  name_vn       VARCHAR(80)  NOT NULL,
  PRIMARY KEY (emp_type_code)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci
  COMMENT='고용형태 코드표 — Loại hợp đồng';

INSERT INTO ref_employment_types VALUES
  ('PERM',    '정규직',       'Hợp đồng không xác định thời hạn'),
  ('FIXED1',  '계약직 1년',   'Hợp đồng 1 năm'),
  ('FIXED2',  '계약직 2년',   'Hợp đồng 2 năm'),
  ('PROB',    '수습',         'Thử việc'),
  ('INTERN',  '인턴',         'Thực tập');


-- ─────────────────────────────────────────────────────
--  1. 직원 기본 인사카드  (employees)  ← 시트②
-- ─────────────────────────────────────────────────────
CREATE TABLE employees (
  -- ── 식별자 ──────────────────────────────────────────
  emp_id          CHAR(10)      NOT NULL COMMENT '직원번호 (Mã nhân viên) — PK',

  -- ── A. 기본정보 ─────────────────────────────────────
  full_name_vn    VARCHAR(100)  NOT NULL COMMENT '성명 (베트남어) — Họ và tên',
  full_name_ko    VARCHAR(100)      NULL COMMENT '성명 (한국어) — 선택',
  full_name_en    VARCHAR(100)      NULL COMMENT '성명 (영문) — Tên tiếng Anh',
  birth_year_month CHAR(7)          NULL COMMENT '생년월일 YYYY-MM (주민번호 미저장 원칙)',
  gender          ENUM('M','F','X') NULL COMMENT '성별 (M=남/Nam, F=여/Nữ, X=미입력)',
  nationality     VARCHAR(50)   NOT NULL DEFAULT 'VN' COMMENT '국적 (ISO 2자리 코드 권장)',
  key_personnel   ENUM('A','B','C','-') NOT NULL DEFAULT '-'
                                COMMENT '핵심인원 등급 A(핵심)/B(중요)/C(잠재)/-',
  photo_path      VARCHAR(500)      NULL COMMENT '증명사진 파일 경로 (3×4cm, 서면동의 필수)',

  -- ── B. 연락처 ───────────────────────────────────────
  email_company   VARCHAR(150)      NULL COMMENT '업무 이메일 — Email công ty',
  phone_company   VARCHAR(20)       NULL COMMENT '업무 전화 — Điện thoại công ty',
  address_home    VARCHAR(300)      NULL COMMENT '자택주소 — Địa chỉ nhà',
  emergency_name  VARCHAR(100)      NULL COMMENT '비상연락처 성명 — Tên người liên hệ khẩn',
  emergency_rel   VARCHAR(50)       NULL COMMENT '비상연락처 관계 — Quan hệ',
  emergency_phone VARCHAR(20)       NULL COMMENT '비상연락처 전화',

  -- ── C. 직위·발령 정보 ───────────────────────────────
  hire_date       DATE          NOT NULL COMMENT '입사일 — Ngày vào công ty',
  emp_type_code   VARCHAR(10)   NOT NULL COMMENT '고용형태 — FK → ref_employment_types',
  dept_code       VARCHAR(10)   NOT NULL COMMENT '현재 부서 — FK → ref_departments',
  work_location   VARCHAR(100)      NULL COMMENT '근무지 — Địa điểm làm việc',
  pos_code        VARCHAR(10)   NOT NULL COMMENT '현재 직위 — FK → ref_positions',
  grade_code      VARCHAR(10)       NULL COMMENT '현재 급여등급코드 — FK → ref_salary_grades',

  -- ── D. 학력 ─────────────────────────────────────────
  education_level VARCHAR(50)       NULL COMMENT '최종학력 — Trình độ học vấn',
  graduation_year SMALLINT          NULL COMMENT '졸업연도 — Năm tốt nghiệp',
  school_name     VARCHAR(200)      NULL COMMENT '학교명 — Trường',
  major           VARCHAR(100)      NULL COMMENT '전공 — Chuyên ngành',

  -- ── E. 비고 ─────────────────────────────────────────
  notes           TEXT              NULL COMMENT '비고 — Ghi chú',

  -- ── 시스템 필드 ─────────────────────────────────────
  status          ENUM('ACTIVE','RESIGNED','LOA','SUSPENDED')
                                NOT NULL DEFAULT 'ACTIVE'
                                COMMENT '재직상태 (ACTIVE=재직, RESIGNED=퇴직, LOA=휴직)',
  resign_date     DATE              NULL COMMENT '퇴직일 (RESIGNED 시 입력)',
  card_updated_at DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                                COMMENT '인사카드 최종 업데이트 일시',
  created_by      VARCHAR(50)       NULL COMMENT '등록 담당자',
  updated_by      VARCHAR(50)       NULL COMMENT '최종 수정 담당자',
  created_at      DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at      DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

  -- ── 제약조건 ────────────────────────────────────────
  PRIMARY KEY (emp_id),
  KEY idx_emp_dept     (dept_code),
  KEY idx_emp_pos      (pos_code),
  KEY idx_emp_status   (status),
  KEY idx_emp_hire     (hire_date),
  CONSTRAINT fk_emp_dept     FOREIGN KEY (dept_code)      REFERENCES ref_departments    (dept_code)      ON UPDATE CASCADE,
  CONSTRAINT fk_emp_pos      FOREIGN KEY (pos_code)       REFERENCES ref_positions      (pos_code)       ON UPDATE CASCADE,
  CONSTRAINT fk_emp_emptype  FOREIGN KEY (emp_type_code)  REFERENCES ref_employment_types(emp_type_code) ON UPDATE CASCADE,
  CONSTRAINT fk_emp_grade    FOREIGN KEY (grade_code)     REFERENCES ref_salary_grades  (grade_code, effective_from)
    -- NOTE: 복합PK FK는 grade_code만 참조하려면 별도 단순 컬럼 또는 애플리케이션 레벨 관리 권장
    -- 실제 구현 시 grade_code 단일 컬럼 참조로 단순화 가능
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci
  COMMENT='직원 기본 인사카드 — Hồ sơ nhân sự (시트②)';


-- ─────────────────────────────────────────────────────
--  2. 진급 이력  (promotion_history)  ← 시트③-A
-- ─────────────────────────────────────────────────────
CREATE TABLE promotion_history (
  promo_id        BIGINT        NOT NULL AUTO_INCREMENT COMMENT '진급이력 ID (PK)',
  emp_id          CHAR(10)      NOT NULL COMMENT '직원번호 — FK → employees',
  promo_date      DATE          NOT NULL COMMENT '진급일 — Ngày thăng chức',
  pos_code_from   VARCHAR(10)       NULL COMMENT '이전 직위 코드',
  pos_code_to     VARCHAR(10)   NOT NULL COMMENT '신규 직위 코드',
  pos_level_from  TINYINT           NULL COMMENT '이전 직급 레벨',
  pos_level_to    TINYINT           NULL COMMENT '신규 직급 레벨',
  reason_ko       VARCHAR(300)      NULL COMMENT '진급 사유 (한국어)',
  reason_vn       VARCHAR(300)      NULL COMMENT '진급 사유 (베트남어)',
  approved_by     VARCHAR(50)       NULL COMMENT '승인자 — Người phê duyệt',
  notes           TEXT              NULL COMMENT '비고 — Ghi chú',
  created_by      VARCHAR(50)       NULL COMMENT '입력자',
  created_at      DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,

  PRIMARY KEY (promo_id),
  KEY idx_promo_emp  (emp_id),
  KEY idx_promo_date (promo_date),
  CONSTRAINT fk_promo_emp      FOREIGN KEY (emp_id)        REFERENCES employees    (emp_id)   ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_promo_pos_from FOREIGN KEY (pos_code_from) REFERENCES ref_positions(pos_code) ON UPDATE CASCADE,
  CONSTRAINT fk_promo_pos_to   FOREIGN KEY (pos_code_to)   REFERENCES ref_positions(pos_code) ON UPDATE CASCADE
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci
  COMMENT='진급 이력 — Lịch sử thăng chức (시트③-A)';


-- ─────────────────────────────────────────────────────
--  3. 발령·전보 이력  (assignment_history)  ← 시트③-B
-- ─────────────────────────────────────────────────────
CREATE TABLE assignment_history (
  assign_id       BIGINT        NOT NULL AUTO_INCREMENT COMMENT '발령이력 ID (PK)',
  emp_id          CHAR(10)      NOT NULL COMMENT '직원번호 — FK → employees',
  assign_date     DATE          NOT NULL COMMENT '발령일 — Ngày bổ nhiệm',
  assign_type     ENUM('TRANSFER','DISPATCH','RETURN','SECONDMENT','OTHER')
                                NOT NULL DEFAULT 'TRANSFER'
                                COMMENT '발령 유형 (TRANSFER=부서이동, DISPATCH=파견)',
  dept_code_from  VARCHAR(10)       NULL COMMENT '이전 부서 코드',
  dept_code_to    VARCHAR(10)   NOT NULL COMMENT '발령 부서 코드',
  pos_code        VARCHAR(10)       NULL COMMENT '발령 직위 코드',
  location_to     VARCHAR(100)      NULL COMMENT '발령 근무지',
  reason_ko       VARCHAR(300)      NULL COMMENT '발령 사유 (한국어)',
  reason_vn       VARCHAR(300)      NULL COMMENT '발령 사유 (베트남어)',
  approved_by     VARCHAR(50)       NULL COMMENT '승인자',
  notes           TEXT              NULL COMMENT '비고',
  created_by      VARCHAR(50)       NULL,
  created_at      DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,

  PRIMARY KEY (assign_id),
  KEY idx_assign_emp  (emp_id),
  KEY idx_assign_date (assign_date),
  CONSTRAINT fk_assign_emp      FOREIGN KEY (emp_id)         REFERENCES employees      (emp_id)   ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_assign_dept_f   FOREIGN KEY (dept_code_from) REFERENCES ref_departments(dept_code) ON UPDATE CASCADE,
  CONSTRAINT fk_assign_dept_t   FOREIGN KEY (dept_code_to)   REFERENCES ref_departments(dept_code) ON UPDATE CASCADE,
  CONSTRAINT fk_assign_pos      FOREIGN KEY (pos_code)       REFERENCES ref_positions  (pos_code)  ON UPDATE CASCADE
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci
  COMMENT='발령·전보 이력 — Lịch sử bổ nhiệm & luân chuyển (시트③-B)';


-- ─────────────────────────────────────────────────────
--  4. 자격증·인증 목록  (certifications)  ← 시트④
-- ─────────────────────────────────────────────────────
CREATE TABLE certifications (
  cert_id         BIGINT        NOT NULL AUTO_INCREMENT COMMENT '자격증 ID (PK)',
  emp_id          CHAR(10)      NOT NULL COMMENT '직원번호 — FK → employees',
  cert_name_ko    VARCHAR(200)  NOT NULL COMMENT '자격증·인증명 (한국어)',
  cert_name_vn    VARCHAR(200)      NULL COMMENT '자격증·인증명 (베트남어)',
  issuing_org     VARCHAR(200)      NULL COMMENT '발급기관 — Cơ quan cấp',
  issue_date      DATE              NULL COMMENT '취득일 — Ngày cấp',
  expiry_date     DATE              NULL COMMENT '유효기간 만료일 (NULL=영구)',
  is_expired      TINYINT(1)    NOT NULL DEFAULT 0 COMMENT '만료 여부 (자동 또는 수동 업데이트)',
  cert_file_path  VARCHAR(500)      NULL COMMENT '자격증 스캔본 파일 경로',
  notes           TEXT              NULL COMMENT '비고 — Ghi chú',
  created_by      VARCHAR(50)       NULL,
  created_at      DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at      DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

  PRIMARY KEY (cert_id),
  KEY idx_cert_emp    (emp_id),
  KEY idx_cert_expiry (expiry_date),
  CONSTRAINT fk_cert_emp FOREIGN KEY (emp_id) REFERENCES employees(emp_id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci
  COMMENT='자격증·인증 목록 — Chứng chỉ & bằng cấp (시트④)';


-- ─────────────────────────────────────────────────────
--  5. 인사평가 이력  (performance_reviews)  ← 시트⑤  [HR 전용]
--     ⚠ 접근 권한: HR 관리자·임원 전용
-- ─────────────────────────────────────────────────────
CREATE TABLE performance_reviews (
  review_id       BIGINT        NOT NULL AUTO_INCREMENT COMMENT '인사평가 ID (PK)',
  emp_id          CHAR(10)      NOT NULL COMMENT '직원번호 — FK → employees',
  review_year     YEAR          NOT NULL COMMENT '평가연도 — Năm đánh giá',
  review_period   ENUM('H1','H2','ANNUAL','Q1','Q2','Q3','Q4')
                                NOT NULL DEFAULT 'ANNUAL'
                                COMMENT '평가 시기 (H1=상반기, H2=하반기, ANNUAL=연간)',
  grade           ENUM('S','A','B','C')
                                NOT NULL COMMENT '평가등급 S(≥95)/A(≥85)/B(≥70)/C(<70)',
  score           DECIMAL(5,2)      NULL COMMENT '평가 점수 (0.00~100.00)',
  reviewer_id     CHAR(10)          NULL COMMENT '평가자 직원번호 — FK → employees',
  reviewer_name   VARCHAR(100)      NULL COMMENT '평가자 성명 (reviewer_id 없을 때)',
  summary_ko      TEXT              NULL COMMENT '종합 의견 (한국어)',
  summary_vn      TEXT              NULL COMMENT '종합 의견 (베트남어)',
  approved_by     VARCHAR(50)       NULL COMMENT '최종 승인자',
  approved_at     DATETIME          NULL COMMENT '승인 일시',
  created_by      VARCHAR(50)       NULL,
  created_at      DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at      DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

  PRIMARY KEY (review_id),
  UNIQUE KEY uq_review (emp_id, review_year, review_period)
                                COMMENT '동일 직원·연도·시기 중복 방지',
  KEY idx_review_year  (review_year),
  KEY idx_review_grade (grade),
  CONSTRAINT fk_review_emp      FOREIGN KEY (emp_id)      REFERENCES employees(emp_id) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_review_reviewer FOREIGN KEY (reviewer_id) REFERENCES employees(emp_id) ON DELETE SET NULL ON UPDATE CASCADE

  -- ⚠ 보안 권고:
  --   - 애플리케이션 레이어에서 ROLE = 'HR_MANAGER' | 'EXECUTIVE' 만 SELECT/INSERT/UPDATE 허용
  --   - 또는 MySQL Row-Level Security (MariaDB: 뷰 + DEFINER) 적용
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci
  COMMENT='인사평가 이력 [HR 관리자·임원 전용] — Đánh giá nhân sự (시트⑤)';


-- ─────────────────────────────────────────────────────
--  6. 급여등급 변경 이력  (salary_grade_history)  ← 시트⑥  [HR 전용]
--     ⚠ 접근 권한: HR 관리자·임원 전용
--     ⚠ 실수령 급여액 절대 미저장 — 등급 코드만 관리
-- ─────────────────────────────────────────────────────
CREATE TABLE salary_grade_history (
  sg_history_id   BIGINT        NOT NULL AUTO_INCREMENT COMMENT '급여등급이력 ID (PK)',
  emp_id          CHAR(10)      NOT NULL COMMENT '직원번호 — FK → employees',
  effective_date  DATE          NOT NULL COMMENT '발효일 — Ngày hiệu lực',
  grade_code_from VARCHAR(10)       NULL COMMENT '이전 급여등급 코드',
  grade_code_to   VARCHAR(10)   NOT NULL COMMENT '신규 급여등급 코드',
  reason_type     ENUM('HIRE','PROMOTION','REVIEW','ADJUSTMENT','OTHER')
                                NOT NULL DEFAULT 'ADJUSTMENT'
                                COMMENT '조정 사유 유형',
  reason_detail   VARCHAR(300)      NULL COMMENT '조정 사유 상세',
  approved_by     VARCHAR(50)   NOT NULL COMMENT '승인자 — Người phê duyệt',
  approved_at     DATETIME          NULL COMMENT '승인 일시',
  notes           TEXT              NULL COMMENT '비고',
  created_by      VARCHAR(50)       NULL,
  created_at      DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,

  PRIMARY KEY (sg_history_id),
  KEY idx_sg_emp  (emp_id),
  KEY idx_sg_date (effective_date),
  CONSTRAINT fk_sg_emp FOREIGN KEY (emp_id) REFERENCES employees(emp_id) ON DELETE CASCADE ON UPDATE CASCADE

  -- ⚠ 보안 권고: 위 performance_reviews 와 동일한 접근 제한 적용 필요
  -- ⚠ 실수령 급여(VND/USD 금액)는 별도 급여 원장 시스템(HR_Salary.xlsx 연동)에서 관리
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci
  COMMENT='급여등급 변경 이력 [HR 관리자·임원 전용] — Bậc lương (시트⑥)';


-- =============================================================================
--  VIEW: 현재 직원 기본 현황  (일반 HR 담당자용 — 제한 시트 컬럼 제외)
-- =============================================================================
CREATE OR REPLACE VIEW v_employee_summary AS
SELECT
  e.emp_id,
  e.full_name_vn,
  e.full_name_ko,
  e.full_name_en,
  e.gender,
  e.nationality,
  e.key_personnel,
  e.hire_date,
  et.name_ko   AS emp_type_name,
  d.dept_name_ko,
  d.dept_name_vn,
  p.pos_name_ko,
  p.pos_name_vn,
  p.pos_level,
  e.work_location,
  e.email_company,
  e.phone_company,
  e.education_level,
  e.status,
  e.card_updated_at
FROM employees e
LEFT JOIN ref_departments     d  ON e.dept_code     = d.dept_code
LEFT JOIN ref_positions       p  ON e.pos_code      = p.pos_code
LEFT JOIN ref_employment_types et ON e.emp_type_code = et.emp_type_code
WHERE e.status = 'ACTIVE';

COMMENT ON TABLE v_employee_summary IS
  '현재 재직 직원 기본 현황 (급여등급·인사평가 컬럼 제외) — HR 담당자 열람용';


-- =============================================================================
--  VIEW: 자격증 만료 임박 목록  (30일 이내)
-- =============================================================================
CREATE OR REPLACE VIEW v_cert_expiring_soon AS
SELECT
  c.cert_id,
  c.emp_id,
  e.full_name_vn,
  e.dept_code,
  d.dept_name_ko,
  c.cert_name_ko,
  c.issuing_org,
  c.expiry_date,
  DATEDIFF(c.expiry_date, CURDATE()) AS days_until_expiry
FROM certifications c
JOIN employees       e ON c.emp_id    = e.emp_id
JOIN ref_departments d ON e.dept_code = d.dept_code
WHERE
  c.expiry_date IS NOT NULL
  AND c.expiry_date BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 30 DAY)
ORDER BY c.expiry_date;


-- =============================================================================
--  인덱스 추가 (성능 최적화)
-- =============================================================================
-- 직원번호 + 발령일 복합 인덱스 (이력 조회 최적화)
ALTER TABLE promotion_history   ADD INDEX idx_promo_emp_date   (emp_id, promo_date DESC);
ALTER TABLE assignment_history  ADD INDEX idx_assign_emp_date  (emp_id, assign_date DESC);
ALTER TABLE certifications      ADD INDEX idx_cert_emp_expiry  (emp_id, expiry_date);
ALTER TABLE performance_reviews ADD INDEX idx_review_emp_year  (emp_id, review_year DESC);
ALTER TABLE salary_grade_history ADD INDEX idx_sg_emp_date     (emp_id, effective_date DESC);


-- =============================================================================
--  접근 권한 예시  (MySQL 사용자 기준)
--  실제 운영 시 사용자명·호스트·비밀번호를 변경하여 사용하세요.
-- =============================================================================

-- HR 담당자: 일반 시트 열람·입력 (⑤⑥ 접근 불가)
-- CREATE USER 'hr_staff'@'%' IDENTIFIED BY 'ChangeMe!';
-- GRANT SELECT, INSERT, UPDATE ON hr_db.employees              TO 'hr_staff'@'%';
-- GRANT SELECT, INSERT, UPDATE ON hr_db.promotion_history      TO 'hr_staff'@'%';
-- GRANT SELECT, INSERT, UPDATE ON hr_db.assignment_history     TO 'hr_staff'@'%';
-- GRANT SELECT, INSERT, UPDATE ON hr_db.certifications         TO 'hr_staff'@'%';
-- GRANT SELECT                 ON hr_db.v_employee_summary     TO 'hr_staff'@'%';
-- GRANT SELECT                 ON hr_db.v_cert_expiring_soon   TO 'hr_staff'@'%';
-- GRANT SELECT                 ON hr_db.ref_departments        TO 'hr_staff'@'%';
-- GRANT SELECT                 ON hr_db.ref_positions          TO 'hr_staff'@'%';
-- GRANT SELECT                 ON hr_db.ref_salary_grades      TO 'hr_staff'@'%';
-- GRANT SELECT                 ON hr_db.ref_employment_types   TO 'hr_staff'@'%';
-- -- ⚠ performance_reviews, salary_grade_history 는 GRANT 하지 않음

-- HR 관리자: 전체 테이블 접근
-- CREATE USER 'hr_manager'@'%' IDENTIFIED BY 'ChangeMe!';
-- GRANT SELECT, INSERT, UPDATE ON hr_db.*                      TO 'hr_manager'@'%';

-- 임원 (읽기 전용):
-- CREATE USER 'executive'@'%' IDENTIFIED BY 'ChangeMe!';
-- GRANT SELECT                 ON hr_db.*                      TO 'executive'@'%';

-- FLUSH PRIVILEGES;


-- =============================================================================
--  테이블 구조 요약  (ERD 텍스트)
-- =============================================================================
/*
 ref_employment_types ─┐
 ref_departments      ─┤
 ref_positions        ─┤──► employees (emp_id PK)
 ref_salary_grades    ─┘         │
                                  ├──► promotion_history     (시트③-A)
                                  ├──► assignment_history    (시트③-B)
                                  ├──► certifications        (시트④)
                                  ├──► performance_reviews   (시트⑤) [HR 전용]
                                  └──► salary_grade_history  (시트⑥) [HR 전용]

 VIEW
  v_employee_summary       ← employees + ref_* (제한 컬럼 제외)
  v_cert_expiring_soon     ← certifications + employees + ref_departments
*/
-- =============================================================================
--  END OF FILE
-- =============================================================================
