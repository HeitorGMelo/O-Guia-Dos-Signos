#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
O Guia Emocional dos Signos - PARTE 1: Capa + Fundamentos
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor, white, black
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame,
    Paragraph, Spacer, PageBreak, HRFlowable,
    KeepTogether, Table, TableStyle
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfgen import canvas as pdfcanvas
from reportlab.lib import colors

# ─── CORES ───────────────────────────────────────────────────
GOLD        = HexColor('#c9a96e')
GOLD_LIGHT  = HexColor('#e8c98a')
DARK_BG     = HexColor('#0d0d16')
SURFACE     = HexColor('#1a1a2e')
ACCENT      = HexColor('#9b8bdb')
DARK_TEXT   = HexColor('#1c1c2e')
BODY_TEXT   = HexColor('#2d2d3a')
MUTED       = HexColor('#7a7a9a')
LIGHT_BG    = HexColor('#f9f7f3')
CREAM       = HexColor('#fdf8ef')
BORDER      = HexColor('#e8e0d0')

PW, PH = A4   # 595.27 x 841.89 pt

# ─── ESTILOS ─────────────────────────────────────────────────
def make_styles():
    s = {}

    # Capa / títulos grandes
    s['cover_title'] = ParagraphStyle('cover_title',
        fontName='Times-Bold', fontSize=38, leading=46,
        textColor=GOLD_LIGHT, alignment=TA_CENTER, spaceAfter=16)

    s['cover_subtitle'] = ParagraphStyle('cover_subtitle',
        fontName='Times-Roman', fontSize=16, leading=22,
        textColor=HexColor('#d4c8b0'), alignment=TA_CENTER, spaceAfter=10)

    s['cover_badge'] = ParagraphStyle('cover_badge',
        fontName='Helvetica', fontSize=10, leading=14,
        textColor=GOLD, alignment=TA_CENTER, spaceAfter=6,
        letterSpacing=2)

    # Parte / divisor
    s['part_title'] = ParagraphStyle('part_title',
        fontName='Times-Bold', fontSize=32, leading=40,
        textColor=GOLD_LIGHT, alignment=TA_CENTER, spaceAfter=10)

    s['part_num'] = ParagraphStyle('part_num',
        fontName='Helvetica', fontSize=11, leading=16,
        textColor=GOLD, alignment=TA_CENTER, spaceAfter=14,
        letterSpacing=3)

    # Capítulo
    s['chapter_title'] = ParagraphStyle('chapter_title',
        fontName='Times-Bold', fontSize=26, leading=32,
        textColor=DARK_TEXT, spaceBefore=28, spaceAfter=10)

    s['chapter_label'] = ParagraphStyle('chapter_label',
        fontName='Helvetica-Bold', fontSize=9, leading=13,
        textColor=GOLD, spaceBefore=0, spaceAfter=8,
        letterSpacing=2)

    # Subtítulo de seção
    s['section_title'] = ParagraphStyle('section_title',
        fontName='Times-Bold', fontSize=17, leading=22,
        textColor=DARK_TEXT, spaceBefore=22, spaceAfter=8)

    # Subtítulo nível 2
    s['sub_title'] = ParagraphStyle('sub_title',
        fontName='Helvetica-Bold', fontSize=12, leading=17,
        textColor=SURFACE, spaceBefore=14, spaceAfter=6)

    # Corpo principal
    s['body'] = ParagraphStyle('body',
        fontName='Helvetica', fontSize=11, leading=18,
        textColor=BODY_TEXT, spaceAfter=10, alignment=TA_JUSTIFY)

    # Corpo com destaque
    s['body_bold'] = ParagraphStyle('body_bold',
        fontName='Helvetica-Bold', fontSize=11, leading=18,
        textColor=DARK_TEXT, spaceAfter=6)

    # Bullet / lista
    s['bullet'] = ParagraphStyle('bullet',
        fontName='Helvetica', fontSize=11, leading=18,
        textColor=BODY_TEXT, spaceAfter=5,
        leftIndent=18, firstLineIndent=-12)

    # Citação / insight
    s['insight'] = ParagraphStyle('insight',
        fontName='Times-Italic', fontSize=12, leading=20,
        textColor=DARK_TEXT, spaceAfter=10, alignment=TA_CENTER,
        leftIndent=24, rightIndent=24)

    # Nota de rodapé / label menor
    s['label'] = ParagraphStyle('label',
        fontName='Helvetica', fontSize=9, leading=13,
        textColor=MUTED, spaceAfter=4, letterSpacing=1)

    # Sumário
    s['toc_part'] = ParagraphStyle('toc_part',
        fontName='Times-Bold', fontSize=13, leading=20,
        textColor=DARK_TEXT, spaceBefore=14, spaceAfter=4)

    s['toc_item'] = ParagraphStyle('toc_item',
        fontName='Helvetica', fontSize=11, leading=18,
        textColor=BODY_TEXT, spaceAfter=3, leftIndent=18)

    # Sign banner
    s['sign_emoji'] = ParagraphStyle('sign_emoji',
        fontName='Helvetica-Bold', fontSize=36, leading=44,
        textColor=GOLD_LIGHT, alignment=TA_CENTER, spaceAfter=6)

    s['sign_name'] = ParagraphStyle('sign_name',
        fontName='Times-Bold', fontSize=28, leading=34,
        textColor=GOLD_LIGHT, alignment=TA_CENTER, spaceAfter=6)

    s['sign_meta'] = ParagraphStyle('sign_meta',
        fontName='Helvetica', fontSize=10, leading=15,
        textColor=HexColor('#c0b090'), alignment=TA_CENTER,
        spaceAfter=4, letterSpacing=1)

    return s

