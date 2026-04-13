; Arquivo de Configuração do Instalador (Inno Setup)
; Baixe o Inno Setup em: https://jrsoftware.org/isdl.php

[Setup]
AppName=Gerador de Lista de Produção
AppVersion={#MyAppVersion}
AppPublisher=ColorsPro
DefaultDirName={localappdata}\Programs\GeradorDeLista
DefaultGroupName=Gerador de Lista
; Instalar apenas para o usuário atual evita pedir acesso de Administrador e permite que o atualizador automático funcione!
PrivilegesRequired=lowest
OutputDir=Output
OutputBaseFilename=Instalador_GeradorDeLista
Compression=lzma
SolidCompression=yes
SetupIconFile=compiler:SetupClassicIcon.ico
UninstallDisplayIcon={app}\GeradorDeLista.exe

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; Aponta para o EXE que o PyInstaller criou
Source: "dist\GeradorDeLista.exe"; DestDir: "{app}"; Flags: ignoreversion
; Adicione a base de dados em branco inicial se quiser, ou deixe o app criar na hr de abrir

[Icons]
Name: "{group}\Gerador de Lista de Produção"; Filename: "{app}\GeradorDeLista.exe"
Name: "{group}\Desinstalar Gerador"; Filename: "{uninstallexe}"
Name: "{autodesktop}\Gerador de Lista de Produção"; Filename: "{app}\GeradorDeLista.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\GeradorDeLista.exe"; Description: "{cm:LaunchProgram,Gerador de Lista de Produção}"; Flags: nowait postinstall skipifsilent
