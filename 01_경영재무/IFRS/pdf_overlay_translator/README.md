# PDF Overlay Translator

원본 PDF의 디자인·레이아웃을 유지하면서 본문 텍스트만 다른 언어로 오버레이 번역하는 도구입니다.

ACCA CertIFR 영문 슬라이드를 베트남어로 번역하는 용도로 제작되었지만, 다른 PDF 자료에도 동일하게 사용 가능합니다.

---

## 1. 환경 준비 (Windows 기준, 최초 1회만)

### 1-1. Python 설치 확인

명령 프롬프트(`cmd`)에서:

```cmd
python --version
```

`Python 3.10` 이상이면 OK. 없으면 https://www.python.org/downloads/ 에서 설치 (설치 시 "Add Python to PATH" 체크).

### 1-2. 의존성 설치

이 폴더로 이동한 뒤:

```cmd
cd C:\Users\MISTOP\Documents\01_경영재무\IFRS\pdf_overlay_translator
pip install -r requirements.txt
```

설치되는 라이브러리:
- `PyMuPDF` — PDF 텍스트 추출·오버레이 (핵심)
- `anthropic` — Claude API 호출 (provider=claude 사용 시)
- `requests` — DeepL/Google API 호출

### 1-3. API 키 설정

`config.yaml.example` 파일을 복사해 `config.yaml`로 이름 변경 후, 사용할 제공사의 API 키만 입력하세요.

```yaml
claude_api_key: "sk-ant-api03-xxxxx..."
```

**API 키 발급 안내**:
- Claude: https://console.anthropic.com/ → API Keys → Create Key (사용량 종량제, IFRS 슬라이드 4개 챕터 약 $3~5 추정)
- DeepL Free: https://www.deepl.com/pro-api → 월 50만 자 무료 (전체 49.5만 자가 무료 한도에 거의 딱 들어맞음)
- DeepL Pro: 월 €7.49부터, 무제한
- Google Cloud Translate: $20/100만 자

---

## 2. 사용법

### 2-1. 기본 형식

```cmd
python translate_pdf.py --pdf <원본PDF> --pages <범위> --output <결과PDF> --provider <제공사>
```

### 2-2. 챕터별 실행 (권장)

ACCA CertIFR 원본 PDF의 챕터별 페이지 번호:

| 챕터 | 페이지 범위 |
| --- | --- |
| Ch.1 Conceptual Framework | 4-45 |
| Ch.2 Presentation & Disclosure | 46-59 |
| Ch.3 Revenue (IFRS 15) | 60-101 |
| Ch.4 Accounting Policies | 102-115 |
| Ch.5 PP&E & Borrowing | 116-151 |
| Ch.6 Intangibles | 152-178 |
| Ch.7 Impairment | 179-206 |
| Ch.8 IP / NCAHFS | 207-233 |
| Ch.9 Govt Grants | 234-246 |
| Ch.10 Inventory & Agriculture | 247-270 |
| Ch.11 Lease (IFRS 16) | 271-298 |
| Ch.12 Fair Value | 299-314 |
| Ch.13 Financial Instruments (IFRS 9) | 315-352 |
| Ch.14 Provisions | 353-372 |
| Ch.15 Events after | 373-391 |
| Ch.16 Employee Benefits | 392-409 |
| Ch.17 Income Taxes | 410-426 |
| Ch.18 Share-based Payment | 427-444 |
| Ch.19 Exploration (additional) | 445-450 |
| Ch.20A/B Group & Goodwill | 451-485 |
| Ch.21 Associates & JV | 486-513 |
| Ch.22 Foreign Currency | 514-534 |
| Ch.23 Hyperinflation (additional) | 535-542 |
| Ch.24 Cash Flows | 543-567 |
| Ch.25 Operating Segments | 568-590 |
| Ch.26 Related Party | 591-613 |
| Ch.27 EPS | 614-654 |
| Ch.28 Interim Reporting | 655-664 |
| Ch.29 IFRS 1 (additional) | 665-671 |
| Ch.30 Insurance | 672-355 |

**우선순위 챕터 (사용자가 선택한 4개)**:

```cmd
:: Ch.1 개념체계
python translate_pdf.py --pdf "..\1778244921003_SAPP_ACCA_CertIFR_Slide_Eng_Print_2425ver3.pdf" --pages 4-45 --output Ch01_VI.pdf --provider claude

:: Ch.3 IFRS 15 수익인식
python translate_pdf.py --pdf "..\1778244921003_SAPP_ACCA_CertIFR_Slide_Eng_Print_2425ver3.pdf" --pages 60-101 --output Ch03_VI.pdf --provider claude

:: Ch.11 IFRS 16 리스
python translate_pdf.py --pdf "..\1778244921003_SAPP_ACCA_CertIFR_Slide_Eng_Print_2425ver3.pdf" --pages 271-298 --output Ch11_VI.pdf --provider claude

:: Ch.13 IFRS 9 금융상품
python translate_pdf.py --pdf "..\1778244921003_SAPP_ACCA_CertIFR_Slide_Eng_Print_2425ver3.pdf" --pages 315-352 --output Ch13_VI.pdf --provider claude
```

### 2-3. 검증 모드 (API 호출 없이 동작 확인)

API 키 없이 텍스트 박스가 잘 잡히는지 먼저 확인할 때:

```cmd
python translate_pdf.py --pdf "..\원본.pdf" --pages 4-10 --output test.pdf --provider none --dry-run
```

