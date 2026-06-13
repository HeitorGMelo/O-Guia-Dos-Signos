#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Corrige erros de acentuação e gramatica em gerar_parte4.py e gerar_bonus.py"""
import re

FIXES_PARTE4 = [
    # Palavras com ó indevido
    ('issó', 'isso'), ('Issó', 'Isso'), ('nossó', 'nosso'),
    ('ansiosó', 'ansioso'), ('nervosó', 'nervoso'), ('passó', 'passo'),
    ('impulsó', 'impulso'), ('pesó', 'peso'), ('presó', 'preso'),
    ('sensó', 'senso'), ('propensó', 'propenso'), ('silenciosó', 'silencioso'),
    ('generosó', 'generoso'), ('fracassó', 'fracasso'), ('intensó', 'intenso'),
    ('orgulhosó', 'orgulhoso'), ('usó', 'uso'),
    # Acentos errados
    ('essêncial', 'essencial'), ('templaté', 'template'),
    ('análisei', 'analisei'), ('atravéssar', 'atravessar'),
    ('apróxima', 'aproxima'), ('fácilidade', 'facilidade'),
    ('fácilmente', 'facilmente'), ('genuínamente', 'genuinamente'),
    ('manifestá ', 'manifesta '), ('afastêm', 'afastem'), ('ontêm', 'ontem'),
    # Verbos
    ('Escorpião testá', 'Escorpião testa'),
    # frequentemente máscara o medo (verbo, sem acento)
    ('frequentemente máscara o medo', 'frequentemente mascara o medo'),
    # é/e contextuais
    ('a intensidade é a espontaneidade', 'a intensidade e a espontaneidade'),
    ('a confiabilidade é a ambição', 'a confiabilidade e a ambição'),
    ('a inteligência é o\n            \'imprevisível', 'a inteligência e o\n            \'imprevisível'),
    ('nossa sombra é que estamos', 'nossa sombra e que estamos'),
    ('arrogância é a encontrar nos', 'arrogância e a encontrar nos'),
    ('combinados com o signo solar é o\n    \'elemento dominante', 'combinados com o signo solar e o\n    \'elemento dominante'),
    ('estimulação intelectual é a multiplicidade', 'estimulação intelectual e a multiplicidade'),
    ('em relação ao parceiro, é uma tendência de intelectualizar o que', 'em relação ao parceiro, e uma tendência de intelectualizar o que'),
    ('Ao manter o controle sobre si mesmo é sua rotina', 'Ao manter o controle sobre si mesmo e sua rotina'),
    ('é a rejeição é o conflito', 'é a rejeição e o conflito'),
    ('causas maiores, é uma tendência de intelectualizar o\n            \'afeto', 'causas maiores, e uma tendência de intelectualizar o\n            \'afeto'),
    ('limites borrados — é issó se estende', 'limites borrados — e isso se estende'),
    ('termina é onde o outro começa', 'termina e onde o outro começa'),
    ('de uma forma é o outro recebe de outra', 'de uma forma e o outro recebe de outra'),
    ('de Vênus é o\n    \'elemento dominante', 'de Vênus e o\n    \'elemento dominante'),
    ('originalidade é sua visão de mundo específica', 'originalidade e sua visão de mundo específica'),
    ('é o signo faz jus — ou não', 'e o signo faz jus — ou não'),
    ('A ruminação\n            \'prolongada é a dificuldade', 'A ruminação\n            \'prolongada e a dificuldade'),
    ('reconstruindo a rotina é o senso de controle', 'reconstruindo a rotina e o senso de controle'),
    ('Aquário processa em solidão é a seu próprio ritmo', 'Aquário processa em solidão e a seu próprio ritmo'),
    ('performance maior (para garantir\n            \'atenção) é um recuo orgulhoso', 'performance maior (para garantir\n            \'atenção) e um recuo orgulhoso'),
    ('reconhecer o esforço é a competência', 'reconhecer o esforço e a competência'),
    # têm → tem (sujeito singular)
    ('o outro não têm aquelas', 'o outro não tem aquelas'),
    ('Se você têm Leão', 'Se você tem Leão'),
    ('mas têm Netuno em destaque', 'mas tem Netuno em destaque'),
    ('Leão têm uma contradição', 'Leão tem uma contradição'),
    ('não têm valor real', 'não tem valor real'),
    ('Parceiro que têm sua própria vida', 'Parceiro que tem sua própria vida'),
    ('raramente sente que têm garantia suficiente', 'raramente sente que tem garantia suficiente'),
    ('genuinamente ama a humanidade, mas têm\n            \'dificuldade', 'genuinamente ama a humanidade, mas tem\n            \'dificuldade'),
    ('mas cada signo têm tendências', 'mas cada signo tem tendências'),
    ('porque têm fácilidade de', 'porque tem facilidade de'),
    ('"O que têm\n            \'de errado comigo?"', '"O que tem\n            \'de errado comigo?"'),
    ('a dor\n            \'não têm contornos', 'a dor\n            \'não tem contornos'),
    ('Cada elemento têm sensibilidades', 'Cada elemento tem sensibilidades'),
    ('o fogo precisa sentir que têm espaço', 'o fogo precisa sentir que tem espaço'),
    ('A água têm memória', 'A água tem memória'),
]

