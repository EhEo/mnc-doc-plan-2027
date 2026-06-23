const fs = require('fs');
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  AlignmentType, HeadingLevel, BorderStyle, WidthType, ShadingType,
  PageBreak, LevelFormat, PageNumber, Header, Footer
} = require('/sessions/eager-awesome-bohr/mnt/outputs/node_modules/docx');

// 색상 팔레트
const HEADER_BG = "1F4E78";       // 진한 파랑
const SUBHEADER_BG = "D9E2F3";    // 연한 파랑
const POS_BG = "E2EFDA";          // 연한 초록 (개선)
const NEG_BG = "FCE4D6";          // 연한 주황 (악화)
const NEU_BG = "F2F2F2";          // 회색 (중립)

const border = { style: BorderStyle.SINGLE, size: 4, color: "808080" };
const borders = { top: border, bottom: border, left: border, right: border };

// Korean font
const FONT = "맑은 고딕";

function p(text, opts = {}) {
  return new Paragraph({
    alignment: opts.align || AlignmentType.LEFT,
    spacing: { before: opts.before || 0, after: opts.after || 60, line: 280 },
    children: [
      new TextRun({
        text: String(text),
        font: FONT,
        size: opts.size || 20,
        bold: opts.bold || false,
        color: opts.color || "000000",
      })
    ]
  });
}

function bulletP(text, opts = {}) {
  return new Paragraph({
    spacing: { after: 40, line: 280 },
    indent: { left: 360, hanging: 200 },
    children: [
      new TextRun({ text: "• ", font: FONT, size: 20 }),
      new TextRun({
        text: String(text),
        font: FONT,
        size: opts.size || 20,
        bold: opts.bold || false,
        color: opts.color || "000000",
      })
    ]
  });
}

function h1(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_1,
    spacing: { before: 360, after: 180 },
    children: [
      new TextRun({ text, font: FONT, size: 32, bold: true, color: "1F4E78" })
    ],
    border: { bottom: { style: BorderStyle.SINGLE, size: 12, color: "1F4E78", space: 1 } }
  });
}

function h2(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2,
    spacing: { before: 280, after: 120 },
    children: [
      new TextRun({ text, font: FONT, size: 26, bold: true, color: "2E5984" })
    ]
  });
}

function h3(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_3,
    spacing: { before: 200, after: 80 },
    children: [
      new TextRun({ text, font: FONT, size: 22, bold: true, color: "404040" })
    ]
  });
}

// Cell 생성 helper
function cell(text, opts = {}) {
  const widthDxa = opts.width || 1872;
  return new TableCell({
    borders,
    width: { size: widthDxa, type: WidthType.DXA },
    shading: opts.bg ? { fill: opts.bg, type: ShadingType.CLEAR } : undefined,
    margins: { top: 80, bottom: 80, left: 100, right: 100 },
    verticalAlign: "center",
    children: [
      new Paragraph({
        alignment: opts.align || AlignmentType.LEFT,
        spacing: { after: 0, line: 260 },
        children: [
          new TextRun({
            text: String(text),
            font: FONT,
            size: opts.size || 18,
            bold: opts.bold || false,
            color: opts.color || "000000",
          })
        ]
      })
    ]
  });
}

// Table 생성 helper - columnWidths 합 = 9360 (US Letter content width)
function makeTable(rows, columnWidths) {
  const totalWidth = columnWidths.reduce((a, b) => a + b, 0);
  return new Table({
    width: { size: totalWidth, type: WidthType.DXA },
    columnWidths,
    rows
  });
}

// ========================
// 보고서 컨텐츠 작성
// ========================

const content = [];

// 표지 / 제목
content.push(new Paragraph({
  alignment: AlignmentType.CENTER,
  spacing: { before: 0, after: 240 },
  children: [
    new TextRun({ text: "베트남 법인 W18주차 주간보고", font: FONT, size: 40, bold: true, color: "1F4E78" })
  ]
}));
content.push(new Paragraph({
  alignment: AlignmentType.CENTER,
  spacing: { after: 120 },
  children: [
    new TextRun({ text: "전주(W17) 대비 비교 분석 보고서", font: FONT, size: 32, bold: true, color: "2E5984" })
  ]
}));
content.push(new Paragraph({
  alignment: AlignmentType.CENTER,
  spacing: { after: 360 },
  children: [
    new TextRun({ text: "보고일자: 2026.05.01  |  비교기간: W17(2026.04.24) ↔ W18(2026.05.01)",
      font: FONT, size: 20, color: "606060" })
  ]
}));

// ────────────────────────────────────────
// 1. 종합 요약 (Executive Summary)
// ────────────────────────────────────────
content.push(h1("1. 종합 요약 (Executive Summary)"));

content.push(p("W18주차 주간보고를 W17주차와 비교한 결과 다음과 같은 주요 변동 사항을 확인하였습니다.", { after: 120 }));

const summaryRows = [
  new TableRow({
    tableHeader: true,
    children: [
      cell("구분", { width: 1700, bg: HEADER_BG, color: "FFFFFF", bold: true, align: AlignmentType.CENTER }),
      cell("주요 지표", { width: 2200, bg: HEADER_BG, color: "FFFFFF", bold: true, align: AlignmentType.CENTER }),
      cell("W17", { width: 1730, bg: HEADER_BG, color: "FFFFFF", bold: true, align: AlignmentType.CENTER }),
      cell("W18", { width: 1730, bg: HEADER_BG, color: "FFFFFF", bold: true, align: AlignmentType.CENTER }),
      cell("증감/평가", { width: 2000, bg: HEADER_BG, color: "FFFFFF", bold: true, align: AlignmentType.CENTER }),
    ]
  }),
  new TableRow({ children: [
    cell("매출", { width: 1700, bg: SUBHEADER_BG, bold: true }),
    cell("4월 누적/예상", { width: 2200 }),
    cell("$3,242,290 (84%)", { width: 1730, align: AlignmentType.RIGHT }),
    cell("$3,283,347 (85%)", { width: 1730, align: AlignmentType.RIGHT }),
    cell("+$41K 개선 ▲", { width: 2000, bg: POS_BG, align: AlignmentType.CENTER }),
  ]}),
  new TableRow({ children: [
    cell("매출", { width: 1700, bg: SUBHEADER_BG, bold: true }),
    cell("1~7월 누적 예상", { width: 2200 }),
    cell("$25,989,189 (98%)", { width: 1730, align: AlignmentType.RIGHT }),
    cell("$26,217,194 (99%)", { width: 1730, align: AlignmentType.RIGHT }),
    cell("+$228K 개선 ▲", { width: 2000, bg: POS_BG, align: AlignmentType.CENTER }),
  ]}),
  new TableRow({ children: [
    cell("AR", { width: 1700, bg: SUBHEADER_BG, bold: true }),
    cell("총 AR 잔액", { width: 2200 }),
    cell("$11,043,150", { width: 1730, align: AlignmentType.RIGHT }),
    cell("$9,339,958", { width: 1730, align: AlignmentType.RIGHT }),
    cell("-$1,703K 개선 ▼", { width: 2000, bg: POS_BG, align: AlignmentType.CENTER }),
  ]}),
  new TableRow({ children: [
    cell("AP", { width: 1700, bg: SUBHEADER_BG, bold: true }),
    cell("총 AP 잔액", { width: 2200 }),
    cell("$9,124,517", { width: 1730, align: AlignmentType.RIGHT }),
    cell("$8,587,029", { width: 1730, align: AlignmentType.RIGHT }),
    cell("-$537K 개선 ▼", { width: 2000, bg: POS_BG, align: AlignmentType.CENTER }),
  ]}),
  new TableRow({ children: [
    cell("AR/AP 차이", { width: 1700, bg: SUBHEADER_BG, bold: true }),
    cell("순포지션", { width: 2200 }),
    cell("$192만", { width: 1730, align: AlignmentType.RIGHT }),
    cell("$75만 (5/4 $111만 입금 반영)", { width: 1730, align: AlignmentType.RIGHT }),
    cell("개선 ▼", { width: 2000, bg: POS_BG, align: AlignmentType.CENTER }),
  ]}),
  new TableRow({ children: [
    cell("VMI 재고", { width: 1700, bg: SUBHEADER_BG, bold: true }),
    cell("LGIT Balance 금액", { width: 2200 }),
    cell("$823,449", { width: 1730, align: AlignmentType.RIGHT }),
    cell("$634,156", { width: 1730, align: AlignmentType.RIGHT }),
    cell("-$189K 감소 ▼", { width: 2000, bg: POS_BG, align: AlignmentType.CENTER }),
  ]}),
  new TableRow({ children: [
    cell("VMI 재고", { width: 1700, bg: SUBHEADER_BG, bold: true }),
    cell("MBZ Balance 금액", { width: 2200 }),
    cell("$884,276", { width: 1730, align: AlignmentType.RIGHT }),
    cell("$480,286", { width: 1730, align: AlignmentType.RIGHT }),
    cell("-$404K 감소 ▼", { width: 2000, bg: POS_BG, align: AlignmentType.CENTER }),
  ]}),
  new TableRow({ children: [
    cell("인원", { width: 1700, bg: SUBHEADER_BG, bold: true }),
    cell("총 인원", { width: 2200 }),
    cell("799명", { width: 1730, align: AlignmentType.CENTER }),
    cell("796명", { width: 1730, align: AlignmentType.CENTER }),
    cell("-3명 (Worker 감소)", { width: 2000, bg: NEU_BG, align: AlignmentType.CENTER }),
  ]}),
  new TableRow({ children: [
    cell("생산 1팀", { width: 1700, bg: SUBHEADER_BG, bold: true }),
    cell("Casting 달성율", { width: 2200 }),
    cell("92% (W16)", { width: 1730, align: AlignmentType.CENTER }),
    cell("90% (W17)", { width: 1730, align: AlignmentType.CENTER }),
    cell("-2%p ▼", { width: 2000, bg: NEG_BG, align: AlignmentType.CENTER }),
  ]}),
  new TableRow({ children: [
    cell("생산 1팀", { width: 1700, bg: SUBHEADER_BG, bold: true }),
    cell("Casting 수율", { width: 2200 }),
    cell("87% (W16)", { width: 1730, align: AlignmentType.CENTER }),
    cell("87% (W17)", { width: 1730, align: AlignmentType.CENTER }),
    cell("동일", { width: 2000, bg: NEU_BG, align: AlignmentType.CENTER }),
  ]}),
  new TableRow({ children: [
    cell("직통율", { width: 1700, bg: SUBHEADER_BG, bold: true }),
    cell("전체 직통율", { width: 2200 }),
    cell("81.1% (W16)", { width: 1730, align: AlignmentType.CENTER }),
    cell("82.1% (W17)", { width: 1730, align: AlignmentType.CENTER }),
    cell("+1.0%p 개선 ▲", { width: 2000, bg: POS_BG, align: AlignmentType.CENTER }),
  ]}),
  new TableRow({ children: [
    cell("품질", { width: 1700, bg: SUBHEADER_BG, bold: true }),
    cell("4월 NCR 건수", { width: 2200 }),
    cell("9건", { width: 1730, align: AlignmentType.CENTER }),
    cell("13건", { width: 1730, align: AlignmentType.CENTER }),
    cell("+4건 ▲ (악화)", { width: 2000, bg: NEG_BG, align: AlignmentType.CENTER }),
  ]}),
  new TableRow({ children: [
    cell("품질", { width: 1700, bg: SUBHEADER_BG, bold: true }),
    cell("4월 외부비용 누적", { width: 2200 }),
    cell("$322,415", { width: 1730, align: AlignmentType.RIGHT }),
    cell("$344,523", { width: 1730, align: AlignmentType.RIGHT }),
    cell("+$22K ▲", { width: 2000, bg: NEG_BG, align: AlignmentType.CENTER }),
  ]}),
];
content.push(makeTable(summaryRows, [1700, 2200, 1730, 1730, 2000]));

