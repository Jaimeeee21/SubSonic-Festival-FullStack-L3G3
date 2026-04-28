@echo off
setlocal

powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0sync-data-files.ps1" "%~dp0."

endlocal