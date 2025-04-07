#!/usr/bin/env python
"""
Script para criar o executável do Agendador de Desligamento usando PyInstaller.
Este script cria um ícone básico e empacota o aplicativo em um executável único.
"""

import os
import sys
import subprocess
import shutil
import time
from pathlib import Path

def create_simple_icon():
    """Cria um ícone simples usando apenas Pillow."""
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        print("Instalando dependência Pillow...")
        subprocess.run([sys.executable, "-m", "pip", "install", "Pillow"])
        from PIL import Image, ImageDraw
    
    print("Criando ícone simples...")
    
    # Tamanhos para o ícone
    sizes = [16, 32, 48, 64, 128, 256]
    tmp_png_files = []
    
    # Define cores
    bg_color = (0, 120, 212)  # Azul
    fg_color = (255, 255, 255)  # Branco
    
    try:
        # Limpar qualquer arquivo temporário anterior que possa existir
        for size in sizes:
            png_path = f"icon_{size}.png"
            if os.path.exists(png_path):
                try:
                    os.remove(png_path)
                    time.sleep(0.5)  # Pequena pausa
                except:
                    print(f"Aviso: Não foi possível remover {png_path} pré-existente")
        
        # Criar os novos ícones
        for size in sizes:
            # Criar uma imagem quadrada azul
            img = Image.new('RGB', (size, size), bg_color)
            draw = ImageDraw.Draw(img)
            
            # Desenhar um "círculo" de relógio simples
            margin = size // 4
            draw.ellipse([margin, margin, size - margin, size - margin], outline=fg_color, width=max(1, size // 16))
            
            # Desenhar os "ponteiros" do relógio
            center = size // 2
            # Ponteiro de hora
            draw.line([center, center, center, center - margin], fill=fg_color, width=max(1, size // 16))
            # Ponteiro de minuto
            draw.line([center, center, center + margin//2, center], fill=fg_color, width=max(1, size // 16))
            
            # Salvar como PNG temporário com nome único
            png_path = f"icon_{size}_{int(time.time())}.png"
            img.save(png_path)
            tmp_png_files.append(png_path)
        
        # Criar o arquivo ICO
        if os.path.exists("icon.ico"):
            try:
                os.remove("icon.ico")
                time.sleep(0.5)  # Pequena pausa
            except:
                print("Aviso: Não foi possível remover o icon.ico pré-existente")
                # Usar um nome alternativo
                ico_path = f"agendador_icon_{int(time.time())}.ico"
        else:
            ico_path = "icon.ico"
        
        icons = [Image.open(png) for png in tmp_png_files]
        icons[0].save(ico_path, format="ICO", sizes=[(size, size) for size in sizes], append_images=icons[1:])
        
        # Limpar arquivos temporários com pausa entre operações
        for png in tmp_png_files:
            try:
                if os.path.exists(png):
                    time.sleep(0.5)  # Pequena pausa antes de remover
                    os.remove(png)
            except Exception as e:
                print(f"Aviso: Não foi possível remover {png}: {e}")
        
        print(f"Ícone simples criado com sucesso: {ico_path}")
        return ico_path
    
    except Exception as e:
        print(f"Erro ao criar ícone: {e}")
        # Retornar None em caso de erro
        return None

def build_executable():
    """Cria o executável do Agendador de Desligamento."""
    print("=" * 70)
    print("Iniciando o processo de criação do executável")
    print("=" * 70)
    
    # Tentar encontrar ou criar um ícone
    icon_path = None
    if os.path.exists("icon.ico"):
        icon_path = "icon.ico"
    else:
        # Tenta criar um ícone simples
        icon_path = create_simple_icon()
    
    # Se ainda não temos um ícone, prosseguir sem ele
    if not icon_path:
        print("Aviso: Não foi possível criar um ícone. Continuando sem ícone.")
        icon_arg = []
    else:
        icon_arg = [f"--icon={icon_path}"]
    
    # Lista de arquivos para incluir no executável
    data_files = [
        ("icon.svg", "."),
        ("check.svg", "."),
        ("down_arrow.svg", "."),
        ("config.json", "."),
        ("README.md", "."),
        ("LICENSE", ".")
    ]
    
    # Cria os argumentos para incluir os arquivos
    add_data_args = []
    for src, dst in data_files:
        if os.path.exists(src):
            add_data_args.extend(["--add-data", f"{src};{dst}"])
    
    # Comando básico do PyInstaller
    cmd = [
        "pyinstaller",
        "--name=Agendador de Desligamento",
        "--onefile",
        "--windowed",
        "--clean",
        "--noconfirm"
    ]
    
    # Adiciona o ícone se disponível
    if icon_path:
        cmd.extend(icon_arg)
    
    # Adiciona os arquivos de dados
    cmd.extend(add_data_args)
    
    # Adiciona o arquivo principal
    cmd.append("main.py")
    
    # Executa o PyInstaller
    print("Executando PyInstaller...")
    print(" ".join(cmd))
    subprocess.run(cmd)
    
    print("=" * 70)
    print("Executável criado com sucesso!")
    print("O arquivo está em: dist/Agendador de Desligamento.exe")
    print("=" * 70)

if __name__ == "__main__":
    build_executable()