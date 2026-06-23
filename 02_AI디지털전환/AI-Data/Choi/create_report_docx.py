# 제조현장 머신러닝 보고서를 Word(.docx) 파일로 생성하는 스크립트
from docx import Document
from docx.shared import Pt, Cm, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import copy

def set_korean_font(run_or_rpr, font_name='맑은 고딕'):
    """Run 또는 rPr 요소에 한글 폰트를 XML 레벨에서 강제 설정한다."""
    if hasattr(run_or_rpr, '_r'):
        rpr = run_or_rpr._r.get_or_add_rPr()
    else:
        rpr = run_or_rpr
    rfonts = rpr.find(qn('w:rFonts'))
    if rfonts is None:
        rfonts = OxmlElement('w:rFonts')
        rpr.insert(0, rfonts)
    for attr in ['w:ascii', 'w:hAnsi', 'w:eastAsia', 'w:cs']:
        rfonts.set(qn(attr), font_name)

def set_style_korean_font(style, font_name='맑은 고딕'):
    """스타일의 rPr에 한글 폰트를 강제 설정한다."""
    element = style.element
    rpr = element.find(qn('w:rPr'))
    if rpr is None:
        rpr = OxmlElement('w:rPr')
        element.append(rpr)
    set_korean_font(rpr, font_name)
    style.font.name = font_name

def add_heading(doc, text, level, font_size, bold=True, color=None):
    """제목 단락을 추가하고 한글 폰트를 적용한다."""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(6)
    run = p.add_run(text)
    run.bold = bold
    run.font.size = Pt(font_size)
    if color:
        run.font.color.rgb = RGBColor(*color)
    set_korean_font(run)
    return p

def add_body(doc, text, indent=False):
    """본문 단락을 추가하고 한글 폰트를 적용한다."""
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(6)
    if indent:
        p.paragraph_format.left_indent = Cm(0.5)
    run = p.add_run(text)
    run.font.size = Pt(10.5)
    set_korean_font(run)
    return p

def add_bullet(doc, text, level=0):
    """글머리 기호 항목을 추가한다."""
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.left_indent = Cm(0.5 + level * 0.5)
    p.paragraph_format.space_after = Pt(3)
    run = p.add_run(text)
    run.font.size = Pt(10)
    set_korean_font(run)
    return p

def set_table_style(table):
    """표에 기본 스타일을 적용한다."""
    table.style = 'Table Grid'

def add_table_row(table, cells_data, is_header=False):
    """표에 행을 추가한다."""
    row = table.add_row()
    for i, text in enumerate(cells_data):
        cell = row.cells[i]
        cell.text = ''
        p = cell.paragraphs[0]
        run = p.add_run(text)
        run.font.size = Pt(9.5)
        run.bold = is_header
        set_korean_font(run)
        if is_header:
            cell._tc.get_or_add_tcPr()
            shd = OxmlElement('w:shd')
            shd.set(qn('w:fill'), 'D9E1F2')
            shd.set(qn('w:color'), 'auto')
            shd.set(qn('w:val'), 'clear')
            cell._tc.tcPr.append(shd)