content.push(h3("주요 변화 포인트"));
content.push(bulletP("매출/재무: 4월 매출 $41K 개선, AR $1.7M·AP $537K 동시 감소로 운전자본 회수 양호. AR/AP 차이 $192만 → $75만 (단기 자금 부담 완화)"));
content.push(bulletP("개발 영업: 삼성 A27 IA70 최종 치수 검증 시료 발송 완료, A사 Eagle Eye PEO 적용 진행, 퀄컴 MTP Mavros 신규 4벌 내작 진척"));
content.push(bulletP("VMI 재고: LGIT/MBZ 양사 모두 재고 금액 감소. 출하 진행 양호, MBZ NX4 Housing 한국 이관 영향 일부 반영"));
content.push(bulletP("생산: 달성율 일부 하락(AL5 Housing, GEN4 Cover의 금형 수리 비가동), 수율은 안정적 유지. 직통율은 W17 82.1%로 W16 대비 소폭 상승"));
content.push(bulletP("품질: 4월 NCR 4건 추가 발생(LGIT LQ2 미가공, ZF EU2L Housing QR 라벨 번짐), 외부비용 약 $22K 증가. 후속 대응 필요"));
content.push(bulletP("AS9100 인증: 절차서 47종 중 1건 작성 완료(생산관리 지침서) → 진척도 2%, 5/23 완료 목표 달성을 위한 진척 가속 필요"));

// 페이지 분리
content.push(new Paragraph({ children: [new PageBreak()] }));

// ────────────────────────────────────────
// 2. 개발 영업
// ────────────────────────────────────────
content.push(h1("2. 개발 영업"));

content.push(h2("2-1. 매출 현황 (4~7월 예상)"));
const salesRows = [
  new TableRow({ tableHeader: true, children: [
    cell("고객사", { width: 1500, bg: HEADER_BG, color: "FFFFFF", bold: true, align: AlignmentType.CENTER }),
    cell("구분", { width: 1200, bg: HEADER_BG, color: "FFFFFF", bold: true, align: AlignmentType.CENTER }),
    cell("W17 (4/22 누적)", { width: 1700, bg: HEADER_BG, color: "FFFFFF", bold: true, align: AlignmentType.CENTER }),
    cell("W18 (4/29 누적)", { width: 1700, bg: HEADER_BG, color: "FFFFFF", bold: true, align: AlignmentType.CENTER }),
    cell("증감 ($)", { width: 1530, bg: HEADER_BG, color: "FFFFFF", bold: true, align: AlignmentType.CENTER }),
    cell("평가", { width: 1730, bg: HEADER_BG, color: "FFFFFF", bold: true, align: AlignmentType.CENTER }),
  ]}),
  new TableRow({ children: [
    cell("LGIT", { width: 1500, bold: true }),
    cell("4월", { width: 1200 }),
    cell("$924,813", { width: 1700, align: AlignmentType.RIGHT }),
    cell("$928,285", { width: 1700, align: AlignmentType.RIGHT }),
    cell("+$3,472", { width: 1530, align: AlignmentType.RIGHT, bg: POS_BG }),
    cell("계획 147% 초과", { width: 1730, align: AlignmentType.CENTER }),
  ]}),
  new TableRow({ children: [
    cell("Mando", { width: 1500, bold: true }),
    cell("4월", { width: 1200 }),
    cell("$624,009", { width: 1700, align: AlignmentType.RIGHT }),
    cell("$650,944", { width: 1700, align: AlignmentType.RIGHT }),
    cell("+$26,935", { width: 1530, align: AlignmentType.RIGHT, bg: POS_BG }),
    cell("계획 119% 초과", { width: 1730, align: AlignmentType.CENTER }),
  ]}),
  new TableRow({ children: [
    cell("Samsung", { width: 1500, bold: true }),
    cell("4월", { width: 1200 }),
    cell("$1,108,645", { width: 1700, align: AlignmentType.RIGHT }),
    cell("$1,054,551", { width: 1700, align: AlignmentType.RIGHT }),
    cell("-$54,094", { width: 1530, align: AlignmentType.RIGHT, bg: NEG_BG }),
    cell("계획 63% (미달)", { width: 1730, align: AlignmentType.CENTER, bg: NEG_BG }),
  ]}),
  new TableRow({ children: [
    cell("Qualcomm", { width: 1500, bold: true }),
    cell("4월", { width: 1200 }),
    cell("$75,276", { width: 1700, align: AlignmentType.RIGHT }),
    cell("$60,033", { width: 1700, align: AlignmentType.RIGHT }),
    cell("-$15,243", { width: 1530, align: AlignmentType.RIGHT, bg: NEG_BG }),
    cell("계획 45% (미달)", { width: 1730, align: AlignmentType.CENTER, bg: NEG_BG }),
  ]}),
  new TableRow({ children: [
    cell("ZF", { width: 1500, bold: true }),
    cell("4월", { width: 1200 }),
    cell("$364,838", { width: 1700, align: AlignmentType.RIGHT }),
    cell("$382,378", { width: 1700, align: AlignmentType.RIGHT }),
    cell("+$17,540", { width: 1530, align: AlignmentType.RIGHT, bg: POS_BG }),
    cell("계획 51% (개선)", { width: 1730, align: AlignmentType.CENTER }),
  ]}),
  new TableRow({ children: [
    cell("A사", { width: 1500, bold: true }),
    cell("4월", { width: 1200 }),
    cell("$77,328", { width: 1700, align: AlignmentType.RIGHT }),
    cell("$81,663", { width: 1700, align: AlignmentType.RIGHT }),
    cell("+$4,335", { width: 1530, align: AlignmentType.RIGHT, bg: POS_BG }),
    cell("신규 PJT 진척", { width: 1730, align: AlignmentType.CENTER }),
  ]}),
  new TableRow({ children: [
    cell("Others", { width: 1500, bold: true }),
    cell("4월", { width: 1200 }),
    cell("$100,000", { width: 1700, align: AlignmentType.RIGHT }),
    cell("$125,494", { width: 1700, align: AlignmentType.RIGHT }),
    cell("+$25,494", { width: 1530, align: AlignmentType.RIGHT, bg: POS_BG }),
    cell("Scrap 매출 증가", { width: 1730, align: AlignmentType.CENTER }),
  ]}),
  new TableRow({ children: [
    cell("합계", { width: 1500, bg: SUBHEADER_BG, bold: true }),
    cell("4월", { width: 1200, bg: SUBHEADER_BG, bold: true }),
    cell("$3,274,909 (85%)", { width: 1700, align: AlignmentType.RIGHT, bg: SUBHEADER_BG, bold: true }),
    cell("$3,283,347 (85%)", { width: 1700, align: AlignmentType.RIGHT, bg: SUBHEADER_BG, bold: true }),
    cell("+$8,438", { width: 1530, align: AlignmentType.RIGHT, bg: POS_BG, bold: true }),
    cell("계획 85% 동등", { width: 1730, align: AlignmentType.CENTER, bg: SUBHEADER_BG, bold: true }),
  ]}),
  new TableRow({ children: [
    cell("합계", { width: 1500, bg: SUBHEADER_BG, bold: true }),
    cell("1~7월 누적", { width: 1200, bg: SUBHEADER_BG, bold: true }),
    cell("$25,989,189 (98%)", { width: 1700, align: AlignmentType.RIGHT, bg: SUBHEADER_BG, bold: true }),
    cell("$26,217,194 (99%)", { width: 1700, align: AlignmentType.RIGHT, bg: SUBHEADER_BG, bold: true }),
    cell("+$228,005", { width: 1530, align: AlignmentType.RIGHT, bg: POS_BG, bold: true }),
    cell("연간 99% 도달", { width: 1730, align: AlignmentType.CENTER, bg: SUBHEADER_BG, bold: true }),
  ]}),
];
content.push(makeTable(salesRows, [1500, 1200, 1700, 1700, 1530, 1730]));