ST = make_styles()

# ─── CANVAS CALLBACKS ────────────────────────────────────────
def page_cover(cv, doc):
    """Página de capa escura com gradiente simulado."""
    cv.saveState()
    cv.setFillColor(DARK_BG)
    cv.rect(0, 0, PW, PH, fill=1, stroke=0)

    # Borda dourada superior
    cv.setStrokeColor(GOLD)
    cv.setLineWidth(1.5)
    cv.line(2*cm, PH - 2*cm, PW - 2*cm, PH - 2*cm)
    cv.line(2*cm, 2*cm, PW - 2*cm, 2*cm)

    # Ornamento central superior
    cv.setFillColor(GOLD)
    cv.setFont('Helvetica', 18)
    cv.drawCentredString(PW/2, PH - 1.5*cm, '✦')

    # Círculo de fundo decorativo
    cv.setStrokeColor(HexColor('#2a2a3e'))
    cv.setLineWidth(0.5)
    cv.circle(PW/2, PH/2, 7*cm, fill=0, stroke=1)
    cv.circle(PW/2, PH/2, 8.5*cm, fill=0, stroke=1)

    # Rodapé
    cv.setFillColor(MUTED)
    cv.setFont('Helvetica', 8)
    cv.drawCentredString(PW/2, 1.5*cm, 'O Guia Emocional dos Signos  ·  Edição Premium 2025')
    cv.restoreState()

def page_dark(cv, doc):
    """Página de divisor de parte — fundo escuro."""
    cv.saveState()
    cv.setFillColor(DARK_BG)
    cv.rect(0, 0, PW, PH, fill=1, stroke=0)
    cv.setFillColor(GOLD)
    cv.setFont('Helvetica', 14)
    cv.drawCentredString(PW/2, 1.5*cm, '✦')
    cv.restoreState()

def page_normal(cv, doc):
    """Página normal com cabeçalho e rodapé."""
    cv.saveState()
    cv.setFillColor(LIGHT_BG)
    cv.rect(0, 0, PW, PH, fill=1, stroke=0)

    # Barra superior dourada
    cv.setFillColor(GOLD)
    cv.rect(0, PH - 0.6*cm, PW, 3, fill=1, stroke=0)

    # Rodapé
    cv.setFillColor(MUTED)
    cv.setFont('Helvetica', 8)
    cv.drawCentredString(PW/2, 0.8*cm, f'O Guia Emocional dos Signos')
    cv.setFillColor(GOLD)
    cv.drawString(PW - 2*cm, 0.8*cm, str(doc.page))
    cv.setStrokeColor(BORDER)
    cv.setLineWidth(0.5)
    cv.line(2*cm, 1.2*cm, PW - 2*cm, 1.2*cm)
    cv.restoreState()

def page_sign_banner(cv, doc):
    """Página de banner de signo — fundo escuro."""
    cv.saveState()
    cv.setFillColor(SURFACE)
    cv.rect(0, 0, PW, PH, fill=1, stroke=0)
    # Linha decorativa
    cv.setFillColor(GOLD)
    cv.rect(0, PH - 0.4*cm, PW, 3, fill=1, stroke=0)
    cv.rect(0, 0.4*cm, PW, 1, fill=1, stroke=0)
    cv.restoreState()