def create_report():
    doc = Document()

    # 페이지 여백 설정
    section = doc.sections[0]
    section.page_width = Cm(21)
    section.page_height = Cm(29.7)
    section.left_margin = Cm(3)
    section.right_margin = Cm(3)
    section.top_margin = Cm(2.5)
    section.bottom_margin = Cm(2.5)

    # 기본 스타일에 한글 폰트 적용
    normal_style = doc.styles['Normal']
    normal_style.font.name = '맑은 고딕'
    normal_style.font.size = Pt(10.5)
    set_style_korean_font(normal_style)

    # ─── 표지 ───────────────────────────────────────────
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(60)
    run = p_title.add_run('제조현장의 머신러닝 혁신')
    run.bold = True
    run.font.size = Pt(22)
    run.font.color.rgb = RGBColor(0x1F, 0x49, 0x7D)
    set_korean_font(run)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p_sub.add_run('예지보전 · 불량 검출 · 반도체 수율 향상 사례 연구')
    run.font.size = Pt(14)
    run.font.color.rgb = RGBColor(0x2E, 0x74, 0xB5)
    set_korean_font(run)

    doc.add_paragraph()
    doc.add_paragraph()

    meta_lines = [
        ('과목', '머신러닝 개론 — 사례 조사 과제'),
        ('작성일', '2026년 5월 23일'),
        ('제출 기한', '2026년 5월 31일'),
    ]
    for label, value in meta_lines:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r1 = p.add_run(f'{label}: ')
        r1.bold = True
        r1.font.size = Pt(11)
        set_korean_font(r1)
        r2 = p.add_run(value)
        r2.font.size = Pt(11)
        set_korean_font(r2)

    doc.add_page_break()

    # ─── 1. 서론 ──────────────────────────────────────────
    add_heading(doc, '1. 서론: 왜 제조업에 머신러닝인가?', 1, 16, color=(0x1F, 0x49, 0x7D))

    add_heading(doc, '제조업이 직면한 도전', 2, 13, color=(0x2E, 0x74, 0xB5))
    add_body(doc, '현대 제조업은 세 가지 압력을 동시에 받고 있다. 첫째, 제품의 복잡도가 높아지면서 단 하나의 부품 불량이 전체 시스템 오류로 이어지는 경우가 빈번해졌다. 항공기 엔진의 경우 수천 개의 부품이 정밀하게 맞물려 작동하며, 반도체 웨이퍼 한 장을 완성하기까지 300단계 이상의 공정을 거친다.')
    add_body(doc, '둘째, 생산 속도가 빨라지면서 사람이 직접 품질을 확인할 수 있는 물리적 한계가 드러났다. 자동차 부품 생산 라인에서는 초당 수십 개의 부품이 쏟아져 나오며, 그 모든 부품에 대해 수천 가지 측정값을 동시에 검토하는 것은 인간의 능력 밖이다.')
    add_body(doc, '셋째, 설비 고장의 비용이 천문학적 수준으로 높아졌다. 항공사에서 비계획적 엔진 정비 한 건의 비용은 수십억 원에 달하며, 반도체 팹(Fab, 제조 공장)의 생산 라인이 한 시간 멈추는 데 드는 손실은 수억 원을 초과하기도 한다.')
    add_body(doc, '머신러닝은 이 세 가지 문제를 정면으로 해결할 수 있는 잠재력을 가지고 있다. 사람이 처리할 수 없는 수천 가지 변수를 동시에 학습하고, 고장이 발생하기 전에 징후를 포착하며, 이미지 속의 미세한 결함을 1마이크로미터 단위까지 탐지할 수 있다. 중요한 것은, 이것이 단순한 규칙 기반 자동화가 아니라는 점이다. 머신러닝 모델은 데이터로부터 스스로 패턴을 학습하며, 개발자가 미리 정의하지 않은 상관관계도 발견한다.')

    add_heading(doc, '이 보고서의 구성', 2, 13, color=(0x2E, 0x74, 0xB5))
    add_body(doc, '이 보고서는 제조현장에서 실제로 활용되고 있는 머신러닝 사례 세 가지를 심층적으로 다룬다. 각 사례는 어떤 데이터를 사용했는지, 어떤 모델이 어떻게 학습했는지, 그리고 어떤 성과를 거뒀는지를 중심으로 분석한다.')

    # ─── 2. 핵심 기법 해설 ────────────────────────────────────
    add_heading(doc, '2. 머신러닝 핵심 기법 해설 (용어 정의)', 1, 16, color=(0x1F, 0x49, 0x7D))

    add_heading(doc, '2.1 지도학습 vs. 비지도학습', 2, 13, color=(0x2E, 0x74, 0xB5))
    add_body(doc, '지도학습(Supervised Learning)은 정답(레이블, Label)이 있는 데이터로 모델을 훈련시키는 방식이다. 예를 들어 "이 부품은 불량(1), 이 부품은 정상(0)"이라는 정답 데이터를 주고, 새로운 부품이 들어왔을 때 불량인지 정상인지 예측하게 한다.')
    add_body(doc, '비지도학습(Unsupervised Learning)은 정답 없이 데이터 자체의 구조와 패턴을 찾는 방식이다. "정상 상태"의 데이터만으로 학습하여 이상한 패턴이 나타나면 이상(Anomaly)으로 탐지하는 방식이 제조현장에서 많이 쓰인다.')

    add_heading(doc, '2.2 주요 알고리즘 용어 해설', 2, 13, color=(0x2E, 0x74, 0xB5))

    algorithms = [
        ('랜덤 포레스트 (Random Forest)',
         '수많은 결정 트리(Decision Tree)를 함께 사용하는 앙상블(Ensemble) 모델이다. 각각의 결정 트리는 "진동이 X 이상이고 온도가 Y 이상이면 고장 위험"과 같은 규칙의 집합이다. 랜덤 포레스트는 수백 개의 트리가 각자 예측하고 다수결로 최종 결론을 내린다. 변수 중요도(Feature Importance)를 계산할 수 있어 "어떤 센서 값이 고장 예측에 가장 중요한가"를 분석할 수 있다.'),
        ('XGBoost (Extreme Gradient Boosting)',
         '결정 트리를 순차적으로 쌓아가는 방식이다. 첫 번째 트리가 틀린 부분을 두 번째 트리가 보완하고, 두 번째 트리가 틀린 부분을 세 번째 트리가 보완하는 식으로 점점 정확해진다. 정형 데이터(표 형태의 숫자 데이터)에서 매우 강력한 성능을 보이며, 특히 수천 개의 변수가 있는 복잡한 제조 데이터에서 뛰어난 성과를 보인다.'),
        ('SVM (Support Vector Machine, 서포트 벡터 머신)',
         '데이터를 두 클래스로 나누는 최적의 경계선을 찾는 알고리즘이다. 경계선과 각 클래스의 가장 가까운 점(서포트 벡터) 사이의 간격(마진)을 최대화한다. 커널 트릭(Kernel Trick)을 통해 선형으로 분리되지 않는 복잡한 데이터도 처리할 수 있다.'),
        ('LSTM (Long Short-Term Memory, 장단기 기억 네트워크)',
         '순환 신경망(RNN)의 한 종류로 시계열 데이터 처리에 특화되어 있다. 이전 시점의 정보를 "기억"하면서 현재 입력을 처리한다. 셀 상태(장기 기억)와 은닉 상태(단기 기억) 두 채널로 정보를 관리하며, 항공기 센서처럼 시간에 따라 변하는 데이터 분석에 적합하다.'),
        ('Isolation Forest (아이솔레이션 포레스트)',
         '"정상 데이터는 분리하기 어렵고, 이상 데이터는 분리하기 쉽다"는 원리를 이용한 이상 탐지 전용 알고리즘이다. 정상 데이터만으로도 학습할 수 있어 불량 사례가 부족한 제조 환경에 유용하다.'),
        ('CNN (Convolutional Neural Network, 합성곱 신경망)',
         '이미지 처리에 특화된 딥러닝 모델이다. 낮은 수준의 특징(모서리, 색상 변화)부터 높은 수준의 특징(결함 형태, 패턴)까지 계층적으로 학습한다. 반도체 웨이퍼 결함 분류에 활용된다.'),
        ('GAN (Generative Adversarial Network, 생성적 적대 신경망)',
         '생성자와 판별자 두 네트워크가 서로 경쟁하면서 학습하는 모델이다. 훈련 데이터가 부족한 희귀 결함 패턴에 대해 인공 데이터를 생성하여 학습 데이터를 보충하는 데 활용된다.'),
    ]

    for name, desc in algorithms:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.left_indent = Cm(0.3)
        r_name = p.add_run(f'{name}: ')
        r_name.bold = True
        r_name.font.size = Pt(10.5)
        set_korean_font(r_name)
        r_desc = p.add_run(desc)
        r_desc.font.size = Pt(10)
        set_korean_font(r_desc)

    # ─── 3. 사례 1 ────────────────────────────────────────
    add_heading(doc, '3. 사례 1: 항공기 엔진 잔여 수명 예측', 1, 16, color=(0x1F, 0x49, 0x7D))
    add_heading(doc, '— LSTM 기반 예지보전 (Predictive Maintenance)', 2, 12, color=(0x2E, 0x74, 0xB5))

    add_heading(doc, '3.1 배경과 문제 정의', 2, 13, color=(0x2E, 0x74, 0xB5))
    add_body(doc, '항공기 엔진은 지구에서 가장 극단적인 조건에서 작동하는 기계 중 하나다. 외부 온도가 영하 60도인 고고도에서 연소실 내부는 1,700도를 넘나든다. 이 극한 환경에서 수만 개의 부품이 수백만 번의 사이클을 반복한다.')
    add_body(doc, '기존의 항공기 엔진 정비는 크게 두 가지 방식으로 이루어졌다. 시간 기반 정비(Time-Based Maintenance)는 특정 비행 시간에 도달하면 부품을 교체하는 방식이다. 이 방식은 안전하지만 아직 사용 가능한 부품을 버리는 비효율이 발생한다. 사후 정비(Reactive Maintenance)는 고장 발생 후 정비하는 방식인데, 항공기 안전과 직결되므로 용납할 수 없다.')
    add_body(doc, '머신러닝 기반의 예지보전(PdM)은 부품이 실제로 고장나기 전에, 그러나 아직 사용 가능한 수명이 남았을 때 정비하는 것을 목표로 한다. 이를 위해 모델은 엔진의 잔여 수명(RUL, Remaining Useful Life)을 예측한다.')

    add_heading(doc, '3.2 데이터: NASA CMAPSS 데이터셋', 2, 13, color=(0x2E, 0x74, 0xB5))
    add_body(doc, 'NASA 에임스 연구소(Ames Research Center)에서 항공기 엔진 시뮬레이션을 통해 생성된 CMAPSS(Commercial Modular Aero-Propulsion System Simulation) 데이터셋 [1]은 이 분야의 표준 벤치마크다.')

    # 데이터 표
    tbl1 = doc.add_table(rows=1, cols=2)
    set_table_style(tbl1)
    add_table_row(tbl1, ['항목', '내용'], is_header=True)
    rows1 = [
        ('서브셋 구성', 'FD001~FD004 (4개 시나리오)'),
        ('FD001 (주 벤치마크)', '훈련 100대, 테스트 100대, 운전 조건 1개, 고장 모드 1개'),
        ('FD004 (복잡 시나리오)', '훈련 249대, 테스트 248대, 운전 조건 6개, 고장 모드 2개'),
        ('센서 수', '엔진당 21개 (온도, 압력, 팬 속도, 연료 유량 등)'),
        ('성과 비교 기준', '이하 성능 표는 모두 FD001 기준'),
    ]
    for row in rows1:
        add_table_row(tbl1, list(row))
    doc.add_paragraph()

    add_heading(doc, '3.3 모델: LSTM 기반 시계열 회귀', 2, 13, color=(0x2E, 0x74, 0xB5))
    add_body(doc, '시계열 데이터에서 단순 회귀나 랜덤 포레스트를 적용할 경우, 각 타임스텝을 독립된 관측값으로 취급하게 된다. 이는 "최근 20번의 비행 동안 점점 악화되는 추세"와 같은 장기적인 맥락을 놓치게 만든다.')
    add_body(doc, 'LSTM은 이 문제를 해결한다. 셀 상태(Cell State)는 이전 시점의 정보를 다음 시점으로 전달하는 장기 기억 채널이고, 은닉 상태(Hidden State)는 현재 시점에서 중요한 정보를 담는 단기 기억 채널이다. 세 개의 게이트(잊기 게이트, 입력 게이트, 출력 게이트)가 어떤 정보를 기억하고 버릴지, 그리고 다음 층으로 얼마나 전달할지를 학습에 의해 결정한다. Zheng et al.(2017) [2]의 연구에서 제시된 구조는 다음과 같다.')

    steps_lstm = [
        '입력층: 30개 타임스텝(직전 30회 비행)의 센서 데이터를 윈도우로 잘라 입력',
        'LSTM 1층: 64개 유닛, 순서 정보 유지(return_sequences=True)',
        'LSTM 2층: 32개 유닛, 최종 요약 벡터 출력',
        '드롭아웃(Dropout 20%): 과적합 방지',
        '출력층: 잔여 수명(RUL) 값 1개를 출력하는 선형 회귀',
    ]
    for s in steps_lstm:
        add_bullet(doc, s)

    add_heading(doc, '3.4 성과', 2, 13, color=(0x2E, 0x74, 0xB5))

    tbl2 = doc.add_table(rows=1, cols=3)
    set_table_style(tbl2)
    add_table_row(tbl2, ['모델', 'RMSE', 'Score (비대칭 손실)'], is_header=True)
    perf_rows = [
        ('다층 퍼셉트론(MLP)', '~37 사이클', '~1,862'),
        ('랜덤 포레스트', '~31 사이클', '~1,603'),
        ('LSTM (2층)', '~16 사이클', '~338'),
    ]
    for row in perf_rows:
        add_table_row(tbl2, list(row))
    doc.add_paragraph()

    add_body(doc, 'GE Digital은 Predix 플랫폼 기반 예지보전 시스템을 통해 비계획적 엔진 탈거(Unscheduled Engine Removal)를 유의미하게 줄였다고 자체 보고하고 있다 [3]. 다만 이는 GE 자사의 마케팅 자료에 기반한 것이므로 독립적인 학술 검증이 필요하다는 점을 명시한다. 항공 업계 전문 매체들은 비계획적 엔진 정비 한 건당 수백만 달러 수준의 비용이 발생한다고 추산하며, 예지보전의 경제적 효과는 광범위하게 인정된다.')

    # ─── 4. 사례 2 ────────────────────────────────────────
    add_heading(doc, '4. 사례 2: Bosch 생산 라인 불량 검출', 1, 16, color=(0x1F, 0x49, 0x7D))
    add_heading(doc, '— XGBoost 기반 이진 분류 (Binary Classification)', 2, 12, color=(0x2E, 0x74, 0xB5))

    add_heading(doc, '4.1 배경과 문제 정의', 2, 13, color=(0x2E, 0x74, 0xB5))
    add_body(doc, '독일의 Bosch는 세계 최대 자동차 부품 공급업체 중 하나로, 연간 수억 개의 부품을 생산한다. 기존의 방법은 각 측정값이 허용 오차 범위 내에 있는지만 확인했는데, 변수들 간의 복잡한 상호작용을 무시하는 것이었다. 예를 들어 "변수 A는 정상이고 변수 B도 정상이지만, A와 B의 특정 조합은 불량을 유발한다"는 패턴은 기존 방식으로 잡아낼 수 없었다.')

    add_heading(doc, '4.2 데이터: Bosch 생산 라인 성능 데이터셋 (Kaggle, 2016)', 2, 13, color=(0x2E, 0x74, 0xB5))

    tbl3 = doc.add_table(rows=1, cols=2)
    set_table_style(tbl3)
    add_table_row(tbl3, ['항목', '내용'], is_header=True)
    bosch_rows = [
        ('훈련 샘플 수', '약 1,183,747개 (부품 수)'),
        ('변수(측정값) 수', '수치형 968개, 범주형 2,140개, 날짜형 1,156개 ≈ 총 4,264개'),
        ('레이블', '정상(0) / 불량(1) 이진 분류'),
        ('불량률', '약 0.58% — 극단적 클래스 불균형'),
        ('특이사항', '변수명 모두 익명화 — 도메인 지식 적용 불가'),
    ]
    for row in bosch_rows:
        add_table_row(tbl3, list(row))
    doc.add_paragraph()

    add_body(doc, '가장 큰 도전은 클래스 불균형 문제였다. 전체 부품의 0.58%만 불량이기 때문에 모든 부품을 "정상"이라고 예측하는 단순 모델도 99.42%의 정확도를 보인다. 따라서 단순 정확도(Accuracy)는 의미 없는 지표이며, MCC(Matthews Correlation Coefficient)를 사용해야 했다.')

    add_heading(doc, '4.3 모델: XGBoost와 특성 공학', 2, 13, color=(0x2E, 0x74, 0xB5))

    steps_xgb = [
        '특성 공학: 결측값 자체를 정보로 활용 (어떤 스테이션을 통과했는지)',
        '변수 중요도 분석: 4,264개 → 상위 100~200개 변수 선택',
        '클래스 불균형 처리: scale_pos_weight = (정상 수) / (불량 수) 파라미터 적용',
        '교차 검증: 10-fold Stratified Cross-Validation',
        '앙상블: 여러 XGBoost 모델의 예측 확률을 평균',
    ]
    for s in steps_xgb:
        add_bullet(doc, s)

    add_heading(doc, '4.4 성과', 2, 13, color=(0x2E, 0x74, 0xB5))
    add_body(doc, '경진대회 최상위 솔루션의 테스트 MCC 점수는 약 0.44~0.47 수준이었다. MCC는 -1(완전히 틀림)에서 +1(완전히 맞음), 0(무작위 예측)의 범위를 가지므로, 0.44는 심각한 클래스 불균형 속에서 상당히 높은 성과다 [4].')
    add_body(doc, '또한 XGBoost의 설명 가능성(Explainability)은 중요한 실용적 이점이다. 변수 중요도 분석을 통해 특정 라인-스테이션-피처 조합(예: L3_S36_F3939 형태의 코드)이 불량 예측에 가장 중요한 변수임을 파악할 수 있다. 단, Bosch 공개 데이터셋은 완전히 익명화되어 있어 해당 변수가 실제로 어떤 물리량인지는 Bosch 내부 매핑 없이는 알 수 없다.')

    # ─── 5. 사례 3 ────────────────────────────────────────
    add_heading(doc, '5. 사례 3: 반도체 웨이퍼 결함 패턴 분류', 1, 16, color=(0x1F, 0x49, 0x7D))
    add_heading(doc, '— CNN + GAN을 활용한 수율 향상', 2, 12, color=(0x2E, 0x74, 0xB5))

    add_heading(doc, '5.1 배경과 문제 정의', 2, 13, color=(0x2E, 0x74, 0xB5))
    add_body(doc, '반도체 생산은 현존하는 제조 공정 중 가장 복잡한 것 중 하나다. 실리콘 웨이퍼 한 장에 수천 개의 칩을 새기기 위해 300단계 이상의 공정(증착, 식각, 노광, 세정 등)을 거치며, 이 과정에서 발생하는 결함은 칩을 사용 불가능하게 만든다.')
    add_body(doc, '웨이퍼 빈 맵(WBM, Wafer Bin Map)은 각 칩 위치의 양불 여부를 점으로 표시한 지도다. 불량 칩들이 특정 패턴을 이루면, 그 패턴의 형태가 어떤 공정에서 문제가 생겼는지를 나타낸다. 기존에는 숙련된 엔지니어가 WBM을 육안으로 검토하여 결함 패턴을 분류했는데, 하루에 수백~수천 장의 웨이퍼를 처리해야 하는 현실에서 병목이 되었다.')

    add_heading(doc, '5.2 데이터: WM-811K 데이터셋', 2, 13, color=(0x2E, 0x74, 0xB5))
    add_body(doc, 'Wu et al.(2015) [5]이 공개한 WM-811K 데이터셋은 실제 반도체 공장에서 18개월간 수집된 811,457장의 웨이퍼 빈 맵을 포함하며, 반도체 결함 분류 연구의 표준 벤치마크로 자리 잡았다.')

    tbl4 = doc.add_table(rows=1, cols=3)
    set_table_style(tbl4)
    add_table_row(tbl4, ['결함 패턴', '설명', '대표 원인'], is_header=True)
    defect_rows = [
        ('Center', '웨이퍼 중심부 집중 불량', 'CMP 과연마'),
        ('Donut', '가운데가 비어 있는 도넛 형태', '스핀 코팅 불균일'),
        ('Edge-Ring', '가장자리 원형 패턴', '온도 불균일, 테두리 효과'),
        ('Edge-Loc', '국소 가장자리 패턴', '기계적 충격'),
        ('Loc', '국소 집중 패턴', '입자 오염'),
        ('Near-full', '전체면에 가까운 불량', '공정 오염 또는 장비 고장'),
        ('Random', '무작위 분포', '체계적 원인 없음'),
        ('Scratch', '선형 긁힘 패턴', '로봇 핸들링 오류'),
        ('Normal', '정상 (불량 없음)', '—'),
    ]
    for row in defect_rows:
        add_table_row(tbl4, list(row))
    doc.add_paragraph()

    add_heading(doc, '5.3 모델: CNN + GAN 데이터 증강', 2, 13, color=(0x2E, 0x74, 0xB5))
    add_body(doc, '초기 연구들은 WBM에서 수동 특성(불량 칩의 밀도, 원형성, 장단축 비율 등)을 추출한 후 k-NN, SVM, 랜덤 포레스트를 적용했다. 이 접근법은 약 70~75%의 분류 정확도를 보였으나, 특성 설계 자체에 도메인 전문가의 시간이 많이 소요됐다.')
    add_body(doc, 'CNN은 WBM 이미지에서 특성을 자동으로 학습한다. Ji et al.(2020) [6]의 연구에서는 사전학습된 CNN 모델을 미세조정하여 전체 분류 정확도 약 97.0%를 달성했다. 그러나 희귀 패턴(Donut, Near-full 등)의 재현율은 여전히 낮은 문제가 있었다.')
    add_body(doc, '이 문제를 해결하기 위해 조건부 GAN(Conditional GAN)을 활용했다. GAN은 특정 결함 패턴 레이블을 입력받아 해당 패턴의 WBM 이미지를 인공적으로 생성한다. GAN 증강 후 전체 정확도가 97.0%에서 98.3%로 향상되었으며, 특히 희귀 패턴 클래스의 분류 성능이 집중적으로 개선되었다.')

    add_heading(doc, '5.4 성과와 의의', 2, 13, color=(0x2E, 0x74, 0xB5))
    add_body(doc, '자동화된 결함 패턴 분류 시스템은 공정 이상의 조기 감지, 근본 원인 분석(Root Cause Analysis)의 가속화, 수율(Yield) 향상을 가능하게 한다. 반도체 팹에서 수율 1% 향상은 수억에서 수십억 원의 추가 매출에 해당하므로, 이 기술의 경제적 가치는 매우 크다.')

    # ─── 6. 개인 관점 분석 ────────────────────────────────────
    add_heading(doc, '6. 개인 관점 분석', 1, 16, color=(0x1F, 0x49, 0x7D))

    add_heading(doc, '6.1 내가 이 문제를 접근했다면', 2, 13, color=(0x2E, 0x74, 0xB5))

    add_body(doc, '【사례 1 - LSTM vs. Transformer】')
    add_body(doc, '항공기 엔진 RUL 예측에서 나라면 Transformer 기반 모델을 시도해볼 것 같다. LSTM은 과거 정보를 순차적으로 처리하기 때문에 매우 먼 과거의 정보가 희석되는 문제가 있다. 반면 Transformer의 어텐션 메커니즘(Attention Mechanism)은 "과거 어떤 시점이 현재 예측에 가장 중요한가"를 직접 학습한다. 엔진이 특정 극한 운전 조건을 겪은 시점이 100번의 비행 전이었더라도, 그 경험이 현재 열화 상태에 영향을 주고 있다면 어텐션이 그 시점에 집중할 수 있다.')

    add_body(doc, '【사례 2 - Bosch: 이상 탐지 병행】')
    add_body(doc, '클래스 불균형이 0.58%라는 극단적인 상황에서, 나라면 이상 탐지(Anomaly Detection) 접근법을 XGBoost와 병행할 것이다. 구체적으로 정상 부품 데이터만으로 Autoencoder를 훈련시키고, 불량 부품은 정상 패턴에서 벗어나므로 재구성 오류(Reconstruction Error)가 높게 나올 것이라 가정한다. Autoencoder와 XGBoost의 예측을 앙상블하면 희귀한 불량 패턴을 더 잘 잡아낼 수 있을 것으로 생각한다.')

    add_body(doc, '【사례 3 - 능동 학습(Active Learning) 도입】')
    add_body(doc, '811,457장의 WBM에 레이블을 달기 위해 얼마나 많은 전문가 시간이 들었을지를 생각하면, 데이터 레이블링 자체가 큰 비용이다. 나라면 능동 학습(Active Learning)을 도입할 것이다. 모델이 가장 확신하지 못하는 샘플만 전문가에게 레이블링 요청을 보내는 방식으로, 전체 데이터의 10~20%만 레이블링하고도 전체 레이블링에 가까운 성능을 얻을 수 있다.')

    add_heading(doc, '6.2 한계와 윤리적 고려사항', 2, 13, color=(0x2E, 0x74, 0xB5))

    concerns = [
        ('도메인 변이(Data Drift) 문제',
         '새로운 원자재 배치가 도착하거나, 기계 교체, 계절 변화 등으로 공장 환경이 달라지면 모델의 정확도가 떨어질 수 있다. 지속적인 모델 모니터링과 재학습 체계(MLOps)가 반드시 필요하다.'),
        ('모델 과신의 위험',
         'ML 모델이 "이 엔진은 50사이클 더 안전하다"고 예측했다고 해서 맹목적으로 믿어서는 안 된다. 특히 항공안전과 같이 인명과 직결된 영역에서는 ML의 예측이 의사결정 보조 도구여야 하며, 최종 판단은 항상 숙련된 인간 전문가가 해야 한다.'),
        ('편향된 훈련 데이터',
         '"우리가 본 적 없는 결함"에 대해서는 어떤 ML 모델도 예측하기 어렵다. GAN이 생성한 인공 데이터도 기존 데이터의 분포를 기반으로 하므로 이 한계를 근본적으로 해결하지는 못한다.'),
        ('고용 영향',
         '예지보전 및 자동 품질 검사 시스템의 도입으로 일부 숙련 검사 직무가 줄어들 수 있다. 기업이 기술 도입에 따른 인력 전환 교육에 책임 있는 자세를 갖는 것이 중요하다.'),
    ]

    for title, desc in concerns:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.left_indent = Cm(0.3)
        r_t = p.add_run(f'▶ {title}: ')
        r_t.bold = True
        r_t.font.size = Pt(10.5)
        set_korean_font(r_t)
        r_d = p.add_run(desc)
        r_d.font.size = Pt(10)
        set_korean_font(r_d)

    # ─── 7. 결론 ────────────────────────────────────────
    add_heading(doc, '7. 결론', 1, 16, color=(0x1F, 0x49, 0x7D))
    add_body(doc, '이 보고서에서는 제조현장의 머신러닝 적용 사례 세 가지를 심층적으로 분석했다.')
    add_body(doc, '항공기 엔진 RUL 예측은 LSTM이 시계열 데이터에서 장기 의존성을 학습하여 전통적인 방법보다 훨씬 정확한 고장 예측을 가능하게 함을 보여주었다. Bosch 생산 라인 불량 검출은 수천 개의 변수가 있는 정형 데이터에서 XGBoost가 얼마나 강력한지를 보여주었으며, 극단적인 클래스 불균형이라는 현실적 도전을 극복하기 위한 기법들도 함께 다루었다. 반도체 웨이퍼 결함 분류는 이미지 분류에서 CNN의 위력과 데이터 부족 문제를 GAN으로 해결하는 창의적인 접근법을 소개했다.')
    add_body(doc, '세 가지 사례 모두에서 공통적으로 확인되는 점이 있다. 머신러닝의 도입은 단순한 기술 교체가 아니라 문제 정의의 전환이다. "이 부품은 허용 오차 안에 있는가"라는 질문에서 "이 부품이 미래에 실패할 가능성은 얼마인가"로 질문 자체가 바뀐다. 이 전환이 실제로 수십억 원 규모의 비용 절감과 품질 향상으로 이어진다는 것이 이 사례들을 통해 명확히 드러난다.')
    add_body(doc, '동시에 ML 모델은 만능이 아니다. 도메인 변이에 취약하고, 레이블 데이터 확보에 많은 비용이 들며, 본 적 없는 패턴에 대한 예측은 신뢰하기 어렵다. 이러한 한계를 인식하고 ML을 인간 전문가의 도구로 활용하는 균형 잡힌 시각이 필요하다.')

    # ─── 8. 참고문헌 ────────────────────────────────────────
    add_heading(doc, '8. 참고문헌', 1, 16, color=(0x1F, 0x49, 0x7D))

    refs = [
        '[1] Saxena, A., Goebel, K., Simon, D., & Eklund, N. (2008). Damage propagation modeling for aircraft engine run-to-failure simulation. In 2008 International Conference on Prognostics and Health Management (PHM 2008). IEEE. https://doi.org/10.1109/PHM.2008.4711414',
        '[2] Zheng, S., Ristovski, K., Farahat, A., & Gupta, C. (2017). Long short-term memory network for remaining useful life estimation. In 2017 IEEE International Conference on Prognostics and Health Management (ICPHM 2017). IEEE. https://doi.org/10.1109/ICPHM.2017.7998311',
        '[3] GE Digital. (n.d.). Predix Platform for Industrial IoT. GE Digital 공식 페이지. https://www.ge.com/digital/applications/predix ※ GE 자사 플랫폼 소개 페이지이므로 성과 수치는 독립적 학술 검증이 필요함.',
        '[4] Bosch. (2016). Bosch Production Line Performance. Kaggle Competition. https://www.kaggle.com/c/bosch-production-line-performance ※ 실제 Bosch 생산 라인 데이터를 사용한 검증된 공개 데이터셋.',
        '[5] Wu, M. J., Jang, J. S. R., & Chen, J. L. (2015). Wafer map failure pattern recognition and similarity ranking for large-scale data sets. IEEE Transactions on Semiconductor Manufacturing, 28(1), 1–12. https://doi.org/10.1109/TSM.2014.2364237',
        '[6] Ji, Y. S., & Lee, J. H. (2020). Using GAN to improve CNN performance of wafer map defect type classification. In 2020 31st Annual SEMI Advanced Semiconductor Manufacturing Conference (ASMC 2020). IEEE. https://doi.org/10.1109/ASMC49169.2020.9185193',
        '[7] POSCO. (2019). POSCO Named Lighthouse Factory. World Economic Forum. https://www.weforum.org/press/2019/07/posco-named-lighthouse-factory/ ※ WEF 공식 등재로 확인 가능한 사실.',
    ]

    for ref in refs:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Cm(0.5)
        p.paragraph_format.first_line_indent = Cm(-0.5)
        p.paragraph_format.space_after = Pt(4)
        run = p.add_run(ref)
        run.font.size = Pt(9)
        set_korean_font(run)

    # 면주 (하단)
    doc.add_paragraph()
    p_footer = doc.add_paragraph()
    p_footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_f = p_footer.add_run('본 보고서에 포함된 기업 공개 자료 수치는 해당 기업의 공식 발표를 기반으로 하며, 독립적 학술 검증이 필요합니다. Bosch 및 NASA CMAPSS 관련 수치는 공개 학술 연구에서 재현 가능한 결과를 인용했습니다.')
    r_f.font.size = Pt(8)
    r_f.font.color.rgb = RGBColor(0x80, 0x80, 0x80)
    set_korean_font(r_f)

    output_path = r'C:\Users\MISTOP\Documents\02_AI디지털전환\AI-Data\Choi\제조현장_머신러닝_사례_보고서.docx'
    doc.save(output_path)
    print(f'저장 완료: {output_path}')


if __name__ == '__main__':
    create_report()
