#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
O Guia Emocional dos Signos - PARTE 2: Os 12 Signos em Profundidade
Sem travessoes no texto. Pontuação natural: ponto, virgula, dois-pontos, parenteses.
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame,
    Paragraph, Spacer, PageBreak, HRFlowable,
    KeepTogether, Table, TableStyle, NextPageTemplate
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY

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

PW, PH = A4

def make_styles():
    s = {}
    s['cover_badge'] = ParagraphStyle('cover_badge', fontName='Helvetica',
        fontSize=10, textColor=GOLD, alignment=TA_CENTER, letterSpacing=2, leading=14)
    s['part_title'] = ParagraphStyle('part_title', fontName='Times-Bold',
        fontSize=30, leading=38, textColor=GOLD_LIGHT, alignment=TA_CENTER, spaceAfter=10)
    s['part_num'] = ParagraphStyle('part_num', fontName='Helvetica',
        fontSize=11, leading=16, textColor=GOLD, alignment=TA_CENTER,
        spaceAfter=14, letterSpacing=3)
    s['chapter_title'] = ParagraphStyle('chapter_title', fontName='Times-Bold',
        fontSize=26, leading=32, textColor=DARK_TEXT, spaceBefore=28, spaceAfter=10)
    s['chapter_label'] = ParagraphStyle('chapter_label', fontName='Helvetica-Bold',
        fontSize=9, leading=13, textColor=GOLD, spaceAfter=8, letterSpacing=2)
    s['section_title'] = ParagraphStyle('section_title', fontName='Times-Bold',
        fontSize=17, leading=22, textColor=DARK_TEXT, spaceBefore=22, spaceAfter=8)
    s['sub_title'] = ParagraphStyle('sub_title', fontName='Helvetica-Bold',
        fontSize=12, leading=17, textColor=SURFACE, spaceBefore=14, spaceAfter=6)
    s['body'] = ParagraphStyle('body', fontName='Helvetica', fontSize=11,
        leading=18, textColor=BODY_TEXT, spaceAfter=10, alignment=TA_JUSTIFY)
    s['body_bold'] = ParagraphStyle('body_bold', fontName='Helvetica-Bold',
        fontSize=11, leading=18, textColor=DARK_TEXT, spaceAfter=6)
    s['bullet'] = ParagraphStyle('bullet', fontName='Helvetica', fontSize=11,
        leading=18, textColor=BODY_TEXT, spaceAfter=5,
        leftIndent=18, firstLineIndent=-12)
    s['insight'] = ParagraphStyle('insight', fontName='Times-Italic', fontSize=12,
        leading=20, textColor=DARK_TEXT, spaceAfter=10, alignment=TA_CENTER,
        leftIndent=24, rightIndent=24)
    s['label'] = ParagraphStyle('label', fontName='Helvetica', fontSize=9,
        leading=13, textColor=MUTED, spaceAfter=4, letterSpacing=1)
    s['sign_name'] = ParagraphStyle('sign_name', fontName='Times-Bold',
        fontSize=32, leading=38, textColor=GOLD_LIGHT, alignment=TA_CENTER, spaceAfter=6)
    s['sign_meta'] = ParagraphStyle('sign_meta', fontName='Helvetica', fontSize=10,
        leading=15, textColor=HexColor('#c0b090'), alignment=TA_CENTER,
        spaceAfter=4, letterSpacing=1)
    s['sign_sym'] = ParagraphStyle('sign_sym', fontName='Helvetica-Bold',
        fontSize=40, leading=48, textColor=GOLD, alignment=TA_CENTER, spaceAfter=8)
    s['compat_good'] = ParagraphStyle('compat_good', fontName='Helvetica-Bold',
        fontSize=11, leading=17, textColor=HexColor('#4a9a6a'), spaceAfter=4)
    s['compat_ok'] = ParagraphStyle('compat_ok', fontName='Helvetica-Bold',
        fontSize=11, leading=17, textColor=HexColor('#c9a96e'), spaceAfter=4)
    s['compat_hard'] = ParagraphStyle('compat_hard', fontName='Helvetica-Bold',
        fontSize=11, leading=17, textColor=HexColor('#c96e6e'), spaceAfter=4)
    return s

ST = make_styles()

def page_dark(cv, doc):
    cv.saveState()
    cv.setFillColor(DARK_BG)
    cv.rect(0, 0, PW, PH, fill=1, stroke=0)
    cv.setFillColor(GOLD)
    cv.setFont('Helvetica', 12)
    cv.drawCentredString(PW/2, 1.4*cm, '✦')
    cv.restoreState()

def page_sign_banner(cv, doc):
    cv.saveState()
    cv.setFillColor(SURFACE)
    cv.rect(0, 0, PW, PH, fill=1, stroke=0)
    cv.setFillColor(GOLD)
    cv.rect(0, PH - 3, PW, 3, fill=1, stroke=0)
    cv.setFillColor(DARK_BG)
    cv.rect(0, 0, PW, 0.35*cm, fill=1, stroke=0)
    cv.restoreState()

def page_normal(cv, doc):
    cv.saveState()
    cv.setFillColor(LIGHT_BG)
    cv.rect(0, 0, PW, PH, fill=1, stroke=0)
    cv.setFillColor(GOLD)
    cv.rect(0, PH - 3, PW, 3, fill=1, stroke=0)
    cv.setFillColor(MUTED)
    cv.setFont('Helvetica', 8)
    cv.drawCentredString(PW/2, 0.8*cm, 'O Guia Emocional dos Signos')
    cv.setFillColor(GOLD)
    cv.drawString(PW - 2*cm, 0.8*cm, str(doc.page))
    cv.setStrokeColor(BORDER)
    cv.setLineWidth(0.5)
    cv.line(2*cm, 1.2*cm, PW - 2*cm, 1.2*cm)
    cv.restoreState()

def insight_box(text):
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

def compat_box(melhor, bom, desafiador):
    rows = [
        [Paragraph('Melhor com:', ST['label']),
         Paragraph(melhor, ST['compat_good'])],
        [Paragraph('Funciona bem:', ST['label']),
         Paragraph(bom, ST['compat_ok'])],
        [Paragraph('Mais desafiador:', ST['label']),
         Paragraph(desafiador, ST['compat_hard'])],
    ]
    t = Table(rows, colWidths=[4*cm, 9*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), CREAM),
        ('BOX',        (0,0), (-1,-1), 0.8, BORDER),
        ('LINEBELOW',  (0,0), (-1,-2), 0.5, BORDER),
        ('LEFTPADDING',  (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING',   (0,0), (-1,-1), 7),
        ('BOTTOMPADDING',(0,0), (-1,-1), 7),
        ('VALIGN',       (0,0), (-1,-1), 'MIDDLE'),
    ]))
    return t

def h1(t): return Paragraph(t, ST['chapter_title'])
def h2(t): return Paragraph(t, ST['section_title'])
def h3(t): return Paragraph(t, ST['sub_title'])
def p(t):  return Paragraph(t, ST['body'])
def lbl(t): return Paragraph(t, ST['chapter_label'])
def sp(n=1): return Spacer(1, n * 0.4*cm)
def hr(): return HRFlowable(width='100%', thickness=0.8, color=BORDER, spaceAfter=12, spaceBefore=4)
def bul(t): return Paragraph(f'<b>•</b>  {t}', ST['bullet'])

def sign_header(símbolo, nome, elemento, modalidade, planeta, período):
    """Pagina de abertura de cada signo (fundo escuro)."""
    items = [
        NextPageTemplate('SignBanner'),
        PageBreak(),
        Spacer(1, 3.5*cm),
        Paragraph(símbolo, ST['sign_sym']),
        Spacer(1, 0.3*cm),
        Paragraph(nome, ST['sign_name']),
        Spacer(1, 0.5*cm),
        Paragraph(
            f'{elemento}  |  {modalidade}  |  {planeta}',
            ST['sign_meta']),
        Paragraph(período, ST['sign_meta']),
        Spacer(1, 1.2*cm),
        HRFlowable(width='40%', thickness=0.8, color=GOLD,
                   spaceAfter=0, spaceBefore=0, hAlign='CENTER'),
        NextPageTemplate('Normal'),
        PageBreak(),
    ]
    return items

# ════════════════════════════════════════
# CONTEUDO DOS 12 SIGNOS
# ════════════════════════════════════════

