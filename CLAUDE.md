# 📚 wiki.md 관리 및 문서 생성 통합 지침 (수정판)

> **수정 핵심:** Claude의 공식 문서 스킬(docx / pptx / xlsx / pdf)을 **최우선으로 활용**하고, Python 폰트 강제 코드는 **Claude 스킬을 사용할 수 없는 폴백 상황**에만 적용한다.

---

## 1. 문서 생성 시 핵심 원칙 (가장 먼저 읽을 것)

### 1-1. 사용 도구 우선순위 (변경됨 ⚡)

| 파일 형식 | 1순위 (반드시 먼저 시도) | 2순위 (폴백) |
|----------|------------------------|-------------|
| `.docx` | **Claude `docx` 스킬** (`docx-js` / Node.js) | python-docx + 폰트 강제 코드 |
| `.pptx` | **Claude `pptx` 스킬** (`pptxgenjs` 또는 템플릿 편집) | python-pptx + 폰트 강제 코드 |
| `.xlsx` | **Claude `xlsx` 스킬** (`openpyxl`) | openpyxl + Malgun Gothic 적용 |
| `.pdf` | **Claude `pdf` 스킬** (HTML→PDF 권장) | reportlab + 한글 폰트 등록 |

### 1-2. Claude 스킬을 우선 사용하는 이유

1. **컨테이너 환경 검증 완료** — Claude의 공식 스킬은 claude.ai 웹/Cowork 환경 모두에서 검증된 라이브러리 조합을 사용한다.
2. **자동 검증 도구 내장** — `validate.py`, `recalc.py` 등 파일 무결성 자동 검증 스크립트가 포함되어 있다.
3. **레이아웃 품질 우수** — 페이지 사이즈, 표 너비, 이중 너비(columnWidths + cell width) 등 호환성 이슈를 자동 처리한다.
4. **유지보수 부담 감소** — 사용자 정의 폰트 강제 코드를 매번 복사·관리할 필요 없음.

### 1-3. Claude 스킬 사용 시 한글 처리 원칙

Claude 공식 스킬은 폰트명을 지정하면 **렌더링 시 OS의 폰트 fallback 메커니즘**이 한글을 자동 처리한다. 따라서:

- **docx-js 사용 시**: `font: "Malgun Gothic"` (또는 `"맑은 고딕"`) 한 줄로 충분.
- **pptxgenjs 사용 시**: `fontFace: "Malgun Gothic"` 지정.
- **openpyxl 사용 시**: `Font(name='맑은 고딕')` 적용.
- **pdf 변환 시**: HTML 단계에서 `font-family: 'Malgun Gothic', 'Noto Sans KR', sans-serif;` 명시.

> ⚠️ **XML 레벨의 `w:eastAsia` 강제 설정은 Claude 스킬을 사용하는 한 불필요하다.** 이 코드는 python-docx로 직접 작성하는 폴백 상황에서만 적용한다.

### 1-4. 폴백(Python 라이브러리 직접 사용)이 정당화되는 경우

다음 조건 중 하나라도 해당될 때만 첨부 원본 지침의 폰트 강제 코드를 사용한다:

- Claude `docx` / `pptx` 스킬을 시도했으나 실패한 경우
- 사용자가 명시적으로 `python-docx` 등 특정 라이브러리를 요청한 경우
- 기존에 python-docx로 작성된 코드를 수정/유지보수하는 경우
- Cowork 데스크톱 환경에서 사용자 로컬 Python에서만 실행해야 하는 경우

---

## 2. wiki.md 인덱스 관리 (원본 유지 — 우수한 원칙)

### 2-1. 폴더 구조

새 파일 생성 전에 반드시 `wiki.md`의 폴더 구조를 확인하여 적합한 카테고리를 선택한다:

```
01_경영재무 / 02_AI디지털전환 / 03_품질관리 / 04_설비구매
05_법무계약 / 06_경영보고 / 07_투자분석 / 08_MyWiki
09_생산·제조시스템 / 10_IT·시스템 / 11_인사·총무 / 12_참고자료
```

기존 카테고리에 맞지 않는 경우에만 새 폴더를 생성한다.

