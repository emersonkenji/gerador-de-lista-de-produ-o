@echo off
REM ============================================================
REM Gerador de Lista v1.0.3 - SCRIPT COMPLETO DE BUILD E RELEASE
REM ============================================================

setlocal enabledelayedexpansion

echo.
echo ============================================================
echo    GERADOR DE LISTA - BUILD AUTOMÁTICO v1.0.3
echo ============================================================
echo.

REM Verifica versão
for /f "delims=" %%i in ('python -c "from app.version import VERSION; print(VERSION)"') do set APP_VERSION=%%i
echo [✓] Versão detectada: %APP_VERSION%
echo.

REM Menu de opções
echo Escolha a opção desejada:
echo.
echo 1 - Build Simples (.exe compactado)
echo 2 - Build Profissional (Instalador + .exe)
echo 3 - Limpar builds antigos
echo 4 - Testar aplicação (python)
echo.

set /p CHOICE="Digite sua opção (1-4): "

if "%CHOICE%"=="1" goto SIMPLE_BUILD
if "%CHOICE%"=="2" goto PRO_BUILD
if "%CHOICE%"=="3" goto CLEAN_BUILD
if "%CHOICE%"=="4" goto TEST_APP
goto INVALID

:SIMPLE_BUILD
echo.
echo ============================================================
echo Iniciando BUILD SIMPLES...
echo ============================================================
echo.

if exist "dist" (
    echo [!] Removendo build anterior...
    rmdir /s /q dist >nul 2>&1
    rmdir /s /q build >nul 2>&1
)

echo [→] Executando PyInstaller...
python -m PyInstaller ^
    --name "GeradorDeLista" ^
    --windowed ^
    --onefile ^
    --noconfirm ^
    --clean ^
    --hidden-import="PySide6.QtPrintSupport" ^
    --hidden-import="openpyxl" ^
    --hidden-import="pandas" ^
    --hidden-import="sqlalchemy" ^
    main.py

if errorlevel 1 (
    echo.
    echo [✗] ERRO! Falha na compilação.
    pause
    exit /b 1
)

echo.
echo [✓] Build Concluído!
echo [✓] Executável: dist\GeradorDeLista.exe
echo.
pause
goto END

:PRO_BUILD
echo.
echo ============================================================
echo Iniciando BUILD PROFISSIONAL (com Instalador)...
echo ============================================================
echo.

REM Step 1: Build simples
if exist "dist" (
    echo [!] Removendo build anterior...
    rmdir /s /q dist >nul 2>&1
    rmdir /s /q build >nul 2>&1
)

echo [→] Etapa 1/2: Compilando executável...
python -m PyInstaller ^
    --name "GeradorDeLista" ^
    --windowed ^
    --onefile ^
    --noconfirm ^
    --clean ^
    --hidden-import="PySide6.QtPrintSupport" ^
    --hidden-import="openpyxl" ^
    --hidden-import="pandas" ^
    --hidden-import="sqlalchemy" ^
    main.py

if errorlevel 1 (
    echo.
    echo [✗] ERRO! Falha na compilação do executável.
    pause
    exit /b 1
)

echo [✓] Executável criado com sucesso!
echo.

REM Step 2: Inno Setup
if not exist "dist\GeradorDeLista.exe" (
    echo [✗] ERRO! Arquivo dist\GeradorDeLista.exe não encontrado!
    pause
    exit /b 1
)

echo [→] Etapa 2/2: Gerando instalador profissional...
if exist "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" (
    "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" /dMyAppVersion="%APP_VERSION%" setup.iss
    
    if errorlevel 1 (
        echo [!] Aviso: Inno Setup não gerou corretamente o instalador.
        echo [!] Verifique se Inno Setup 6 está instalado corretamente.
    ) else (
        echo [✓] Instalador criado com sucesso!
    )
) else (
    echo [!] Aviso: Inno Setup 6 não encontrado!
    echo [!] Instalador não será gerado.
    echo [!] Você pode instalar em: https://jrsoftware.org/isinfo.php
)

echo.
echo [✓] Build Profissional Concluído!
echo [✓] Executável: dist\GeradorDeLista.exe
echo [✓] Instalador: Output\GeradorDeLista-%APP_VERSION%.exe
echo.
pause
goto END

:CLEAN_BUILD
echo.
echo ============================================================
echo Limpando builds antigos...
echo ============================================================
echo.

if exist "dist" (
    echo [→] Removendo dist...
    rmdir /s /q dist
)

if exist "build" (
    echo [→] Removendo build...
    rmdir /s /q build
)

if exist "Output" (
    echo [→] Removendo Output...
    rmdir /s /q Output
)

if exist "GeradorDeLista.spec" (
    echo [→] Removendo GeradorDeLista.spec...
    del GeradorDeLista.spec
)

echo [✓] Limpeza concluída!
echo.
pause
goto END

:TEST_APP
echo.
echo ============================================================
echo Testando aplicação...
echo ============================================================
echo.

echo [→] Iniciando main.py...
python main.py

goto END

:INVALID
echo.
echo [✗] Opção inválida!
echo.
pause
goto END

:END
echo.
exit /b