def signo_áries():
    s = []
    s += sign_header('♈', 'Áries', 'Fogo', 'Cardinal', 'Marte', '21 de março a 19 de abril')

    s.append(lbl('PERFIL EMOCIONAL'))
    s.append(h1('Áries'))
    s.append(hr())
    s.append(sp())
    s.append(p(
        'Áries é o primeiro signo do zodíaco, e isso se reflete em tudo que esse signo faz. '
        'Ele não pede licença para existir. Sente antes de pensar, age antes de planejar '
        'e ama antes de saber se é recíproco. Há algo de primordial no ariano: uma energia '
        'bruta, genuína e completamente sem filtro que poucos conseguem acompanhar no longo prazo.'
    ))
    s.append(p(
        'O mundo emocional do ariano é intenso e imediato. Eles não experienciam as emoções '
        'de forma gradual: elas chegam com tudo, são processadas (ou não) em tempo real, '
        'e passam com a mesma velocidade que chegaram. A raiva é expressiva. A alegria é '
        'contagiante. A paixão é avassaladora. E no momento em que sentem, é a coisa mais '
        'real do mundo.'
    ))
    s.append(p(
        'Mas há algo que a maioria das pessoas não percebe: por baixo de toda essa intensidade '
        'existe uma vulnerabilidade que arianos protegem com unhas e dentes. Toda a ação, '
        'toda a intensidade, é em parte uma forma de garantir que as pessoas os vejam, os sintam, '
        'os reconhecam. O medo de ser invisível move Áries tanto quanto a coragem.'
    ))

    s.append(sp())
    s.append(h2('Como Áries Ama'))
    s.append(p(
        'Amar para um ariano é uma aventura, pelo menos no começo. Eles se jogam na conquista '
        'com tudo que tem. São diretos (nunca vão ficar mandando sinais mistos), apaixonados '
        'e incrivelmente protetores de quem amam.'
    ))
    s.append(p(
        'O problema é que arianos precisam de desafio constante. Quando a conquista acaba '
        'e a rotina começa, eles podem sentir que o fogo diminuiu. Não necessáriamente porque '
        'o amor acabou, mas porque precisam ser estimulados para se sentir vivos dentro de '
        'uma relação. Um parceiro que nunca surpreende, nunca desafia, nunca faz pensar '
        'é um parceiro que Áries vai gradualmente deixando de lado sem culpa.'
    ))
    s.append(sp(0.5))
    s.append(h3('O que Áries precisa em uma relação:'))
    s.append(bul('Ser admirado pela sua força e independência, não apesar delas.'))
    s.append(bul('Liberdade para ser quem é sem ter que se explicar o tempo todo.'))
    s.append(bul('Um parceiro que tenha sua própria vida, suas próprias paixões.'))
    s.append(bul('Conflitos resolvidos de forma direta, sem drama passivo-agressivo.'))
    s.append(bul('Aventura, novidade e surpresas periódicas que reacendam o interesse.'))

    s.append(sp())
    s.append(h2('O Lado Sombrio'))
    s.append(p(
        'O lado sombrio do ariano é tão intenso quanto seu lado luminoso. '
        'Quando desequilibrado ou ferido, Áries pode ser egocêntrico ao ponto de genuinamente '
        'não conseguir ouvir o ponto de vista do outro. A impulsividade vira destruição: '
        'diz coisas que ferem, toma decisões sem pensar, abandona o que começou no meio. '
        'O ciúme surge disfarçado de proteção. É o traço mais difícil: Áries tem uma dificuldade '
        'real em admitir erros porque o ego é frágil exatamente onde parece mais forte.'
    ))
    s.append(bul('Competitividade que prejudica quem ama porque precisa vencer em tudo.'))
    s.append(bul('Impaciência que vira crueldade quando as coisas não andam no ritmo dele.'))
    s.append(bul('Possessividade que chama de cuidado mas é controle.'))
    s.append(bul('Dificuldade profunda em pedir desculpas de forma genuína.'))

    s.append(sp())
    s.append(h2('Traços Secretos'))
    s.append(insight_box(
        'Por baixo de toda a intensidade existe alguém que tem medo de não ser suficiente. '
        'Arianos são mais sensíveis do que parecem. '
        'Uma crítica que para outros seria minima pode devasta-los por dentro, '
        'embora por fora não demonstrem nada.'
    ))
    s.append(sp())
    s.append(p(
        'Arianos têm uma capacidade de cuidado que poucos esperam. Quando estão do seu lado '
        'de verdade, são dos mais leais e protetores que existem. Também têm um humor genuíno '
        'e uma leveza que surge quando se sentem seguros: o ariano que não precisa se defender '
        'é completamente diferente do que a maioria conhece.'
    ))

    s.append(sp())
    s.append(h2('Medos Profundos'))
    s.append(bul('Ser invisível: que ninguém o veja ou reconheça de verdade.'))
    s.append(bul('Perder o controle de uma situação importante.'))
    s.append(bul('Ser considerado fraco ou covarde por quem admira.'))
    s.append(bul('Fracasso público e humilhação diante dos outros.'))
    s.append(bul('Não ser amado apesar de toda a intensidade que oferece.'))

    s.append(sp())
    s.append(h2('O que Bloqueia Áries'))
    s.append(bul('Dificuldade em pedir ajuda porque pedir seria admitir fraqueza.'))
    s.append(bul('Começa muita coisa e termina pouco quando o entusiasmo inicial passa.'))
    s.append(bul('Impaciência com processos lentos que exigem persistência.'))
    s.append(bul('Reatividade: toma decisões baseadas em raiva que depois lamenta.'))
    s.append(bul('Resistência a feedback crítico mesmo quando vem de quem ama.'))

    s.append(sp())
    s.append(h2('Compatibilidade'))
    s.append(compat_box(
        'Leão e Sagitário: o mesmo fogo alimenta a chama mútuamente.',
        'Libra: opostos que se completam, com tensão criativa entre ação e equilíbrio.',
        'Câncer e Capricórnio: ritmos e linguagens emocionais muito diferentes.'
    ))

    return s


def signo_touro():
    s = []
    s += sign_header('♉', 'Touro', 'Terra', 'Fixo', 'Vênus', '20 de abril a 20 de maio')

    s.append(lbl('PERFIL EMOCIONAL'))
    s.append(h1('Touro'))
    s.append(hr())
    s.append(sp())
    s.append(p(
        'Touro é o signo da presença. Enquanto outros signos existem no futuro ou no passado, '
        'Touro existe agora: no toque, no sabor, no cheiro, no conforto de uma noite que não '
        'precisa de mais nada. A regência de Vênus faz com que os taurinos sejam movidos '
        'pela beleza e pelo prazer de existir no mundo físico.'
    ))
    s.append(p(
        'O mundo interno do taurino é rico, sensorial e emocionalmente denso. '
        'Eles simplesmente processam por dentro, raramente exibem o que está acontecendo, '
        'e chegam às conclusões no próprio tempo. A famosa estabilidade de Touro não é '
        'ausência de emoção: é um controle consciente e constante para que o mundo não desmorone.'
    ))
    s.append(p(
        'Há um nível de ansiedade silênciosa em Touro que pouca gente percebe. '
        'Tudo que eles constroem ao redor de si, a rotina, os hábitos, as seguranças materiais '
        'e relacionais, é uma forma de manter a estabilidade que precisam para funcionar. '
        'Quando essa estabilidade é ameaçada, o taurino pode se tornar irreconhecível.'
    ))

    s.append(sp())
    s.append(h2('Como Touro Ama'))
    s.append(p(
        'Touro ama de forma total e duradora. Quando um taurino te escolhe, te escolhe de verdade. '
        'São leais de uma forma que poucas pessoas conhecem: para eles, o amor não é uma emoção '
        'passageira, é uma decisão que se reafirma todos os dias através de ações concretas.'
    ))
    s.append(p(
        'Mas eles amam no tempo deles. Não apresse um taurino. A construção da confiança '
        'é um processo cuidadoso e intencional. Uma vez quebrada, raramente é reconstruída '
        'completamente. Taurinos não esquecem como foram tratados, mesmo que perdoem.'
    ))
    s.append(sp(0.5))
    s.append(h3('O que Touro precisa em uma relação:'))
    s.append(bul('Segurança emocional, não palavras bonitas. Ações que provem consistência.'))
    s.append(bul('Afeto físico real: toque, presença, momentos compartilhados.'))
    s.append(bul('Previsibilidade saudável: não suportam parceiros quentes e frios ao mesmo tempo.'))
    s.append(bul('Ser apreciado pelo que constroem e pelo cuidado que dedicam.'))
    s.append(bul('Parceiro que não os pressione a mudar mais rápido do que conseguem.'))

    s.append(sp())
    s.append(h2('O Lado Sombrio'))
    s.append(p(
        'Touro desequilibrado pode ser teimoso ao extremo, confundindo rigidez com força de caráter. '
        'A possessividade surge quando se sentem inseguros e tratam pessoas como pertences '
        'sem perceber que estão fazendo isso. Guardam rancor por anos sem dizer nada, '
        'e quando finalmente explodem, assustam a todos que pensavam conhecer aquela pessoa.'
    ))
    s.append(bul('Materialismo como substituto para necessidades emocionais não atendidas.'))
    s.append(bul('Resistência a mudanças necessárias mesmo quando está sendo prejudicado.'))
    s.append(bul('Rancor acumulado que nunca é expresso diretamente.'))
    s.append(bul('Inércia que impede de sair de situações ruins por medo do desconhecido.'))

    s.append(sp())
    s.append(h2('Traços Secretos'))
    s.append(insight_box(
        'Taurinos têm uma vida interior rica de beleza, prazer e percepção estética '
        'que as pessoas ao redor nunca suspeitam. '
        'São profundamente artísticos, sentem a música no corpo, '
        'percebem detalhes visuais que outros ignoram.'
    ))
    s.append(sp())
    s.append(p(
        'Também têm uma intuição quase corporal sobre pessoas e situações: '
        'sentem quando algo está errado antes de ter qualquer evidência concreta. '
        'Raramente falam sobre isso porque preferem esperar a prova antes de agir. '
    ))

    s.append(sp())
    s.append(h2('Medos Profundos'))
    s.append(bul('Instabilidade em qualquer forma: emocional, financeira, relacional.'))
    s.append(bul('Abandono depois de se abrir completamente para alguém.'))
    s.append(bul('Perda do conforto material que tanto trabalhou para construir.'))
    s.append(bul('Ser substituido por alguém que parece mais interessante.'))
    s.append(bul('Mudanças súbitas que fogem ao controle.'))

    s.append(sp())
    s.append(h2('O que Bloqueia Touro'))
    s.append(bul('Resistência a mudanças mesmo quando a mudança seria a melhor opção.'))
    s.append(bul('Dificuldade em processar e comunicar emoções diretamente.'))
    s.append(bul('Apego ao famíliar mesmo quando o famíliar está causando dano.'))
    s.append(bul('Rancor que nunca é expresso e vai corroendo por dentro.'))

    s.append(sp())
    s.append(h2('Compatibilidade'))
    s.append(compat_box(
        'Virgem e Capricórnio: mesma base terra, mesma necessidade de segurança e consistência.',
        'Escorpião: opostos que se sustentam mútuamente com intensidade e profundidade.',
        'Aquário e Leão: Aquário é imprevisível demais; Leão precisa de admiração que Touro raramente demonstra.'
    ))

    return s


