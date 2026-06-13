#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gera todos os PDFs individuais e os mescla em VERSAO_FINAL_2.0
"""
import subprocess, sys, os

BASE = r'c:\Users\Heitor Melo\Desktop\Grana no Digital\Astrologia'
PYTHON = sys.executable

SCRIPTS = [
    'gerar_ebook_parte1.py',
    'gerar_ebook_parte2.py',
    'gerar_parte3.py',
    'gerar_parte4.py',
    'gerar_parte5.py',
    'gerar_bonus.py',
]

PARTES = [
    'O_Guia_Emocional_dos_Signos_PARTE1.pdf',
    'O_Guia_Emocional_dos_Signos_PARTE2.pdf',
    'O_Guia_Emocional_dos_Signos_PARTE3.pdf',
    'O_Guia_Emocional_dos_Signos_PARTE4.pdf',
    'O_Guia_Emocional_dos_Signos_PARTE5.pdf',
    'O_Guia_Emocional_dos_Signos_BONUS.pdf',
]

OUTPUT = os.path.join(BASE, 'O_Guia_Emocional_dos_Signos_VERSAO_FINAL_2.0.pdf')

# ── 1. Gerar cada parte ──────────────────────────────────────────────────────
for script in SCRIPTS:
    path = os.path.join(BASE, script)
    print(f'\n>>> Gerando {script}...')
    result = subprocess.run([PYTHON, path], capture_output=True, text=True, cwd=BASE)
    if result.stdout: print(result.stdout.strip())
    if result.returncode != 0:
        print(f'ERRO em {script}:\n{result.stderr}')
        sys.exit(1)

# ── 2. Mesclar com pypdf ─────────────────────────────────────────────────────
try:
    from pypdf import PdfWriter
except ImportError:
    try:
        from PyPDF2 import PdfWriter, PdfReader
        PYPDF2 = True
    except ImportError:
        print('\nInstalando pypdf...')
        subprocess.run([PYTHON, '-m', 'pip', 'install', 'pypdf'], check=True)
        from pypdf import PdfWriter
        PYPDF2 = False
else:
    PYPDF2 = False

writer = PdfWriter()
for parte in PARTES:
    path = os.path.join(BASE, parte)
    if not os.path.exists(path):
        print(f'AVISO: {parte} não encontrado, pulando.')
        continue
    if PYPDF2:
        from PyPDF2 import PdfReader
        reader = PdfReader(path)
        for page in reader.pages:
            writer.add_page(page)
    else:
        writer.append(path)
    print(f'  + {parte}')

with open(OUTPUT, 'wb') as f:
    writer.write(f)

print(f'\n[OK] VERSAO_FINAL_2.0 gerada: {OUTPUT}')
