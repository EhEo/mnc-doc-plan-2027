// KPI 대시보드 공통 유틸리티

function calcPct(actual, target) {
    if (!target || target === 0) return 0;
    return Math.min((actual / target) * 100, 150);
}

function pctClass(pct) {
    if (pct >= 100) return "green";
    if (pct >= 80) return "yellow";
    return "red";
}

function renderProgressBar(container, pct) {
    const cls = pctClass(pct);
    const width = Math.min(pct, 100);
    container.innerHTML = `
        <div class="progress-bar">
            <div class="progress-fill fill-${cls}" style="width:${width}%"></div>
        </div>`;
}

function formatDate(dateStr) {
    if (!dateStr) return "-";
    return dateStr.substring(0, 7);
}

function getLatestActual(monthlyActuals) {
    const keys = Object.keys(monthlyActuals || {}).sort().reverse();
    return keys.length > 0 ? { month: keys[0], value: monthlyActuals[keys[0]] } : null;
}