# ─── CAIXA DE INSIGHT ────────────────────────────────────────
def insight_box(text):
    """Retorna uma Table com fundo dourado para insights."""
    p = Paragraph(text, ST['insight'])
    t = Table([[p]], colWidths=[13*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), CREAM),
        ('BOX',        (0,0), (-1,-1), 1.2, GOLD),
        ('LEFTPADDING',  (0,0), (-1,-1), 18),
        ('RIGHTPADDING', (0,0), (-1,-1), 18),
        ('TOPPADDING',   (0,0), (-1,-1), 14),
        ('BOTTOMPADDING',(0,0), (-1,-1), 14),
    ]))
    return t

def sign_meta_table(signo, símbolo, elemento, modalidade, planeta, período):
    """Tabela de metadados de um signo."""
    data = [
        [Paragraph('<b>Elemento</b>', ST['label']),   Paragraph(elemento,  ST['body_bold'])],
        [Paragraph('<b>Modalidade</b>', ST['label']), Paragraph(modalidade,ST['body_bold'])],
        [Paragraph('<b>Planeta</b>', ST['label']),    Paragraph(planeta,   ST['body_bold'])],
        [Paragraph('<b>Período</b>', ST['label']),    Paragraph(período,   ST['body_bold'])],
    ]
    t = Table(data, colWidths=[4*cm, 9*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), CREAM),
        ('BOX',        (0,0), (-1,-1), 0.8, BORDER),
        ('LINEBELOW',  (0,0), (-1,-2), 0.5, BORDER),
        ('LEFTPADDING',  (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING',   (0,0), (-1,-1), 6),
        ('BOTTOMPADDING',(0,0), (-1,-1), 6),
    ]))
    return t

# ─── HELPERS DE CONTEÚDO ─────────────────────────────────────
def h1(text):  return Paragraph(text, ST['chapter_title'])
def h2(text):  return Paragraph(text, ST['section_title'])
def h3(text):  return Paragraph(text, ST['sub_title'])
def p(text):   return Paragraph(text, ST['body'])
def lbl(text): return Paragraph(text, ST['chapter_label'])
def sp(n=1):   return Spacer(1, n*0.4*cm)
def hr():      return HRFlowable(width='100%', thickness=0.8, color=BORDER, spaceAfter=12, spaceBefore=4)
def bul(text): return Paragraph(f'<b>•</b>  {text}', ST['bullet'])

# ════════════════════════════════════════════════════════════════
#  CONTEÚDO
# ════════════════════════════════════════════════════════════════

def build_cover():
    return []   # tudo feito no canvas page_cover

def build_toc():
    story = []
    story.append(lbl('ÍNDICE'))
    story.append(h1('Sumário'))
    story.append(hr())
    story.append(sp())

    parts = [
        ('PARTE 1', 'Os Fundamentos do Zodíaco', [
            'O que é astrologia e o que ela não é',
            'Os 4 Elementos: Fogo, Terra, Ar e Água',
            'As 3 Modalidades: Cardinal, Fixo e Mutável',
            'Os Planetas Regentes',
            'Sol, Lua e Ascendente: a tríade essencial',
        ]),
        ('PARTE 2', 'Os 12 Signos em Profundidade', [
            'Áries  ·  Touro  ·  Gêmeos  ·  Câncer',
            'Leão  ·  Virgem  ·  Libra  ·  Escorpião',
            'Sagitário  ·  Capricórnio  ·  Aquário  ·  Peixes',
            'Perfil emocional, amor, sombra, segredos, medos e compatibilidade',
        ]),
        ('PARTE 3', 'Combinações e Compatibilidades', [
            'Compatibilidade por elemento',
            'As melhores combinações do zodíaco',
            'As combinações mais desafiadoras',
            'Todas as combinações: o que cada par revela',
        ]),
        ('PARTE 4', 'Padrões Emocionais Profundos', [
            'Por que você se apaixona sempre pelo mesmo tipo',
            'Estilos de apego por signo',
            'Linguagens do amor dos 12 signos',
            'Como cada signo lida com términos e rejeição',
            'Gatilhos emocionais por elemento',
        ]),
        ('PARTE 5', 'Autoconhecimento pela Astrologia', [
            'Além do signo solar: Lua e Ascendente',
            'Transformando sua sombra em força',
            'Práticas de reflexão por signo',
            'Como usar este guia ao longo da vida',
        ]),
    ]

    for num, title, items in parts:
        story.append(Paragraph(f'<b>{num}</b>  —  {title}', ST['toc_part']))
        for item in items:
            story.append(Paragraph(f'    {item}', ST['toc_item']))

    return story