content.push(h3("매출 증감 사유 (전주 대비, W18 보고 기준)"));
content.push(bulletP("MBZ J100 4K 증가 (+$2만)"));
content.push(bulletP("ZF FCA4.8 4.5K 증가 (+$1.4만)"));
content.push(bulletP("Qualcomm Kaanapali 2K 감소 (-$1.5만)"));
content.push(bulletP("Scrap 매출 증가 (+$2.2만)"));
content.push(bulletP("4월 합계 전주 대비 +$41,058 개선", { bold: true }));

content.push(h2("2-2. 주요 개발/영업 진척 사항"));

content.push(h3("LGIT - VMI → LGIT 출하 잔량 (4/29 기준)"));
content.push(bulletP("최종 협의 수량 1,569,206 → 출고 376,575 (전주 313,158 대비 +63K), 잔량 813,555 (전주 863,904 대비 -50K)"));
content.push(bulletP("Gen3 AL5: 잔량 254,832 → 231,264 (-23K), CL4 Housing: 153,245 → 148,096 (-5K)"));
content.push(bulletP("출하 지속 진행 중, 잔량 50K 감소로 진도 양호"));

content.push(h3("삼성 A27/A18"));
content.push(bulletP("[W17] IA70 버전 자재 납품 완료, 백업금형 4벌 라인테스트 자재 납품 예정 → [W18] IA70 최종 버전 치수 검증 시료 발송 완료, 5/4 결과 접수 예정", { bold: true }));
content.push(bulletP("이랜텍 사출 승인 일정: 5/20 (변동 없음)"));
content.push(bulletP("[변동] 삼성 휴무(4/25~5/3) 및 내부 금형 설비 이동으로 백업 금형 검증 일정 5/9 → 5/12 지연. 공급 일정(5/20) 영향 없도록 대응 예정"));
content.push(bulletP("백업 금형 외작 1벌 양산 투입 준비(5/11), 내작 4벌 치수 검증 및 양산 투입 준비(5/12), Spare 2벌 제작 중(~5/10)"));
content.push(bulletP("A18: 이규희 프로 방문 미팅 진행 완료(4/29)"));

content.push(h3("MBCo / 만도브로제"));
content.push(bulletP("거래 종료 협의: 당사 최종 제안 메일 발송(4/22) 후 고객사 협의 지속 진행 중"));

content.push(h3("ZF SCAM6"));
content.push(bulletP("[W17] 브라질 휴무로 DFM 2차 미팅 연기 → [W18] DFM 2차 미팅 자료 보완 및 시스템 업로드 완료, 5/6 미팅 진행 예정", { bold: true }));

content.push(h3("A사 Eagle Eye"));
content.push(bulletP("총 수취 PO $414,828, 출고 $371,949(전주 $317,949 대비 +$54K 진척), PO 잔액 $42,879"));
content.push(bulletP("Glass frame: Mg 73set 출고 완료, 잔여 10set는 Mg Oakley 로고 PEO 적용본으로 5/12 출하 예정"));
content.push(bulletP("PEO 후처리 1차 진행 완료(4/29): 총 12세트, World 7개·Eye 10개 양품 확인"));
content.push(bulletP("2차 패키지 사출 및 실리콘(Temple Arm 외 7종) 초품 입고 확인, TPU Black 대체 소재 검토 중"));
content.push(bulletP("Micro screw M2*3: 4K 4/29 입고 완료 → PEO Glass frame 10set와 함께 출하 예정(5/12)"));

content.push(h3("퀄컴 MTP Mavros / 대만 방문"));
content.push(bulletP("[W17] 신규 4벌 1벌 내작 중, W19 완료 예정 → [W18] 신규 제작 4벌 모두 내작 중, 5/20 완료 목표", { bold: true }));
content.push(bulletP("[W17] 추가 설변 도면 접수(4/22) → [W18] DFM 대응 완료(4/28), 초품 PO 접수 및 수량 확인 완료"));
content.push(bulletP("Martin과 대만 방문 일정 W22 또는 W23으로 합의(MTP Mavros 초품 일정에 따라 조정)"));
content.push(bulletP("초품 일정 지연 만회를 위해 핸드 캐리 예정"));

// ────────────────────────────────────────
// 3. VMI 창고
// ────────────────────────────────────────
content.push(new Paragraph({ children: [new PageBreak()] }));
content.push(h1("3. VMI 창고 재고"));

content.push(h2("3-1. LGIT VMI 재고"));
const lgitVmiRows = [
  new TableRow({ tableHeader: true, children: [
    cell("구분", { width: 2400, bg: HEADER_BG, color: "FFFFFF", bold: true, align: AlignmentType.CENTER }),
    cell("W17 (4/22 기준)", { width: 2320, bg: HEADER_BG, color: "FFFFFF", bold: true, align: AlignmentType.CENTER }),
    cell("W18 (4/29 기준)", { width: 2320, bg: HEADER_BG, color: "FFFFFF", bold: true, align: AlignmentType.CENTER }),
    cell("증감", { width: 2320, bg: HEADER_BG, color: "FFFFFF", bold: true, align: AlignmentType.CENTER }),
  ]}),
  new TableRow({ children: [
    cell("M&C 출고 합계", { width: 2400, bold: true }),
    cell("231,959", { width: 2320, align: AlignmentType.RIGHT }),
    cell("298,990", { width: 2320, align: AlignmentType.RIGHT }),
    cell("+67,031 (출고 증가)", { width: 2320, align: AlignmentType.CENTER, bg: POS_BG }),
  ]}),
  new TableRow({ children: [
    cell("창고에서 출고 합계", { width: 2400, bold: true }),
    cell("278,463", { width: 2320, align: AlignmentType.RIGHT }),
    cell("355,021", { width: 2320, align: AlignmentType.RIGHT }),
    cell("+76,558 (출고 증가)", { width: 2320, align: AlignmentType.CENTER, bg: POS_BG }),
  ]}),
  new TableRow({ children: [
    cell("Balance 합계", { width: 2400, bold: true }),
    cell("364,414", { width: 2320, align: AlignmentType.RIGHT }),
    cell("354,887", { width: 2320, align: AlignmentType.RIGHT }),
    cell("-9,527", { width: 2320, align: AlignmentType.CENTER, bg: POS_BG }),
  ]}),
  new TableRow({ children: [
    cell("4월 불출 금액", { width: 2400, bold: true }),
    cell("$543,814", { width: 2320, align: AlignmentType.RIGHT }),
    cell("$747,951", { width: 2320, align: AlignmentType.RIGHT }),
    cell("+$204,137 (매출 인식 증가)", { width: 2320, align: AlignmentType.CENTER, bg: POS_BG }),
  ]}),
  new TableRow({ children: [
    cell("Balance 금액", { width: 2400, bold: true, bg: SUBHEADER_BG }),
    cell("$823,449", { width: 2320, align: AlignmentType.RIGHT, bg: SUBHEADER_BG, bold: true }),
    cell("$634,156", { width: 2320, align: AlignmentType.RIGHT, bg: SUBHEADER_BG, bold: true }),
    cell("-$189,293 (-23%)", { width: 2320, align: AlignmentType.CENTER, bg: POS_BG, bold: true }),
  ]}),
];
content.push(makeTable(lgitVmiRows, [2400, 2320, 2320, 2320]));

content.push(h2("3-2. MBZ VMI 재고"));
const mbzVmiRows = [
  new TableRow({ tableHeader: true, children: [
    cell("구분", { width: 2400, bg: HEADER_BG, color: "FFFFFF", bold: true, align: AlignmentType.CENTER }),
    cell("W17 (4/22 기준)", { width: 2320, bg: HEADER_BG, color: "FFFFFF", bold: true, align: AlignmentType.CENTER }),
    cell("W18 (4/29 기준)", { width: 2320, bg: HEADER_BG, color: "FFFFFF", bold: true, align: AlignmentType.CENTER }),
    cell("증감", { width: 2320, bg: HEADER_BG, color: "FFFFFF", bold: true, align: AlignmentType.CENTER }),
  ]}),
  new TableRow({ children: [
    cell("M&C 출고 합계", { width: 2400, bold: true }),
    cell("127,312", { width: 2320, align: AlignmentType.RIGHT }),
    cell("209,608", { width: 2320, align: AlignmentType.RIGHT }),
    cell("+82,296 (출고 증가)", { width: 2320, align: AlignmentType.CENTER, bg: POS_BG }),
  ]}),
  new TableRow({ children: [
    cell("창고에서 출고 합계", { width: 2400, bold: true }),
    cell("210,348", { width: 2320, align: AlignmentType.RIGHT }),
    cell("265,748", { width: 2320, align: AlignmentType.RIGHT }),
    cell("+55,400", { width: 2320, align: AlignmentType.CENTER, bg: POS_BG }),
  ]}),
  new TableRow({ children: [
    cell("Balance 합계", { width: 2400, bold: true }),
    cell("193,379", { width: 2320, align: AlignmentType.RIGHT }),
    cell("220,275", { width: 2320, align: AlignmentType.RIGHT }),
    cell("+26,896", { width: 2320, align: AlignmentType.CENTER, bg: NEU_BG }),
  ]}),
  new TableRow({ children: [
    cell("4월 불출 금액", { width: 2400, bold: true }),
    cell("$573,112", { width: 2320, align: AlignmentType.RIGHT }),
    cell("$705,951", { width: 2320, align: AlignmentType.RIGHT }),
    cell("+$132,839 (매출 인식 증가)", { width: 2320, align: AlignmentType.CENTER, bg: POS_BG }),
  ]}),
  new TableRow({ children: [
    cell("Balance 금액", { width: 2400, bold: true, bg: SUBHEADER_BG }),
    cell("$884,276", { width: 2320, align: AlignmentType.RIGHT, bg: SUBHEADER_BG, bold: true }),
    cell("$480,286", { width: 2320, align: AlignmentType.RIGHT, bg: SUBHEADER_BG, bold: true }),
    cell("-$403,990 (-46%)", { width: 2320, align: AlignmentType.CENTER, bg: POS_BG, bold: true }),
  ]}),
];
content.push(makeTable(mbzVmiRows, [2400, 2320, 2320, 2320]));