`--provider none --dry-run` 조합은 텍스트 추출만 수행하고 결과 PDF는 만들지 않습니다.

`--provider none` 만 쓰면 원문에 `[vi] ` 접두사만 붙여 오버레이하므로 박스 위치·폰트·마스킹이 잘 동작하는지 시각적으로 검증할 수 있습니다.

---

## 3. 옵션 전체 설명

| 옵션 | 기본값 | 설명 |
| --- | --- | --- |
| `--pdf` | (필수) | 입력 PDF 파일 경로 |
| `--pages` | `all` | 페이지 범위. `4-45` / `4,7,9` / `4-45,60-101` / `all` |
| `--output` | (필수) | 출력 PDF 경로 |
| `--target` | `vi` | 대상 언어 코드 (vi/ko/en/zh/ja) |
| `--provider` | `claude` | 번역 제공사 (claude/deepl/google/none) |
| `--config` | `config.yaml` | API 키 설정 파일 |
| `--cache` | `cache.json` | 번역 캐시 파일 (재실행 시 자동 활용) |
| `--font` | (자동탐색) | 베트남어/한국어 지원 폰트 .ttf 경로 |
| `--model` | `claude-sonnet-4-6` | Claude 모델명 |
| `--rate-limit` | `0.5` | API 호출 간 대기시간(초) |
| `--dry-run` | (off) | 텍스트 추출만, 번역·출력 생략 |

---

## 4. 동작 원리

```
원본 PDF
  ↓ PyMuPDF로 페이지별 텍스트 스팬 추출 (위치·폰트크기·색상 포함)
  ↓ 캐시 확인 → 미번역 항목만 API 호출
  ↓ 원본 텍스트 위치에 흰색 사각형 마스킹
  ↓ 동일 위치에 베트남어 텍스트 삽입 (박스 폭 초과 시 폰트 자동 축소)
  ↓ 페이지 단위로 cache.json 즉시 저장 → 중단 후 재실행 가능
결과 PDF
```

**캐시의 효용**: 한 번 번역한 텍스트는 `cache.json`에 저장되어, 다음 실행 때는 API를 호출하지 않습니다. 챕터별로 나눠 실행해도 중복 문구(예: "Conceptual Framework", "Performance obligation")는 재번역되지 않아 비용·시간이 크게 절감됩니다.

---

## 5. 주의사항 · 한계

### 5-1. 박스 넘침
베트남어는 영어보다 평균 10% 길어, 일부 좁은 박스에서 텍스트가 잘릴 수 있습니다. 스크립트는 박스 폭을 넘으면 폰트를 자동 축소하지만, 차이가 큰 경우 수동 편집이 필요할 수 있습니다.

### 5-2. 다이어그램 안 텍스트
PDF 안의 일부 텍스트는 본문 텍스트 레이어가 아닌 **이미지 안의 그림 라벨**일 수 있습니다 (전체의 약 5~10% 추정). 이런 텍스트는 본 스크립트로 처리되지 않습니다.

### 5-3. 회계 용어 정확도
Claude를 쓸 경우 IFRS 표준 용어를 잘 알지만, DeepL/Google은 단어 단위로는 정확해도 회계 문맥에서는 어색할 수 있습니다. 번역 후 `..\ACCA_CertIFR_EN-VI-KO_용어집.xlsx`와 대조하면서 핵심 용어 통일 검토를 권장합니다.

### 5-4. 저작권
원본 PDF는 본인이 정당하게 보유한 자료에 한해 번역하시고, 번역 결과물도 **개인 학습용**으로만 사용해 주세요. 재배포·외부 공유는 SAPP/ACCA의 허가가 필요합니다.

---

## 6. 트러블슈팅

| 증상 | 원인/해결 |
| --- | --- |
| `ModuleNotFoundError: fitz` | `pip install -r requirements.txt` 재실행 |
| `claude API 키가 설정되지 않았습니다` | `config.yaml`에 키 입력 또는 환경변수 `ANTHROPIC_API_KEY` 설정 |
| 베트남어 글자가 □ 로 표시 | `--font "C:\Windows\Fonts\NotoSans-Regular.ttf"` 같은 식으로 지원 폰트 명시 |
| 박스가 비어있게 표시 | 원본이 이미지로 그려진 경우. OCR이 필요한 페이지일 수 있음 |
| API 호출 실패 (rate limit) | `--rate-limit 1.5` 등으로 대기시간 늘려 재시도 |
| 중간에 끊김 | 같은 명령으로 재실행하면 캐시 덕분에 이미 처리된 페이지는 건너뜀 |

---

## 7. 예상 비용·시간

4개 우선순위 챕터 (Ch.1 + Ch.3 + Ch.11 + Ch.13 = 150p, 약 22만 자) 기준:

| 제공사 | 비용(추정) | 시간(추정) |
| --- | --- | --- |
| Claude Sonnet 4.6 | $1.5~3 | 15~25분 |
| DeepL Free | 무료 (월 50만 자 한도 내) | 5~10분 |
| DeepL Pro | €0.7~1.5 | 5~10분 |
| Google Translate | $0.4~0.8 | 3~5분 |

회계 용어 정확도는 Claude > DeepL > Google 순. 우선 DeepL Free로 전체를 빠르게 한 번 돌려보고, 핵심 챕터만 Claude로 다시 돌려 비교하는 것도 효율적입니다.