def signo_gêmeos():
    s = []
    s += sign_header('♊', 'Gêmeos', 'Ar', 'Mutável', 'Mercúrio', '21 de maio a 20 de junho')

    s.append(lbl('PERFIL EMOCIONAL'))
    s.append(h1('Gêmeos'))
    s.append(hr())
    s.append(sp())
    s.append(p(
        'Gêmeos não é raso. É rápido. Há uma diferença crucial que a maioria das pessoas não '
        'percebe. O geminiano existe em múltiplas frequências simultaneamente, processando '
        'o mundo em uma velocidade que outros dificilmente acompanham. Isso não significa '
        'que não sente profundamente: significa que segue em frente enquanto outros ficariam parados.'
    ))
    s.append(p(
        'A mente é o principal órgão sensorial de Gêmeos. Eles processam emoções através '
        'de palavras, conversas e análise. Se não conseguem articular o que estão sentindo, '
        'literalmente não conseguem processá-lo. Por isso às vezes parecem frios ou desconexos: '
        'não porque não sintam, mas porque ainda não encontraram as palavras certas.'
    ))
    s.append(p(
        'O dualismo de Gêmeos é real. Eles genuinamente podem se sentir de formas '
        'contraditórias ao mesmo tempo. Não é manipulação, não é instabilidade, não é inconsequência. '
        'É simplesmente como percebem a realidade, e tentar forçá-los a escolher apenas '
        'um lado é como tentar fazer o vento soprar em uma só direção.'
    ))

    s.append(sp())
    s.append(h2('Como Gêmeos Ama'))
    s.append(p(
        'Gêmeos ama com a mente primeiro. Se não há estimulação intelectual, não há interesse '
        'genuíno. A atração começa na conversa, na curiosidade, no prazer de descobrir '
        'como o outro pensa. Um parceiro que para de surpreender para de ser interessante.'
    ))
    s.append(p(
        'Em relacionamentos, Gêmeos precisa de liberdade e variedade mais do que qualquer '
        'outro signo de ar. Não necessáriamente liberdade de trair, mas liberdade de ser '
        'múltiplo: de mudar de ideia, de explorar, de não ser colocado em uma caixa '
        'com uma etiqueta que já não corresponde a quem ele é hoje.'
    ))
    s.append(sp(0.5))
    s.append(h3('O que Gêmeos precisa em uma relação:'))
    s.append(bul('Estimulação intelectual constante: conversas que vão além da superfície.'))
    s.append(bul('Liberdade e autonomia dentro do relacionamento.'))
    s.append(bul('Parceiro que acompanhe suas mudanças sem se sentir traído por elas.'))
    s.append(bul('Comunicação honesta e sem drama excessivo.'))
    s.append(bul('Variedade: surpresas, experiências novas, dinâmicas que evoluem.'))

    s.append(sp())
    s.append(h2('O Lado Sombrio'))
    s.append(p(
        'Gêmeos desequilibrado pode ser inconsistente ao ponto de parecer completamente '
        'não confiável. Usa o humor e a intelectualização para evitar sentimentos que '
        'não sabe como processar. Pode ser fofoqueiro ou usar palavras de formas que '
        'ferem mais do que qualquer ato físico. A dificuldade de comprometimento pode '
        'virar uma fuga crônica de tudo que exige mais do que o entusiasmo inicial.'
    ))
    s.append(bul('Evasão emocional: quando o assunto fica sério demais, desvia.'))
    s.append(bul('Dizer o que o outro quer ouvir para evitar conflito.'))
    s.append(bul('Incapacidade de aprofundar o que começa por medo do comprometimento.'))
    s.append(bul('Indecisão crônica que paralisa ele mesmo e frustra quem está ao lado.'))

    s.append(sp())
    s.append(h2('Traços Secretos'))
    s.append(insight_box(
        'Gêmeos carrega uma solidão profunda que raramente admite. '
        'Justamente porque se conecta tão facilmente com tantas pessoas, '
        'às vezes sente que ninguém de verdade o conhece. '
        'O humor e a versatilidade são, com frequência, uma armadura.'
    ))
    s.append(sp())
    s.append(p(
        'Por baixo de toda a sociabilidade existe alguém que quer desesperadamente '
        'ser compreendido em sua totalidade: contradições incluídas. '
        'Quando Gêmeos encontra alguém que consegue sustentá-lo sem precisar que escolha '
        'um lado, é simplesmente transformador.'
    ))

    s.append(sp())
    s.append(h2('Medos Profundos'))
    s.append(bul('Ser completamente conhecido e depois rejeitado exatamente por isso.'))
    s.append(bul('Comprometimento que aprisione a liberdade de ser múltiplo.'))
    s.append(bul('Monotonia e estagnação que façam a vida perder o sabor.'))
    s.append(bul('Ser considerado superficial ou de pouca substância.'))

    s.append(sp())
    s.append(h2('O que Bloqueia Gêmeos'))
    s.append(bul('Dificuldade em aprofundar o que começa: sempre há algo novo mais interessante.'))
    s.append(bul('Intelectualização de sentimentos que precisariam ser simplesmente sentidos.'))
    s.append(bul('Indecisão crônica que posterga escolhas importantes.'))
    s.append(bul('Comunicação usada como arma quando se sente encurralado.'))

    s.append(sp())
    s.append(h2('Compatibilidade'))
    s.append(compat_box(
        'Libra e Aquário: mesma frequência de ar, liberdade mútua e estimulação intelectual.',
        'Sagitário: opostos que se complementam com aventura, curiosidade e expansão.',
        'Touro e Virgem: Touro é previsível demais; Virgem usa a mesma mente de forma muito diferente.'
    ))

    return s


