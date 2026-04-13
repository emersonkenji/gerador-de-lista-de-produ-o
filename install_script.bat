@echo off
set "TARGET_DIR=%LOCALAPPDATA%\Programs\GeradorDeLista"
if not exist "%TARGET_DIR%" mkdir "%TARGET_DIR%"
copy /Y "GeradorDeLista.exe" "%TARGET_DIR%\GeradorDeLista.exe"

set "SHORTCUT=%TEMP%\shortcut.vbs"
echo Set oWS = WScript.CreateObject("WScript.Shell") > "%SHORTCUT%"
echo sLinkFile = "%USERPROFILE%\Desktop\Gerador de Lista.lnk" >> "%SHORTCUT%"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%SHORTCUT%"
echo oLink.TargetPath = "%TARGET_DIR%\GeradorDeLista.exe" >> "%SHORTCUT%"
echo oLink.Save >> "%SHORTCUT%"

call cscript /nologo "%SHORTCUT%"
del "%SHORTCUT%"
mshta vbscript:Execute("msgbox ""Instalação Concluida com Sucesso! Um ícone foi gerado na sua Área de Trabalho para você abrir o Gerador de Lista."",64,""Gerador de Lista"":close")
