"""Auto-Updater via GitHub Releases.

Suporta repositórios PRIVADOS usando Personal Access Token (PAT).
Verifica a tag mais recente e baixa/aplica a atualização.
"""
import os
import sys
import json
import shutil
import zipfile
import tempfile
import subprocess
import logging
import urllib.request
from packaging import version as pkg_version

logger = logging.getLogger(__name__)

GITHUB_API = "https://api.github.com"


def _make_request(url: str, token: str = "") -> dict | None:
    """Faz uma requisição à API do GitHub, com token se fornecido."""
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        logger.warning(f"Falha na requisição GitHub: {e}")
        return None


def get_latest_release(repo: str, token: str = "") -> dict | None:
    """Consulta a release mais recente (funciona com repos privados se tiver token)."""
    url = f"{GITHUB_API}/repos/{repo}/releases/latest"
    data = _make_request(url, token)
    if not data:
        return None

    return {
        "tag": data.get("tag_name", "").lstrip("v"),
        "name": data.get("name", ""),
        "body": data.get("body", ""),
        "zipball_url": data.get("zipball_url", ""),
        "assets": data.get("assets", []),
        "html_url": data.get("html_url", ""),
    }


def check_for_update(repo: str, current_version: str, token: str = "") -> dict | None:
    """Retorna info da release se houver versão mais nova, senão None."""
    if not repo:
        return None

    release = get_latest_release(repo, token)
    if not release or not release["tag"]:
        return None

    try:
        remote_ver = pkg_version.parse(release["tag"])
        local_ver = pkg_version.parse(current_version)
        if remote_ver > local_ver:
            return release
    except Exception as e:
        logger.warning(f"Erro ao comparar versões: {e}")

    return None


def apply_update(release: dict, target_dir: str = ".", token: str = "") -> bool:
    """Aplica a atualização dependendo se o app está empacotado (.exe) ou em fonte (.py)."""
    is_frozen = getattr(sys, 'frozen', False)
    
    if is_frozen:
        logger.info("Modo Executável Detectado. Atualizando binário...")
        return _update_executable(release, token)
    else:
        logger.info("Modo Fonte Detectado. Atualizando arquivos python...")
        zip_url = release.get("zipball_url")
        if not zip_url:
            return False
        return _update_source(zip_url, target_dir, token)


def _update_executable(release: dict, token: str = "") -> bool:
    """Faz o hot-swap do .exe atual pelo novo."""
    try:
        # Puxa a url do primeiro anexo (asset) que será nosso .exe novo
        assets = release.get("assets", [])
        if not assets:
            logger.error("Nenhum arquivo executável (.exe) anexado nesta Release!")
            return False
            
        exe_url = assets[0].get("browser_download_url")
        if not exe_url:
            return False
            
        current_exe = sys.executable
        exe_dir = os.path.dirname(current_exe)
        exe_name = os.path.basename(current_exe)
        
        tmp_exe = os.path.join(exe_dir, "update_new.exe")
        bat_path = os.path.join(exe_dir, "apply_update.bat")
        
        logger.info(f"Baixando novo executável de {exe_url} para {tmp_exe}")
        
        headers = {}
        if token:
            headers["Authorization"] = f"Bearer {token}"
            
        # Baixa o .exe novo suportando redirects do github
        headers['Accept'] = "application/octet-stream"
        req = urllib.request.Request(exe_url, headers=headers)
        with urllib.request.urlopen(req, timeout=120) as resp:
            with open(tmp_exe, 'wb') as f:
                f.write(resp.read())
                
        # Cria um script .bat que apaga o atual, renomeia o novo, abre, e se apaga.
        bat_content = f"""@echo off
echo Atualizando Gerador de Lista de Producao...
timeout /t 3 /nobreak > nul
del /f /q "{exe_name}"
ren "update_new.exe" "{exe_name}"
start "" "{exe_name}"
del "%~f0"
"""
        with open(bat_path, "w") as f:
            f.write(bat_content)
        
        # Lança o script como processo fantasma
        subprocess.Popen([bat_path], shell=True)
        return True
        
    except Exception as e:
        logger.error(f"Falha ao realizar hot-swap do EXE: {e}")
        return False


def _update_source(zipball_url: str, target_dir: str, token: str = "") -> bool:
    """Baixa o zipball e extrai os códigos fonte (modo desenvolvedor)."""
    try:
        tmp_dir = tempfile.mkdtemp()
        zip_path = os.path.join(tmp_dir, "update.zip")

        headers = {}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        req = urllib.request.Request(zipball_url, headers=headers)
        with urllib.request.urlopen(req, timeout=60) as resp:
            with open(zip_path, 'wb') as f:
                f.write(resp.read())

        with zipfile.ZipFile(zip_path, 'r') as zf:
            root_dirs = [n for n in zf.namelist() if n.count('/') == 1 and n.endswith('/')]
            root_prefix = root_dirs[0] if root_dirs else ""

            for member in zf.namelist():
                if member == root_prefix:
                    continue
                relative_path = member[len(root_prefix):]
                if not relative_path:
                    continue

                dest_path = os.path.join(target_dir, relative_path)

                if member.endswith('/'):
                    os.makedirs(dest_path, exist_ok=True)
                else:
                    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                    with zf.open(member) as src, open(dest_path, 'wb') as dst:
                        dst.write(src.read())

        shutil.rmtree(tmp_dir, ignore_errors=True)
        logger.info("Atualização do código-fonte aplicada com sucesso!")
        return True

    except Exception as e:
        logger.error(f"Falha ao aplicar atualização de código-fonte: {e}")
        return False
