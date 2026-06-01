# 📦 GUIA DE BUILD E RELEASE - Gerador de Lista v1.0.3

## ⚡ FORMA RÁPIDA (Recomendado!)

Abra o PowerShell no diretório do projeto e execute:

```bash
.\build.bat
```

Isso abre um **menu interativo** com 4 opções:
1. ✅ Build Simples (.exe autocontido)
2. ✅ Build Profissional (Instalador Inno Setup)
3. ✅ Limpar builds antigos
4. ✅ Testar aplicação

---

## 1️⃣ OPÇÕES DE BUILD

### Opção A: Build Simples (Executável Único)
Cria um arquivo `.exe` autocontido em `dist/`

```bash
# Usando menu interativo
.\build.bat
# Escolha opção 1

# Ou usando batch direto
build_app.bat

# Ou usando Python
python build_script.py
```

**Resultado**: `dist/GeradorDeLista.exe` (~100-200MB)
**Tempo**: 2-3 minutos
**Instalação**: Apenas copie o .exe para qualquer lugar

---

### Opção B: Build Profissional (Instalador Inno Setup)
Cria um instalador `.exe` profissional com opções de instalação

**Pré-requisitos**:
- ✅ Inno Setup 6 instalado: https://jrsoftware.org/isinfo.php
- ✅ PyInstaller instalado: `pip install pyinstaller`

**Passos (Automático)**:
```bash
.\build.bat
# Escolha opção 2
```

**Passos (Manual)**:
```bash
# 1. Gerar executável base
build_app.bat

# 2. Gerar instalador profissional
gerar_instalador.bat
```

**Resultado**: 
- `dist/GeradorDeLista.exe` (executável)
- `Output/GeradorDeLista-1.0.3.exe` (instalador profissional)

**Tempo**: 3-5 minutos
**Instalação**: Execute o instalador (.exe) na pasta Output

---

### Opção C: Instalação Manual

Use `install_script.bat` para instalar manualmente:

```bash
# Copie o executável para o diretório e execute:
install_script.bat
```

Isso irá:
- ✅ Copiar para `%LOCALAPPDATA%\Programs\GeradorDeLista`
- ✅ Criar atalho na Área de Trabalho
- ✅ Criar entrada no menu Iniciar

---

## 2️⃣ PREPARAÇÃO ANTES DE FAZER BUILD

### Checklist:
```bash
# ✅ Verificar versão
type app\version.py

# ✅ Limpar builds antigos (automático em build.bat)
.\build.bat
# Escolha opção 3

# ✅ Verificar Git status (deve estar limpo)
git status

# ✅ Verificar tag Git
git tag -l | grep v1.0.3
```

---

## 3️⃣ ARQUIVOS PARA INCLUIR NO GIT

### ✅ INCLUIR NO GIT:
```
app/                    (código-fonte)
requirements.txt
main.py
CHANGELOG.md
RELEASE_NOTES_v1.0.3.md
BUILD_GUIDE.md
build.bat              (NOVO! Menu maestro)
build_app.bat
build_script.py
gerar_instalador.bat
install_script.bat
GeradorDeLista.spec
setup.iss
```

### ❌ NÃO INCLUIR NO GIT (.gitignore):
```
build/             (pasta temporária de build)
dist/              (executáveis)
Output/            (instaladores)
*.exe              (arquivos compilados)
__pycache__/
*.pyc
database.db        (dados locais)
.venv/
.pytest_cache/
```

---

## 4️⃣ SCRIPTS DISPONÍVEIS

### `build.bat` (NOVO - MENU INTERATIVO)
```bash
.\build.bat
```
Menu interativo com todas as opções. **RECOMENDADO!**

### `build_app.bat`
```bash
.\build_app.bat
```
Build simples com PyInstaller. Resultado: `dist/GeradorDeLista.exe`

### `build_script.py`
```bash
python build_script.py
```
Alternativa em Python ao `build_app.bat`

### `gerar_instalador.bat`
```bash
.\gerar_instalador.bat
```
Requer: `build_app.bat` já executado
Gera: Instalador profissional com Inno Setup

### `install_script.bat`
```bash
.\install_script.bat
```
Instala a aplicação no `%LOCALAPPDATA%\Programs\GeradorDeLista`

---

## 5️⃣ FLUXO COMPLETO DE RELEASE

### Passo 1: Preparar Código
```bash
# Verificar mudanças
git status

# Corrigir erros/testes
python main.py

# Commitare versionar (JÁ FEITO!)
git log --oneline -5
```

### Passo 2: Fazer Build
```bash
# Executar menu interativo
.\build.bat

# Escolher opção 2 para Build Profissional
```

### Passo 3: Testar Executável
```bash
# Testar .exe gerado
dist\GeradorDeLista.exe

# ou testar instalador
Output\GeradorDeLista-1.0.3.exe
```

### Passo 4: Criar Release no GitHub (Opcional)
1. Acesse: https://github.com/emersonkenji/gerador-de-lista-de-produ-o/releases
2. Clique em "Create a new release"
3. Tag: `v1.0.3`
4. Faça upload do `.exe` de `Output/`

---

## 6️⃣ ARQUIVO .gitignore (Recomendado)

```gitignore
# Build outputs
build/
dist/
Output/
*.exe
*.exe~
*.spec

# Python
__pycache__/
*.pyc
*.pyo
*.egg-info/
.Python
env/
venv/
.venv/

# Database
database.db
*.db

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
Thumbs.db
.DS_Store

# Temporary files
_test_*.py
_analyze.py
*.tmp
*.log
```

---

## 📋 STATUS ATUAL - v1.0.3

```
✅ Código versionado no Git
✅ Tag v1.0.3 criada
✅ CHANGELOG atualizado
✅ RELEASE_NOTES criado
✅ BUILD_GUIDE.md completo
✅ Script build.bat criado

⏳ Próximos passos:
  → Executar: .\build.bat
  → Escolher opção 2
  → Testar Output\GeradorDeLista-1.0.3.exe
  → Fazer upload para GitHub Releases (opcional)
```

---

## 🚀 QUICK START - TUDO EM UM COMANDO

```powershell
# Abra PowerShell no diretório do projeto e execute:
.\build.bat

# Opção 2 para Build Profissional
# Aguarde 3-5 minutos
# Resultado: Output\GeradorDeLista-1.0.3.exe
```

---

## 📝 NOTAS IMPORTANTES

1. **Inno Setup**: Se não tiver instalado, a opção 2 do `build.bat` funcionará parcialmente (gerará o .exe, mas não o instalador)

2. **Antivírus**: Alguns antivírus podem bloquear a geração. Se isso acontecer, adicione o diretório à whitelist do antivírus.

3. **PyInstaller**: Se receber erro, tente: `pip install --upgrade pyinstaller`

4. **Versão**: A versão é lida automaticamente de `app/version.py`. Para mudar a versão, edite aquele arquivo.

---

**Gerador de Lista v1.0.3** - Pronto para release! 🎉

