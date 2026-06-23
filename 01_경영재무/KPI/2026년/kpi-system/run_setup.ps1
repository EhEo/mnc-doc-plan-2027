# KPI 시스템 초기 셋업 스크립트
# 실행: cd "D:\Michael\OneDrive - Team Redpanda\ClaudeCowork\01_경영재무\KPI\2026년" && .\kpi-system\run_setup.ps1

$root = "D:\Michael\OneDrive - Team Redpanda\ClaudeCowork\01_경영재무\KPI\2026년"
Set-Location $root

Write-Host "=== M&C KPI 시스템 초기 셋업 ===" -ForegroundColor Cyan

# 의존성 확인
python -c "import openpyxl" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "openpyxl 설치 중..." -ForegroundColor Yellow
    pip install openpyxl -q
}

# 템플릿 생성
python kpi-system\scripts\setup_templates.py
Write-Host "✅ Excel 템플릿 생성 완료" -ForegroundColor Green

# 빈 대시보드 생성
python kpi-system\scripts\03_generate_dashboard.py
Write-Host "✅ 대시보드 초기 생성 완료" -ForegroundColor Green

Write-Host ""
Write-Host "다음 단계:" -ForegroundColor Yellow
Write-Host "  1. kpi-system\templates\KPI_수립서_TEMPLATE.xlsx 를 각 부문 폴더에 복사하여 작성"
Write-Host "  2. 각 부문 작성 완료 후 run_monthly.ps1 실행"
Write-Host ""
Write-Host "대시보드 열기:" -ForegroundColor Cyan
Write-Host "  Start-Process '$root\kpi-system\dashboard\index.html'"