def build_parte1():
    story = []

    # ── Prefácio ────────────────────────────────────────────
    story.append(lbl('PREFÁCIO'))
    story.append(h1('Uma palavra antes de começar'))
    story.append(hr())
    story.append(sp())
    story.append(insight_box(
        '"Este guia não é sobre previsões. Não é sobre futuro. É sobre você, agora."'
    ))
    story.append(sp(2))
    story.append(p(
        'A astrologia, quando usada com profundidade, funciona como um espelho. '
        'Ela não inventa quem você é: ela reflete. E às vezes, ver-se refletido em palavras '
        'que nunca tinham sido ditas sobre você é a experiência mais libertadora do mundo.'
    ))
    story.append(p(
        'Neste guia, você vai encontrar as partes de você que sempre sentiu, mas nunca conseguiu '
        'nomear. O jeito que você ama. O que te faz recuar. Os padrões que se repetem. '
        'E, mais importante: por que tudo isso faz sentido.'
    ))
    story.append(p(
        'Não importa se você acredita ou não em astrologia. Se você se identificar com o que '
        'está escrito, e vai se identificar, então algo aqui é verdadeiro para você. '
        'Use isso. Leve para sua vida. Compartilhe com quem você ama.'
    ))
    story.append(sp(2))
    story.append(insight_box(
        'Você é mais complexo do que qualquer rótulo. '
        'Este guia é um ponto de partida, não um veredicto.'
    ))
    story.append(PageBreak())

    # ── O que é astrologia ──────────────────────────────────
    story.append(lbl('CAPÍTULO 1'))
    story.append(h1('O que é astrologia e o que ela não é'))
    story.append(hr())
    story.append(sp())
    story.append(p(
        'A astrologia é um sistema simbólico de interpretação da psicologia humana baseado nas '
        'posições dos astros no momento do nascimento. Ela não determina seu destino: ela mapeia '
        'sua natureza. Pense nela como um idioma antigo para descrever padrões humanos que a '
        'psicologia moderna ainda está tentando nomear.'
    ))
    story.append(p(
        'Por mais de 2.000 anos, civilizações diferentes como babilônios, gregos, árabes, indianos, '
        'chineses, desenvolveram sistemas astrológicos independentes. Isso não é coincidência. '
        'É o registro de algo que a humanidade sempre soube: que existe uma correspondência '
        'entre os ritmos do cosmos e os padrões do comportamento humano.'
    ))
    story.append(h3('O que a astrologia NÃO é:'))
    story.append(bul('Não é determinismo. Seu mapa astral é uma disposição, não uma sentença.'))
    story.append(bul('Não é religião. Você pode usar a astrologia sem nenhuma crença específica.'))
    story.append(bul('Não é o horóscopo do jornal. Esses textos são entretenimento, não astrologia de verdade.'))
    story.append(bul('Não é uma desculpa. "Sou assim porque sou Escorpião" não é análise: é fuga.'))
    story.append(sp())
    story.append(h3('O que a astrologia É:'))
    story.append(bul('Uma linguagem para descrever arquétipos psicológicos universais.'))
    story.append(bul('Um mapa de tendências, não de certezas.'))
    story.append(bul('Uma ferramenta de autoconhecimento extraordinariamente precisa quando bem usada.'))
    story.append(bul('Um sistema que revela por que você reage do jeito que reage e o que fazer com isso.'))
    story.append(sp(2))
    story.append(insight_box(
        '"Conhece a ti mesmo." Esta frase, gravada no Oráculo de Delfos há 2.500 anos, '
        'ainda é o maior propósito da astrologia.'
    ))
    story.append(PageBreak())

    # ── Os 4 Elementos ──────────────────────────────────────
    story.append(lbl('CAPÍTULO 2'))
    story.append(h1('Os 4 Elementos'))
    story.append(hr())
    story.append(sp())
    story.append(p(
        'Tudo no zodíaco é organizado em quatro elementos fundamentais: Fogo, Terra, Ar e Água. '
        'Cada elemento representa uma forma básica de experienciar o mundo: '
        'uma linguagem emocional, uma forma de pensar, uma maneira de amar.'
    ))
    story.append(p(
        'Quando você entende o elemento do seu signo, começa a entender não apenas quem você é, '
        'mas POR QUE você é assim. E quando entende o elemento do signo de outra pessoa, '
        'começa a entender conflitos que pareciam inexplicáveis.'
    ))
    story.append(sp())

    # FOGO
    story.append(h2('FOGO — Áries, Leão, Sagitário'))
    story.append(p(
        'Os signos de fogo são movidos por entusiasmo, ação e propósito. São visionários, '
        'apaixonados e muitas vezes impulsivos. Sua maior necessidade é sentir que a vida '
        'tem significado e que eles estão fazendo algo que importa.'
    ))
    story.append(p(
        'O fogo não precisa de permissão para existir. Ele simplesmente queima, '
        'iluminando tudo ao redor, mas também podendo consumir o que está próximo demais.'
    ))
    story.append(bul('<b>No amor:</b> intensos, apaixonados, precisam de admiração e aventura.'))
    story.append(bul('<b>No trabalho:</b> líderes naturais, iniciadores, perdem energia em rotinas longas.'))
    story.append(bul('<b>Na crise:</b> podem explodir e se arrepender, ou sumir para não mostrar vulnerabilidade.'))
    story.append(bul('<b>Desequilibrado:</b> egocentrismo, impulsividade destrutiva, incapacidade de ouvir.'))
    story.append(sp())

    # TERRA
    story.append(h2('TERRA — Touro, Virgem, Capricórnio'))
    story.append(p(
        'Os signos de terra constroem. São práticos, confiáveis, sensoriais e orientados a resultados. '
        'Precisam de segurança: financeira, emocional, material. São os que persistem quando '
        'todos os outros desistem.'
    ))
    story.append(p(
        'A terra não se move rapidamente, mas quando se move, não volta atrás. '
        'Há uma força silenciosa e inabalável nos signos de terra que os signos de fogo e ar '
        'raramente compreendem até que precisam de algo sólido para se apoiar.'
    ))
    story.append(bul('<b>No amor:</b> leais, provedores, mostram amor através de ações e consistência.'))
    story.append(bul('<b>No trabalho:</b> meticulosos, persistentes, melhores na execução do que no início.'))
    story.append(bul('<b>Na crise:</b> internalizam, ficam rígidos, podem usar trabalho como fuga.'))
    story.append(bul('<b>Desequilibrado:</b> teimosia excessiva, materialismo, resistência a mudanças necessárias.'))
    story.append(sp())

    # AR
    story.append(h2('AR — Gêmeos, Libra, Aquário'))
    story.append(p(
        'Os signos de ar vivem no mundo das ideias, conexões e comunicação. São curiosos, '
        'sociáveis, adaptáveis e muitas vezes brilhantes. Precisam de liberdade intelectual '
        'e variedade para se sentir vivos.'
    ))
    story.append(p(
        'O ar é invisível mas essencial. Signos de ar são frequentemente subestimados '
        'emocionalmente: as pessoas confundem sua capacidade de articular sentimentos '
        'com ausência de profundidade. O erro é enorme.'
    ))
    story.append(bul('<b>No amor:</b> precisam de estimulação mental, liberdade e amizade como base.'))
    story.append(bul('<b>No trabalho:</b> comunicadores, estrategistas, melhores em ambientes dinâmicos.'))
    story.append(bul('<b>Na crise:</b> intelectualizam o que deveriam sentir, ficam indecisos ou evasivos.'))
    story.append(bul('<b>Desequilibrado:</b> superficialidade, incapacidade de comprometimento, frieza emocional.'))
    story.append(sp())

    # ÁGUA
    story.append(h2('ÁGUA — Câncer, Escorpião, Peixes'))
    story.append(p(
        'Os signos de água sentem em profundidades que poucos alcançam. São intuitivos, '
        'empáticos, emocionalmente intensos e frequentemente psíquicos em sua capacidade '
        'de sentir o que está por baixo da superfície.'
    ))
    story.append(p(
        'A água assume a forma do recipiente: signos de água se adaptam, absorvem, '
        'sentem o que outros não percebem. Isso os torna os parceiros mais profundos e '
        'os mais vulneráveis ao mesmo tempo.'
    ))
    story.append(bul('<b>No amor:</b> profundos, devotados, precisam de reciprocidade emocional real.'))
    story.append(bul('<b>No trabalho:</b> intuitivos, criativos, melhores em ambientes com propósito emocional.'))
    story.append(bul('<b>Na crise:</b> podem se afogar nas próprias emoções ou manipular passivamente.'))
    story.append(bul('<b>Desequilibrado:</b> dependência emocional, vitimização, dificuldade em estabelecer limites.'))
    story.append(sp(2))
    story.append(insight_box(
        'Você não tem apenas um elemento: você tem um mapa inteiro. '
        'Seu signo solar é o ponto de partida. Sua Lua e seu Ascendente '
        'revelam outros elementos que completam quem você é.'
    ))
    story.append(PageBreak())

    # ── Modalidades ─────────────────────────────────────────
    story.append(lbl('CAPÍTULO 3'))
    story.append(h1('As 3 Modalidades'))
    story.append(hr())
    story.append(sp())
    story.append(p(
        'Além dos elementos, cada signo pertence a uma das três modalidades: Cardinal, Fixo ou Mutável. '
        'As modalidades descrevem como cada signo usa sua energia, especialmente diante de desafios, '
        'mudanças e oportunidades.'
    ))
    story.append(sp())

    story.append(h2('CARDINAL — Áries, Câncer, Libra, Capricórnio'))
    story.append(p(
        'Os signos cardinais iniciam. São os arquitetos de novos começos, os líderes que '
        'colocam projetos em movimento. Cada um dos quatro cardinais representa o início '
        'de uma estação, e isso se reflete no seu caráter: eles arrancam coisas do chão.'
    ))
    story.append(p(
        'O desafio cardinal é a continuidade. Eles são excepcionais em começar, '
        'mas podem perder o interesse depois que a ação inicial já foi tomada. '
        'Precisam de estrutura que os mantenha comprometidos além do entusiasmo inicial.'
    ))
    story.append(bul('<b>Áries:</b> inicia pela ação direta e pela coragem.'))
    story.append(bul('<b>Câncer:</b> inicia pelo cuidado e pela criação de um lar emocional.'))
    story.append(bul('<b>Libra:</b> inicia pela conexão e pela busca de equilíbrio.'))
    story.append(bul('<b>Capricórnio:</b> inicia pela ambição e pela construção de estrutura.'))
    story.append(sp())

    story.append(h2('FIXO — Touro, Leão, Escorpião, Aquário'))
    story.append(p(
        'Os signos fixos sustentam. São os que pegam o que foi iniciado e levam até o fim '
        'com força de vontade extraordinária. São os pilares: quase impossível de mover '
        'quando decidiram algo.'
    ))
    story.append(p(
        'O desafio fixo é a rigidez. Eles podem confundir teimosia com força, '
        'e persistência com incapacidade de adaptação. Quando percebem que o que '
        'estão sustentando não vale mais a pena, a mudança pode demorar mais do que deveria.'
    ))
    story.append(bul('<b>Touro:</b> sustenta pela estabilidade, lealdade e persistência.'))
    story.append(bul('<b>Leão:</b> sustenta pelo orgulho, pela lealdade profunda e pela força da identidade.'))
    story.append(bul('<b>Escorpião:</b> sustenta pela intensidade, comprometimento total e memória emocional.'))
    story.append(bul('<b>Aquário:</b> sustenta pela convicção, ideais e visão de longo prazo.'))
    story.append(sp())

    story.append(h2('MUTÁVEL — Gêmeos, Virgem, Sagitário, Peixes'))
    story.append(p(
        'Os signos mutáveis adaptam. São os mais flexíveis, versáteis e bons em transições. '
        'Cada um representa o fim de uma estação e a preparação para a próxima. '
        'Eles existem na mudança, são bons em ambiguidade e em situações que exigem ajuste constante.'
    ))
    story.append(p(
        'O desafio mutável é o comprometimento. Eles podem ter dificuldade em se manter firmes '
        'em decisões, em sustentar relações por tempo suficiente para se aprofundar, '
        'ou em terminar o que começaram, porque já estão antecipando o próximo movimento.'
    ))
    story.append(bul('<b>Gêmeos:</b> adapta pelo intelecto, curiosidade e comunicação.'))
    story.append(bul('<b>Virgem:</b> adapta pela análise, detalhamento e aperfeiçoamento constante.'))
    story.append(bul('<b>Sagitário:</b> adapta pela busca de significado, expansão e filosofia.'))
    story.append(bul('<b>Peixes:</b> adapta pela intuição, empatia e dissolução de fronteiras.'))
    story.append(PageBreak())

    # ── Planetas Regentes ───────────────────────────────────
    story.append(lbl('CAPÍTULO 4'))
    story.append(h1('Os Planetas Regentes'))
    story.append(hr())
    story.append(sp())
    story.append(p(
        'Cada signo é regido por um planeta, e esse planeta define a energia central, '
        'o tema de vida e o estilo emocional do signo. Entender o planeta regente do '
        'seu signo (e dos signos que você ama) revela camadas que vão muito além do elemento e da modalidade.'
    ))
    story.append(sp())

    planetas = [
        ('Marte', 'Áries', 'Ação, desejo, coragem, agressividade. Marte é a força de colocar o que quer em movimento. Nativos de Marte são diretos, impulsivos e têm dificuldade em esperar. O desejo vem antes do plano.'),
        ('Vênus', 'Touro e Libra', 'Amor, beleza, prazer, conexão. Vênus é o princípio do que você considera valioso. Nativos de Vênus precisam de estética, relacionamentos e conforto para se sentir em casa no mundo.'),
        ('Mercúrio', 'Gêmeos e Virgem', 'Mente, comunicação, análise. Mercúrio é como você pensa e como você se expressa. Nativos de Mercúrio são brilhantes na comunicação, mas podem se perder na própria mente.'),
        ('Lua', 'Câncer', 'Emoções, instintos, memória, o lar. A Lua governa o que você precisa para se sentir seguro. Nativos da Lua são profundamente emocionais e guiados por intuição e memória afetiva.'),
        ('Sol', 'Leão', 'Identidade, propósito, ego, vitalidade. O Sol é quem você é no centro mais profundo. Nativos do Sol precisam brilhar, ser reconhecidos e ter propósito claro para prosperar.'),
        ('Saturno', 'Capricórnio', 'Disciplina, estrutura, tempo, responsabilidade. Saturno é o professor austero do zodíaco. Nativos de Saturno aprendem pelo esforço e constroem com paciência e determinação.'),
        ('Júpiter', 'Sagitário', 'Expansão, abundância, sabedoria, fé. Júpiter é o princípio do crescimento. Nativos de Júpiter buscam o grande, o significativo, o que expande a consciência.'),
        ('Urano', 'Aquário', 'Revolução, originalidade, mudança súbita, liberdade. Urano rompe padrões. Nativos de Urano são diferentes por natureza e encontram seu caminho fora dos trilhos estabelecidos.'),
        ('Netuno', 'Peixes', 'Sonhos, ilusões, transcendência, empatia. Netuno dissolve fronteiras. Nativos de Netuno sentem o que está além do visível, mas podem confundir ilusão com realidade.'),
        ('Plutão', 'Escorpião', 'Transformação, poder, morte e renascimento, profundidade. Plutão destrói para reconstruir. Nativos de Plutão passam por metamorfoses profundas e não saem das experiências como entraram.'),
    ]

    for planeta, signo, desc in planetas:
        story.append(KeepTogether([
            h3(f'{planeta}  —  {signo}'),
            p(desc),
            sp(0.5),
        ]))

    story.append(PageBreak())

    # ── Sol, Lua e Ascendente ────────────────────────────────
    story.append(lbl('CAPÍTULO 5'))
    story.append(h1('Sol, Lua e Ascendente'))
    story.append(Paragraph('A tríade essencial', ST['cover_subtitle']))
    story.append(hr())
    story.append(sp())
    story.append(p(
        'Quando as pessoas falam em "signo", quase sempre estão se referindo ao signo solar: '
        'a posição do Sol no momento do nascimento. Mas um mapa astral completo tem muito mais. '
        'As três posições mais importantes são o Sol, a Lua e o Ascendente. '
        'Juntos, eles criam um perfil muito mais completo e preciso do que qualquer um individualmente.'
    ))
    story.append(sp())

    story.append(h2('O SIGNO SOLAR — Sua identidade central'))
    story.append(p(
        'O signo solar representa quem você é na sua essência: sua identidade, seu ego, '
        'seu propósito de vida e a energia que você busca expressar no mundo. '
        'É o "eu" que você conscientemente cultiva ao longo da vida.'
    ))
    story.append(p(
        'Porém, o signo solar não opera sozinho. Se você não se identifica completamente '
        'com o seu signo, é porque sua Lua e seu Ascendente (e outros planetas) '
        'também estão presentes e podem ser igualmente influentes, ou até mais.'
    ))
    story.append(sp())
    story.append(h2('O SIGNO LUNAR — Sua vida emocional'))
    story.append(p(
        'A Lua representa sua vida emocional: os instintos, as necessidades não ditas, '
        'o que você precisa para se sentir seguro e amado. E também a memória afetiva: '
        'como você foi condicionado na infância e como isso ainda molda suas reações hoje.'
    ))
    story.append(p(
        'Se você já sentiu que suas reações emocionais não combinam com o seu signo solar, '
        'é quase certo que sua Lua é de um signo completamente diferente. '
        'A Lua governa como você ama em privado, o que quer dizer que é a posição '
        'mais reveladora para relacionamentos íntimos.'
    ))
    story.append(sp())

    story.append(h2('O ASCENDENTE — Como o mundo te vê'))
    story.append(p(
        'O ascendente (ou signo ascendente) é a máscara que você apresenta ao mundo: '
        'como as pessoas te percebem quando acabaram de te conhecer. '
        'É determinado pelo signo que estava nascendo no horizonte leste no momento do seu nascimento, '
        'por isso muda a cada duas horas aproximadamente.'
    ))
    story.append(p(
        'O ascendente é com frequência a primeira impressão que você causa. '
        'Se as pessoas frequentemente te descrevem de forma diferente de como você se vê, '
        'o ascendente é a explicação. Também influencia a aparência física e o estilo social.'
    ))
    story.append(sp(2))
    story.append(insight_box(
        'Para descobrir sua Lua e seu Ascendente, você precisa da data, '
        'hora e local exatos do seu nascimento. '
        'Com esses dados, um mapa astral completo revela uma dimensão inteiramente nova de quem você é.'
    ))
    story.append(sp(2))
    story.append(p(
        'Ao longo deste guia, sempre que ler sobre um signo, seja o seu ou o de alguém que você ama, '
        'lembre-se de que essas descrições se aplicam a qualquer posição em que esse signo aparece no mapa. '
        'Você pode ter características de Escorpião sem ser escorpiano, se sua Lua ou Ascendente for em Escorpião.'
    ))

    return story