def signo_câncer():
    s = []
    s += sign_header('♋', 'Câncer', 'Água', 'Cardinal', 'Lua', '21 de junho a 22 de julho')

    s.append(lbl('PERFIL EMOCIONAL'))
    s.append(h1('Câncer'))
    s.append(hr())
    s.append(sp())
    s.append(p(
        'Câncer é talvez o signo mais mal compreendido do zodíaco. A fachada pode ser dura, '
        'a pinça do caranguejo, a armadura que aparece quando se sente ameaçado, '
        'mas por baixo existe uma das almas mais profundamente sensíveis e amorosas '
        'de todo o zodíaco.'
    ))
    s.append(p(
        'Câncerianos vivem dentro das suas emoções como outros vivem em uma casa. '
        'As emoções não são algo que acontece a eles: são o próprio ambiente em que habitam. '
        'Sentem o que outros nem percebem. Captam mudanças de humor em uma sala antes de '
        'qualquer palavra ser dita. Memorizam como as pessoas os fazem sentir com uma '
        'precisão fotográfica que pode surpreender anos depois.'
    ))
    s.append(p(
        'A Lua, seu regente, os torna ciclicamente emocionais. Haverá dias de grande '
        'abertura e vulnerabilidade, e dias em que a pinça fecha completamente. '
        'Ambos são legítimos. Nenhum é definitivo. Quem conhece Câncer de verdade '
        'aprende a respeitar os dois.'
    ))

    s.append(sp())
    s.append(h2('Como Câncer Ama'))
    s.append(p(
        'Câncer ama com a totalidade do que é. Quando um cânceriano te deixa entrar de verdade, '
        'você passa a ser parte do seu mundo interior de uma forma que poucos alcançam. '
        'São os parceiros mais devotados, cuidadosos e emocionalmente presentes que existem.'
    ))
    s.append(p(
        'Mas esse amor vem com uma necessidade fundamental: reciprocidade emocional. '
        'Se sentem que estão amando mais do que recebem, recuam para se proteger. '
        'Esse ciclo de abertura e fechamento pode ser confuso para parceiros que não '
        'entendem que não é rejeição, é autopreservação.'
    ))
    s.append(sp(0.5))
    s.append(h3('O que Câncer precisa em uma relação:'))
    s.append(bul('Segurança emocional profunda: saber que pode se abrir sem ser julgado.'))
    s.append(bul('Ser escolhido ativamente, não apenas tolerado.'))
    s.append(bul('Carinho e afeto demonstrados em ações, não apenas sentidos internamente.'))
    s.append(bul('Um lar emocional: um espaço seguro para ser vulnerável.'))
    s.append(bul('Parceiro que apareça nas suas vulnerabilidades sem fugir.'))

    s.append(sp())
    s.append(h2('O Lado Sombrio'))
    s.append(p(
        'Quando desequilibrado, Câncer pode ser manipulador emocional sem perceber: '
        'usa a culpa como ferramenta, o silêncio como punição, o choro como pressão. '
        'Guarda magoas que nunca foram expressas diretamente e depois age a partir delas '
        'sem avisar o parceiro do que está acontecendo. O cuidado excessivo pode virar '
        'controle disfarçado de amor.'
    ))
    s.append(bul('Ressentimento acumulado que nunca é nomeado mas sempre presente.'))
    s.append(bul('Apego a relações ou pessoas que não servem mais por medo da perda.'))
    s.append(bul('Oscilações de humor que afastam quem ama e depois geram culpa.'))
    s.append(bul('Dificuldade em estabelecer limites porque cuidar é sua identidade.'))

    s.append(sp())
    s.append(h2('Traços Secretos'))
    s.append(insight_box(
        'Câncerianos são muito mais resilientes do que parecem. '
        'Por baixo da sensibilidade existe uma força cardinal real: '
        'eles iniciam, constroem, persistem. '
        'São com frequência os pilares silenciosos que sustentam as famílias inteiras.'
    ))
    s.append(sp())
    s.append(p(
        'Também têm uma intuição quase sobrenatural sobre pessoas. '
        'Frequentemente sabem quando algo está errado antes de ter qualquer evidência concreta, '
        'e raramente estão errados. O problema é que às vezes preferem não olhar de perto '
        'para não ter que agir com base no que perceberam.'
    ))

    s.append(sp())
    s.append(h2('Medos Profundos'))
    s.append(bul('Abandono: ser deixado por alguém que amava profundamente.'))
    s.append(bul('Não ser amado da forma que precisa, do jeito que precisa.'))
    s.append(bul('Perder a família ou os vínculos mais próximos.'))
    s.append(bul('Abertura emocional que não é correspondida com cuidado.'))
    s.append(bul('Ser visto como fraco ou "demais" por ser tãosensível.'))

    s.append(sp())
    s.append(h2('O que Bloqueia Câncer'))
    s.append(bul('Dificuldade em comunicar necessidades diretamente, espera que o outro adivinhe.'))
    s.append(bul('Cuida de todos enquanto ignora as próprias necessidades.'))
    s.append(bul('Apega-se a situações que já terminaram por medo de começar de novo.'))
    s.append(bul('Toma decisões a partir da emoção do momento, não da perspectiva mais ampla.'))

    s.append(sp())
    s.append(h2('Compatibilidade'))
    s.append(compat_box(
        'Escorpião e Peixes: profundidade emocional e intuição mútua criam conexão rara.',
        'Capricórnio: opostos complementares, Câncer oferece emoção, Capricórnio oferece estrutura.',
        'Áries e Aquário: Áries é direto demais para a sensibilidade de Câncer; Aquário é desapegado demais.'
    ))

    return s


def signo_leão():
    s = []
    s += sign_header('♌', 'Leão', 'Fogo', 'Fixo', 'Sol', '23 de julho a 22 de agosto')

    s.append(lbl('PERFIL EMOCIONAL'))
    s.append(h1('Leão'))
    s.append(hr())
    s.append(sp())
    s.append(p(
        'Leão é o signo do Sol. Como o Sol, existe para iluminar. '
        'Mas o que a maioria não percebe é que por trás de todo esse brilho existe '
        'uma das personalidades mais leais, generosas e carinhosas do zodíaco. '
        'O leonino não quer apenas atencao: quer reconhecimento genuíno. '
        'Há uma diferença enorme entre as duas coisas.'
    ))
    s.append(p(
        'Não precisam ser os mais famosos da sala. Precisam sentir que sua presença '
        'importa, que o que fazem tem valor, que são vistos na própria essência. '
        'Quando se sentem amados e reconhecidos, Leão é capaz de uma generosidade '
        'que surpreende até quem o conhece bem. Quando se sentem ignorados ou menosprezados, '
        'o ego ferido pode transformar o Leão mais amoroso em algo irreconhecível.'
    ))

    s.append(sp())
    s.append(h2('Como Leão Ama'))
    s.append(p(
        'Com drama e magnificência, no sentido mais genuíno. O amor para Leão é uma performance: '
        'eles adoram surpreender, presentear, criar momentos memoráveis. O romance não é um bônus, '
        'é uma necessidade. Um relacionamento sem gestos significativos é um relacionamento '
        'que vai lentamente perdendo o sentido para eles.'
    ))
    s.append(p(
        'Em relacionamentos, Leão é incrivelmente leal. Uma vez que escolhe alguém, '
        'defende essa pessoa com a intensidade de um leão protegendo seu território. '
        'Mas precisa de admiração em troca, não é vaidade, é a linguagem do amor deles: '
        'precisam sentir que o parceiro os vê como especiais.'
    ))
    s.append(sp(0.5))
    s.append(h3('O que Leão precisa em uma relação:'))
    s.append(bul('Ser admirado e escolhido ativamente, não dado como certo.'))
    s.append(bul('Romance e gestos que mostrem que o parceiro se importa.'))
    s.append(bul('Lealdade inabalável: trair a confiança de Leão é destruir a relação.'))
    s.append(bul('Espaço para ser o protagonista sem precisar diminuir o outro para isso.'))
    s.append(bul('Parceiro de quem se orgulhe e que o orgulhe em troca.'))

    s.append(sp())
    s.append(h2('O Lado Sombrio'))
    s.append(p(
        'Leão desequilibrado pode fazer tudo girar ao redor de si mesmo de forma '
        'que exaure as pessoas próximas. O drama pode virar exigência constante de atenção. '
        'O ciúme surge quando sente que o brilho está sendo roubado. '
        'A incapacidade de admitir estar errado pode destruir relações que '
        'poderiam ser salvas com um simples pedido de desculpas genuíno.'
    ))
    s.append(bul('Crueldade quando o orgulho é ferido, especialmente em público.'))
    s.append(bul('Necessidade de aprovação que pode virar dependência emocional.'))
    s.append(bul('Dificuldade em ceder protagonismo mesmo quando seria o certo a fazer.'))
    s.append(bul('Orgulho que impede de pedir ajuda ou admitir fragilidade.'))

    s.append(sp())
    s.append(h2('Traços Secretos'))
    s.append(insight_box(
        'Leoninos são muito mais inseguros do que demonstram. '
        'Todo o brilho é parcialmente uma armadura contra o medo de não ser suficiente. '
        'Por baixo do ego existe alguém que quer ser amado incondicionalmente: '
        'não pelo que faz, mas pelo que é.'
    ))
    s.append(sp())
    s.append(p(
        'São também profundamente sensíveis às emoções alheias, embora raramente admitam. '
        'Um Leão em seu melhor momento é completamente diferente do estereótipo: '
        'é alguém que ilumina genuinamente todos ao redor sem precisar diminuir ninguém.'
    ))

    s.append(sp())
    s.append(h2('Medos Profundos'))
    s.append(bul('Ser ignorado ou irrelevante para quem importa.'))
    s.append(bul('Não ser amado de volta com a mesma intensidade que ama.'))
    s.append(bul('Fracasso público ou humilhação diante dos outros.'))
    s.append(bul('Perder o controle da própria narrativa.'))
    s.append(bul('Não ser suficiente depois de tanto esforço.'))

    s.append(sp())
    s.append(h2('O que Bloqueia Leão'))
    s.append(bul('Ego que torna quase impossível pedir desculpas de forma genuína.'))
    s.append(bul('Necessidade de aprovação que cria dependência de validação externa.'))
    s.append(bul('Dificuldade em ouvir críticas sem se sentir pessoalmente atacado.'))
    s.append(bul('Drama que afasta as pessoas mais próximas quando usada em excesso.'))

    s.append(sp())
    s.append(h2('Compatibilidade'))
    s.append(compat_box(
        'Áries e Sagitário: o fogo se alimenta mútuamente com paixão e entusiasmo.',
        'Aquário: opostos que se fascinam, crescem e se desafiam mútuamente.',
        'Touro e Escorpião: Touro é teimoso demais; Escorpião tem ego igualmente forte.'
    ))

    return s