content.push(p("LGIT VMI Balance 금액은 $189K 감소, MBZ VMI Balance 금액은 $404K 감소하여 양사 모두 적정 재고 수준으로 회복되고 있음. MBZ는 NX4 Housing 한국 이관 영향이 일부 반영된 것으로 분석됨.", { before: 120 }));

// ────────────────────────────────────────
// 4. AR / AP
// ────────────────────────────────────────
content.push(new Paragraph({ children: [new PageBreak()] }));
content.push(h1("4. AR / AP 현황"));

content.push(h2("4-1. AR 현황"));
const arRows = [
  new TableRow({ tableHeader: true, children: [
    cell("구분", { width: 2400, bg: HEADER_BG, color: "FFFFFF", bold: true, align: AlignmentType.CENTER }),
    cell("W17", { width: 2320, bg: HEADER_BG, color: "FFFFFF", bold: true, align: AlignmentType.CENTER }),
    cell("W18", { width: 2320, bg: HEADER_BG, color: "FFFFFF", bold: true, align: AlignmentType.CENTER }),
    cell("증감", { width: 2320, bg: HEADER_BG, color: "FFFFFF", bold: true, align: AlignmentType.CENTER }),
  ]}),
  new TableRow({ children: [
    cell("General Grand Total", { width: 2400, bold: true }),
    cell("$9,876,422", { width: 2320, align: AlignmentType.RIGHT }),
    cell("$8,146,777", { width: 2320, align: AlignmentType.RIGHT }),
    cell("-$1,729,645 ▼", { width: 2320, align: AlignmentType.CENTER, bg: POS_BG }),
  ]}),
  new TableRow({ children: [
    cell("Subsidiary Grand Total (Qualcomm + ASG)", { width: 2400, bold: true }),
    cell("$1,166,728", { width: 2320, align: AlignmentType.RIGHT }),
    cell("$1,193,181", { width: 2320, align: AlignmentType.RIGHT }),
    cell("+$26,454", { width: 2320, align: AlignmentType.CENTER, bg: NEU_BG }),
  ]}),
  new TableRow({ children: [
    cell("TOTAL AR", { width: 2400, bold: true, bg: SUBHEADER_BG }),
    cell("$11,043,150", { width: 2320, align: AlignmentType.RIGHT, bg: SUBHEADER_BG, bold: true }),
    cell("$9,339,958", { width: 2320, align: AlignmentType.RIGHT, bg: SUBHEADER_BG, bold: true }),
    cell("-$1,703,191 ▼", { width: 2320, align: AlignmentType.CENTER, bg: POS_BG, bold: true }),
  ]}),
  new TableRow({ children: [
    cell("AR overdue (전체)", { width: 2400, bold: true }),
    cell("$1,943,930", { width: 2320, align: AlignmentType.RIGHT }),
    cell("$1,666,651", { width: 2320, align: AlignmentType.RIGHT }),
    cell("-$277,279 ▼ (개선)", { width: 2320, align: AlignmentType.CENTER, bg: POS_BG }),
  ]}),
];
content.push(makeTable(arRows, [2400, 2320, 2320, 2320]));

content.push(h3("주요 고객사별 AR 변동"));
content.push(bulletP("LG YANTAI: $1,962,076 → $1,410,682 (-$551,394) 회수 양호 ▼"));
content.push(bulletP("ELENTEC VN: $1,015,413 → $457,118 (-$558,296) 회수 양호 ▼"));
content.push(bulletP("MANDO (ZHANGJIAGANG): $2,299,578 → $1,881,673 (-$417,905) 회수 진행 ▼"));
content.push(bulletP("ZF PSS US (E273): $853,189 → $714,853 (-$138,336) ▼"));
content.push(bulletP("ZF POLAND: $881,547 → $784,805 (-$96,742) ▼"));
content.push(bulletP("LG MEXICO: $516,466 → $562,616 (+$46,150) 소폭 증가"));
content.push(bulletP("MFG-Qualcomm overdue: $766,654 → $797,331 (+$30,677, 4개월 이상 $251,524 잔존) - 지속 모니터링 필요", { bold: true }));

content.push(h2("4-2. AP 현황"));
const apRows = [
  new TableRow({ tableHeader: true, children: [
    cell("구분", { width: 2400, bg: HEADER_BG, color: "FFFFFF", bold: true, align: AlignmentType.CENTER }),
    cell("W17 (4/22 기준)", { width: 2320, bg: HEADER_BG, color: "FFFFFF", bold: true, align: AlignmentType.CENTER }),
    cell("W18 (4/29 기준)", { width: 2320, bg: HEADER_BG, color: "FFFFFF", bold: true, align: AlignmentType.CENTER }),
    cell("증감", { width: 2320, bg: HEADER_BG, color: "FFFFFF", bold: true, align: AlignmentType.CENTER }),
  ]}),
  new TableRow({ children: [
    cell("Total RM (원재료)", { width: 2400 }),
    cell("$4,493,602", { width: 2320, align: AlignmentType.RIGHT }),
    cell("$3,962,760", { width: 2320, align: AlignmentType.RIGHT }),
    cell("-$530,842 ▼", { width: 2320, align: AlignmentType.CENTER, bg: POS_BG }),
  ]}),
  new TableRow({ children: [
    cell("Total Supplies (소모품)", { width: 2400 }),
    cell("$1,874,233", { width: 2320, align: AlignmentType.RIGHT }),
    cell("$1,873,173", { width: 2320, align: AlignmentType.RIGHT }),
    cell("-$1,060", { width: 2320, align: AlignmentType.CENTER, bg: NEU_BG }),
  ]}),
  new TableRow({ children: [
    cell("Total Repair & Service", { width: 2400 }),
    cell("$484,554", { width: 2320, align: AlignmentType.RIGHT }),
    cell("$485,447", { width: 2320, align: AlignmentType.RIGHT }),
    cell("+$893", { width: 2320, align: AlignmentType.CENTER, bg: NEU_BG }),
  ]}),
  new TableRow({ children: [
    cell("Total Outsourcing", { width: 2400 }),
    cell("$293,652", { width: 2320, align: AlignmentType.RIGHT }),
    cell("$250,253", { width: 2320, align: AlignmentType.RIGHT }),
    cell("-$43,399 ▼", { width: 2320, align: AlignmentType.CENTER, bg: POS_BG }),
  ]}),
  new TableRow({ children: [
    cell("Total AP Logistics", { width: 2400 }),
    cell("$304,674", { width: 2320, align: AlignmentType.RIGHT }),
    cell("$352,420", { width: 2320, align: AlignmentType.RIGHT }),
    cell("+$47,746 ▲", { width: 2320, align: AlignmentType.CENTER, bg: NEG_BG }),
  ]}),
  new TableRow({ children: [
    cell("Total AP Mold", { width: 2400 }),
    cell("$1,373,795", { width: 2320, align: AlignmentType.RIGHT }),
    cell("$1,387,896", { width: 2320, align: AlignmentType.RIGHT }),
    cell("+$14,101", { width: 2320, align: AlignmentType.CENTER, bg: NEU_BG }),
  ]}),
  new TableRow({ children: [
    cell("Total AP GA", { width: 2400 }),
    cell("$300,006", { width: 2320, align: AlignmentType.RIGHT }),
    cell("$275,080", { width: 2320, align: AlignmentType.RIGHT }),
    cell("-$24,926 ▼", { width: 2320, align: AlignmentType.CENTER, bg: POS_BG }),
  ]}),
  new TableRow({ children: [
    cell("Grand TOTAL", { width: 2400, bold: true, bg: SUBHEADER_BG }),
    cell("$9,124,517", { width: 2320, align: AlignmentType.RIGHT, bg: SUBHEADER_BG, bold: true }),
    cell("$8,587,029", { width: 2320, align: AlignmentType.RIGHT, bg: SUBHEADER_BG, bold: true }),
    cell("-$537,488 ▼", { width: 2320, align: AlignmentType.CENTER, bg: POS_BG, bold: true }),
  ]}),
  new TableRow({ children: [
    cell("AP overdue (전체)", { width: 2400, bold: true }),
    cell("$4,190,736", { width: 2320, align: AlignmentType.RIGHT }),
    cell("$3,464,457", { width: 2320, align: AlignmentType.RIGHT }),
    cell("-$726,279 ▼ (개선)", { width: 2320, align: AlignmentType.CENTER, bg: POS_BG }),
  ]}),
];
content.push(makeTable(apRows, [2400, 2320, 2320, 2320]));

