# KPI 대시보드 HTML 생성기 — JSON 데이터를 읽어 정적 HTML 생성

import json
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).parent.parent
DEPT_ORDER = ["관리부문","생산1부문","생산2부문","품질부문","개발영업부문"]

def collect_all_kpi_data(kpi_root: Path) -> list:
    result = []
    for dept in DEPT_ORDER:
        json_path = kpi_root / dept / "kpi_data.json"
        if json_path.exists():
            data = json.loads(json_path.read_text(encoding="utf-8"))
            result.append(data)
    return result

def get_latest_actual(monthly_actuals: dict):
    if not monthly_actuals:
        return None, None
    keys = sorted(monthly_actuals.keys(), reverse=True)
    return keys[0], monthly_actuals[keys[0]]

def calc_pct(actual, target):
    if not target:
        return 0
    return round(min((actual / target) * 100, 150), 1)

def pct_class(pct):
    if pct >= 100: return "green"
    if pct >= 80:  return "yellow"
    return "red"

def render_kpi_row(kpi: dict) -> str:
    _, actual = get_latest_actual(kpi.get("monthly_actuals", {}))
    if actual is not None:
        pct = calc_pct(actual, kpi["target"])
        pct_str = f"{pct:.1f}%"
        actual_str = f"{actual}{kpi['unit']}"
        cls = pct_class(pct)
        width = min(pct, 100)
        bar = f'<div class="progress-bar"><div class="progress-fill fill-{cls}" style="width:{width:.0f}%"></div></div>'
        badge = f'<span class="pct-badge pct-{cls}">{pct_str}</span>'
    else:
        actual_str = "미입력"
        bar = '<div class="progress-bar"><div class="progress-fill fill-yellow" style="width:0%"></div></div>'
        badge = '<span class="pct-badge pct-yellow">-</span>'

    return f"""
    <div class="kpi-row">
        <span class="kpi-name">{kpi['name']}</span>
        <span class="kpi-target">목표: {kpi['target']}{kpi['unit']}</span>
        {bar}
        <span class="kpi-actual">{actual_str}</span>
        {badge}
    </div>"""

def render_dept_card(dept_data: dict) -> str:
    kpi_rows = "".join(render_kpi_row(k) for k in dept_data["kpis"])
    status = dept_data.get("status", "draft")
    status_badge = f'<span class="badge badge-{status}">{status}</span>'
    dept_name = dept_data["dept"]
    dept_url = f"dept_{dept_name}.html"
    return f"""
    <div class="dept-card">
        <h3><a href="{dept_url}">{dept_name}</a> {status_badge}</h3>
        {kpi_rows}
    </div>"""

def render_index_html(all_data: list) -> str:
    generated = datetime.now().strftime("%Y-%m-%d %H:%M")
    dept_cards = "\n".join(render_dept_card(d) for d in all_data)

    total_kpis = sum(len(d["kpis"]) for d in all_data)
    depts_active = sum(1 for d in all_data if d.get("status") == "active")

    achieved, total = 0, 0
    for d in all_data:
        for k in d["kpis"]:
            _, actual = get_latest_actual(k.get("monthly_actuals", {}))
            if actual is not None:
                if calc_pct(actual, k["target"]) >= 100:
                    achieved += 1
                total += 1
    overall_pct = f"{achieved}/{total}" if total else "데이터 없음"
    summary_cls = "green" if total > 0 else "yellow"

    nav_links = "".join(f'<a href="dept_{d["dept"]}.html">{d["dept"]}</a>' for d in all_data)
    empty_msg = '<p style="color:#888;padding:24px;">등록된 KPI 데이터가 없습니다. Excel 수립서를 제출하고 변환 스크립트를 실행하세요.</p>'

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>M&amp;C KPI 대시보드 — 2026</title>
<link rel="stylesheet" href="css/style.css">
</head>
<body>
<div class="header">
    <div>
        <h1>M&amp;C Electronics Vina — KPI 관리 대시보드</h1>
        <div class="subtitle">2026 하반기 / 최종 업데이트: {generated}</div>
    </div>
</div>
<nav class="nav">
    <a href="index.html" class="active">전체 현황</a>
    {nav_links}