def signo_virgem():
    s = []
    s += sign_header('♍', 'Virgem', 'Terra', 'Mutável', 'Mercúrio', '23 de agosto a 22 de setembro')

    s.append(lbl('PERFIL EMOCIONAL'))
    s.append(h1('Virgem'))
    s.append(hr())
    s.append(sp())
    s.append(p(
        'Virgem é o signo mais mal compreendido quando se trata de emoções. '
        'A reputação de frio ou analítico esconde uma das almas mais cuidadosas '
        'e emocionalmente atenciosas do zodíaco. Virgianos simplesmente expressam '
        'amor de formas práticas, e isso é frequentemente invisível para quem '
        'está procurando declarações dramáticas.'
    ))
    s.append(p(
        'O mundo interno de Virgem é um lugar de análise constante. '
        'Eles processam tudo: situações, conversas, relações, com uma mente '
        'que nunca realmente desliga. Isso pode ser exaustivo para eles mesmos. '
        'A autocrítica virgiana não é frescura, é genuinamente automática e, '
        'com frequência, mais cruel consigo mesmo do que com qualquer outra pessoa.'
    ))

    s.append(sp())
    s.append(h2('Como Virgem Ama'))
    s.append(p(
        'Com serviço e presença. Um virgiano que te ama vai pesquisar o restaurante perfeito '
        'para o seu aniversário, vai lembrar que você mencionou que estava com dor de cabeça '
        'e aparecer com o remédio certo, vai revisar seu currículo às 23h porque você pediu. '
        'Esse é o amor deles: concreto, atencioso, funcional.'
    ))
    s.append(p(
        'Mas precisam de alguém que entenda esse idioma, porque raramente vão dizer '
        '"eu te amo" com a frequência que outros signos. Eles mostram. '
        'E quando o parceiro não percebe ou não valoriza o que fazem, '
        'Virgem se sente completamente invisível dentro da relação.'
    ))
    s.append(sp(0.5))
    s.append(h3('O que Virgem precisa em uma relação:'))
    s.append(bul('Ser apreciado pelo que faz, não apenas pelo que é.'))
    s.append(bul('Parceiro que não os critique excessivamente, pois já se autocriticam demais.'))
    s.append(bul('Espaço para processar internamente antes de dar uma resposta.'))
    s.append(bul('Confianca construída com consistência ao longo do tempo.'))
    s.append(bul('Parceiro que perceba os detalhes, porque eles percebem os de todos.'))

    s.append(sp())
    s.append(h2('O Lado Sombrio'))
    s.append(p(
        'Virgem desequilibrado pode ser crítico ao ponto de destruir relações com observações '
        'que poderiam ser úteis mas são ditas na hora errada, do jeito errado, vezes demais. '
        'O perfeccionismo paralisa: não começa porque ainda não está perfeito. '
        'O controle surge disfarçado de ajuda: "eu só estou tentando melhorar as coisas".'
    ))
    s.append(bul('Ansiedade crônica e debilitante que afeta decisões e relações.'))
    s.append(bul('Rigidez que impede de aceitar imperfeições inevitáveis.'))
    s.append(bul('Autocrítica que se torna crítica dos outros quando transferida.'))
    s.append(bul('Dificuldade em receber cuidado: mais fácil dar do que receber.'))

    s.append(sp())
    s.append(h2('Traços Secretos'))
    s.append(insight_box(
        'Virgianos são extremamente leais e raramente reconhecidos por isso. '
        'Quando Virgem está do seu lado, está de verdade. '
        'São também profundamente humanos: a autocrítica que aplicam nos outros '
        'é dez vezes mais intensa quando aplicada a si mesmos.'
    ))

    s.append(sp())
    s.append(h2('Medos Profundos'))
    s.append(bul('Falhar em algo que poderia ter controlado.'))
    s.append(bul('Ser considerado inadequado ou insuficiente.'))
    s.append(bul('Desordem e imprevisibilidade no ambiente ou nas relações.'))
    s.append(bul('Ser criticado exatamente pelos defeitos que já se autocrítica.'))

    s.append(sp())
    s.append(h2('O que Bloqueia Virgem'))
    s.append(bul('Perfeccionismo que impede de começar: espera que tudo esteja pronto.'))
    s.append(bul('Autocrítica que paralisa ao invés de motivar.'))
    s.append(bul('Dificuldade em receber cuidado sem se sentir em dívida.'))
    s.append(bul('Análise excessiva que substitui ação quando ação seria necessária.'))

    s.append(sp())
    s.append(h2('Compatibilidade'))
    s.append(compat_box(
        'Touro e Capricórnio: mesma base terra, valores compatíveis e ritmo semelhante.',
        'Peixes: opostos que se complementam, Virgem oferece estrutura, Peixes oferece profundidade.',
        'Sagitário e Gêmeos: Sagitário quer o panorama; Gêmeos usa a mesma mente de forma oposta.'
    ))

    return s


def signo_libra():
    s = []
    s += sign_header('♎', 'Libra', 'Ar', 'Cardinal', 'Vênus', '23 de setembro a 22 de outubro')

    s.append(lbl('PERFIL EMOCIONAL'))
    s.append(h1('Libra'))
    s.append(hr())
    s.append(sp())
    s.append(p(
        'Libra é movida por harmonia, mas não de uma forma passiva. '
        'A necessidade de equilíbrio de Libra é ativa, intensa e às vezes exaustiva. '
        'Eles constantemente avaliam, pesam, consideram todos os lados de uma questão. '
        'A famosa indecisão libriana não é preguiça mental: é a incapacidade de ignorar '
        'qualquer perspectiva válida antes de chegar a uma conclusão.'
    ))
    s.append(p(
        'Libra sente as emoções em relação, sempre em referência a como o outro está, '
        'o que o outro precisa, como a relação está sendo afetada. '
        'Isso os torna parceiros extraordinários, mas frequentemente os faz perder '
        'de vista as próprias necessidades no processo de cuidar de todos ao redor. '
    ))

    s.append(sp())
    s.append(h2('Como Libra Ama'))
    s.append(p(
        'Com elegância, atenção e um desejo profundo de parceria real. '
        'Libra não quer um relacionamento: quer uma aliança. Um companheiro de vida '
        'que compartilhe tanto os momentos cotidianos quanto as grandes decisões. '
        'São românticos genuínos que veem relacionamentos como obras de arte que se '
        'constroem com cuidado e intenção.'
    ))
    s.append(p(
        'Mas tem uma tendência de dizer o que o parceiro quer ouvir em vez do que '
        'realmente sentem. Com o tempo, isso pode criar uma distância entre o que '
        'Libra realmente precisa e o que o relacionamento está oferecendo, '
        'sem que o parceiro saiba que há algo errado.'
    ))
    s.append(sp(0.5))
    s.append(h3('O que Libra precisa em uma relação:'))
    s.append(bul('Parceria real: divisão equilibrada de responsabilidades e emoções.'))
    s.append(bul('Harmonia no ambiente: brigas sem resolução são fisicamente insuportáveis.'))
    s.append(bul('Reciprocidade genuína, não apenas aparente.'))
    s.append(bul('Apreciação pelo cuidado que dedica a relação.'))
    s.append(bul('Espaço para ser indeciso sem ser julgado por isso.'))

    s.append(sp())
    s.append(h2('O Lado Sombrio'))
    s.append(p(
        'Libra desequilibrado pode ser manipulador passivo: nunca diz o que quer diretamente, '
        'mas manobra para conseguir. Concorda com tudo para evitar conflito mesmo quando '
        'discorda profundamente, e isso vai acumulando até explodir de forma que surpreende '
        'quem achava que conhecia Libra. A dependência de relações para se sentir completo '
        'pode levar a ficar em situações que não servem mais.'
    ))
    s.append(bul('Superficialidade como escudo contra profundidade emocional desconfortável.'))
    s.append(bul('Indecisão que paralisa mesmo em situações urgentes.'))
    s.append(bul('Dependência de validação externa para tomar qualquer decisão.'))
    s.append(bul('Falsidade por harmonia: concorda por fora quando discorda por dentro.'))

    s.append(sp())
    s.append(h2('Traços Secretos'))
    s.append(insight_box(
        'Librianos têm opiniões muito mais fortes do que demonstram. '
        'Raramente as expressam porque antecipam o conflito que isso pode gerar. '
        'Por baixo da diplomacia existe alguém que tem visões claras sobre tudo: '
        'só aprendeu que expressar discordância tem um custo social.'
    ))

    s.append(sp())
    s.append(h2('Medos Profundos'))
    s.append(bul('Conflito sem resolução que não encontra equilíbrio.'))
    s.append(bul('Estar sozinho de forma prolongada.'))
    s.append(bul('Ser considerado injusto ou desequilibrado.'))
    s.append(bul('Tomar a decisão errada e não poder voltar atrás.'))

    s.append(sp())
    s.append(h2('O que Bloqueia Libra'))
    s.append(bul('Indecisão que posterga escolhas até que a janela se feche.'))
    s.append(bul('Sacrifica as próprias necessidades pela harmonia do outro.'))
    s.append(bul('Evita conversas dificeis até que o problema seja grande demais.'))
    s.append(bul('Dependência de aprovação externa para se sentir seguro.'))

    s.append(sp())
    s.append(h2('Compatibilidade'))
    s.append(compat_box(
        'Gêmeos e Aquário: mesma frequência de ar, liberdade e estimulação intelectual.',
        'Áries: opostos complementares, ambos cardinais com energia de iniciativa.',
        'Câncer e Capricórnio: linguagens emocionais muito diferentes das de Libra.'
    ))

    return s


