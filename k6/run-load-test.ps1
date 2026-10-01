# Runner script para ejecutar la prueba de carga con k6 usando Docker
param(
    [string]$TargetUrl = "http://api:8000"
)

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "     INICIANDO PRUEBA DE CARGA CON K6 (10-20 VUs)         " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "Destino:   $TargetUrl" -ForegroundColor Yellow
Write-Host "Dashboard: http://localhost:3000 (Abre tu navegador para ver los graficos en vivo)" -ForegroundColor Green
Write-Host "Duracion:  ~40 segundos (10s subida a 10 VUs -> 20s sostenido a 20 VUs -> 10s bajada)`n" -ForegroundColor Gray

$k6Path = (Get-Item $PSScriptRoot).FullName -replace '\\', '/'

docker run --rm -i `
  --network docker_default `
  -e TARGET_URL="$TargetUrl" `
  -v "${k6Path}:/k6" `
  grafana/k6 run /k6/load_test.js

Write-Host "`n[OK] Prueba de carga finalizada. Revisa los paneles en Grafana (http://localhost:3000)." -ForegroundColor Green
