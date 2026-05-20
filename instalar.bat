@echo off
title Instalador de UnificarPDFs
echo ===========================================
echo   Instalando Unificador de PDFs (toolfast)
echo ===========================================
echo.
powershell -ExecutionPolicy Bypass -Command "[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.SecurityProtocolType]::Tls12; iwr -useb https://raw.githubusercontent.com/AlejoColazurda/toolfast/main/instalar_unificarpdfs.ps1 | iex"
echo.
echo Presiona cualquier tecla para cerrar esta ventana.
pause > nul