def signo_escorpião():
    s = []
    s += sign_header('♏', 'Escorpião', 'Água', 'Fixo', 'Plutão e Marte', '23 de outubro a 21 de novembro')

    s.append(lbl('PERFIL EMOCIONAL'))
    s.append(h1('Escorpião'))
    s.append(hr())
    s.append(sp())
    s.append(p(
        'Escorpião sente com uma profundidade que a maioria das pessoas nunca experimenta. '
        'Não há emoções rasas aqui: cada sentimento é uma imersão total. '
        'Alegria, amor, traição, perda: tudo é sentido na sua forma mais absoluta. '
        'Mas esse oceano emocional existe quase inteiramente por baixo da superfície.'
    ))
    s.append(p(
        'Escorpianos são mestres em controlar o que mostram. A intensidade está sempre lá, '
        'simplesmente não é para todos. Apenas quem conquista a confiança de um escorpiano '
        've o que existe por dentro. Esse processo pode levar meses. Anos. '
        'E não há atalho.'
    ))
    s.append(p(
        'Plutão, seu planeta regente, governa transformação, morte e renascimento. '
        'Escorpião está em constante processo de se destruir e se reconstruir. '
        'Cada grande experiência emocional os transforma, e eles raramente saem '
        'de uma crise exatamente como entraram nela.'
    ))

    s.append(sp())
    s.append(h2('Como Escorpião Ama'))
    s.append(p(
        'Com obsessão e totalidade. Para um escorpiano, o amor não é uma coisa de meio-termo. '
        'Quando amam, amam com toda a intensidade do que são. São completamente devotados, '
        'mas também completamente exigentes. A lealdade é o valor supremo. '
        'Uma traição não é apenas uma falha: é uma destruição.'
    ))
    s.append(p(
        'E Escorpião não esquece. Pode perdoar, raramente, mas jamais esquece. '
        'A memória emocional de Escorpião é extraordinária e pode ser usada '
        'tanto para nutrir o relacionamento quanto para destrui-lo '
        'quando se sente traído.'
    ))
    s.append(sp(0.5))
    s.append(h3('O que Escorpião precisa em uma relação:'))
    s.append(bul('Lealdade absoluta: não há negociação nesse ponto.'))
    s.append(bul('Profundidade emocional e intelectual genuínas.'))
    s.append(bul('Parceiro que suporte a intensidade sem fugir ou diminuir.'))
    s.append(bul('Honestidade total: não suporta meias verdades.'))
    s.append(bul('Espaço para processar sem ser pressionado a se abrir antes do tempo.'))

    s.append(sp())
    s.append(h2('O Lado Sombrio'))
    s.append(p(
        'Escorpião desequilibrado tem uma capacidade extraordinária de encontrar '
        'as fraquezas alheias e usá-las de formas que poucas pessoas conseguem se defender. '
        'A vingatividade de Escorpião é real: a memória emocional que usam para nutrir '
        'um relacionamento é a mesma que usam para destruir quem os traiu. '
        'O controle surge como necessidade: precisam ter o poder em qualquer situação '
        'porque a vulnerabilidade lhes parece ameaçadora demais.'
    ))
    s.append(bul('Ciúme que vira possessividade tóxica quando não trabalhado.'))
    s.append(bul('Autodestrutividade quando ferido: é mais fácil se machucar que pedir ajuda.'))
    s.append(bul('Segredos guardados que criam distância onde poderia haver intimidade.'))
    s.append(bul('Tudo ou nada: não há zona cinza quando Escorpião decide.'))

    s.append(sp())
    s.append(h2('Traços Secretos'))
    s.append(insight_box(
        'Por baixo de toda a intensidade e poder existe alguém com medo profundo de ser traído. '
        'Cada camada de controle e mistério é uma proteção construída sobre '
        'vulnerabilidades reais que raramente mostram. '
        'Escorpianos precisam desesperadamente de um espaço seguro onde possam ser frágeis.'
    ))
    s.append(sp())
    s.append(p(
        'São também muito mais sensíveis ao sofrimento alheio do que admitem. '
        'Frequentemente escolhem profissões ou situações onde podem transformar dor, '
        'a sua e a dos outros. Há uma compaixão profunda em Escorpião que raramente '
        'aparece na superfície mas que molda suas escolhas de vida.'
    ))

    s.append(sp())
    s.append(h2('Medos Profundos'))
    s.append(bul('Traicao em qualquer forma, por qualquer pessoa.'))
    s.append(bul('Ser manipulado ou enganado por alguém em quem confiou.'))
    s.append(bul('Perder o controle sobre si mesmo em situações de alta carga emocional.'))
    s.append(bul('Vulnerabilidade que não é recebida com cuidado.'))
    s.append(bul('Abandono depois de se abrir completamente.'))

    s.append(sp())
    s.append(h2('O que Bloqueia Escorpião'))
    s.append(bul('Dificuldade em confiar mesmo quando há evidências de que é seguro.'))
    s.append(bul('Rancor que consome a si mesmo muito mais do que ao outro.'))
    s.append(bul('Necessidade de controle que afasta as pessoas que mais ama.'))
    s.append(bul('Incapacidade de pedir o que precisa diretamente.'))

    s.append(sp())
    s.append(h2('Compatibilidade'))
    s.append(compat_box(
        'Câncer e Peixes: profundidade emocional e intuição mútua que sustenta ambos.',
        'Touro: opostos que se sustentam com intensidade e lealdade compartilhada.',
        'Aquário e Leão: Aquário é desapegado demais; Leão tem ego igualmente forte.'
    ))

    return s


def signo_sagitário():
    s = []
    s += sign_header('♐', 'Sagitário', 'Fogo', 'Mutável', 'Júpiter', '22 de novembro a 21 de dezembro')

    s.append(lbl('PERFIL EMOCIONAL'))
    s.append(h1('Sagitário'))
    s.append(hr())
    s.append(sp())
    s.append(p(
        'Sagitário é a busca encarnada. Eles vivem com uma sensação perpétua de que '
        'existe algo maior la fora: uma verdade, uma experiência, um horizonte que '
        'ainda não alcançaram. Isso os torna apaixonantes e exasperantes ao mesmo tempo, '
        'dependendo de quem está ao lado deles.'
    ))
    s.append(p(
        'Júpiter, seu planeta regente, é o maior planeta do sistema solar, '
        'e Sagitário vive no grande. Pensa no grandioso, sonha no épico, '
        'se entedia com o pequeno. O mundo emocional sagitariano é expansivo '
        'e otimista por natureza: tem uma capacidade quase sobrenatural de encontrar '
        'o lado positivo de qualquer situação, o que pode ser um dom ou uma fuga.'
    ))

    s.append(sp())
    s.append(h2('Como Sagitário Ama'))
    s.append(p(
        'Com entusiasmo genuíno e uma liberdade que pode assustar parceiros mais apegados. '
        'Sagitário ama de verdade, mas ama dentro de uma filosofia de vida que inclui '
        'crescimento constante, aventura e expansão. Um relacionamento que tenta cerca-los '
        'vai durar pouco, não por falta de amor, mas por incompatibilidade fundamental com '
        'o que Sagitário precisa para existir.'
    ))
    s.append(p(
        'São completamente honestos, às vezes de forma brutal, porque valorizam a verdade '
        'acima do conforto emocional. Isso pode ser refrescante e machucador ao mesmo tempo, '
        'dependendo de quem está recebendo.'
    ))
    s.append(sp(0.5))
    s.append(h3('O que Sagitário precisa em uma relação:'))
    s.append(bul('Liberdade real, não é negociável e não é sobre trair.'))
    s.append(bul('Parceiro que cresca junto e que não o segure no lugar.'))
    s.append(bul('Aventura e experiências novas que mantenham o interesse vivo.'))
    s.append(bul('Honestidade mútua sem filtros excessivos.'))
    s.append(bul('Respeito pela sua filosofia de vida mesmo que seja diferente.'))

    s.append(sp())
    s.append(h2('O Lado Sombrio'))
    s.append(p(
        'Sagitário desequilibrado pode ser irresponsável com os sentimentos alheios: '
        'a honestidade sem tato pode ser cruel mesmo quando bem intencionada. '
        'A fuga de comprometimento surge não por maldade mas por um medo menos reconhecido: '
        'que a liberdade que tanto defende é, na verdade, uma forma de evitar vínculos '
        'que não sabe como sustentar no longo prazo.'
    ))
    s.append(bul('Otimismo excessivo que ignora problemas reais que precisam ser enfrentados.'))
    s.append(bul('Inconstância que frustra quem está ao lado e espera consistência.'))
    s.append(bul('Filosofia que paralisa a ação concreta: muito pensar, pouco fazer.'))
    s.append(bul('Fuga dos problemas para o próximo horizonte em vez de resolvê-los.'))

    s.append(sp())
    s.append(h2('Traços Secretos'))
    s.append(insight_box(
        'Sagitarianos têm um medo menos reconhecido: que a liberdade que tanto defendem '
        'é uma fuga de vínculos que não sabem como sustentar. '
        'Por baixo do cavaleiro livre existe alguém que também quer pertencer, '
        'mas tem medo de perder a si mesmo no processo.'
    ))

    s.append(sp())
    s.append(h2('Medos Profundos'))
    s.append(bul('Aprisionamento em qualquer forma, física, relacional ou mental.'))
    s.append(bul('Estagnação e rotina sem propósito ou crescimento.'))
    s.append(bul('Que a vida não tenha significado além do que é visível.'))
    s.append(bul('Perder a liberdade de ser quem é ao entrar em uma relação.'))

    s.append(sp())
    s.append(h2('O que Bloqueia Sagitário'))
    s.append(bul('Dificuldade com comprometimento duradouro mesmo quando quer ficar.'))
    s.append(bul('Otimismo que adia o enfrentamento de problemas necessários.'))
    s.append(bul('Inconstância que frustra projetos e relações de longo prazo.'))
    s.append(bul('Fuga para o próximo horizonte quando o atual fica complicado.'))

    s.append(sp())
    s.append(h2('Compatibilidade'))
    s.append(compat_box(
        'Áries e Leão: o fogo compartilhado sustenta a aventura e a paixão.',
        'Gêmeos: curiosidade e expansão compartilhadas com liberdade mútua.',
        'Touro e Câncer: Touro precisa de estabilidade; Câncer precisa de presença constante.'
    ))

    return s