</nav>
<div class="container">
    <div class="summary-grid">
        <div class="summary-card">
            <div class="label">등록 부문</div>
            <div class="value">{len(all_data)}</div>
            <div class="sub">/ 5 부문</div>
        </div>
        <div class="summary-card green">
            <div class="label">활성 부문</div>
            <div class="value">{depts_active}</div>
            <div class="sub">실적 입력 완료</div>
        </div>
        <div class="summary-card">
            <div class="label">전체 KPI 수</div>
            <div class="value">{total_kpis}</div>
            <div class="sub">개 지표</div>
        </div>
        <div class="summary-card {summary_cls}">
            <div class="label">목표 달성 항목</div>
            <div class="value">{overall_pct}</div>
            <div class="sub">개 달성 (≥100%)</div>
        </div>
    </div>
    <div class="dept-grid">
        {dept_cards if all_data else empty_msg}
    </div>
</div>
<script src="js/app.js"></script>
</body>
</html>"""

def render_dept_html(dept_data: dict, all_depts: list) -> str:
    dept_name = dept_data["dept"]
    generated = datetime.now().strftime("%Y-%m-%d %H:%M")
    nav_links = "\n".join(
        f'<a href="dept_{d["dept"]}.html" {"class=\"active\"" if d["dept"]==dept_name else ""}>{d["dept"]}</a>'
        for d in all_depts
    )
    rows = ""
    for k in dept_data["kpis"]:
        _, actual = get_latest_actual(k.get("monthly_actuals", {}))
        if actual is not None:
            pct = calc_pct(actual, k["target"])
            pct_str = f'{pct:.1f}%'
            cls = pct_class(pct)
            bar = f'<div class="progress-bar" style="width:120px;display:inline-block"><div class="progress-fill fill-{cls}" style="width:{min(pct,100):.0f}%"></div></div>'
        else:
            pct_str, bar = "-", '<span style="color:#888">미입력</span>'
        rows += f"""
        <tr>
            <td>{k['id']}</td>
            <td>{k['category']}</td>
            <td>{k['name']}</td>
            <td>{k['target']}{k['unit']}</td>
            <td>{actual if actual is not None else '-'}{k['unit'] if actual is not None else ''}</td>
            <td>{bar}</td>
            <td><strong>{pct_str}</strong></td>
            <td>{k['weight']}%</td>
            <td>{k['owner']}</td>
        </tr>"""

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<title>{dept_name} — KPI 현황</title>
<link rel="stylesheet" href="css/style.css">
</head>
<body>
<div class="header">
    <div>
        <h1>M&amp;C KPI — {dept_name}</h1>
        <div class="subtitle">2026 하반기 / 업데이트: {generated}</div>
    </div>
</div>
<nav class="nav">
    <a href="index.html">전체 현황</a>
    {nav_links}
</nav>
<div class="container">
    <table class="kpi-table">
        <thead>
            <tr>
                <th>KPI_ID</th><th>분류</th><th>KPI명</th>
                <th>목표</th><th>실적</th><th>진행</th>
                <th>달성률</th><th>가중치</th><th>담당자</th>
            </tr>
        </thead>
        <tbody>{rows}</tbody>
    </table>
</div>
<script src="js/app.js"></script>
</body>
</html>"""

def main():
    kpi_root = BASE_DIR / "01_KPI수립_2026H2"
    dash_dir = BASE_DIR / "dashboard"
    dash_dir.mkdir(parents=True, exist_ok=True)

    all_data = collect_all_kpi_data(kpi_root)

    (dash_dir / "index.html").write_text(render_index_html(all_data), encoding="utf-8")
    print("[OK] index.html created")

    for dept_data in all_data:
        fname = f"dept_{dept_data['dept']}.html"
        (dash_dir / fname).write_text(render_dept_html(dept_data, all_data), encoding="utf-8")
        print(f"[OK] {fname} created")

    if not all_data:
        print("[WARN] No KPI data — empty dashboard generated")
    else:
        print(f"\nDashboard path: {dash_dir / 'index.html'}")

if __name__ == "__main__":
    main()
