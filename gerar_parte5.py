#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
O Guia Emocional dos Signos - PARTE 5: Autoconhecimento pela Astrologia
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, PageBreak,
                                  HRFlowable, KeepTogether, Table, TableStyle)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus.flowables import Flowable
import os

FONT_DIR = r'C:\Windows\Fonts'
pdfmetrics.registerFont(TTFont('Georgia',      os.path.join(FONT_DIR, 'georgia.ttf')))
pdfmetrics.registerFont(TTFont('Georgia-Bold', os.path.join(FONT_DIR, 'georgiab.ttf')))
pdfmetrics.registerFont(TTFont('Georgia-Ital', os.path.join(FONT_DIR, 'georgiai.ttf')))

NAVY      = colors.HexColor('#10142B')
GOLD      = colors.HexColor('#C9A96E')
CREAM     = colors.HexColor('#FAF7F0')
DARK_TEXT = colors.HexColor('#2A2540')
MID_GRAY  = colors.HexColor('#8A8598')
GREEN     = colors.HexColor('#4A7C5E')

W, H = A4
LEFT_MARGIN   = 2 * cm
BOTTOM_MARGIN = 1.8 * cm


class DarkPage(Flowable):
    def __init__(self, title, subtitle='', tag=''):
        super().__init__()
        self.title    = title
        self.subtitle = subtitle
        self.tag      = tag

    def wrap(self, availWidth, availHeight):
        return (availWidth, availHeight)

    def draw(self):
        c = self.canv
        c.saveState()
        c.translate(-LEFT_MARGIN, -BOTTOM_MARGIN)
        c.setFillColor(NAVY)
        c.rect(0, 0, W, H, fill=1, stroke=0)
        c.setStrokeColor(GOLD)
        c.setLineWidth(0.8)
        c.line(2*cm, H - 1.5*cm, W - 2*cm, H - 1.5*cm)
        c.line(2*cm, 1.5*cm,     W - 2*cm, 1.5*cm)
        if self.tag:
            c.setFillColor(GOLD)
            c.setFont('Georgia', 9)
            c.drawCentredString(W/2, H*0.58, self.tag)
        c.setFillColor(GOLD)
        c.setFont('Georgia-Bold', 40)
        lines = self.title.split('\n')
        y = H*0.50 if len(lines) == 1 else H*0.54
        for ln in lines:
            c.drawCentredString(W/2, y, ln)
            y -= 50
        if self.subtitle:
            c.setFillColor(MID_GRAY)
            c.setFont('Georgia-Ital', 13)
            for i, ln in enumerate(self.subtitle.split('\n')):
                c.drawCentredString(W/2, H*0.38 - i*18, ln)
        c.setFillColor(GOLD)
        cx, cy = W/2, 1.8*cm
        s = 5
        p = c.beginPath()
        p.moveTo(cx, cy+s); p.lineTo(cx+s, cy)
        p.lineTo(cx, cy-s); p.lineTo(cx-s, cy)
        p.close()
        c.drawPath(p, fill=1, stroke=0)
        c.restoreState()


def content_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(CREAM)
    canvas.rect(0, 0, W, H, fill=1, stroke=0)
    canvas.setStrokeColor(GOLD)
    canvas.setLineWidth(2)
    canvas.line(0, H - 0.4*cm, W, H - 0.4*cm)
    canvas.setFont('Georgia', 8)
    canvas.setFillColor(MID_GRAY)
    canvas.drawCentredString(W/2, 0.7*cm, 'O Guia Emocional dos Signos: Autoconhecimento')
    canvas.drawRightString(W - 2*cm, 0.7*cm, str(doc.page))
    canvas.restoreState()


