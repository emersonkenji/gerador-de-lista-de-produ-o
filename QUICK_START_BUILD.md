# 🚀 COMO GERAR O APP E ENVIAR PARA GIT - v1.0.3

## 📋 RESUMO RÁPIDO

Você tem **3 opções** para gerar o executável:

---

## ✅ OPÇÃO 1: Menu Interativo (RECOMENDADO)

```bash
.\build.bat
```

Abre um menu com 4 opções:
1. **Build Simples** → `dist/GeradorDeLista.exe` (autocontido)
2. **Build Profissional** → Instalador profissional com Inno Setup
3. **Limpar** → Remove builds antigos
4. **Testar** → Roda a aplicação Python

---

## 📦 OPÇÃO 2: Build Simples (Rápido)

```bash
build_app.bat
```

Gera: `dist/GeradorDeLista.exe`
Tempo: 2-3 minutos
Tamanho: ~100-200MB

---

## 📀 OPÇÃO 3: Build Profissional (Com Instalador)

**Requer**: Inno Setup 6 instalado (https://jrsoftware.org/isinfo.php)

```bash
build_app.bat
gerar_instalador.bat
```

Gera:
- `dist/GeradorDeLista.exe` (executável)
- `Output/GeradorDeLista-1.0.3.exe` (instalador)

Tempo: 3-5 minutos

---

## 🔄 FLUXO COMPLETO: CÓDIGO → GIT → RELEASE

### Passo 1: Atualizar Versão (Se necessário)
```bash
# Edite: app/version.py
# Mude: VERSION = "1.0.4"  (próxima versão)
```

### Passo 2: Fazer Commit no Git
```bash
git add .
git commit -m "v1.0.3: Sua mensagem de mudanças"
git tag -a v1.0.3 -m "Release v1.0.3"
git push origin master
git push origin v1.0.3
```

### Passo 3: Gerar Executável
```bash
# Menu interativo
.\build.bat
# Escolha opção 2 para instalador profissional
```

### Passo 4: Testar Executável
```bash
# Teste o arquivo gerado
Output\GeradorDeLista-1.0.3.exe
```

### Passo 5: Upload no GitHub (Opcional)
1. Vá para: https://github.com/emersonkenji/gerador-de-lista-de-produ-o/releases
2. Clique: "Create a new release"
3. Selecione tag: `v1.0.3`
4. Upload: `Output/GeradorDeLista-1.0.3.exe`
5. Clique: "Publish release"

---

## 📊 ESTRUTURA DO GIT

```
Repo: gerador-de-lista-de-produ-o
├── app/                    (Código-fonte)
├── build.bat              (Menu interativo) ✨ NOVO
├── build_app.bat          (Build simples)
├── build_script.py        (Build alternativo)
├── gerar_instalador.bat   (Gera instalador)
├── install_script.bat     (Instala app)
├── main.py
├── requirements.txt
├── CHANGELOG.md
├── BUILD_GUIDE.md         (Documentação) ✨ NOVO
├── RELEASE_NOTES_v1.0.3.md
└── setup.iss              (Config Inno Setup)
```

---

## 🎯 STATUS ATUAL - v1.0.3

```
✅ Código pronto no Git
✅ Versão 1.0.3 marcada com tag
✅ CHANGELOG criado
✅ RELEASE_NOTES criado
✅ BUILD_GUIDE criado
✅ Scripts de build prontos
✅ Menu interativo pronto (build.bat)

Próximo passo: Execute .\build.bat opção 2
```

---

## 🔧 SCRIPTS EXPLICADOS

| Script | O que faz | Comando |
|--------|-----------|---------|
| **build.bat** | Menu interativo com todas as opções | `.\build.bat` |
| **build_app.bat** | Gera executável simples | `build_app.bat` |
| **build_script.py** | Alternativa em Python | `python build_script.py` |
| **gerar_instalador.bat** | Gera instalador Inno Setup | `gerar_instalador.bat` |
| **install_script.bat** | Instala no Windows | `install_script.bat` |

---

## ⚡ COMANDO ÚNICO PARA TUDO

```powershell
# 1. Abre menu interativo
.\build.bat

# 2. Escolha opção 2
# 3. Aguarde 3-5 minutos
# 4. Resultado: Output\GeradorDeLista-1.0.3.exe
```

---

## 📝 NOTAS IMPORTANTES

### ⚠️ Pré-requisitos:
- Python 3.11+
- PyInstaller: `pip install pyinstaller`
- Inno Setup 6 (opcional, para instalador): https://jrsoftware.org/isinfo.php

### 💡 Dicas:
- Se receber erro, tente: `pip install --upgrade pyinstaller`
- Build simples é mais rápido (2-3 min)
- Build profissional cria instalador completo (3-5 min)
- Antivírus pode bloquear geração - adicione à whitelist se necessário

### 📦 .gitignore (não commitie):
```
build/
dist/
Output/
*.exe
__pycache__/
*.pyc
database.db
```

---

## 🎉 VOCÊ ESTÁ PRONTO!

A aplicação v1.0.3 está:
- ✅ Versionada no Git
- ✅ Marcada com tag
- ✅ Pronta para build
- ✅ Pronta para deploy

**Execute `.\build.bat` e escolha sua opção!**

---

Generated: 1 de Junho de 2026
Version: 1.0.3