content.push(h3("AR/AP 차이"));
content.push(bulletP("W17: AR $11,043K - AP $9,125K = 순포지션 +$1,918K (≈ $192만)"));
content.push(bulletP("W18: AR $9,340K - AP $8,587K = 순포지션 +$753K (≈ $75만, 5/4 $111만 입금 반영)"));
content.push(bulletP("AR/AP 격차 축소 → 단기 자금 부담 완화 및 운전자본 효율화 진전", { bold: true }));

// ────────────────────────────────────────
// 5. 관리 (인사·총무·전산·자동화)
// ────────────────────────────────────────
content.push(new Paragraph({ children: [new PageBreak()] }));
content.push(h1("5. 관리 (인사·총무·전산·자동화)"));

content.push(h2("5-1. 인원 현황"));
const hrRows = [
  new TableRow({ tableHeader: true, children: [
    cell("직군", { width: 2340, bg: HEADER_BG, color: "FFFFFF", bold: true, align: AlignmentType.CENTER }),
    cell("W17", { width: 2340, bg: HEADER_BG, color: "FFFFFF", bold: true, align: AlignmentType.CENTER }),
    cell("W18", { width: 2340, bg: HEADER_BG, color: "FFFFFF", bold: true, align: AlignmentType.CENTER }),
    cell("증감", { width: 2340, bg: HEADER_BG, color: "FFFFFF", bold: true, align: AlignmentType.CENTER }),
  ]}),
  new TableRow({ children: [
    cell("직접 (생산+검사)", { width: 2340 }),
    cell("557명", { width: 2340, align: AlignmentType.CENTER }),
    cell("554명", { width: 2340, align: AlignmentType.CENTER }),
    cell("-3명", { width: 2340, align: AlignmentType.CENTER, bg: NEU_BG }),
  ]}),
  new TableRow({ children: [
    cell("간접 (관리·기술)", { width: 2340 }),
    cell("242명", { width: 2340, align: AlignmentType.CENTER }),
    cell("242명", { width: 2340, align: AlignmentType.CENTER }),
    cell("0명", { width: 2340, align: AlignmentType.CENTER, bg: NEU_BG }),
  ]}),
  new TableRow({ children: [
    cell("Total", { width: 2340, bold: true, bg: SUBHEADER_BG }),
    cell("799명", { width: 2340, align: AlignmentType.CENTER, bg: SUBHEADER_BG, bold: true }),
    cell("796명", { width: 2340, align: AlignmentType.CENTER, bg: SUBHEADER_BG, bold: true }),
    cell("-3명", { width: 2340, align: AlignmentType.CENTER, bg: NEU_BG, bold: true }),
  ]}),
  new TableRow({ children: [
    cell("월별 인원계획 (5월 목표)", { width: 2340 }),
    cell("807명", { width: 2340, align: AlignmentType.CENTER }),
    cell("807명", { width: 2340, align: AlignmentType.CENTER }),
    cell("계획 대비 -11명", { width: 2340, align: AlignmentType.CENTER, bg: NEG_BG }),
  ]}),
  new TableRow({ children: [
    cell("퇴직 예정 (금주+내주)", { width: 2340 }),
    cell("3명", { width: 2340, align: AlignmentType.CENTER }),
    cell("6명 (금주 2 + 내주 4)", { width: 2340, align: AlignmentType.CENTER }),
    cell("+3명 ▲", { width: 2340, align: AlignmentType.CENTER, bg: NEG_BG }),
  ]}),
];
content.push(makeTable(hrRows, [2340, 2340, 2340, 2340]));
content.push(p("전월 대비 11명 감소(W17: 8명 감소). 5월 목표 807명 대비 11명 부족 → 충원 필요", { before: 80 }));

content.push(h3("인사·총무 주요 업무 (W18 신규/변경 사항)"));
content.push(bulletP("[W17→W18] 휴일 당직 운영 대상 변경: 4/26~27 + 4/30~5/1 → 4/30~5/1 노동절 휴일 당직 계획"));
content.push(bulletP("[W18 신규] CNC1 화장실 안내·경고 표지 설치(4/29~5/6)"));
content.push(bulletP("[W18 신규] 화물차 단가 조정 및 택시업체 Mai Linh → Xanh SM 전환 검토(4/22~4/28)"));
content.push(bulletP("[W18 신규] 출장자용 회사 숙소 임대 계약 - 선샤인시티 S-3305호(5/5)"));
content.push(bulletP("[W18 신규] 주방 바닥 보수 실시(4/30 휴일 활용)"));
content.push(bulletP("[W17 진행] RBA 1차(EHS) 평가 75.5점(C등급) 후속 개선 작업 진행 중 → W18에서는 별도 보고 항목 없음"));

content.push(h2("5-2. 전산팀"));
content.push(bulletP("[W17] A사 이중 백업 시스템 구축, 사내방송시스템 수리 → [W18] 비전시스템 업데이트(전용 카메라 → 일반 카메라 + AI 소프트웨어, 카메라 4대 추가하여 총 6대) 진행", { bold: true }));
content.push(bulletP("ZF Cover 모델 적용, 향후 ERP/MES 연동 생산·불량 조회 추가 개발 예정"));

content.push(h2("5-3. 자동화 (현장 개선)"));
content.push(h3("주요 진행 변동"));
content.push(bulletP("화장실 개조: CNC1 완료, 사무실 구역 5/15 진행 (W17은 4/26 사무실 진행 예정 → 일정 변경)"));
content.push(bulletP("주조기용 집진 팬·집진 처리 타워 설치: 4/26 배기팬 설치, 4/30 덕트 공사 진행 → W18에서는 5/2 완료 예정으로 진척"));
content.push(bulletP("[W18 신규] 중전압 차단기 교체 및 변전소 시험 (5/1 작업), 5/1 07:00~12:00 정전 예정 (알루미늄 용해로 유지를 위해 발전기 1대 사용)"));
content.push(bulletP("Mold 실 철거 및 개조 공사 4/30 시작 예정 (W17에서는 4/26 설비 이전 진행)"));
content.push(bulletP("[W17 → W18] 2500kVA 변압기 일정: 7/15 → 4/28~6/25로 단축 및 승인 완료 후 발주 예정", { bold: true }));
content.push(bulletP("[W18 신규] CNC4 구역 Cleaning·Deburring 공정 설치(4/28~6/28) 방안 수립 중"));

// ────────────────────────────────────────
// 6. 생산
// ────────────────────────────────────────
content.push(new Paragraph({ children: [new PageBreak()] }));
content.push(h1("6. 생산"));

content.push(h2("6-1. 생산 1팀 - Casting 공정 달성율/수율"));
const prod1Rows = [
  new TableRow({ tableHeader: true, children: [
    cell("부품군", { width: 1872, bg: HEADER_BG, color: "FFFFFF", bold: true, align: AlignmentType.CENTER }),
    cell("W16 달성율/수율", { width: 1872, bg: HEADER_BG, color: "FFFFFF", bold: true, align: AlignmentType.CENTER }),
    cell("W17 달성율/수율", { width: 1872, bg: HEADER_BG, color: "FFFFFF", bold: true, align: AlignmentType.CENTER }),
    cell("달성율 증감", { width: 1872, bg: HEADER_BG, color: "FFFFFF", bold: true, align: AlignmentType.CENTER }),
    cell("수율 증감", { width: 1872, bg: HEADER_BG, color: "FFFFFF", bold: true, align: AlignmentType.CENTER }),
  ]}),
  new TableRow({ children: [
    cell("자동차 하우징 (7종)", { width: 1872, bold: true }),
    cell("95% / 78%", { width: 1872, align: AlignmentType.CENTER }),
    cell("92% / 82%", { width: 1872, align: AlignmentType.CENTER }),
    cell("-3%p ▼", { width: 1872, align: AlignmentType.CENTER, bg: NEG_BG }),
    cell("+4%p ▲", { width: 1872, align: AlignmentType.CENTER, bg: POS_BG }),
  ]}),
  new TableRow({ children: [
    cell("자동차 커버 (7종)", { width: 1872, bold: true }),
    cell("95% / 90%", { width: 1872, align: AlignmentType.CENTER }),
    cell("92% / 90%", { width: 1872, align: AlignmentType.CENTER }),
    cell("-3%p ▼", { width: 1872, align: AlignmentType.CENTER, bg: NEG_BG }),
    cell("동일", { width: 1872, align: AlignmentType.CENTER, bg: NEU_BG }),
  ]}),
  new TableRow({ children: [
    cell("카메라/그외 (10종)", { width: 1872, bold: true }),
    cell("85% / 89%", { width: 1872, align: AlignmentType.CENTER }),
    cell("84% / 88%", { width: 1872, align: AlignmentType.CENTER }),
    cell("-1%p ▼", { width: 1872, align: AlignmentType.CENTER, bg: NEG_BG }),
    cell("-1%p ▼", { width: 1872, align: AlignmentType.CENTER, bg: NEG_BG }),
  ]}),
  new TableRow({ children: [
    cell("브라켓 (1종)", { width: 1872, bold: true }),
    cell("92% / 91%", { width: 1872, align: AlignmentType.CENTER }),
    cell("90% / 91%", { width: 1872, align: AlignmentType.CENTER }),
    cell("-2%p ▼", { width: 1872, align: AlignmentType.CENTER, bg: NEG_BG }),
    cell("동일", { width: 1872, align: AlignmentType.CENTER, bg: NEU_BG }),
  ]}),
  new TableRow({ children: [
    cell("전체 (25종)", { width: 1872, bold: true, bg: SUBHEADER_BG }),
    cell("92% / 87%", { width: 1872, align: AlignmentType.CENTER, bg: SUBHEADER_BG, bold: true }),
    cell("90% / 87%", { width: 1872, align: AlignmentType.CENTER, bg: SUBHEADER_BG, bold: true }),
    cell("-2%p ▼", { width: 1872, align: AlignmentType.CENTER, bg: NEG_BG, bold: true }),
    cell("동일", { width: 1872, align: AlignmentType.CENTER, bg: NEU_BG, bold: true }),
  ]}),
];
content.push(makeTable(prod1Rows, [1872, 1872, 1872, 1872, 1872]));

