@echo off
echo ==============================================
echo =   GERANDO O INSTALADOR INNO SETUP          =
echo ==============================================

if not exist "dist\GeradorDeLista.exe" (
    echo ERRO: Arquivo base nao encontrado! Rode build_app.bat primeiro!
    pause
    exit /b
)

echo Extraindo versao do codigo Python...
for /f "delims=" %%i in ('python -c "from app.version import VERSION; print(VERSION)"') do set APP_VERSION=%%i
echo Versao %APP_VERSION% carregada com sucesso!

"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" /dMyAppVersion="%APP_VERSION%" setup.iss

echo.
echo SUCESSO! O Instalador Profissional esta na pasta "Output"!
pause