### 2-2. wiki.md 즉시 업데이트

파일 생성·이동·삭제 직후 `D:\Michael\OneDrive - Team Redpanda\ClaudeCowork\wiki.md`를 업데이트한다:

- 해당 카테고리 섹션의 **파일 목록 테이블**에 신규 항목 추가 (파일명 + 한 줄 설명)
- 폴더 신설 시 **폴더 구조 개요** 블록과 해당 섹션 추가
- **변경 이력** 테이블 (`## 🔄 변경 이력`) 맨 아래에 날짜·작업 내용 1줄 추가
- **총 카테고리** 수 변경 시 파일 상단 메타데이터 수정

### 2-3. 설명 품질 기준

- 파일 설명은 "무엇을 담고 있는가"를 한 줄로 명확하게 작성
- 버전·날짜가 있는 파일은 `v숫자` 또는 `YYYY-MM` 형태로 버전 정보 포함
- 베트남어·영어 원문은 언어 정보를 괄호로 표기 (예: `(베트남어 원본)`)

### 2-4. 동기화 원칙

- wiki.md는 Claude가 대화 시작 시 폴더 구조를 빠르게 파악하는 인덱스
- 항상 **현재 실제 폴더 상태와 동기화**된 상태 유지
- 파일 삭제/이동 시 wiki.md에서도 반드시 항목 제거·수정
- 임시 파일이나 백업(`bk/`)은 별도 행 없이 폴더명만 표기 가능

---

## 3. 보고서 작성 시 출력 형식 원칙 (개선됨 ⚡)

### 3-1. 기본 원칙: 단일 형식 출력

요청한 파일 형식만 생성한다 (예: `.xlsx` 요청 시 `.xlsx` 1개만 생성).

### 3-2. .md 사본을 추가로 생성하는 경우 (선택적)

다음 조건 중 하나일 때만 `.md` 사본을 함께 생성한다:

- 사용자가 명시적으로 "마크다운 사본도 만들어줘"라고 요청한 경우
- 보고서 내용이 향후 다른 대화에서 재참조될 가능성이 높고, 원본 형식(예: pptx)이 텍스트 추출이 어려운 경우
- 임원 보고용 정형 문서이며 Claude가 후속 분석 작업에 활용해야 하는 경우

> 💡 **이유:** Claude는 `.docx`, `.pptx`, `.xlsx` 모두 직접 읽고 분석할 수 있다 (`extract-text` 도구 보유). 이중 형식 출력은 토큰 소모를 늘리고 동기화 부담을 발생시키므로 **기본값은 단일 형식**이 합리적이다.

### 3-3. .md 사본 생성 시 규칙 (생성하기로 한 경우만 적용)

- MD 파일명은 원본과 동일, 확장자만 `.md`
- 동일 폴더에 나란히 저장
- 보고서 전체 내용을 Markdown 표·제목·목록으로 충실히 재현
- wiki.md에 두 파일 모두 등록

---

## 4. 한글 처리 — 상황별 가이드 (재정리 ⚡)

### 4-1. Claude `docx` 스킬 사용 시 (1순위)

```javascript
// docx-js — 한 줄로 끝
const doc = new Document({
  styles: {
    default: { document: { run: { font: "Malgun Gothic", size: 22 } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal",
        run: { size: 32, bold: true, font: "Malgun Gothic" },
        paragraph: { spacing: { before: 240, after: 240 }, outlineLevel: 0 } },
    ]
  },
  sections: [{ children: [/* ... */] }]
});
```

### 4-2. Claude `pptx` 스킬 사용 시 (1순위)

```javascript
// pptxgenjs
slide.addText("한글 본문", {
  x: 1, y: 1, w: 8, h: 1,
  fontFace: "Malgun Gothic",
  fontSize: 18,
});
```

### 4-3. Claude `xlsx` 스킬 사용 시 (1순위)

```python
# openpyxl
from openpyxl import Workbook
from openpyxl.styles import Font

wb = Workbook()
ws = wb.active
ws['A1'] = '한글 헤더'
ws['A1'].font = Font(name='맑은 고딕', size=11, bold=True)
```