content.push(h3("W17 달성율 미달성 사유 (생산 1팀)"));
content.push(bulletP("AL5 HOUSING (81%): 형상핀 파손으로 인한 금형 핀 교체 작업으로 비가동 발생"));
content.push(bulletP("GEN4 COVER (84%): 게이트부 침식에 인한 덧살 발생 수리 작업으로 비가동 발생"));
content.push(p("수율은 전반적으로 W16과 유사한 수준으로 안정적으로 유지됨. 달성율 2%p 하락은 금형 수리 비가동에 기인.", { before: 80 }));

content.push(h2("6-2. 생산 2팀 - 공정별 달성율/수율"));
const prod2Rows = [
  new TableRow({ tableHeader: true, children: [
    cell("공정", { width: 2340, bg: HEADER_BG, color: "FFFFFF", bold: true, align: AlignmentType.CENTER }),
    cell("W16 달성율/수율", { width: 2340, bg: HEADER_BG, color: "FFFFFF", bold: true, align: AlignmentType.CENTER }),
    cell("W17 달성율/수율", { width: 2340, bg: HEADER_BG, color: "FFFFFF", bold: true, align: AlignmentType.CENTER }),
    cell("증감 평가", { width: 2340, bg: HEADER_BG, color: "FFFFFF", bold: true, align: AlignmentType.CENTER }),
  ]}),
  new TableRow({ children: [
    cell("TRIMMING (33모델)", { width: 2340 }),
    cell("91.6% / 98.5%", { width: 2340, align: AlignmentType.CENTER }),
    cell("89.3% / 98.6%", { width: 2340, align: AlignmentType.CENTER }),
    cell("달성율 -2.3%p ▼", { width: 2340, align: AlignmentType.CENTER, bg: NEG_BG }),
  ]}),
  new TableRow({ children: [
    cell("POLISHING (25모델)", { width: 2340 }),
    cell("91.3% / 98.8%", { width: 2340, align: AlignmentType.CENTER }),
    cell("87.7% / 98.9%", { width: 2340, align: AlignmentType.CENTER }),
    cell("달성율 -3.6%p ▼", { width: 2340, align: AlignmentType.CENTER, bg: NEG_BG }),
  ]}),
  new TableRow({ children: [
    cell("CHROMATE (14모델)", { width: 2340 }),
    cell("77.8% / 98.6%", { width: 2340, align: AlignmentType.CENTER }),
    cell("78.4% / 98.7%", { width: 2340, align: AlignmentType.CENTER }),
    cell("달성율 +0.6%p ▲", { width: 2340, align: AlignmentType.CENTER, bg: POS_BG }),
  ]}),
  new TableRow({ children: [
    cell("CNC (33모델)", { width: 2340 }),
    cell("89.7% / 94.7%", { width: 2340, align: AlignmentType.CENTER }),
    cell("93.5% / 92.1%", { width: 2340, align: AlignmentType.CENTER }),
    cell("달성율 +3.8%p ▲", { width: 2340, align: AlignmentType.CENTER, bg: POS_BG }),
  ]}),
];
content.push(makeTable(prod2Rows, [2340, 2340, 2340, 2340]));

content.push(h3("W17 미달성 모델 및 대책"));
content.push(bulletP("NX4 COVER (CNC, 98.3%/79.5%): 17주차 동심도 치수 불량 급증. JIG 검사 NG품 CMM 측정 시 OK 판정 → JIG 베어링 유동에 의한 측정 편차로 확인, JIG 수리 진행 중"));
content.push(bulletP("LQ2 COVER (TRIMMING, 95.4%/99.2%): 박리(57.1%), 뜯김(20%), 미성형(13%) 불량. 트리밍 하측 JIG 안착 시 유동으로 상측 핀에 의한 눌림 확인 → 금형팀에 유동방지 핀 추가 요청, 일정 확인 중"));

content.push(h3("CNC 설비 가동율 (W17)"));
content.push(bulletP("총 444대 중 437대 가동, 가동율 98% (전주 99% 대비 -1%p)"));
content.push(bulletP("설비 고장율 1.1% (목표 1% 이하 관리, 전주 1.3% 대비 개선)"));
content.push(bulletP("AL5 라인 외주업체 이동 완료, 금형실 설비 CNC 1공정 이동 완료"));

content.push(h2("6-3. 직통율"));
const dtRows = [
  new TableRow({ tableHeader: true, children: [
    cell("부품군", { width: 1872, bg: HEADER_BG, color: "FFFFFF", bold: true, align: AlignmentType.CENTER }),
    cell("구분", { width: 1872, bg: HEADER_BG, color: "FFFFFF", bold: true, align: AlignmentType.CENTER }),
    cell("W16", { width: 1872, bg: HEADER_BG, color: "FFFFFF", bold: true, align: AlignmentType.CENTER }),
    cell("W17", { width: 1872, bg: HEADER_BG, color: "FFFFFF", bold: true, align: AlignmentType.CENTER }),
    cell("증감", { width: 1872, bg: HEADER_BG, color: "FFFFFF", bold: true, align: AlignmentType.CENTER }),
  ]}),
  new TableRow({ children: [
    cell("Auto Housing", { width: 1872, bold: true }),
    cell("캐스팅", { width: 1872, align: AlignmentType.CENTER }),
    cell("95.69%", { width: 1872, align: AlignmentType.CENTER }),
    cell("96.59%", { width: 1872, align: AlignmentType.CENTER }),
    cell("+0.90%p ▲", { width: 1872, align: AlignmentType.CENTER, bg: POS_BG }),
  ]}),
  new TableRow({ children: [
    cell("Auto Housing", { width: 1872 }),
    cell("공정전체", { width: 1872, align: AlignmentType.CENTER }),
    cell("73.62%", { width: 1872, align: AlignmentType.CENTER }),
    cell("72.79%", { width: 1872, align: AlignmentType.CENTER }),
    cell("-0.83%p ▼", { width: 1872, align: AlignmentType.CENTER, bg: NEG_BG }),
  ]}),
  new TableRow({ children: [
    cell("Auto Cover", { width: 1872, bold: true }),
    cell("캐스팅", { width: 1872, align: AlignmentType.CENTER }),
    cell("96.94%", { width: 1872, align: AlignmentType.CENTER }),
    cell("97.54%", { width: 1872, align: AlignmentType.CENTER }),
    cell("+0.60%p ▲", { width: 1872, align: AlignmentType.CENTER, bg: POS_BG }),
  ]}),
  new TableRow({ children: [
    cell("Auto Cover", { width: 1872 }),
    cell("공정전체", { width: 1872, align: AlignmentType.CENTER }),
    cell("87.54%", { width: 1872, align: AlignmentType.CENTER }),
    cell("84.00%", { width: 1872, align: AlignmentType.CENTER }),
    cell("-3.54%p ▼", { width: 1872, align: AlignmentType.CENTER, bg: NEG_BG }),
  ]}),
  new TableRow({ children: [
    cell("Camera & Others", { width: 1872, bold: true }),
    cell("캐스팅", { width: 1872, align: AlignmentType.CENTER }),
    cell("97.64%", { width: 1872, align: AlignmentType.CENTER }),
    cell("97.97%", { width: 1872, align: AlignmentType.CENTER }),
    cell("+0.33%p ▲", { width: 1872, align: AlignmentType.CENTER, bg: POS_BG }),
  ]}),
  new TableRow({ children: [
    cell("Camera & Others", { width: 1872 }),
    cell("공정전체", { width: 1872, align: AlignmentType.CENTER }),
    cell("85.43%", { width: 1872, align: AlignmentType.CENTER }),
    cell("84.73%", { width: 1872, align: AlignmentType.CENTER }),
    cell("-0.70%p ▼", { width: 1872, align: AlignmentType.CENTER, bg: NEG_BG }),
  ]}),
  new TableRow({ children: [
    cell("Mobile", { width: 1872, bold: true }),
    cell("캐스팅", { width: 1872, align: AlignmentType.CENTER }),
    cell("98.96%", { width: 1872, align: AlignmentType.CENTER }),
    cell("98.80%", { width: 1872, align: AlignmentType.CENTER }),
    cell("-0.16%p", { width: 1872, align: AlignmentType.CENTER, bg: NEU_BG }),
  ]}),
  new TableRow({ children: [
    cell("Mobile", { width: 1872 }),
    cell("공정전체", { width: 1872, align: AlignmentType.CENTER }),
    cell("86.36%", { width: 1872, align: AlignmentType.CENTER }),
    cell("87.74%", { width: 1872, align: AlignmentType.CENTER }),
    cell("+1.38%p ▲", { width: 1872, align: AlignmentType.CENTER, bg: POS_BG }),
  ]}),
  new TableRow({ children: [
    cell("전체 직통율", { width: 1872, bold: true, bg: SUBHEADER_BG }),
    cell("주차 평균", { width: 1872, align: AlignmentType.CENTER, bg: SUBHEADER_BG, bold: true }),
    cell("81.1%", { width: 1872, align: AlignmentType.CENTER, bg: SUBHEADER_BG, bold: true }),
    cell("82.1%", { width: 1872, align: AlignmentType.CENTER, bg: SUBHEADER_BG, bold: true }),
    cell("+1.0%p ▲", { width: 1872, align: AlignmentType.CENTER, bg: POS_BG, bold: true }),
  ]}),
];
content.push(makeTable(dtRows, [1872, 1872, 1872, 1872, 1872]));

