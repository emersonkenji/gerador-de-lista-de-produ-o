import os
import subprocess

def build():
    print("Iniciando processo de build com PyInstaller...")
    
    # Check if pyinstaller is installed
    try:
        import PyInstaller
    except ImportError:
        print("Instalando PyInstaller...")
        subprocess.check_call(["pip", "install", "pyinstaller"])
        
    cmd = [
        "pyinstaller",
        "--noconfirm",
        "--onedir",
        "--windowed",
        "--name", "GeradorDeLista",
        "--add-data", "app;app/",
        "--hidden-import", "sqlite3",
        "--hidden-import", "pandas",
        "--hidden-import", "openpyxl",
        "main.py"
    ]
    
    print(f"Executando comando: {' '.join(cmd)}")
    subprocess.check_call(cmd)
    
    print("Build completado com sucesso! O executável está na pasta 'dist/GeradorDeLista'.")

if __name__ == "__main__":
    build()