### 4-4. PDF 생성 시 (1순위: HTML → PDF)

```css
/* HTML 단계에서 폰트 명시 */
body {
  font-family: 'Malgun Gothic', 'Noto Sans KR', '맑은 고딕', sans-serif;
}
```

### 4-5. 폴백 — python-docx 직접 사용 시 (필요한 경우만)

> 아래 코드는 **Claude `docx` 스킬이 사용 불가하거나 사용자가 명시적으로 python-docx를 요청한 경우에만** 적용한다.

```python
from docx import Document
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

def set_korean_font(run_or_style, font_name='Malgun Gothic'):
    """run 또는 style에 한글 폰트를 강제 지정한다."""
    element = run_or_style.element if hasattr(run_or_style, 'element') else run_or_style._element
    rpr = element.get_or_add_rPr() if hasattr(element, 'get_or_add_rPr') else element.find(qn('w:rPr'))
    if rpr is None:
        rpr = OxmlElement('w:rPr')
        element.insert(0, rpr)
    rfonts = rpr.find(qn('w:rFonts'))
    if rfonts is None:
        rfonts = OxmlElement('w:rFonts')
        rpr.append(rfonts)
    for attr in ['ascii', 'hAnsi', 'eastAsia', 'cs']:
        rfonts.set(qn(f'w:{attr}'), font_name)

doc = Document()
for style_name in ['Normal'] + [f'Heading {i}' for i in range(1, 10)]:
    try:
        style = doc.styles[style_name]
        style.font.name = 'Malgun Gothic'
        set_korean_font(style)
    except KeyError:
        pass
```

(원본 지침의 python-pptx, reportlab 폰트 강제 코드도 동일한 폴백 위치에 보존)

### 4-6. 인코딩 원칙 (모든 경우 공통)

- 모든 파일 입출력은 `encoding='utf-8'` 명시
- CSV 저장 시 Excel 호환을 위해 필요하면 `encoding='utf-8-sig'`(BOM 포함) 사용

### 4-7. 검증 단계

- 문서 생성 후 짧은 검증 스크립트로 한글이 올바르게 들어갔는지 확인
- Claude `docx` 스킬은 `validate.py`로 자동 검증 가능
- 한글 깨짐이 의심되면 즉시 폰트 설정 재점검

---

## 5. 의사결정 흐름도 (요약)

```
사용자가 문서 생성 요청
  ↓
1. Claude 공식 스킬(docx/pptx/xlsx/pdf) 사용 시도 (1순위)
  ↓
   성공? → 2번으로 / 실패? → 폴백(python 라이브러리 + 폰트 강제 코드)
  ↓
2. 적합한 폴더 선택 (wiki.md 폴더 구조 참조)
  ↓
3. 파일 생성 (한글 폰트는 위 4번 가이드 적용)
  ↓
4. wiki.md 업데이트
   - 파일 목록 테이블에 추가
   - 변경 이력 테이블에 1줄 추가
   - 폴더 신설 시 메타데이터·구조 개요 갱신
  ↓
5. (조건부) .md 사본 생성 — 사용자가 요청했거나 재참조 가능성이 높을 때만
  ↓
6. 검증 (한글 표시 확인, 파일 무결성 확인)
```

---

## 📌 변경 사항 요약

| 항목 | 원본 지침 | 수정안 |
|------|---------|--------|
| 문서 생성 도구 | python-docx/pptx/openpyxl/reportlab을 기본값으로 가정 | **Claude 공식 스킬을 1순위, Python 라이브러리는 폴백** |
| 한글 폰트 처리 | 모든 문서에 XML 레벨 `eastAsia` 강제 코드 적용 | Claude 스킬 사용 시 폰트명 지정만으로 충분, 폴백 시에만 강제 코드 적용 |
| .md 사본 생성 | 모든 보고서에 강제 | 사용자 요청 또는 재참조 필요 시에만 |
| wiki.md 관리 | 우수한 원칙 | **그대로 유지** |
| 폴더 구조 | 12개 카테고리 | **그대로 유지** |