def signo_capricórnio():
    s = []
    s += sign_header('♑', 'Capricórnio', 'Terra', 'Cardinal', 'Saturno', '22 de dezembro a 19 de janeiro')

    s.append(lbl('PERFIL EMOCIONAL'))
    s.append(h1('Capricórnio'))
    s.append(hr())
    s.append(sp())
    s.append(p(
        'Capricórnio aprendeu cedo que o mundo exige esforço, responsabilidade e seriedade. '
        'Por isso, construiu ao redor de si uma armadura de competência e autocontrole '
        'que pode ser impenetrável para a maioria das pessoas. '
        'Mas por dentro, especialmente quando ninguém está olhando, '
        'existe um ser profundamente emocional com um senso de humor surpreendente '
        'e uma capacidade de amor que só aparece para quem tiver paciência de esperar.'
    ))
    s.append(p(
        'Saturno, seu planeta regente, é o planeta da disciplina, estrutura e tempo. '
        'Capricórnio opera com uma perspectiva de longo prazo que às vezes parece fria, '
        'mas é, na verdade, uma forma de cuidado profundo. '
        'Eles não prometem o que não podem cumprir. Quando prometem algo, cumprem.'
    ))

    s.append(sp())
    s.append(h2('Como Capricórnio Ama'))
    s.append(p(
        'Lentamente, profundamente e permanentemente. A construção de um relacionamento '
        'com um capricorniano é gradual porque eles precisam ter certeza antes de '
        'se comprometer. Mas quando se comprometem, é total. '
        'Querem construir algo sólido: um futuro real, não apenas sentimentos.'
    ))
    s.append(p(
        'São provedores no sentido mais amplo da palavra: não necessariamente só financeiro, '
        'mas de estabilidade. Querem que o parceiro saiba que pode contar com eles '
        'independente do que aconteça. Essa é a linguagem do amor de Capricórnio.'
    ))
    s.append(sp(0.5))
    s.append(h3('O que Capricórnio precisa em uma relação:'))
    s.append(bul('Respeito pela ambição e pelo trabalho, não competição com eles.'))
    s.append(bul('Parceiro que entenda que amor é construção, não apenas sentimento imediato.'))
    s.append(bul('Consistência e confiabilidade ao longo do tempo.'))
    s.append(bul('Espaço para trabalhar sem se sentir culpado por isso.'))
    s.append(bul('Parceiro que tenha seus próprios objetivos de vida.'))

    s.append(sp())
    s.append(h2('O Lado Sombrio'))
    s.append(p(
        'Capricórnio desequilibrado usa o trabalho como fuga da intimidade: '
        'é mais seguro construir do que sentir. '
        'O controle surge do perfeccionismo: tudo precisa ser feito de um jeito específico. '
        'O pessimismo pode virar cinismo que drena as relações ao redor. '
        'E o julgamento, de si e dos outros, pode ser implacável quando '
        'os padrões não são alcançados.'
    ))
    s.append(bul('Frieza e inacessibilidade emocional que afasta quem quer se aproximar.'))
    s.append(bul('Workaholic que usa o sucesso profissional como substituto do afeto.'))
    s.append(bul('Rigidez que impede de aproveitar momentos sem agenda.'))
    s.append(bul('Dificuldade profunda em pedir ajuda: seria fraqueza.'))

    s.append(sp())
    s.append(h2('Traços Secretos'))
    s.append(insight_box(
        'Capricornianos são muito mais engraçados do que parecem. '
        'Têm um senso de humor seco e irônico que surge completamente inesperadamente. '
        'Por baixo de toda a seriedade existe alguém que simplesmente quer construir algo '
        'que dure: um amor, uma família, uma obra que comprove que valeu a pena.'
    ))

    s.append(sp())
    s.append(h2('Medos Profundos'))
    s.append(bul('Fracasso e incompetência, especialmente públicos.'))
    s.append(bul('Ser visto como fraco ou vulnerável.'))
    s.append(bul('Instabilidade financeira ou material depois de tanto trabalho.'))
    s.append(bul('Que o esforço de uma vida inteira não seja suficiente.'))

    s.append(sp())
    s.append(h2('O que Bloqueia Capricórnio'))
    s.append(bul('Dificuldade em ser vulnerável com quem ama.'))
    s.append(bul('Trabalho como fuga emocional que atrasa conexões reais.'))
    s.append(bul('Rigidez que impede de aceitar ajuda ou mudar de rota.'))
    s.append(bul('Autocrítica que nunca permite descansar no que já foi conquistado.'))

    s.append(sp())
    s.append(h2('Compatibilidade'))
    s.append(compat_box(
        'Touro e Virgem: mesma base terra, valores compartilhados e ritmo semelhante.',
        'Câncer: opostos complementares, estrutura e emoção que se equilibram.',
        'Áries e Libra: Áries é rápido demais; Libra quer harmonia imediata que Capricórnio não oferece.'
    ))

    return s


def signo_aquário():
    s = []
    s += sign_header('♒', 'Aquário', 'Ar', 'Fixo', 'Urano e Saturno', '20 de janeiro a 18 de fevereiro')

    s.append(lbl('PERFIL EMOCIONAL'))
    s.append(h1('Aquário'))
    s.append(hr())
    s.append(sp())
    s.append(p(
        'Aquário é o paradoxo do zodíaco. Por um lado, o signo mais humanitário: '
        'genuinamente comprometido com o bem coletivo, com a evolução, com a liberdade. '
        'Por outro, frequentemente o mais emocionalmente inacessível em relacionamentos íntimos. '
        'Cuida da humanidade e tem dificuldade com a pessoa ao lado.'
    ))
    s.append(p(
        'Urano, seu planeta regente, governa revolução, originalidade e mudança súbita. '
        'Aquário não consegue seguir regras que não fizerem sentido para eles, '
        'seja em comportamento, em relacionamentos ou em estrutura de vida. '
        'Isso não é rebeldia por rebeldia: é uma necessidade genuína de autenticidade '
        'que muitàs vezes os coloca em conflito com o convencional.'
    ))

    s.append(sp())
    s.append(h2('Como Aquário Ama'))
    s.append(p(
        'De forma única, não convencional, e frequentemente desconcertante para '
        'parceiros mais tradicionais. Aquário não segue o script do relacionamento padrão, '
        'e isso pode ser libertador ou confuso dependendo de quem está do outro lado. '
    ))
    s.append(p(
        'A amizade é a base de qualquer relação aquariana profunda. '
        'Se não existe amizade genuína, não existe amor verdadeiro para Aquário. '
        'São amigos íntimos antes de serem amantes, e essa base é o que os sustenta '
        'quando a paixão inicial se transforma em algo mais cotidiano.'
    ))
    s.append(sp(0.5))
    s.append(h3('O que Aquário precisa em uma relação:'))
    s.append(bul('Liberdade individual, mesmo dentro do relacionamento.'))
    s.append(bul('Amizade genuína como base de tudo que vier depois.'))
    s.append(bul('Parceiro que respeite sua originalidade sem tentar normalizá-lo.'))
    s.append(bul('Estimulação intelectual e conversas que expandam perspectivas.'))
    s.append(bul('Amor que não sufoque a independência que precisa para existir.'))

    s.append(sp())
    s.append(h2('O Lado Sombrio'))
    s.append(p(
        'Aquário desequilibrado pode ser emocionalmente frio de uma forma que parece crueldade, '
        'mesmo quando não é a intenção. A rebeldia pode virar postura: '
        'ser diferente por ser diferente, sem reflexão real. '
        'O desapego que nas melhores versões é maturidade pode virar '
        'incapacidade de se comprometer com qualquer coisa ou qualquer um.'
    ))
    s.append(bul('Arrogância sobre a própria originalidade e inteligência.'))
    s.append(bul('Desapego que parece indiferença para quem precisa de mais presença.'))
    s.append(bul('Incapacidade de comprometimento mesmo quando deseja a relação.'))
    s.append(bul('Intelectualização de tudo que deveria simplesmente ser sentido.'))

    s.append(sp())
    s.append(h2('Traços Secretos'))
    s.append(insight_box(
        'Aquarianos se importam mais profundamente do que demonstram. '
        'A aparente frieza emocional é com frequência uma proteção. '
        'Eles sentem muito, mas aprenderam que sentir profundamente em público '
        'cria vulnerabilidade que preferem evitar.'
    ))

    s.append(sp())
    s.append(h2('Medos Profundos'))
    s.append(bul('Perder a individualidade dentro de um relacionamento.'))
    s.append(bul('Ser como todos os outros, ser comum.'))
    s.append(bul('Aprisionamento em qualquer estrutura rígida.'))
    s.append(bul('Ser mal compreendido especialmente por quem ama.'))

    s.append(sp())
    s.append(h2('O que Bloqueia Aquário'))
    s.append(bul('Desconexão emocional usada como mecanismo de defesa.'))
    s.append(bul('Dificuldade em comprometimento mesmo quando quer ficar.'))
    s.append(bul('Intelectualiza o que deveria ser apenas sentido.'))
    s.append(bul('Necessidade de ser diferente mesmo quando o convencional seria melhor.'))

    s.append(sp())
    s.append(h2('Compatibilidade'))
    s.append(compat_box(
        'Gêmeos e Libra: liberdade e estimulação intelectual com respeito mútuo.',
        'Leão: opostos que se fascinam e crescem desafiando um ao outro.',
        'Touro e Escorpião: Touro precisa de segurança; Escorpião é intenso demais.'
    ))

    return s