def make_styles():
    s = {}
    s['chapter_tag'] = ParagraphStyle('chapter_tag',
        fontName='Georgia', fontSize=8, textColor=GREEN,
        spaceAfter=4, alignment=TA_LEFT, leading=10)
    s['chapter_title'] = ParagraphStyle('chapter_title',
        fontName='Georgia-Bold', fontSize=26, textColor=DARK_TEXT,
        spaceAfter=6, alignment=TA_LEFT, leading=32)
    s['section_title'] = ParagraphStyle('section_title',
        fontName='Georgia-Bold', fontSize=15, textColor=DARK_TEXT,
        spaceBefore=18, spaceAfter=5, alignment=TA_LEFT, leading=19)
    s['sign_title'] = ParagraphStyle('sign_title',
        fontName='Georgia-Bold', fontSize=13, textColor=DARK_TEXT,
        spaceBefore=12, spaceAfter=3, alignment=TA_LEFT, leading=16)
    s['body'] = ParagraphStyle('body',
        fontName='Georgia', fontSize=10.5, textColor=DARK_TEXT,
        spaceAfter=8, alignment=TA_JUSTIFY, leading=16)
    s['insight'] = ParagraphStyle('insight',
        fontName='Georgia-Ital', fontSize=11, textColor=DARK_TEXT,
        spaceAfter=8, alignment=TA_CENTER, leading=16,
        leftIndent=20, rightIndent=20)
    s['label'] = ParagraphStyle('label',
        fontName='Georgia-Bold', fontSize=9.5, textColor=GREEN,
        spaceAfter=2, alignment=TA_LEFT, leading=12)
    s['bullet'] = ParagraphStyle('bullet',
        fontName='Georgia', fontSize=10.5, textColor=DARK_TEXT,
        spaceAfter=5, alignment=TA_JUSTIFY, leading=16,
        leftIndent=16, firstLineIndent=-10)
    return s


def hr():
    return HRFlowable(width='100%', thickness=0.5, color=GOLD, spaceAfter=10, spaceBefore=4)


def insight_box(text, S):
    p = Paragraph(text, S['insight'])
    t = Table([[p]], colWidths=[13*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F5F0E8')),
        ('BOX',        (0,0), (-1,-1), 1, GOLD),
        ('LEFTPADDING',  (0,0), (-1,-1), 16),
        ('RIGHTPADDING', (0,0), (-1,-1), 16),
        ('TOPPADDING',   (0,0), (-1,-1), 12),
        ('BOTTOMPADDING',(0,0), (-1,-1), 12),
    ]))
    return t


# ══════════════════════════════════════════════════════
#  CAPÍTULO 15: ALÉM DO SIGNO SOLAR
# ══════════════════════════════════════════════════════

CAP15_INTRO = (
    'A maioria das pessoas conhece apenas seu signo solar. Mas um mapa astral completo é um '
    'documento muito mais rico: ele descreve não apenas quem você é, mas como você sente, '
    'como o mundo te percebe e quais são suas necessidades mais profundas. As três posições '
    'mais importantes, Sol, Lua e Ascendente,formam uma tríade que, quando compreendida '
    'em conjunto, oferece um retrato muito mais preciso do que qualquer uma individualmente.'
)

CAP15_SOL = (
    'O signo solar representa sua identidade central: o ego que você conscientemente '
    'desenvolve ao longo da vida, o que você quer expressar no mundo e onde busca propósito. '
    'É o "eu" que você reconhece como seu. Mas o Sol opera melhor quando sustentado pelas '
    'outras duas posições, sem elas, o quadro está incompleto.'
)

CAP15_LUA = (
    'A Lua descreve sua vida emocional: como você sente, o que precisa para se sentir seguro '
    'e amado, e a herança emocional que carrega da infância. A posição lunar muda a cada dois '
    'dias e meio, por isso requer hora de nascimento para ser calculada com precisão. Ela governa '
    'suas reações automáticas, seus instintos, e o tipo de cuidado que você busca, e oferece,'
    'em relacionamentos íntimos.'
)

CAP15_LUA2 = (
    'Se você se identifica pouco com seu signo solar em questões emocionais, é quase certo '
    'que sua Lua conta uma história diferente. Uma pessoa com Sol em Capricórnio e Lua em '
    'Câncer vai agir com disciplina no mundo externo, mas sentir com profundidade e '
    'necessidade de cuidado em casa. Essas aparentes contradições são, na verdade, camadas '
    'complementares de uma mesma pessoa.'
)

CAP15_ASC = (
    'O Ascendente, ou signo ascendente,é determinado pelo signo que estava no horizonte '
    'leste no momento exato do nascimento. Muda a cada duas horas, portanto é a posição mais '
    'pessoal do mapa. Ele representa a máscara social: como o mundo te vê antes de te conhecer, '
    'a primeira impressão que você causa e o estilo com que você aborda situações novas.'
)

CAP15_ASC2 = (
    'Muitas pessoas sentem que o Ascendente as representa mais do que o próprio signo solar, '
    'especialmente em contextos sociais e profissionais. Um Ascendente em Escorpião vai criar '
    'uma presença intensa e reservada mesmo que o signo solar seja Sagitário. '
    'Conhecer o Ascendente ajuda a entender por que as pessoas te percebem de formas que '
    'nem sempre correspondem à sua autopercepção.'
)

