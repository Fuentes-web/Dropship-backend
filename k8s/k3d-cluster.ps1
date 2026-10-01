# Helper script para gestionar el cluster de K3s local con k3d
param(
    [ValidateSet("create", "delete", "start", "stop", "status")]
    [string]$Action = "status"
)

$ClusterName = "dropship-k3s"

switch ($Action) {
    "create" {
        Write-Host "Creando cluster K3s '$ClusterName'..." -ForegroundColor Cyan
        k3d cluster create $ClusterName `
            -p "30080:30080@server:0" `
            --k3s-arg "--disable=traefik@server:0"
        
        Write-Host "`nImportando imagen dropship-api:latest..." -ForegroundColor Yellow
        k3d image import dropship-api:latest -c $ClusterName
        
        Write-Host "`nAplicando manifiestos..." -ForegroundColor Green
        kubectl apply -f "$PSScriptRoot/configmap.yaml" `
                      -f "$PSScriptRoot/secret.yaml" `
                      -f "$PSScriptRoot/postgres-pvc.yaml" `
                      -f "$PSScriptRoot/postgres-deployment.yaml" `
                      -f "$PSScriptRoot/api-deployment.yaml"
    }
    "delete" {
        Write-Host "Eliminando cluster K3s '$ClusterName'..." -ForegroundColor Red
        k3d cluster delete $ClusterName
    }
    "stop" {
        Write-Host "Deteniendo cluster K3s '$ClusterName' para ahorrar memoria..." -ForegroundColor Yellow
        k3d cluster stop $ClusterName
    }
    "start" {
        Write-Host "Iniciando cluster K3s '$ClusterName'..." -ForegroundColor Green
        k3d cluster start $ClusterName
    }
    "status" {
        Write-Host "=== ESTADO DE NODOS K3S ===" -ForegroundColor Cyan
        kubectl get nodes -o wide
        Write-Host "`n=== ESTADO DE PODS ===" -ForegroundColor Cyan
        kubectl get pods -o wide
        Write-Host "`n=== SERVICIOS ===" -ForegroundColor Cyan
        kubectl get svc
    }
}
