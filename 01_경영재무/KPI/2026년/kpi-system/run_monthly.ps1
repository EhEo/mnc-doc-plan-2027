# 월간 KPI 실적 처리 스크립트
# 실행: .\kpi-system\run_monthly.ps1 -Month 2026-07

param([string]$Month = (Get-Date -Format "yyyy-MM"))

$root = "D:\Michael\OneDrive - Team Redpanda\ClaudeCowork\01_경영재무\KPI\2026년"
Set-Location $root

Write-Host "=== M&C KPI 월간 처리: $Month ===" -ForegroundColor Cyan

$depts = @("관리부문","생산1부문","생산2부문","품질부문","개발영업부문")
$mm = ($Month -split '-')[1]

# Step 1: Excel → JSON 변환
Write-Host "`nStep 1: Excel → JSON 변환" -ForegroundColor Cyan
foreach ($dept in $depts) {
    $xlsxPath = "kpi-system\02_월간추적\$Month\${dept}_${mm}실적.xlsx"
    $jsonOut   = "kpi-system\01_KPI수립_2026H2\$dept\kpi_data.json"
    if (Test-Path $xlsxPath) {
        Write-Host "  변환 중: $dept" -ForegroundColor Gray
        python kpi-system\scripts\02_excel_to_json.py $xlsxPath --out $jsonOut
    } else {
        Write-Host "  ⚠️  실적 파일 없음: $xlsxPath" -ForegroundColor Yellow
    }
}

# Step 2: 검증
Write-Host "`nStep 2: 데이터 검증" -ForegroundColor Cyan
foreach ($dept in $depts) {
    $jsonPath = "kpi-system\01_KPI수립_2026H2\$dept\kpi_data.json"
    if (Test-Path $jsonPath) {
        python kpi-system\scripts\01_validate_kpi.py $jsonPath
    }
}

# Step 3: 대시보드 갱신
Write-Host "`nStep 3: 대시보드 갱신" -ForegroundColor Cyan
python kpi-system\scripts\03_generate_dashboard.py
Write-Host "✅ 대시보드 갱신 완료" -ForegroundColor Green

# Step 4: 결과 열기
$dashPath = "$root\kpi-system\dashboard\index.html"
Write-Host "`n대시보드 경로: $dashPath" -ForegroundColor Cyan
Write-Host "브라우저로 열려면: Start-Process '$dashPath'"