CAP15_OUTROS = (
    'Além da tríade, outros planetas em posições específicas contribuem para o retrato completo. '
    'Marte descreve como você age e o que desperta seu desejo. Vênus revela o que você chama '
    'de beleza e de amor. Mercúrio define como você pensa e se comunica. Saturno aponta suas '
    'áreas de desafio e crescimento. Cada planeta acrescenta uma dimensão que torna o mapa '
    'progressivamente mais preciso, e progressivamente mais seu.'
)

# ══════════════════════════════════════════════════════
#  CAPÍTULO 16: TRANSFORMANDO SUA SOMBRA EM FORÇA
# ══════════════════════════════════════════════════════

CAP16_INTRO = (
    'Carl Jung chamou de "sombra" o conjunto de traços que reprimimos porque, em algum momento, '
    'aprendemos que eles eram inaceitáveis. Esses traços não desaparecem, eles vão para um '
    'lugar menos visível e continuam operando de lá, frequentemente causando mais dano do que '
    'causariam se fossem reconhecidos e integrados.'
)

CAP16_INTRO2 = (
    'A astrologia oferece um mapa da sombra. O signo oposto ao seu solar, as casas difíceis '
    'do mapa, os planetas em tensão, tudo isso indica onde estão suas partes menos aceitas. '
    'Reconhecer a sombra não é capitular a ela: é aprender a usar a energia que ela contém '
    'de forma consciente e construtiva.'
)

SOMBRAS = [
    ('Áries', 'A sombra de Áries é a impulsividade destrutiva e o egocentrismo. Integrada, essa energia se torna liderança corajosa e capacidade de agir onde outros hesitam. O trabalho é aprender a pausar antes de reagir, não para suprimir, mas para canalizar.'),
    ('Touro', 'A sombra de Touro é a rigidez e a possessividade. Integrada, ela se torna perseverança e capacidade de construir algo que dura. O trabalho é aprender que segurança pode coexistir com mudança.'),
    ('Gêmeos', 'A sombra de Gêmeos é a superficialidade e a evasão. Integrada, ela se torna versatilidade e inteligência adaptativa. O trabalho é aprender a ficar presente tempo suficiente para aprofundar o que começa.'),
    ('Câncer', 'A sombra de Câncer é a dependência emocional e a manipulação passiva. Integrada, ela se torna cuidado profundo e inteligência emocional. O trabalho é aprender a expressar necessidades diretamente, sem esperar que o outro adivinhe.'),
    ('Leão', 'A sombra de Leão é a arrogância e a necessidade de aprovação. Integrada, ela se torna carisma genuíno e generosidade. O trabalho é aprender que o valor não depende da plateia.'),
    ('Virgem', 'A sombra de Virgem é o perfeccionismo paralisante e a autocrítica severa. Integrada, ela se torna precisão e cuidado com o que realmente importa. O trabalho é aprender que "bom o suficiente" é frequentemente excelente.'),
    ('Libra', 'A sombra de Libra é a indecisão e a falsidade por harmonia. Integrada, ela se torna diplomacia real e capacidade de mediar conflitos. O trabalho é aprender que a própria voz não destrói o equilíbrio, às vezes o cria.'),
    ('Escorpião', 'A sombra de Escorpião é a vingatividade e o controle obsessivo. Integrada, ela se torna profundidade emocional e capacidade de transformação. O trabalho é aprender que vulnerabilidade não é fraqueza, é coragem.'),
    ('Sagitário', 'A sombra de Sagitário é a irresponsabilidade e a fuga do comprometimento. Integrada, ela se torna expansão genuína e filosofia viva. O trabalho é aprender que profundidade e liberdade não são opostos.'),
    ('Capricórnio', 'A sombra de Capricórnio é o controle emocional excessivo e o uso do trabalho como fuga. Integrada, ela se torna disciplina a serviço de algo que importa. O trabalho é aprender que sentir não é sinal de fraqueza, é sinal de humanidade.'),
    ('Aquário', 'A sombra de Aquário é o distanciamento e a arrogância intelectual. Integrada, ela se torna visão genuína e capacidade de inovar. O trabalho é aprender que profundidade emocional com uma pessoa específica não contradiz a visão de mundo.'),
    ('Peixes', 'A sombra de Peixes é a vitimização e a fuga da realidade. Integrada, ela se torna empatia extraordinária e criatividade profunda. O trabalho é aprender que limites não destroem a sensibilidade, a protegem.'),
]

