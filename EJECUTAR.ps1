#!/usr/bin/env powershell
# SubSonic Festival - Start Server
# Solo ejecuta el servidor y abre el navegador

Write-Host "🚀 Iniciando SubSonic Festival..." -ForegroundColor Green
Write-Host ""

# Instalar dependencias si falta algo
Write-Host "⏳ Verificando dependencias..." -ForegroundColor Yellow
pip install -q -r requirements.txt 2>$null

# Crear BD si no existe
Write-Host "📦 Inicializando base de datos..." -ForegroundColor Yellow
python seed_data.py 2>$null

# Abrir navegador
Write-Host ""
Write-Host "✅ Servidor iniciado en http://localhost:8000" -ForegroundColor Green
Write-Host ""
start "http://localhost:8000"

# Ejecutar servidor
python run.py
