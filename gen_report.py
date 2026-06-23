# 자동화 요청사항 분석보고서 docx 생성 스크립트
from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement


def set_korean_font(run_or_style, font_name='Malgun Gothic'):
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


def set_cell_bg(cell, hex_color):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), hex_color)
    tcPr.append(shd)


def add_heading(doc, text, level, color='1F4E79'):
    para = doc.add_heading(text, level=level)
    para.alignment = WD_ALIGN_PARAGRAPH.LEFT
    for run in para.runs:
        run.font.name = 'Malgun Gothic'
        set_korean_font(run)
        run.font.color.rgb = RGBColor(*bytes.fromhex(color))
    return para


def add_para(doc, text, bold=False, size=10, indent=False, color=None):
    para = doc.add_paragraph()
    if indent:
        para.paragraph_format.left_indent = Cm(0.5)
    run = para.add_run(text)
    run.font.name = 'Malgun Gothic'
    run.font.size = Pt(size)
    run.bold = bold
    if color:
        run.font.color.rgb = RGBColor(*bytes.fromhex(color))
    set_korean_font(run)
    return para


def add_table(doc, headers, rows, col_widths=None, header_color='1F4E79'):
    table = doc.add_table(rows=1, cols=len(headers))
    table.style = 'Table Grid'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr_cells = table.rows[0].cells
    for i, h in enumerate(headers):
        set_cell_bg(hdr_cells[i], header_color)
        para = hdr_cells[i].paragraphs[0]
        run = para.add_run(h)
        run.font.name = 'Malgun Gothic'
        run.font.size = Pt(9)
        run.bold = True
        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        set_korean_font(run)
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for row_data in rows:
        row_cells = table.add_row().cells
        for i, val in enumerate(row_data):
            para = row_cells[i].paragraphs[0]
            run = para.add_run(str(val))
            run.font.name = 'Malgun Gothic'
            run.font.size = Pt(9)
            set_korean_font(run)
    if col_widths:
        for row in table.rows:
            for i, cell in enumerate(row.cells):
                cell.width = Cm(col_widths[i])
    return table


doc = Document()

# 전체 기본 스타일 한글 폰트 설정
for sn in ['Normal'] + [f'Heading {i}' for i in range(1, 5)]:
    try:
        s = doc.styles[sn]
        s.font.name = 'Malgun Gothic'
        set_korean_font(s)
    except KeyError:
        pass

section = doc.sections[0]
section.top_margin = Cm(2.0)
section.bottom_margin = Cm(2.0)
section.left_margin = Cm(2.5)
section.right_margin = Cm(2.5)

# ── 제목 ──
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run('금형 자동화 라인 구축')
r.font.name = 'Malgun Gothic'; r.font.size = Pt(18); r.bold = True
r.font.color.rgb = RGBColor(0x1F, 0x4E, 0x79); set_korean_font(r)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run('설비별 자동화 요구사항 분석보고서')
r.font.name = 'Malgun Gothic'; r.font.size = Pt(14); r.bold = True
r.font.color.rgb = RGBColor(0x2E, 0x74, 0xB5); set_korean_font(r)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run('작성일: 2026-06-09   |   출처: 자동화요청사항 폴더 원문 PDF 4건')
r.font.name = 'Malgun Gothic'; r.font.size = Pt(9)
r.font.color.rgb = RGBColor(0x60, 0x60, 0x60); set_korean_font(r)
doc.add_paragraph()

# ── 1. 개요 ──
add_heading(doc, '1. 개요', 1)
add_para(doc, '본 문서는 금형 자동화 라인(로봇 + 설비 연동 시스템) 구축을 위해 자동화 업체가 전달한 설비별 필수 옵션 체크리스트 4종을 한국어로 정리·분석한 보고서입니다.')
doc.add_paragraph()
add_heading(doc, '1-1. 분석 대상 문서', 2, '2E74B5')
add_table(doc,
    ['설비', '원문 파일명', '작성일'],
    [
        ['Sodick 방전가공기 (EDM)', '沙迪克电火花做自动化需要具备的功能-2026-05-29.pdf', '2026-05-29'],
        ['Makino 머시닝센터 (CNC)', '牧野加工中心做自动化需要具备的功能.pdf', '—'],
        ['CMM 3좌표 측정기', '三坐标做自动化需要具备的功能--2026-05-29.pdf', '2026-05-29'],
        ['CNC 머시닝센터 (범용 상세판)', '数控加工中心机床自动化需求-2024-08-02.pdf', '2024-08-02'],
    ],
    col_widths=[4.5, 9.0, 3.0]
)
doc.add_paragraph()