# ══════════════════════════════════════════════════════
#  CAPÍTULO 17: PRÁTICAS DE REFLEXÃO POR SIGNO
# ══════════════════════════════════════════════════════

CAP17_INTRO = (
    'Autoconhecimento não é um evento, é uma prática. O que a astrologia oferece é uma '
    'linguagem para nomear o que você já experimenta. Mas nomear não é suficiente: é '
    'necessário criar espaços regulares para observar seus padrões em ação e fazer escolhas '
    'mais conscientes. A seguir, uma prática específica para cada signo, baseada nas '
    'tendências naturais e nos pontos de crescimento de cada um.'
)

PRATICAS = [
    ('Áries', 'A pausa intencionada',
     'Antes de reagir a qualquer situação carregada, pratique uma pausa de 60 segundos. '
     'Não para suprimir a reação, mas para observá-la. Pergunte: "isso é urgente agora ou '
     'parece urgente?" Arianos que desenvolvem essa prática mantêm a energia sem o custo da impulsividade.'),
    ('Touro', 'O inventário do que já é suficiente',
     'Uma vez por semana, liste três coisas que você já tem e que são suficientes. '
     'Taurinos tendem a construir segurança acumulando; essa prática reconstrói segurança '
     'a partir do reconhecimento do que já existe. Também ajuda a identificar quando o apego '
     'está servindo e quando está aprisionando.'),
    ('Gêmeos', 'O diário de uma ideia por dia',
     'Escolha uma ideia por dia e escreva sobre ela com profundidade durante 15 minutos, '
     'sem mudar de assunto. Geminianos têm facilidade de gerar; o desafio é aprofundar. '
     'Essa prática treina a mente para tolerar a riqueza que existe dentro de um único tema.'),
    ('Câncer', 'A carta não enviada',
     'Quando sentir uma mágoa que não consegue expressar diretamente, escreva uma carta '
     'para a pessoa, sem enviá-la. Câncerianos frequentemente guardam ressentimentos porque '
     'temem a reação do outro. A carta cria um espaço seguro para nomear o que foi sentido, '
     'o que frequentemente dissolve parte da intensidade antes de qualquer conversa real.'),
    ('Leão', 'O registro do que você criou',
     'Mantenha um registro semanal de algo que você criou, expressou ou contribuiu, '
     'independente do tamanho. Leoninos constroem autoestima a partir do reconhecimento externo; '
     'essa prática desenvolve uma fonte interna de validação que não depende de plateia.'),
    ('Virgem', 'O "bom o suficiente" intencional',
     'Escolha uma tarefa por dia para completar em 80% da perfeição e declarar concluída. '
     'O objetivo não é baixar o padrão, mas treinar a percepção de que completar é mais '
     'valioso do que aperfeiçoar indefinidamente. Virgianos que praticam isso frequentemente '
     'descobrem que o resultado de 80% era melhor do que imaginavam.'),
    ('Libra', 'A decisão sem consulta',
     'Uma vez por semana, tome uma decisão, qualquer uma,sem pedir a opinião de ninguém. '
     'Librianos desenvolvem dependência de validação externa por medo de escolher errado. '
     'Essa prática reconstrói confiança na própria percepção e revela que a intuição interna '
     'é mais confiável do que parece.'),
    ('Escorpião', 'O inventário de controle',
     'Mensalmente, revise uma área da sua vida e pergunte: "onde estou usando controle '
     'como proteção contra vulnerabilidade?" Escorpianos frequentemente controlam o ambiente '
     'como forma de evitar ser surpreendidos pela dor. Identificar isso não elimina o padrão '
     'imediatamente, mas começa a criar espaço entre o gatilho e a resposta automática.'),
    ('Sagitário', 'O comprometimento de 30 dias',
     'Escolha uma prática simples, meditação, leitura, exercício,e mantenha por 30 dias '
     'consecutivos sem exceção. Sagitarianos são excelentes em começar; o desafio é a '
     'continuidade além do entusiasmo inicial. Completar um ciclo curto reconstrói confiança '
     'na própria capacidade de comprometimento.'),
    ('Capricórnio', 'O descanso agendado',
     'Coloque na agenda um momento de descanso não produtivo, sem objetivos, sem resultados. '
     'Capricornianos precisam de permissão para não produzir; colocar o descanso na agenda '
     'transforma-o em algo que pode ser "feito" corretamente. Com o tempo, o descanso começa '
     'a acontecer de forma mais natural e menos culpada.'),
    ('Aquário', 'A conversa sem teoria',
     'Uma vez por semana, tenha uma conversa com alguém próximo onde o único objetivo seja '
     'ouvir, sem analisar, sem oferecer perspectivas, sem resolver. Aquarianos frequentemente '
     'intelectualizam o que deveria simplesmente ser presença. Essa prática desenvolve a '
     'capacidade de estar com o outro sem precisar fazer nada com o que escuta.'),
    ('Peixes', 'O limite do dia',
     'Pratique dizer não a um pedido por semana, apenas um, para começar. Piscianos '
     'frequentemente dizem sim quando querem dizer não por medo de decepcionar. Cada "não" '
     'intencional reconstrói a percepção de que os próprios limites são legítimos e que '
     'dizê-los não destrói o relacionamento.'),
]

