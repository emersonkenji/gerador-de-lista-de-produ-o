# Gerador de Lista de Produção

Aplicativo desktop em Python/PySide6 para gerar listas de produção de tintas a partir de planilhas XLSX exportadas do UpSeller.

## Stack
- Python 3.11+
- PySide6 (GUI)
- SQLAlchemy + SQLite (banco local)
- Pandas + openpyxl (leitura XLSX)
- PyInstaller (build)

## Funcionalidades
- Importação de XLSX com auto-save
- Cadastro automático de lojas e produtos
- Classificação inteligente com popup para tipos não identificados
- Gestão de tipos de tinta e litragens customizáveis
- Histórico com visualização, cópia, exportação e impressão
- Atualização automática via GitHub Releases (repos públicos e privados)
- Tema dark/light inspirado em Shadcn/UI

## Como rodar
```bash
pip install PySide6 pandas openpyxl sqlalchemy packaging
python main.py
```

## Como gerar executável
```bash
python build_script.py
```

## Atualização via GitHub
1. Vá em Configurações
2. Informe `usuario/repo` e opcionalmente o Personal Access Token
3. Clique em "Verificar Atualizações"