content.push(p("캐스팅 공정 직통율은 전반적으로 개선(+0.3 ~ +0.9%p)되었으나, Auto Cover 공정전체 -3.5%p 하락이 두드러짐 (NX4 COVER 동심도 치수 불량 영향).", { before: 80 }));

content.push(h2("6-4. 금형 팀"));
content.push(bulletP("수리 외 신작 금형 6세트 제작 중 (W17과 동일 수준 유지)"));
content.push(bulletP("4월 신작 금형 완료 진행: A276 #17~#18 (4/18~4/19 완료), A276 #19~#20 (4/27 완료) → W17 보고 대비 #19/#20 완료 처리"));
content.push(bulletP("A276 #17 S1 / #18 S1: 5/10 완료 예정"));
content.push(bulletP("50-97060-1: 4/29 → 5/5로 일정 변경", { bold: true }));
content.push(bulletP("CNC 가동율 64.8% (W17 65.0%) / EDM 65.8% (W17 65.4%) / 와이어컷 69.3% (W17 66.2%) / 평균 66.5% (W17 66.0%) → +0.5%p 소폭 개선"));
content.push(bulletP("DOOSAN 4050: 베어링 교체 완료 (W17 보고 시점 4/24 수리 완료 예정 → 정상 가동 중)", { bold: true }));

// ────────────────────────────────────────
// 7. 품질
// ────────────────────────────────────────
content.push(new Paragraph({ children: [new PageBreak()] }));
content.push(h1("7. 품질"));

content.push(h2("7-1. 고객 품질 현황 (NCR)"));
const ncrRows = [
  new TableRow({ tableHeader: true, children: [
    cell("구분", { width: 2340, bg: HEADER_BG, color: "FFFFFF", bold: true, align: AlignmentType.CENTER }),
    cell("W17 (4월 누적)", { width: 2340, bg: HEADER_BG, color: "FFFFFF", bold: true, align: AlignmentType.CENTER }),
    cell("W18 (4월 누적)", { width: 2340, bg: HEADER_BG, color: "FFFFFF", bold: true, align: AlignmentType.CENTER }),
    cell("증감", { width: 2340, bg: HEADER_BG, color: "FFFFFF", bold: true, align: AlignmentType.CENTER }),
  ]}),
  new TableRow({ children: [
    cell("4월 NCR 건수", { width: 2340, bold: true }),
    cell("9건", { width: 2340, align: AlignmentType.CENTER }),
    cell("13건", { width: 2340, align: AlignmentType.CENTER }),
    cell("+4건 ▲ (악화)", { width: 2340, align: AlignmentType.CENTER, bg: NEG_BG }),
  ]}),
  new TableRow({ children: [
    cell("월간 목표", { width: 2340 }),
    cell("2건", { width: 2340, align: AlignmentType.CENTER }),
    cell("2건", { width: 2340, align: AlignmentType.CENTER }),
    cell("목표 대비 6.5배 초과", { width: 2340, align: AlignmentType.CENTER, bg: NEG_BG }),
  ]}),
];
content.push(makeTable(ncrRows, [2340, 2340, 2340, 2340]));

content.push(h3("주요 신규/추가 클레임 사항 (W18 신규)"));
content.push(bulletP("LGMQ LQ2 COVER 미가공 문제 접수: 고객사 선별 요청 접수(대상수량 46,872EA), 선별 진행 중", { bold: true }));
content.push(bulletP("EU2L Housing QR 라벨 번짐 발생 (ZF 멕시코): 선별 진행 중 QR 라벨 쉽게 지워짐 고객사 확인(4/29). 기존 확인된 QR 라벨 리본 불량(납품처 라벨 사양 임의 변경) 로트(2025년 11월 ~ 2026년 1월 초)임. 추가 대응 방안 정리 후 5/2 보고 예정", { bold: true }));

content.push(h3("W17 보고 클레임 (참고)"));
content.push(bulletP("CL4/AL5/T6 Housing 외관 불량 및 핀 휨 (LGIT YT) - 재 선별 NCR 대응 중"));
content.push(bulletP("FCA HOUSING 날개부위 치수 불량 - 24K 선별 진행, 운송중 150K 미선별 요청"));
content.push(bulletP("MAS65 외관 불량 선별 - 49,273EA 검사 완료 NG 372EA"));

content.push(h2("7-2. 품질 외부비용"));
const costRows = [
  new TableRow({ tableHeader: true, children: [
    cell("구분", { width: 2340, bg: HEADER_BG, color: "FFFFFF", bold: true, align: AlignmentType.CENTER }),
    cell("W17 (4월 누적)", { width: 2340, bg: HEADER_BG, color: "FFFFFF", bold: true, align: AlignmentType.CENTER }),
    cell("W18 (4월 누적)", { width: 2340, bg: HEADER_BG, color: "FFFFFF", bold: true, align: AlignmentType.CENTER }),
    cell("증감", { width: 2340, bg: HEADER_BG, color: "FFFFFF", bold: true, align: AlignmentType.CENTER }),
  ]}),
  new TableRow({ children: [
    cell("선별비", { width: 2340 }),
    cell("$203,609 (63.2%)", { width: 2340, align: AlignmentType.RIGHT }),
    cell("$213,660 (62.0%)", { width: 2340, align: AlignmentType.RIGHT }),
    cell("+$10,051 ▲", { width: 2340, align: AlignmentType.CENTER, bg: NEG_BG }),
  ]}),
  new TableRow({ children: [
    cell("클레임 비용", { width: 2340 }),
    cell("$1,208 (0.4%)", { width: 2340, align: AlignmentType.RIGHT }),
    cell("$1,208 (0.4%)", { width: 2340, align: AlignmentType.RIGHT }),
    cell("동일", { width: 2340, align: AlignmentType.CENTER, bg: NEU_BG }),
  ]}),
  new TableRow({ children: [
    cell("RMA", { width: 2340 }),
    cell("$43,791 (13.6%)", { width: 2340, align: AlignmentType.RIGHT }),
    cell("$55,848 (16.2%)", { width: 2340, align: AlignmentType.RIGHT }),
    cell("+$12,057 ▲", { width: 2340, align: AlignmentType.CENTER, bg: NEG_BG }),
  ]}),
  new TableRow({ children: [
    cell("VMI 창고", { width: 2340 }),
    cell("$73,807 (22.9%)", { width: 2340, align: AlignmentType.RIGHT }),
    cell("$73,807 (21.4%)", { width: 2340, align: AlignmentType.RIGHT }),
    cell("동일", { width: 2340, align: AlignmentType.CENTER, bg: NEU_BG }),
  ]}),
  new TableRow({ children: [
    cell("총액 (4월 누적)", { width: 2340, bold: true, bg: SUBHEADER_BG }),
    cell("$322,415", { width: 2340, align: AlignmentType.RIGHT, bg: SUBHEADER_BG, bold: true }),
    cell("$344,523", { width: 2340, align: AlignmentType.RIGHT, bg: SUBHEADER_BG, bold: true }),
    cell("+$22,108 ▲", { width: 2340, align: AlignmentType.CENTER, bg: NEG_BG, bold: true }),
  ]}),
];
content.push(makeTable(costRows, [2340, 2340, 2340, 2340]));

content.push(h3("주요 변동 사유"));
content.push(bulletP("LGIT YT 비용: $215,603 → $236,051 (+$20,448) - 4월 4주차 LGIT 선별 추가 진행"));
content.push(bulletP("Mando Brose 비용: $87,223 → $88,883 (+$1,660) 소폭 증가"));
content.push(bulletP("ELENTEC 비용: $8,029 (W18에서 A376 크랙 불량 RMA $2,859 비용 협의 50:50)", { bold: true }));
content.push(bulletP("4월 주말 특근 선별 미진행으로 3월 $49K → 4월 $29K (40.8% 절감) 효과 지속"));