# ── 2. EDM ──
add_heading(doc, '2. Sodick 방전가공기 (EDM) — 자동화 요구사항', 1)
add_table(doc,
    ['No.', '기능', '상세 설명', '중요도'],
    [
        ['1', '이더넷 포트 (하드웨어)', '네트워크 연결용 LAN 포트', '필수'],
        ['2', '자동 승강 오일조', '코드로 오일조 높이 제어 가능', '필수'],
        ['3', '자동화 인터페이스', '6485 포트 — 프로그램 업로드, 설비 모니터링, 원격 시동', '필수'],
        ['4', 'MR 헤드 (C축)', '없으면 자동화 가공 시 제약 多 → 발주 전 사전 확인 필수', '필수'],
        ['5', '항공 커넥터', 'EROWA A타입 공작물/전극 교환기 입출력 인터페이스', '필수'],
        ['6', '매크로 변수 기능', '표준 사양', '필수'],
        ['7', '주축 공압 척 (에어 밀봉공 포함)', '밀봉공 없으면 안전 위험 발생', '필수(안전)'],
    ],
    col_widths=[1.0, 4.0, 9.5, 2.0]
)
add_para(doc, '※ C축(MR 헤드) 미탑재 시 자동화 가공에 상당한 제약 — 발주 전 자동화 업체와 사전 협의 필수.', size=9, indent=True)
doc.add_paragraph()

# ── 3. Makino CNC ──
add_heading(doc, '3. Makino 머시닝센터 (CNC) — 자동화 요구사항', 1)
add_table(doc,
    ['No.', '기능', '상세 설명', '중요도'],
    [
        ['1', '이더넷 포트 (하드웨어)', '—', '필수'],
        ['2', '자동 측면문', '전면문보다 측면문 권장 — 로봇 작업 편의성 우수', '필수'],
        ['3', 'MML 인터페이스', '고속 이더넷 인터페이스 (FAST ETHERNET)', '필수'],
        ['4', '좌표 회전 기능', 'G68 좌표계 회전', '필수'],
        ['5', '항공 커넥터 (EROWA A타입)', '공작물 교환기 입출력 인터페이스', '필수'],
        ['6', '매크로 변수 기능', 'Custom Macro 공용 변수 1100 (표준)', '필수'],
        ['7', '3/4번째 참조점 복귀', '3RD & 4TH REFERENCE POSITION RETURN', '필수'],
        ['8', '기내 공구 측정기 (하드웨어)', '없으면 공구 파손 감지 불가 → 안전 위험', '필수(안전)'],
        ['9', '작업대 척용 에어 배관', '6개, Φ6mm — 옵션이나 권장', '권장'],
        ['9', '공구 매거진', '30개 이상 권장 (강제 아님)', '권장'],
        ['10', '확장 공구 번호 400개', '기외 공구 교환 미사용 시 불필요', '조건부'],
    ],
    col_widths=[1.0, 4.0, 9.5, 2.0]
)
doc.add_paragraph()

# ── 4. CMM ──
add_heading(doc, '4. CMM 3좌표 측정기 — 자동화 요구사항', 1)
add_table(doc,
    ['No.', '기능', '상세 설명', '중요도'],
    [
        ['1', '이더넷 포트 (하드웨어)', 'CMM PC에 LAN 전용 포트 별도 필요', '필수'],
        ['2', '프로그램 호출 인터페이스', 'API 자료 제공 필수 — CMM 제조사에 별도 요청 필요', '필수'],
        ['3', '설비 상태 모니터링 인터페이스', '설비 상태·좌표·실행 프로그램명 모니터링 — API 자료 필수', '필수'],
        ['4', '설비 원격 제어 인터페이스', '원격 프로그램 선택·원격 시동 — API 자료 필수', '필수'],
        ['5', '비상정지 라인 (하드웨어)', '없으면 안전 위험 — 반드시 배선 필요', '필수(안전)'],
        ['6', '프로브 교환 랙', '전극·공작물 빈번한 프로브 교환 시 권장', '권장'],
        ['7', '자동 측정 헤드', '측정 각도 전환이 잦을 경우 권장', '권장'],
    ],
    col_widths=[1.0, 4.0, 9.5, 2.0]
)
add_para(doc, '※ CMM은 API 의존도가 높아 항목 2·3·4 모두 CMM 제조사로부터 API 문서를 사전에 확보해야 자동화 연동 가능.', size=9, indent=True)
doc.add_paragraph()

# ── 5. CNC 범용 ──
add_heading(doc, '5. CNC 머시닝센터 범용 상세판 — 자동화 요구사항', 1)
add_para(doc, '3절 Makino 요구사항의 상세 확장판으로, "구비 여부" 확인 컬럼이 있는 현장 점검표 형식입니다.')
doc.add_paragraph()
add_table(doc,
    ['No.', '기능', '주요 상세 내용', '중요도'],
    [
        ['1', '이더넷 포트', '설비 통신용', '필수'],
        ['2', '설비 메모리', '원격 업로드 시 100MB 이상 필요 (CF카드 연동 시 완화 가능)', '필수'],
        ['3', '자동 측면문', '코드로 개폐 제어 가능해야 함 / 없으면 로봇이 직접 제어', '필수'],
        ['4', '프로그램 업로드 인터페이스', 'TCP/IP (API 또는 FTP) + 삭제 API (매크로 프로그램 삭제 금지 제한 필수)', '필수'],
        ['5', '설비 상태 모니터링', '실행 프로그램명 / 운전·정지·알람 / 알람 번호·내용 / 기계 좌표 / 공구 수명 / 주축 부하·공구번호·이송·회전수', '필수'],
        ['6', '설비 원격 제어', '원격 프로그램 선택·시동 / 원격 Reset', '필수'],
        ['7', '좌표 회전 기능', '측면문 투입 시 필요 / CNC+EDM 혼합 라인은 레이아웃에 따라 판단 / 5축 CNC는 불필요', '조건부'],
        ['8', '자동화 안전 교환 신호', '주축 이동 완료 신호 / 자동문 개폐 신호 / 로봇 진입 시 주축 잠금 (전기 도면·타임차트 제공 필요)', '필수(안전)'],
        ['9', '매크로 변수 기능', '—', '필수'],
        ['10', '기내 공구 측정기', '없으면 공구 파손 감지 불가 → 안전 위험', '필수(안전)'],
    ],
    col_widths=[1.0, 4.0, 9.5, 2.0]
)
doc.add_paragraph()