# ════════════════════════════════════════════════════════════════
#  MONTAGEM DO DOCUMENTO
# ════════════════════════════════════════════════════════════════

def build_doc(output_path):
    # Frames
    cover_frame  = Frame(0, 0, PW, PH, leftPadding=0, rightPadding=0,
                         topPadding=0, bottomPadding=0)
    dark_frame   = Frame(2*cm, 2*cm, PW-4*cm, PH-4*cm,
                         leftPadding=0.5*cm, rightPadding=0.5*cm)
    normal_frame = Frame(2.2*cm, 1.8*cm, PW-4.4*cm, PH-3.8*cm,
                         leftPadding=0, rightPadding=0)

    doc = BaseDocTemplate(output_path, pagesize=A4,
                          title='O Guia Emocional dos Signos',
                          author='Guia Emocional dos Signos',
                          leftMargin=0, rightMargin=0,
                          topMargin=0, bottomMargin=0)

    templates = [
        PageTemplate(id='Cover',  frames=[cover_frame],  onPage=page_cover),
        PageTemplate(id='Dark',   frames=[dark_frame],   onPage=page_dark),
        PageTemplate(id='Normal', frames=[normal_frame], onPage=page_normal),
    ]
    doc.addPageTemplates(templates)

    story = []

    # ── CAPA ──────────────────────────────────────────────────
    story.append(Spacer(1, 6*cm))
    story.append(Paragraph('✦', ST['cover_badge']))
    story.append(Spacer(1, 0.8*cm))
    story.append(Paragraph('O Guia Emocional<br/>dos Signos', ST['cover_title']))
    story.append(Spacer(1, 0.6*cm))
    story.append(Paragraph(
        'Tudo sobre quem você é, como você ama,<br/>'
        'seus padrões, sua sombra<br/>e o que ninguém nunca te contou.',
        ST['cover_subtitle']))
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph('EDIÇÃO PREMIUM  ·  2025', ST['cover_badge']))
    story.append(Spacer(1, 1.2*cm))
    story.append(Paragraph(
        '♈  ♉  ♊  ♋  ♌  ♍  ♎  ♏  ♐  ♑  ♒  ♓',
        ParagraphStyle('signs_row',
            fontName='Helvetica', fontSize=16, leading=22,
            textColor=GOLD, alignment=TA_CENTER, letterSpacing=4)))

    # Transição para página normal
    from reportlab.platypus import NextPageTemplate
    story.append(NextPageTemplate('Normal'))
    story.append(PageBreak())

    # ── SUMÁRIO ───────────────────────────────────────────────
    story += build_toc()
    story.append(PageBreak())

    # ── DIVISOR PARTE 1 ───────────────────────────────────────
    story.append(NextPageTemplate('Dark'))
    story.append(PageBreak())
    story.append(Spacer(1, 5*cm))
    story.append(Paragraph('PARTE  I', ST['part_num']))
    story.append(Spacer(1, 0.4*cm))
    story.append(Paragraph('Os Fundamentos<br/>do Zodíaco', ST['part_title']))
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph(
        'Elementos  ·  Modalidades  ·  Planetas  ·  Sol, Lua e Ascendente',
        ParagraphStyle('part_sub',
            fontName='Helvetica', fontSize=11, leading=16,
            textColor=MUTED, alignment=TA_CENTER, letterSpacing=1)))

    story.append(NextPageTemplate('Normal'))
    story.append(PageBreak())

    # ── CONTEÚDO PARTE 1 ──────────────────────────────────────
    story += build_parte1()

    doc.build(story)
    print(f'[OK] PDF gerado: {output_path}')


if __name__ == '__main__':
    out = r'c:\Users\Heitor Melo\Desktop\Grana no Digital\Astrologia\O_Guia_Emocional_dos_Signos_PARTE1.pdf'
    build_doc(out)
