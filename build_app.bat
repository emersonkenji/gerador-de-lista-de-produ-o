@echo off
echo ==============================================
echo Compilando Gerador de Lista de Producao...
echo ==============================================

python -m PyInstaller --name "GeradorDeLista" --windowed --onefile --noconfirm --clean --hidden-import="PySide6.QtPrintSupport" --hidden-import="openpyxl" --hidden-import="pandas" --hidden-import="sqlalchemy" main.py

echo.
echo ==============================================
echo Compilacao Concluida!
echo O arquivo instalador (.exe) esta na pasta "dist".
echo ==============================================
pause