# ── 6. 공통 비교 ──
add_heading(doc, '6. 설비 공통 요구사항 비교', 1)
add_table(doc,
    ['기능', 'EDM (Sodick)', 'CNC (Makino)', 'CMM', 'CNC (범용)'],
    [
        ['이더넷 포트', 'O', 'O', 'O', 'O'],
        ['자동문', '—', 'O (측면)', '—', 'O (측면)'],
        ['EROWA A타입 커넥터', 'O', 'O', '—', '—'],
        ['매크로 변수 기능', 'O', 'O', '—', 'O'],
        ['원격 제어 인터페이스', 'O (6485)', 'O (MML)', 'O (API)', 'O (TCP/IP)'],
        ['설비 상태 모니터링', 'O', '—', 'O (API)', 'O'],
        ['좌표 회전 (G68)', '—', 'O', '—', '조건부'],
        ['기내 공구 측정기', '—', 'O', '—', 'O'],
        ['비상정지 배선', '—', '—', 'O', '—'],
        ['안전 교환 신호', '—', '—', '—', 'O'],
    ],
    col_widths=[5.0, 3.0, 3.0, 2.5, 3.0],
    header_color='243F60'
)
doc.add_paragraph()

# ── 7. 안전 위험 ──
add_heading(doc, '7. 안전 위험 항목 요약', 1, 'C00000')
add_para(doc, '자동화 연동 시 아래 항목이 미비하면 안전 사고 위험이 있습니다. 발주 및 시공 전 반드시 확인이 필요합니다.')
doc.add_paragraph()
add_table(doc,
    ['설비', '안전 위험 항목', '비고'],
    [
        ['EDM', '주축 공압 척 에어 밀봉공 미비', '원공장 설치 척은 보통 포함, 비표준 설치 시 확인 필요'],
        ['CNC', '기내 공구 측정기 미설치', '자동화 논리에 영향 없으나 공구 파손 감지 불가'],
        ['CMM', '비상정지 라인 미배선', '하드웨어 필수 — 없으면 긴급 정지 불가'],
        ['CNC (범용)', '기내 공구 측정기 미설치 / 안전 교환 신호 미구성', '로봇 진입 시 주축 잠금 신호 없으면 충돌 위험'],
    ],
    col_widths=[3.0, 6.0, 7.5],
    header_color='C00000'
)
doc.add_paragraph()

# ── 8. 후속 조치 ──
add_heading(doc, '8. 후속 조치 권고', 1)
items = [
    ('CMM 제조사 API 확보',
     'CMM 구매 계약 시 프로그램 호출·상태 모니터링·원격 제어 API 제공 조건을 계약서에 명시할 것.'),
    ('EDM C축(MR 헤드) 탑재 여부 확인',
     'Sodick EDM 미탑재 시 자동화 업체와 사전 협의 후 대안 방안 도출 필요.'),
    ('각 설비 구비 여부 현황 파악',
     'CNC 범용 문서의 "구비 여부" 컬럼이 공란임. 현장 확인 후 기입 필요.'),
    ('전기 도면·타임차트 준비',
     '자동화 안전 교환 신호 구성 시 CNC 제조사로부터 관련 전기 도면을 사전 확보할 것.'),
]
for title, desc in items:
    p = doc.add_paragraph(style='List Number')
    r1 = p.add_run(f'{title}: ')
    r1.font.name = 'Malgun Gothic'; r1.font.size = Pt(10); r1.bold = True
    set_korean_font(r1)
    r2 = p.add_run(desc)
    r2.font.name = 'Malgun Gothic'; r2.font.size = Pt(10)
    set_korean_font(r2)

doc.add_paragraph()
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run('본 보고서는 원문 PDF 4건을 번역·정리한 내용이며, 실제 발주 및 시공 전 자동화 업체와 재확인이 필요합니다.')
r.font.name = 'Malgun Gothic'; r.font.size = Pt(8); r.italic = True
r.font.color.rgb = RGBColor(0x80, 0x80, 0x80); set_korean_font(r)

output = r'D:\Michael\OneDrive - Team Redpanda\ClaudeCowork\04_구매·설비\금형자동화(설비&시스템)\자동화요청사항\자동화요청사항_분석보고서.docx'
doc.save(output)
print('저장 완료:', output)