# ══════════════════════════════════════════════════════
#  CAPÍTULO 18: COMO USAR ESTE GUIA AO LONGO DA VIDA
# ══════════════════════════════════════════════════════

CAP18_INTRO = (
    'Este guia foi escrito para ser lido mais de uma vez. Não porque o conteúdo mude, '
    'mas porque você muda. O que uma pessoa de 22 anos lê sobre Escorpião é diferente do '
    'que a mesma pessoa lê aos 35, depois de ter vivido relacionamentos, perdas e '
    'transformações que o texto não podia antecipar, mas que o mapa astral já descrevia.'
)

CAP18_COMO = [
    ('Como ponto de partida',
     'Se você chegou até aqui pela primeira vez, o mais útil agora é identificar dois ou '
     'três pontos que ressoaram com clareza, não os que você gostaria que fossem verdadeiros, '
     'mas os que reconheceu mesmo que desconfortáveis. Esses são os pontos de entrada '
     'para um autoconhecimento mais profundo.'),
    ('Como ferramenta de relacionamento',
     'Quando surgir um conflito com alguém próximo, volte ao capítulo do signo dessa pessoa '
     'antes de reagir. Não para desculpar comportamentos prejudiciais, mas para compreender '
     'o que pode estar por baixo deles. Compreensão não é concordância, é uma ferramenta '
     'para escolher respostas mais eficazes e menos reativas.'),
    ('Como espelho em momentos de crise',
     'Em períodos de dificuldade, um término, uma perda, uma transição,volte ao capítulo '
     'do seu próprio signo e leia a seção sobre sombra e bloqueios. Momentos de crise '
     'frequentemente ativam exatamente os padrões menos integrados. Nomeá-los não resolve '
     'a crise, mas tira parte do poder automático que eles têm sobre você.'),
    ('Como recurso evolutivo',
     'Uma vez por ano, releia o capítulo completo do seu signo e dos signos das pessoas '
     'mais importantes da sua vida. Note o que mudou na sua leitura. O que antes parecia '
     'uma crítica pode agora parecer uma descrição. O que antes parecia irrelevante pode '
     'agora ser o ponto central. Você é o mesmo mapa lido por uma pessoa diferente, '
     'e isso, por si só, é autoconhecimento.'),
]

CAP18_FINAL = (
    'A astrologia não responde perguntas sobre o que vai acontecer. Ela responde perguntas '
    'sobre quem você é e por que você age como age. Essas são as perguntas que realmente '
    'importam, porque são as únicas cujas respostas você pode usar para mudar algo.'
)

CAP18_FINAL2 = (
    'Use este guia com honestidade. Não o use para confirmar o que você já acredita sobre '
    'si mesmo ou sobre os outros. Use-o para ver o que ainda não viu. Para nomear o que '
    'sentiu mas não sabia como dizer. Para compreender por que aquela pessoa age daquele '
    'jeito que parecia inexplicável. Para perceber, finalmente, que o que parecia defeito '
    'pode ser força que ainda não encontrou a forma certa de se expressar.'
)

CAP18_ENCERRAMENTO = (
    '"Conhece a ti mesmo." Essa frase, gravada no templo de Delfos há mais de 2.500 anos, '
    'continua sendo o projeto mais ambicioso que qualquer ser humano pode empreender. '
    'Este guia é apenas um mapa. O território é você.'
)


