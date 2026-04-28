@echo off
REM Script para sincronizar la hora del sistema
REM Ejecutar como administrador

echo Sincronizando hora del sistema...
net start w32time
w32tm /resync /force
w32tm /query /status
echo.
echo Sincronizacion completada
pause