FIXES_BONUS = [
    ('issó', 'isso'), ('Issó', 'Isso'), ('silenciosó', 'silencioso'),
    ('avisó', 'aviso'), ('minhá', 'minha'), ('acessó', 'acesso'),
    ('sensó', 'senso'), ('generosó', 'generoso'), ('imprecisó', 'impreciso'),
    ('precisó', 'preciso'), ('extraordináriamente', 'extraordinariamente'),
    ('rápidamente', 'rapidamente'), ('comúnicar', 'comunicar'),
    ('comúnicação', 'comunicação'), ('visívelmente', 'visivelmente'),
    ('parecerer', 'parecer'), ('genuínamente', 'genuinamente'),
    ('fácilidade', 'facilidade'), ('últimatos', 'ultimatos'),
    ('teimosó', 'teimoso'), ('impulsó', 'impulso'), ('escolhá', 'escolha'),
    ('fechá', 'fecha'), ('marçou', 'marcou'),
    # Verbos
    ('Escorpião testá constantemente', 'Escorpião testa constantemente'),
    # é/e contextuais
    ('é onde estão suas brechas psicológicas', 'e onde estão suas brechas psicológicas'),
    ('é o erro fatal que\n    \'imediatamente fecha sua porta', 'e o erro fatal que\n    \'imediatamente fecha sua porta'),
    ('entre o sentir é o fazer', 'entre o sentir e o fazer'),
    ('que move é o limite\n    \'que cega', 'que move e o limite\n    \'que cega'),
    ('imediatamente é o\n    \'desprezará', 'imediatamente e o\n    \'desprezará'),
    ('de Câncer é o colocam em modo de cooperação', 'de Câncer e o colocam em modo de cooperação'),
    ('entre o ideal é o real', 'entre o ideal e o real'),
    ('é a sua escolha\n            \'naturalmente emergirá', 'e a sua escolha\n            \'naturalmente emergirá'),
    ('issó depois, é o ressente profundamente', 'isso depois, e o ressente profundamente'),
    ('é a decisão costuma ser irreversível', 'e a decisão costuma ser irreversível'),
    ('fecha — é quando percebe que a escolha fortalece', 'fecha — e quando percebe que a escolha fortalece'),
    # têm → tem (sujeito singular)
    ('"não sei se você têm coragem', '"não sei se você tem coragem'),
    ('têm Áries na mão', 'tem Áries na mão'),
    ('quando têm certeza suficiente', 'quando tem certeza suficiente'),
    ('que têm múltiplas camadas', 'que tem múltiplas camadas'),
    ('que têm opiniões', 'que tem opiniões'),
    ('têm muito poder sobre Gêmeos', 'tem muito poder sobre Gêmeos'),
    ('o que marçou positivamente têm crédito', 'o que marcou positivamente tem crédito'),
    ('antes que ele mesmo as tome. que têm acessó', 'antes que ele mesmo as tome. que tem acesso'),
    ('têm conciliação', 'tem conciliação'),
    ('e você têm sua atenção', 'e você tem sua atenção'),
    ('e você têm sua lealdade', 'e você tem sua lealdade'),
    ('quem têm poder e honestidade suficientes', 'quem tem poder e honestidade suficientes'),
    ('têm influência significativa', 'tem influência significativa'),
    ('que têm perspectivas', 'que tem perspectivas'),
    ('Sagitário têm um reflexo imediato', 'Sagitário tem um reflexo imediato'),
    ('essa decisão também têm um componente', 'essa decisão também tem um componente'),
    ('— têm acessó a uma camada', '— tem acesso a uma camada'),
    ('têm muito mais\n            \'espaço', 'tem muito mais\n            \'espaço'),
    ('têm poder significativo', 'tem poder significativo'),
    ('que têm um plano', 'que tem um plano'),
]

def apply_fixes(path, fixes):
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    original = text
    for old, new in fixes:
        text = text.replace(old, new)
    if text != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f'[OK] Corrigido: {path}')
    else:
        print(f'[--] Sem alterações: {path}')

base = r'c:\Users\Heitor Melo\Desktop\Grana no Digital\Astrologia'
apply_fixes(f'{base}\\gerar_parte4.py', FIXES_PARTE4)
apply_fixes(f'{base}\\gerar_bonus.py', FIXES_BONUS)
print('Concluído.')