def signo_peixes():
    s = []
    s += sign_header('♓', 'Peixes', 'Água', 'Mutável', 'Netuno e Júpiter', '19 de fevereiro a 20 de março')

    s.append(lbl('PERFIL EMOCIONAL'))
    s.append(h1('Peixes'))
    s.append(hr())
    s.append(sp())
    s.append(p(
        'Peixes é o último signo do zodíaco e carrega em si um fragmento de todos os outros. '
        'Há uma profundidade pisciana que é difícil de descrever sem recorrer ao místico. '
        'Eles sentem o que está além do visível. Captam camadas de realidade que outros '
        'simplesmente não percebem. Não é imaginação: é uma forma de percepção que '
        'funciona em frequências que a maioria das pessoas não acessa.'
    ))
    s.append(p(
        'O mundo emocional pisciano não tem fronteiras claras. Eles absorvem as emoções '
        'dos ambientes e das pessoas ao redor com uma porosidade que pode ser um dom, '
        'empatia extraordinária, ou uma dificuldade profunda, perder a si mesmo no outro. '
        'Precisam de âncoras para não se dissolver completamente nas energias ao redor.'
    ))

    s.append(sp())
    s.append(h2('Como Peixes Ama'))
    s.append(p(
        'Com uma profundidade que poucos conseguem sustentar. Para um pisciano, '
        'o amor é transcendental: é conexão de alma, não apenas de corpo ou mente. '
        'Amam de uma forma que pode parecer intensa demais para signos mais práticos, '
        'mas que para eles é simplesmente o mínimo do que o amor pode ser.'
    ))
    s.append(p(
        'São os parceiros mais empáticos, criativos e românticos do zodíaco. '
        'Mas também os mais suscetíveis a se dissolver no outro, a idealizar ao ponto '
        'da cegueira, e a ficar em relações que não os servem por medo da dor da separação.'
    ))
    s.append(sp(0.5))
    s.append(h3('O que Peixes precisa em uma relação:'))
    s.append(bul('Parceiro que entenda a profundidade sem se assustar com ela.'))
    s.append(bul('Segurança emocional para se abrir sem medo de ser ridicularizado.'))
    s.append(bul('Que o outro perceba a sensibilidade e a trate com cuidado.'))
    s.append(bul('Espaço para a criatividade, o sonho e a vida interior.'))
    s.append(bul('Conexão que vá além da superfície, que seja real.'))

    s.append(sp())
    s.append(h2('O Lado Sombrio'))
    s.append(p(
        'Peixes desequilibrado foge da realidade de formas que podem ser destrutivas: '
        'vícios, evasão, idealização de situações que precisariam ser enfrentadas. '
        'A vitimização surge: cria narrativas de martírio onde é o único que sofre, '
        'o único que ama de verdade, o único que foi traído. '
        'Os limites que não existem os levam a dar demais e depois ressentir por ter dado.'
    ))
    s.append(bul('Manipulação emocional passiva: choro, silêncio, culpa implícita.'))
    s.append(bul('Incapacidade de estabelecer limites e depois ressentimento por isso.'))
    s.append(bul('Idealização que cria decepções inevitáveis quando a realidade aparece.'))
    s.append(bul('Autodestrutividade quando em sofrimento profundo.'))

    s.append(sp())
    s.append(h2('Traços Secretos'))
    s.append(insight_box(
        'Piscianos são muito mais fortes do que parecem. '
        'A aparência de fragilidade esconde uma resiliência profunda. '
        'Eles sobrevivem a sofrimentos que quebrariam outros e frequentemente '
        'emergem transformados de uma forma que só a água consegue: '
        'fluindo ao redor dos obstáculos até encontrar o caminho.'
    ))
    s.append(sp())
    s.append(p(
        'São também extremamente perceptivos sobre a natureza humana. '
        'Apesar de serem tão frequentemente enganados, têm uma capacidade intuitiva '
        'de ver as pessoas em profundidade: só que às vezes preferem não olhar '
        'de perto para preservar a ilusão que preferem a uma realidade mais dura.'
    ))

    s.append(sp())
    s.append(h2('Medos Profundos'))
    s.append(bul('Não ser amado na profundidade e complexidade que é.'))
    s.append(bul('Estar completamente sozinho sem âncoras que o conectem ao mundo.'))
    s.append(bul('Ser traído por alguém que idealizou profundamente.'))
    s.append(bul('Que a realidade seja mais brutal do que a imagem que construiu dela.'))

    s.append(sp())
    s.append(h2('O que Bloqueia Peixes'))
    s.append(bul('Não consegue dizer não: diz sim quando quer dizer não por medo de decepcionar.'))
    s.append(bul('Idealização que cria decepções inevitáveis quando a realidade aparece.'))
    s.append(bul('Fuga da realidade que adia problemas que precisariam ser enfrentados.'))
    s.append(bul('Absorve emoções alheias e confunde com as próprias.'))

    s.append(sp())
    s.append(h2('Compatibilidade'))
    s.append(compat_box(
        'Câncer e Escorpião: profundidade emocional e intuição mútua que cria conexão rara.',
        'Virgem: opostos que se completam, estrutura e profundidade em equilíbrio.',
        'Gêmeos e Sagitário: Gêmeos é racional demais; Sagitário precisa de liberdade que Peixes confunde com abandono.'
    ))

    return s


# ════════════════════════════════════════
# MONTAGEM DO DOCUMENTO
# ════════════════════════════════════════

def build_doc(output_path):
    cover_frame  = Frame(0, 0, PW, PH, leftPadding=0, rightPadding=0,
                         topPadding=0, bottomPadding=0)
    dark_frame   = Frame(2*cm, 2.5*cm, PW-4*cm, PH-5*cm,
                         leftPadding=0.5*cm, rightPadding=0.5*cm)
    sign_frame   = Frame(2*cm, 2*cm, PW-4*cm, PH-4*cm,
                         leftPadding=0, rightPadding=0)
    normal_frame = Frame(2.2*cm, 1.8*cm, PW-4.4*cm, PH-3.8*cm,
                         leftPadding=0, rightPadding=0)

    doc = BaseDocTemplate(output_path, pagesize=A4,
                          title='O Guia Emocional dos Signos',
                          author='Guia Emocional dos Signos',
                          leftMargin=0, rightMargin=0,
                          topMargin=0, bottomMargin=0)

    templates = [
        PageTemplate(id='Dark',       frames=[dark_frame],   onPage=page_dark),
        PageTemplate(id='SignBanner', frames=[sign_frame],   onPage=page_sign_banner),
        PageTemplate(id='Normal',     frames=[normal_frame], onPage=page_normal),
    ]
    doc.addPageTemplates(templates)

    story = []

    # Divisor Parte 2
    story.append(NextPageTemplate('Dark'))
    story.append(Spacer(1, 5*cm))
    story.append(Paragraph('PARTE  II', ST['part_num']))
    story.append(Spacer(1, 0.4*cm))
    story.append(Paragraph('Os 12 Signos<br/>em Profundidade', ST['part_title']))
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph(
        'Perfil emocional  .  Como ama  .  Lado sombrio',
        ParagraphStyle('p2sub', fontName='Helvetica', fontSize=11, leading=16,
            textColor=MUTED, alignment=TA_CENTER, letterSpacing=1)))
    story.append(Paragraph(
        'Traços secretos  .  Medos profundos  .  Compatibilidade',
        ParagraphStyle('p2sub2', fontName='Helvetica', fontSize=11, leading=16,
            textColor=MUTED, alignment=TA_CENTER, letterSpacing=1)))
    story.append(NextPageTemplate('Normal'))

    # Os 12 signos
    story += signo_áries()
    story += signo_touro()
    story += signo_gêmeos()
    story += signo_câncer()
    story += signo_leão()
    story += signo_virgem()
    story += signo_libra()
    story += signo_escorpião()
    story += signo_sagitário()
    story += signo_capricórnio()
    story += signo_aquário()
    story += signo_peixes()

    doc.build(story)
    print(f'[OK] PDF gerado: {output_path}')


if __name__ == '__main__':
    out = r'c:\Users\Heitor Melo\Desktop\Grana no Digital\Astrologia\O_Guia_Emocional_dos_Signos_PARTE2.pdf'
    build_doc(out)
