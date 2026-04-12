"""Auto-Updater via GitHub Releases.

Suporta repositórios PRIVADOS usando Personal Access Token (PAT).
Verifica a tag mais recente e baixa/aplica a atualização.
"""
import os
import json
import shutil
import zipfile
import tempfile
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
        with urllib.request.urlopen(req, timeout=15) as resp:
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


def download_and_extract_update(zipball_url: str, target_dir: str, token: str = "") -> bool:
    """Baixa o zipball e extrai no diretório do projeto."""
    try:
        tmp_dir = tempfile.mkdtemp()
        zip_path = os.path.join(tmp_dir, "update.zip")

        logger.info(f"Baixando atualização de {zipball_url}")

        # Precisa do token para repos privados
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
        logger.info("Atualização aplicada com sucesso!")
        return True

    except Exception as e:
        logger.error(f"Falha ao aplicar atualização: {e}")
        return False