content.push(h2("7-3. AS9100 인증 진행 (5/23 완료 목표)"));
const as9100Rows = [
  new TableRow({ tableHeader: true, children: [
    cell("부서", { width: 1872, bg: HEADER_BG, color: "FFFFFF", bold: true, align: AlignmentType.CENTER }),
    cell("문서 건수", { width: 1872, bg: HEADER_BG, color: "FFFFFF", bold: true, align: AlignmentType.CENTER }),
    cell("W17 진척도", { width: 1872, bg: HEADER_BG, color: "FFFFFF", bold: true, align: AlignmentType.CENTER }),
    cell("W18 진척도", { width: 1872, bg: HEADER_BG, color: "FFFFFF", bold: true, align: AlignmentType.CENTER }),
    cell("평가", { width: 1872, bg: HEADER_BG, color: "FFFFFF", bold: true, align: AlignmentType.CENTER }),
  ]}),
  new TableRow({ children: [
    cell("인사총무", { width: 1872 }),
    cell("2건", { width: 1872, align: AlignmentType.CENTER }),
    cell("정량 미보고", { width: 1872, align: AlignmentType.CENTER }),
    cell("0%", { width: 1872, align: AlignmentType.CENTER }),
    cell("미착수", { width: 1872, align: AlignmentType.CENTER, bg: NEG_BG }),
  ]}),
  new TableRow({ children: [
    cell("개발영업", { width: 1872 }),
    cell("4건", { width: 1872, align: AlignmentType.CENTER }),
    cell("정량 미보고", { width: 1872, align: AlignmentType.CENTER }),
    cell("0%", { width: 1872, align: AlignmentType.CENTER }),
    cell("미착수", { width: 1872, align: AlignmentType.CENTER, bg: NEG_BG }),
  ]}),
  new TableRow({ children: [
    cell("생산/기술", { width: 1872 }),
    cell("12건", { width: 1872, align: AlignmentType.CENTER }),
    cell("정량 미보고", { width: 1872, align: AlignmentType.CENTER }),
    cell("0%", { width: 1872, align: AlignmentType.CENTER }),
    cell("미착수", { width: 1872, align: AlignmentType.CENTER, bg: NEG_BG }),
  ]}),
  new TableRow({ children: [
    cell("기타(경영)", { width: 1872 }),
    cell("2건", { width: 1872, align: AlignmentType.CENTER }),
    cell("정량 미보고", { width: 1872, align: AlignmentType.CENTER }),
    cell("0%", { width: 1872, align: AlignmentType.CENTER }),
    cell("미착수", { width: 1872, align: AlignmentType.CENTER, bg: NEG_BG }),
  ]}),
  new TableRow({ children: [
    cell("품질", { width: 1872 }),
    cell("21건", { width: 1872, align: AlignmentType.CENTER }),
    cell("정량 미보고", { width: 1872, align: AlignmentType.CENTER }),
    cell("0%", { width: 1872, align: AlignmentType.CENTER }),
    cell("미착수", { width: 1872, align: AlignmentType.CENTER, bg: NEG_BG }),
  ]}),
  new TableRow({ children: [
    cell("구매", { width: 1872 }),
    cell("3건", { width: 1872, align: AlignmentType.CENTER }),
    cell("정량 미보고", { width: 1872, align: AlignmentType.CENTER }),
    cell("0%", { width: 1872, align: AlignmentType.CENTER }),
    cell("미착수", { width: 1872, align: AlignmentType.CENTER, bg: NEG_BG }),
  ]}),
  new TableRow({ children: [
    cell("생산관리", { width: 1872 }),
    cell("3건", { width: 1872, align: AlignmentType.CENTER }),
    cell("정량 미보고", { width: 1872, align: AlignmentType.CENTER }),
    cell("33% (1건 완료)", { width: 1872, align: AlignmentType.CENTER }),
    cell("진척 ▲", { width: 1872, align: AlignmentType.CENTER, bg: POS_BG }),
  ]}),
  new TableRow({ children: [
    cell("TOTAL", { width: 1872, bold: true, bg: SUBHEADER_BG }),
    cell("47건", { width: 1872, align: AlignmentType.CENTER, bg: SUBHEADER_BG, bold: true }),
    cell("정량 미보고", { width: 1872, align: AlignmentType.CENTER, bg: SUBHEADER_BG, bold: true }),
    cell("2% (1건 완료)", { width: 1872, align: AlignmentType.CENTER, bg: SUBHEADER_BG, bold: true }),
    cell("가속 필요 ▲", { width: 1872, align: AlignmentType.CENTER, bg: NEG_BG, bold: true }),
  ]}),
];
content.push(makeTable(as9100Rows, [1872, 1872, 1872, 1872, 1872]));

content.push(p("절차서·지침서 총 47종 중 1건만 완료(생산관리 지침서). 5/23 완료 목표 대비 진척 가속 필요. 매주 금요일마다 진척사항 공지 예정.", { before: 80 }));

content.push(h3("기타 품질 진행 사항"));
content.push(bulletP("강석하 차장 한국 휴가: 4/24 ~ 5/2 (W17 보고 대비 동일)"));
content.push(bulletP("[W18 신규] ZF 중국 안팅 출장 5/8~5/10: 강석하 차장 출장. 고객사 요청에 의한 당사 품질 개선안 발표", { bold: true }));

// ────────────────────────────────────────
// 8. 결론 및 향후 과제
// ────────────────────────────────────────
content.push(new Paragraph({ children: [new PageBreak()] }));
content.push(h1("8. 결론 및 향후 과제"));

content.push(h2("8-1. 긍정적 변화 (개선 항목)"));
content.push(bulletP("재무 건전성: AR $1.7M·AP $537K 동시 감소, AR/AP 차이 $192만 → $75만 축소 → 운전자본 효율 개선", { bold: true }));
content.push(bulletP("매출 진척: 4월 +$41K, 1~7월 누적 +$228K 개선. 7월 예상 매출 $4,145K (계획 109%)로 상반기 목표 달성 가능성 ↑"));
content.push(bulletP("VMI 재고 정상화: LGIT -$189K, MBZ -$404K → 재고 회전 양호"));
content.push(bulletP("직통율: 81.1% → 82.1% (+1.0%p) 개선, 캐스팅 직통율 전반적 상승"));
content.push(bulletP("개발 진척: 삼성 A27 IA70 치수 검증 시료 발송, ZF SCAM6 DFM 2차 진행, 퀄컴 MTP Mavros 신규 4벌 모두 내작 중"));
content.push(bulletP("4월 외부비용 주말 특근 절감 효과 지속 (3월 대비 40.8% 절감)"));

content.push(h2("8-2. 우려/주의 항목"));
content.push(bulletP("품질 NCR 4건 추가 발생 → 4월 13건으로 목표(2건) 대비 6.5배 초과. LGIT LQ2 미가공·ZF EU2L QR 라벨 번짐 후속 대응 필요", { bold: true }));
content.push(bulletP("4월 외부비용 +$22K 증가 (LGIT YT 선별·RMA 증가)"));
content.push(bulletP("생산 1팀 Casting 달성율 -2%p 하락 (AL5 형상핀 파손, GEN4 게이트부 침식 수리)"));
content.push(bulletP("Auto Cover 공정전체 직통율 -3.5%p 하락 (NX4 COVER 동심도 치수 불량)"));
content.push(bulletP("MFG-Qualcomm AR overdue $797K (4개월 이상 $251K 잔존) 지속 관리 필요"));
content.push(bulletP("AS9100 진척도 2%로 5/23 목표 대비 부족 → 전사적 가속 필요"));
content.push(bulletP("인원 현황: 5월 계획 807명 대비 11명 부족, 퇴직 예정 6명(금주 2 + 내주 4)으로 인력 충원 시급"));
content.push(bulletP("Samsung 4월 매출 계획 대비 63%, Qualcomm 45%로 미달 → 5월 회복 필요"));

content.push(h2("8-3. 단기 추진 과제 (5월 첫째 주)"));
content.push(bulletP("ZF EU2L Housing QR 라벨 번짐 추가 대응 방안 5/2 보고"));
content.push(bulletP("LGIT LQ2 COVER 미가공 선별 완료 및 NCR 종결"));
content.push(bulletP("삼성 A27 IA70 최종 치수 검증 결과 접수 (5/4) 및 5/9 #2차 조립 테스트 결과 접수"));
content.push(bulletP("백업 금형 외작 1벌 양산 투입 준비 (5/11), 내작 4벌 치수 검증 (5/12)"));
content.push(bulletP("ZF SCAM6 DFM 2차 미팅 진행 (5/6)"));
content.push(bulletP("A사 Eagle Eye Mg Oakley PEO 10세트 + Micro screw 출하 (5/12)"));
content.push(bulletP("강석하 차장 ZF 중국 안팅 출장 품질 개선안 발표 (5/8~5/10)"));
content.push(bulletP("Casting 동 배기팬·덕트 설치 완료 (5/2), 5/1 변전소 시험 및 정전 작업"));
content.push(bulletP("AS9100 절차서·지침서 작성 가속화 - 매주 금요일 진척 공지"));
content.push(bulletP("인력 충원 활동 강화 (퇴직 6명 발생 예정)"));

// 마지막 푸터 라인
content.push(new Paragraph({
  alignment: AlignmentType.CENTER,
  spacing: { before: 480, after: 0 },
  border: { top: { style: BorderStyle.SINGLE, size: 6, color: "1F4E78", space: 1 } },
  children: [
    new TextRun({ text: "─ 보고서 끝 ─", font: FONT, size: 18, color: "606060", italics: true })
  ]
}));

// ========================
// Document 생성
// ========================
const doc = new Document({
  creator: "Vietnam Subsidiary",
  title: "W18주 주간보고 비교분석 (W17 대비)",
  styles: {
    default: {
      document: { run: { font: FONT, size: 20 } }
    },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 32, bold: true, font: FONT, color: "1F4E78" },
        paragraph: { spacing: { before: 360, after: 180 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 26, bold: true, font: FONT, color: "2E5984" },
        paragraph: { spacing: { before: 280, after: 120 }, outlineLevel: 1 } },
      { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 22, bold: true, font: FONT, color: "404040" },
        paragraph: { spacing: { before: 200, after: 80 }, outlineLevel: 2 } },
    ]
  },
  sections: [{
    properties: {
      page: {
        size: { width: 12240, height: 15840 },
        margin: { top: 1080, right: 1080, bottom: 1080, left: 1080 }
      }
    },
    headers: {
      default: new Header({
        children: [new Paragraph({
          alignment: AlignmentType.RIGHT,
          children: [new TextRun({ text: "베트남 법인 W18 주간보고 비교분석", font: FONT, size: 16, color: "808080" })]
        })]
      })
    },
    footers: {
      default: new Footer({
        children: [new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [
            new TextRun({ text: "Page ", font: FONT, size: 16, color: "808080" }),
            new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: 16, color: "808080" }),
            new TextRun({ text: " / ", font: FONT, size: 16, color: "808080" }),
            new TextRun({ children: [PageNumber.TOTAL_PAGES], font: FONT, size: 16, color: "808080" }),
          ]
        })]
      })
    },
    children: content
  }]
});

Packer.toBuffer(doc).then(buffer => {
  const outPath = "/sessions/eager-awesome-bohr/mnt/주간보고/W18주_주간보고_비교분석_W17주 대비.docx";
  fs.writeFileSync(outPath, buffer);
  console.log("Saved:", outPath);
  console.log("Size:", buffer.length, "bytes");
});
