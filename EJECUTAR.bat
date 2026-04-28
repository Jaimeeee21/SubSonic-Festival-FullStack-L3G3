@echo off
chcp 65001 >nul
cls

echo ╔════════════════════════════════════════════════════════════════╗
echo ║         SubSonic Festival - Backend y Frontend                ║
echo ║              Iniciando automáticamente...                     ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Python no está instalado o no está en PATH
    echo Descarga Python desde: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python detectado
echo.

REM Verificar si ya están instalados los requerimientos
pip show fastapi >nul 2>&1
if errorlevel 1 (
    echo ⏳ Instalando dependencias (esto puede tomar 1-2 minutos)...
    echo.
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ Error al instalar dependencias
        pause
        exit /b 1
    )
    echo ✅ Dependencias instaladas
) else (
    echo ✅ Dependencias ya están instaladas
)

echo.
echo ⏳ Inicializando base de datos...
python seed_data.py >nul 2>&1

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                  Servidor iniciado ✅                         ║
echo ║                                                                ║
echo ║  🌐 URL: http://localhost:8000                                ║
echo ║  📚 Documentación API: http://localhost:8000/docs             ║
echo ║                                                                ║
echo ║  ⏹️  Presiona CTRL+C para detener el servidor                 ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

REM Abrir el navegador automáticamente
start http://localhost:8000

REM Ejecutar el servidor
python run.py
