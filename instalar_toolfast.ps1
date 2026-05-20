# PowerShell Script para instalar 'toolfast' en la máquina de tus compañeros.
# Este script instalará las librerías necesarias y creará los accesos directos para la consola.

$ErrorActionPreference = "Stop"

Write-Host "=== INSTALADOR DE TOOLFAST (Navaja Suiza CLI) ===" -ForegroundColor Cyan

# 1. Comprobar si Python está instalado
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Python detectado: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "Error: Python no está instalado o no se encuentra en el PATH del sistema." -ForegroundColor Red
    Write-Host "Por favor, descarga e instala Python desde https://www.python.org/ y vuelve a intentarlo." -ForegroundColor Yellow
    Exit
}

# 2. Crear carpeta de destino para el script de Python en el directorio de usuario
$userHome = [System.Environment]::GetFolderPath("UserProfile")
$installDir = Join-Path $userHome ".toolfast"
if (-not (Test-Path $installDir)) {
    New-Item -ItemType Directory -Path $installDir | Out-Null
    Write-Host "Creada carpeta de instalacion en: $installDir" -ForegroundColor Gray
}

# 3. Descargar/Copiar el script principal (toolfast.py)
$sourceScript = Join-Path $PSScriptRoot "toolfast.py"
$destScript = Join-Path $installDir "toolfast.py"

if (Test-Path $sourceScript) {
    Copy-Item -Path $sourceScript -Destination $destScript -Force
    Write-Host "Archivo principal copiado localmente con exito." -ForegroundColor Green
} else {
    Write-Host "No se encontro el script localmente. Descargando ultima version desde GitHub..." -ForegroundColor Cyan
    $rawUrl = "https://raw.githubusercontent.com/AlejoColazurda/toolfast/main/toolfast.py"
    try {
        [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.SecurityProtocolType]::Tls12
        Invoke-WebRequest -Uri $rawUrl -OutFile $destScript -UseBasicParsing
        Write-Host "Script toolfast.py descargado correctamente desde GitHub." -ForegroundColor Green
    } catch {
        Write-Host "Error al descargar el script desde GitHub: $_" -ForegroundColor Red
        Exit
    }
}

# 4. Instalar dependencias requeridas (pypdf, pillow, openpyxl)
Write-Host "Instalando/Verificando librerias de Python (pypdf, pillow, openpyxl)..." -ForegroundColor Cyan
& python -m pip install pypdf pillow openpyxl

# 5. Crear accesos directos en la carpeta NPM del usuario (que ya esta en el PATH)
$appData = [System.Environment]::GetFolderPath("ApplicationData")
$npmDir = Join-Path $appData "npm"

if (-not (Test-Path $npmDir)) {
    New-Item -ItemType Directory -Path $npmDir | Out-Null
}

$cmdFile = Join-Path $npmDir "toolfast.cmd"
$ps1File = Join-Path $npmDir "toolfast.ps1"

# Contenido para CMD
$cmdContent = @"
@echo off
python "$destScript" %*
"@

# Contenido para PowerShell
$ps1Content = @"
python "$destScript" `$args
"@

# Escribir los wrappers
Set-Content -Path $cmdFile -Value $cmdContent -Force
Set-Content -Path $ps1File -Value $ps1Content -Force

# Notificacion final amigable
Write-Host "`n============================================================" -ForegroundColor Cyan
Write-Host "       INSTALACION COMPLETADA CON EXITO! (v1.0.0)" -ForegroundColor Green
Write-Host "       Desarrollado por: Alejo Colazurda" -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Para comenzar a usar la herramienta:" -ForegroundColor White
Write-Host "1. Abre una NUEVA ventana de Simbolo del Sistema (cmd) o PowerShell." -ForegroundColor Yellow
Write-Host "   (Esto es obligatorio para que el sistema reconozca el nuevo comando)." -ForegroundColor Gray
Write-Host "2. Escribe el comando para iniciar el programa:" -ForegroundColor White
Write-Host "   ***   toolfast   ***" -ForegroundColor Green
Write-Host "3. Presiona Enter y listo!" -ForegroundColor White
Write-Host "============================================================" -ForegroundColor Cyan