def build():
    out = (r'c:\Users\Heitor Melo\Desktop\Grana no Digital\Astrologia'
           r'\O_Guia_Emocional_dos_Signos_PARTE5.pdf')
    doc = SimpleDocTemplate(
        out, pagesize=A4,
        leftMargin=LEFT_MARGIN, rightMargin=LEFT_MARGIN,
        topMargin=BOTTOM_MARGIN, bottomMargin=BOTTOM_MARGIN,
    )
    S = make_styles()
    story = []

    # ── CAPA DA PARTE 5 ───────────────────────────────────────
    story.append(DarkPage(
        'Autoconhecimento\npela Astrologia',
        'Além do signo solar · Sua sombra como força\n'
        'Práticas por signo · Como usar este guia',
        'PARTE V'
    ))
    story.append(PageBreak())

    # ── CAP 15 ───────────────────────────────────────────────
    story.append(Paragraph('CAPÍTULO 15', S['chapter_tag']))
    story.append(Paragraph('Além do Signo Solar:\nLua e Ascendente', S['chapter_title']))
    story.append(hr())
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(CAP15_INTRO, S['body']))
    story.append(KeepTogether([
        Paragraph('O Signo Solar, sua identidade central', S['section_title']),
        Paragraph(CAP15_SOL, S['body']),
    ]))
    story.append(KeepTogether([
        Paragraph('A Lua, sua vida emocional', S['section_title']),
        Paragraph(CAP15_LUA, S['body']),
        Paragraph(CAP15_LUA2, S['body']),
    ]))
    story.append(KeepTogether([
        Paragraph('O Ascendente, como o mundo te vê', S['section_title']),
        Paragraph(CAP15_ASC, S['body']),
        Paragraph(CAP15_ASC2, S['body']),
    ]))
    story.append(KeepTogether([
        Paragraph('Os outros planetas', S['section_title']),
        Paragraph(CAP15_OUTROS, S['body']),
    ]))
    story.append(Spacer(1, 0.4*cm))
    story.append(insight_box(
        'Para descobrir sua Lua e seu Ascendente, você precisa da data, hora e local exatos '
        'do nascimento. Com esses dados, um mapa astral completo revela dimensões inteiramente '
        'novas de quem você é, e por que você age como age.', S))
    story.append(PageBreak())

    # ── CAP 16 ───────────────────────────────────────────────
    story.append(Paragraph('CAPÍTULO 16', S['chapter_tag']))
    story.append(Paragraph('Transformando Sua Sombra em Força', S['chapter_title']))
    story.append(hr())
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(CAP16_INTRO, S['body']))
    story.append(Paragraph(CAP16_INTRO2, S['body']))
    story.append(Spacer(1, 0.3*cm))
    for signo, texto in SOMBRAS:
        story.append(KeepTogether([
            Paragraph(signo, S['sign_title']),
            Paragraph(texto, S['body']),
        ]))
    story.append(Spacer(1, 0.4*cm))
    story.append(insight_box(
        'Integrar a sombra não significa que os traços difíceis desaparecem. '
        'Significa que você passa a escolher quando e como expressá-los, '
        'em vez de ser controlado por eles sem perceber.', S))
    story.append(PageBreak())

    # ── CAP 17 ───────────────────────────────────────────────
    story.append(Paragraph('CAPÍTULO 17', S['chapter_tag']))
    story.append(Paragraph('Práticas de Reflexão por Signo', S['chapter_title']))
    story.append(hr())
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(CAP17_INTRO, S['body']))
    story.append(Spacer(1, 0.3*cm))
    for signo, nome_pratica, descricao in PRATICAS:
        story.append(KeepTogether([
            Paragraph(f'{signo}, {nome_pratica}', S['sign_title']),
            Paragraph(descricao, S['body']),
        ]))
    story.append(PageBreak())

    # ── CAP 18 ───────────────────────────────────────────────
    story.append(Paragraph('CAPÍTULO 18', S['chapter_tag']))
    story.append(Paragraph('Como Usar Este Guia\nao Longo da Vida', S['chapter_title']))
    story.append(hr())
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(CAP18_INTRO, S['body']))
    story.append(Spacer(1, 0.3*cm))
    for titulo, texto in CAP18_COMO:
        story.append(KeepTogether([
            Paragraph(titulo, S['section_title']),
            Paragraph(texto, S['body']),
        ]))
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph(CAP18_FINAL, S['body']))
    story.append(Paragraph(CAP18_FINAL2, S['body']))
    story.append(Spacer(1, 0.6*cm))
    story.append(insight_box(CAP18_ENCERRAMENTO, S))

    doc.build(story, onFirstPage=content_page, onLaterPages=content_page)
    print(f'[OK] PARTE 5 gerada: {out}')


build()
