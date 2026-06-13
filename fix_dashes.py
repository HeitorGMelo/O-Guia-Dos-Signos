#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Remove travessões "—" do corpo do texto de todos os arquivos do ebook.
Substitui contextualmente: `, ` na maioria dos casos, `: ` antes de explicações/enumerações.
"""
import re

FILES = [
    r'c:\Users\Heitor Melo\Desktop\Grana no Digital\Astrologia\gerar_parte3.py',
    r'c:\Users\Heitor Melo\Desktop\Grana no Digital\Astrologia\gerar_parte4.py',
    r'c:\Users\Heitor Melo\Desktop\Grana no Digital\Astrologia\gerar_parte5.py',
    r'c:\Users\Heitor Melo\Desktop\Grana no Digital\Astrologia\gerar_bonus.py',
]

# Palavras/padrões após " — " que pedem ": " (explicação, enumeração, definição)
DOIS_PONTOS = [
    r'é ', r'são ', r'foi ', r'eram ', r'representa ', r'significa ', r'indica ',
    r'isso ', r'assim ', r'ou seja', r'ambos ', r'cada ', r'mas',
    # Nomes próprios (maiúscula) após em dash também pedem ":"
]

# Palavras após " — " que pedem simples remoção do em dash (a vírgula já vem do contexto)
SEM_VIRGULA = [r'e é ', r'e o ', r'e a ', r'e os ', r'e as ', r'e ambos', r'e isso']


def smart_replace(text):
    """
    Substitui ' — ' por substituição contextual:
    - Antes de 'mas', 'porém', 'contudo' etc.: ', mas'
    - Antes de 'e ', 'ou ': ', e ' / ' ou '
    - Antes de 'é ', 'são ', 'foi ', etc.: ': '
    - Antes de letra maiúscula (enumeração/nome): ': '
    - Demais casos: ', '
    Trata também o padrão de duplo travessão — ... — (parentético)
    """
    # Primeiro, trata duplo travessão parentético: " — texto — " → ", texto,"
    # Padrão: espaço-travessão-espaço + conteúdo sem travessão + espaço-travessão-espaço
    text = re.sub(
        r' — ([^—\n]{2,80}?) — ',
        lambda m: f', {m.group(1)},',
        text
    )

    # Agora trata travessão simples restante com contexto
    def replace_single(m):
        after = m.group(1)

        # Antes de coordenativas adversativas → vírgula
        if re.match(r'(mas |porém|contudo|todavia|entretanto)', after, re.I):
            return ', ' + after

        # Antes de "e " / "ou " → vírgula (exceto "e é" que já está acima)
        if re.match(r'(e |ou )', after, re.I):
            return ', ' + after

        # Antes de "que " / "o que " / "quando " / "porque " / "se " → vírgula
        if re.match(r'(que |o que |quando |porque |pois |se |como |para )', after, re.I):
            return ', ' + after

        # Antes de "não " → vírgula
        if re.match(r'não ', after, re.I):
            return ', ' + after

        # Antes de "é ", "são ", "foi " etc. ou "isso " → dois pontos
        if re.match(r'(é |são |foi |eram |representa |significa |indica |isso |assim )', after, re.I):
            return ': ' + after

        # Antes de letra maiúscula (nome próprio / início de enumeração) → dois pontos
        if re.match(r'[A-ZÁÀÂÃÉÈÊÍÌÎÓÒÔÕÚÙÛÇ]', after):
            return ': ' + after

        # Demais → vírgula
        return ', ' + after

    # Trata travessão seguido de algum texto (sem pular linha)
    text = re.sub(r' — ([^\n—])', replace_single, text)

    # Trata travessão no fim de linha (antes de quebra de linha na string Python)
    # Ex: 'fogo — '\n'e emocionalmente...'
    # Aqui o ' — ' está no final da string: substitui por ','
    text = re.sub(r" — '(\s*\n\s*)'", r",'\\n'", text)
    text = re.sub(r' — \'', r",\'", text)

    return text


for filepath in FILES:
    with open(filepath, 'r', encoding='utf-8') as f:
        original = f.read()

    modified = smart_replace(original)

    # Conta quantas substituições foram feitas
    remaining = modified.count('—')
    replaced = original.count('—') - remaining

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(modified)

    print(f"{filepath.split(chr(92))[-1]}: {replaced} travessões substituídos, {remaining} restantes")

print("\nConcluído.")
