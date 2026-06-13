from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, PageBreak,
                                  HRFlowable, Table, TableStyle, KeepTogether)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus.flowables import Flowable
import os

# ── Fontes ──────────────────────────────────────────────────────────────────
FONT_DIR = r'C:\Windows\Fonts'
pdfmetrics.registerFont(TTFont('Georgia',      os.path.join(FONT_DIR, 'georgia.ttf')))
pdfmetrics.registerFont(TTFont('Georgia-Bold', os.path.join(FONT_DIR, 'georgiab.ttf')))
pdfmetrics.registerFont(TTFont('Georgia-Ital', os.path.join(FONT_DIR, 'georgiai.ttf')))

# ── Paleta ───────────────────────────────────────────────────────────────────
NAVY      = colors.HexColor('#10142B')
GOLD      = colors.HexColor('#C9A96E')
CREAM     = colors.HexColor('#FAF7F0')
DARK_TEXT = colors.HexColor('#2A2540')
MID_GRAY  = colors.HexColor('#8A8598')
GREEN_C   = colors.HexColor('#4A7C5E')
ORANGE_C  = colors.HexColor('#C47A3A')
RED_C     = colors.HexColor('#B84040')

W, H = A4

# ── Página de fundo escuro ───────────────────────────────────────────────────
LEFT_MARGIN   = 2   * cm
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
        # Translate back to absolute page origin (escape the frame margins)
        c.translate(-LEFT_MARGIN, -BOTTOM_MARGIN)
        c.setFillColor(NAVY)
        c.rect(0, 0, W, H, fill=1, stroke=0)
        # Linhas horizontais ouro
        c.setStrokeColor(GOLD)
        c.setLineWidth(0.8)
        c.line(2*cm, H - 1.5*cm, W - 2*cm, H - 1.5*cm)
        c.line(2*cm, 1.5*cm,     W - 2*cm, 1.5*cm)
        # TAG
        if self.tag:
            c.setFillColor(GOLD)
            c.setFont('Georgia', 9)
            c.drawCentredString(W/2, H*0.58, self.tag)
        # TÍTULO
        c.setFillColor(GOLD)
        c.setFont('Georgia-Bold', 40)
        lines = self.title.split('\n')
        y = H*0.50 if len(lines) == 1 else H*0.54
        for ln in lines:
            c.drawCentredString(W/2, y, ln)
            y -= 50
        # SUBTÍTULO
        if self.subtitle:
            c.setFillColor(MID_GRAY)
            c.setFont('Georgia-Ital', 13)
            sub_lines = []
            for part in self.subtitle.split('\n'):
                sub_lines.extend(part.split(' · '))
            for i, ln in enumerate(sub_lines):
                c.drawCentredString(W/2, H*0.38 - i*18, ln)
        # Diamante
        c.setFillColor(GOLD)
        cx, cy = W/2, 1.8*cm
        s = 5
        p = c.beginPath()
        p.moveTo(cx, cy+s); p.lineTo(cx+s, cy)
        p.lineTo(cx, cy-s); p.lineTo(cx-s, cy)
        p.close()
        c.drawPath(p, fill=1, stroke=0)
        c.restoreState()

# ── Página de conteúdo ───────────────────────────────────────────────────────
def content_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(CREAM)
    canvas.rect(0, 0, W, H, fill=1, stroke=0)
    canvas.setStrokeColor(GOLD)
    canvas.setLineWidth(2)
    canvas.line(0, H - 0.4*cm, W, H - 0.4*cm)
    canvas.setFont('Georgia', 8)
    canvas.setFillColor(MID_GRAY)
    canvas.drawCentredString(W/2, 0.7*cm, f'O Guia Emocional dos Signos')
    canvas.drawRightString(W - 2*cm, 0.7*cm, str(doc.page))
    canvas.restoreState()

# ── Estilos ──────────────────────────────────────────────────────────────────
def make_styles():
    s = {}
    s['chapter_tag'] = ParagraphStyle('chapter_tag',
        fontName='Georgia', fontSize=8, textColor=GOLD,
        spaceAfter=4, alignment=TA_LEFT, leading=10)
    s['chapter_title'] = ParagraphStyle('chapter_title',
        fontName='Georgia-Bold', fontSize=28, textColor=DARK_TEXT,
        spaceAfter=6, alignment=TA_LEFT, leading=34)
    s['section_title'] = ParagraphStyle('section_title',
        fontName='Georgia-Bold', fontSize=16, textColor=DARK_TEXT,
        spaceBefore=18, spaceAfter=6, alignment=TA_LEFT, leading=20)
    s['pair_title'] = ParagraphStyle('pair_title',
        fontName='Georgia-Bold', fontSize=13, textColor=DARK_TEXT,
        spaceBefore=14, spaceAfter=4, alignment=TA_LEFT, leading=16)
    s['body'] = ParagraphStyle('body',
        fontName='Georgia', fontSize=10.5, textColor=DARK_TEXT,
        spaceAfter=8, alignment=TA_JUSTIFY, leading=16)
    s['quote'] = ParagraphStyle('quote',
        fontName='Georgia-Ital', fontSize=10.5, textColor=DARK_TEXT,
        spaceAfter=8, alignment=TA_CENTER, leading=16,
        leftIndent=40, rightIndent=40)
    s['label'] = ParagraphStyle('label',
        fontName='Georgia', fontSize=9, textColor=MID_GRAY,
        alignment=TA_LEFT, leading=12)
    s['compat_text_green']  = ParagraphStyle('compat_green',
        fontName='Georgia-Bold', fontSize=10, textColor=GREEN_C,
        alignment=TA_LEFT, leading=14, spaceBefore=2)
    s['compat_text_orange'] = ParagraphStyle('compat_orange',
        fontName='Georgia-Bold', fontSize=10, textColor=ORANGE_C,
        alignment=TA_LEFT, leading=14, spaceBefore=2)
    s['compat_text_red']    = ParagraphStyle('compat_red',
        fontName='Georgia-Bold', fontSize=10, textColor=RED_C,
        alignment=TA_LEFT, leading=14, spaceBefore=2)
    return s

def hr(color=GOLD, thickness=0.5):
    return HRFlowable(width='100%', thickness=thickness, color=color, spaceAfter=10, spaceBefore=4)

def compat_box(label, text, style_key, styles):
    tbl = Table(
        [[Paragraph(label, styles['label']), Paragraph(text, styles[style_key])]],
        colWidths=[3.2*cm, 12.5*cm]
    )
    tbl.setStyle(TableStyle([
        ('VALIGN',      (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING',(0,0), (-1,-1), 6),
        ('TOPPADDING',  (0,0), (-1,-1), 6),
        ('BOTTOMPADDING',(0,0),(-1,-1), 6),
        ('BOX',         (0,0), (-1,-1), 0.5, colors.HexColor('#DDD8C8')),
        ('BACKGROUND',  (0,0), (-1,-1), colors.HexColor('#F5F1E8')),
    ]))
    return tbl

# ══════════════════════════════════════════════════════════════════════════════
#  CONTEÚDO
# ══════════════════════════════════════════════════════════════════════════════

ELEMENTOS = {
    'Fogo + Fogo': {
        'signos': 'Áries, Leão e Sagitário entre si',
        'texto': (
            'Quando dois signos de fogo se encontram, o resultado é uma chama que pode iluminar ou consumir. '
            'Existe uma compreensão mútua imediata, ambos entendem a intensidade, o entusiasmo e a necessidade de movimento do outro. '
            'Não há julgamento sobre a impulsividade ou a paixão, porque os dois a sentem da mesma forma.\n\n'
            'O desafio é que dois fogos também competem. Ambos querem protagonismo, reconhecimento e espaço para brilhar. '
            'A relação funciona quando cada um sustenta o brilho do outro sem tentar ofuscá-lo. '
            'Quando conseguem fazer isso, criam juntos uma energia que raramente se encontra em outras combinações: '
            'uma parceria onde ambos se sentem verdadeiramente vivos.'
        )
    },
    'Fogo + Terra': {
        'signos': 'Áries, Leão ou Sagitário com Touro, Virgem ou Capricórnio',
        'texto': (
            'Fogo e terra operam em ritmos fundamentalmente diferentes, e isso é tanto o maior desafio quanto o maior potencial '
            'desta combinação. O fogo age antes de pensar; a terra pensa antes de agir. O fogo precisa de estimulação constante; '
            'a terra precisa de estabilidade. O fogo vive no entusiasmo do início; a terra vive na construção do longo prazo.\n\n'
            'Quando conseguem se equilibrar, são complementares de formas extraordinárias. A terra oferece ao fogo estrutura, '
            'persistência e um chão para aterrar os projetos que começam com tanto entusiasmo. O fogo oferece à terra inspiração, '
            'movimento e a coragem de arriscar além da zona de conforto. O maior risco é a frustração mútua: o fogo acha a terra '
            'lenta e presa, enquanto a terra acha o fogo inconsequente e impulsivo demais.'
        )
    },
    'Fogo + Ar': {
        'signos': 'Áries, Leão ou Sagitário com Gêmeos, Libra ou Aquário',
        'texto': (
            'Esta é uma das combinações mais naturalmente compatíveis do zodíaco. O ar alimenta o fogo, e é exatamente isso '
            'que acontece nesta relação. O ar oferece ao fogo ideias, estimulação intelectual e liberdade; o fogo dá ao ar '
            'direção, entusiasmo e a coragem de agir sobre o que pensa. Ambos são movidos por possibilidades e detestam estagnação.\n\n'
            'A conversa entre eles é natural, o ritmo é semelhante, e existe uma leveza na relação que os dois apreciam. '
            'O desafio está na profundidade emocional: nenhum dos dois é particularmente voltado para o processamento emocional '
            'profundo, e isso pode criar uma relação vibrante mas superficial se os dois não fizerem esforço consciente '
            'para ir além das camadas mais fáceis.'
        )
    },
    'Fogo + Água': {
        'signos': 'Áries, Leão ou Sagitário com Câncer, Escorpião ou Peixes',
        'texto': (
            'Fogo e água é uma das combinações mais intensas e paradoxais do zodíaco. Na física, a água apaga o fogo, '
            'e emocionalmente, a profundidade e a sensibilidade da água pode de fato esfriar a chama impetuosa do fogo. '
            'Mas o vapor criado quando fogo e água se encontram é uma das forças mais poderosas da natureza.\n\n'
            'O fogo é atraído pela profundidade emocional da água, por algo que não consegue completamente entender nem alcançar. '
            'A água é atraída pela coragem e a vitalidade do fogo, pela energia que a faz sentir que tudo é possível. '
            'O desafio é real: o fogo pode ferir a água sem perceber, sendo direto demais com alguém que processa tudo '
            'profundamente. A água pode sufocar o fogo com demandas emocionais que ele não sabe como atender. '
            'Mas quando funciona, é uma relação de crescimento genuíno para os dois.'
        )
    },
    'Terra + Terra': {
        'signos': 'Touro, Virgem e Capricórnio entre si',
        'texto': (
            'Duas pessoas de terra constroem juntas de uma forma que poucas outras combinações alcançam. Existe uma '
            'compreensão fundamental de valores: segurança, consistência, lealdade e construção de longo prazo. '
            'Ambos entendem que amor se demonstra em ações, não apenas em palavras, e ambos apreciam isso no outro.\n\n'
            'O desafio desta combinação é a rigidez. Dois signos de terra podem criar uma relação sólida demais para '
            'se mover, resistindo a mudanças necessárias, prendendo-se em padrões por teimosia e perdendo a leveza '
            'e a espontaneidade que toda relação precisa. Também podem se tornar excessivamente materialistas, '
            'confundindo a construção de segurança com o significado da relação em si.'
        )
    },
    'Terra + Ar': {
        'signos': 'Touro, Virgem ou Capricórnio com Gêmeos, Libra ou Aquário',
        'texto': (
            'Terra e ar vivem em mundos muito diferentes: a terra existe no concreto, no físico, no que pode ser tocado '
            'e construído; o ar existe nas ideias, nas possibilidades, no que pode ser pensado e comunicado. '
            'Para uns, essa diferença é complementar; para outros, é uma fonte constante de mal-entendidos.\n\n'
            'A terra acha o ar inconsistente, abstrato demais e difícil de confiar no longo prazo. O ar acha a terra '
            'lenta, presa demais no que é concreto e sem imaginação para o que poderia ser. Mas quando conseguem '
            'se entender, o ar traz à terra a capacidade de pensar além do imediato, enquanto a terra traz ao ar '
            'a disciplina e a persistência para transformar ideias em realidade.'
        )
    },
    'Terra + Água': {
        'signos': 'Touro, Virgem ou Capricórnio com Câncer, Escorpião ou Peixes',
        'texto': (
            'Terra e água têm uma compatibilidade natural profunda. A água nutre a terra; a terra dá forma à água. '
            'Esta é uma das combinações mais férteis do zodíaco quando se trata de construir algo duradouro. '
            'A terra oferece à água a estabilidade e o chão que ela tanto precisa para não se perder; '
            'a água oferece à terra a profundidade emocional e a intuição que ela raramente acessa sozinha.\n\n'
            'Ambos valorizam segurança, lealdade e vínculos profundos. Ambos preferem relações de longo prazo a '
            'aventuras passageiras. O risco desta combinação é o estancamento, os dois podem se tornar tão '
            'focados em proteger o que construíram que param de crescer, individual e coletivamente.'
        )
    },
    'Ar + Ar': {
        'signos': 'Gêmeos, Libra e Aquário entre si',
        'texto': (
            'Dois signos de ar criam uma das relações mais estimulantes intelectualmente do zodíaco. '
            'A conversa nunca acaba, as ideias se multiplicam, a liberdade é mutuamente respeitada. '
            'Não há julgamento sobre a necessidade de espaço, sobre a mudança de ideia, sobre a pluralidade de interesses, '
            'porque ambos entendem e precisam das mesmas coisas.\n\n'
            'O desafio desta combinação é exatamente essa leveza que a torna tão agradável. Dois ares podem criar '
            'uma relação rica em ideias mas pobre em profundidade emocional. Podem discutir tudo intelectualmente '
            'e sentir pouco de verdade. A intimidade real, que exige vulnerabilidade e enraizamento,pode ser '
            'perpetuamente adiada em favor de mais uma conversa estimulante.'
        )
    },
    'Ar + Água': {
        'signos': 'Gêmeos, Libra ou Aquário com Câncer, Escorpião ou Peixes',
        'texto': (
            'Ar e água são opostos em sua forma de processar o mundo: o ar vive na mente, na análise, no racional; '
            'a água vive nas emoções, na intuição, no sentido. Essa diferença pode criar uma atração poderosa, '
            'cada um fascinado pelo que o outro representa, ou uma distância que parece intransponível.\n\n'
            'A água sente que o ar não consegue realmente estar presente emocionalmente, que intelectualiza o '
            'que deveria apenas sentir. O ar sente que a água é intensa demais, que as demandas emocionais são '
            'sufocantes. Mas quando conseguem se encontrar no meio-termo, quando o ar aprende a sentir antes de '
            'analisar, e a água aprende a articular o que sente, esta combinação produz algumas das relações '
            'mais completas do zodíaco.'
        )
    },
    'Água + Água': {
        'signos': 'Câncer, Escorpião e Peixes entre si',
        'texto': (
            'Duas águas se entendem em um nível que poucas outras combinações alcançam. Existe uma empatia mútua '
            'imediata, uma capacidade de sentir o que o outro está processando sem precisar de palavras, '
            'uma profundidade emocional compartilhada que cria vínculos extraordinariamente íntimos.\n\n'
            'O desafio desta combinação é que dois signos de água podem se afogar juntos. Sem a estrutura que '
            'os elementos terra ou ar trazem, a relação pode se tornar um vórtice emocional onde os dois '
            'amplificam os medos, as inseguranças e os padrões de cada um. A criação de fronteiras saudáveis, '
            'saber onde um termina e o outro começa, é o maior trabalho desta parceria. '
            'Quando conseguem, criam uma das conexões mais profundas e nutritivas do zodíaco.'
        )
    },
}

MELHORES = [
    ('Leão + Sagitário', 'Fogo + Fogo · Fixo + Mutável',
     'Esta é uma das combinações mais vibrantes e apaixonantes do zodíaco. Leão e Sagitário se alimentam '
     'mutuamente com energia, entusiasmo e uma capacidade compartilhada de viver com intensidade. '
     'Sagitário adora a grandiosidade de Leão; Leão se sente verdadeiramente admirado pelo entusiasmo genuíno '
     'de Sagitário. Ambos adoram aventuras, novas experiências e uma vida maior do que a média. '
     'A lealdade de Leão e a honestidade de Sagitário criam uma base de confiança sólida. '
     'O risco: o ego de Leão pode se chocar com a franqueza brutal de Sagitário, mas quando amadurecem, '
     'esse choque se torna crescimento.'),
    ('Touro + Virgem', 'Terra + Terra · Fixo + Mutável',
     'Touro e Virgem constroem juntos com uma naturalidade que parece predestinada. Ambos valorizam '
     'segurança, consistência e amor demonstrado em ações concretas. Nenhum dos dois precisa de drama '
     'ou de gestos grandiosos, os dois reconhecem amor em coisas pequenas e significativas. '
     'Touro oferece a Virgem a estabilidade que ela tanto precisa para relaxar sua mente analítica; '
     'Virgem oferece a Touro atenção aos detalhes e cuidado prático que Touro profundamente aprecia. '
     'Juntos, criam um lar onde tudo funciona, e onde ambos se sentem seguros para ser exatamente quem são.'),
    ('Câncer + Escorpião', 'Água + Água · Cardinal + Fixo',
     'Câncer e Escorpião compartilham uma profundidade emocional que poucos outros signos conseguem sustentar. '
     'Ambos sentem profundamente, ambos valorizam lealdade acima de tudo, ambos entendem que vulnerabilidade real '
     'exige um espaço seguro que precisam criar juntos. Câncer oferece ao Escorpião o cuidado genuíno '
     'e o lar emocional que ele raramente encontra; Escorpião oferece a Câncer a intensidade e o compromisso '
     'total que ele tanto anseia. Quando a confiança está estabelecida, esta relação tem uma profundidade '
     'que os dois sentem como único e irreplicável.'),
    ('Gêmeos + Aquário', 'Ar + Ar · Mutável + Fixo',
     'Gêmeos e Aquário criam uma parceria intelectualmente extraordinária. Ambos vivem nas ideias, '
     'ambos precisam de liberdade, ambos se entediam facilmente com o convencional. '
     'Aquário oferece a Gêmeos uma visão mais ampla e uma profundidade de pensamento que mantém o interesse vivo; '
     'Gêmeos oferece a Aquário a leveza e a adaptabilidade que equilibra a fixidez aquariana. '
     'A amizade como base desta relação é genuína e duradoura, o que, para os dois, é a fundação '
     'mais sólida que existe. Mesmo quando o romance esfria, a amizade permanece.'),
    ('Áries + Sagitário', 'Fogo + Fogo · Cardinal + Mutável',
     'Áries e Sagitário se encontram em uma frequência de pura ação e entusiasmo. Áries aprecia a honestidade '
     'direta de Sagitário e a liberdade que ele oferece; Sagitário admira a coragem e a iniciativa de Áries. '
     'Ambos são aventureiros, ambos detestam estagnação, ambos precisam de movimento para se sentir vivos. '
     'A relação raramente para: há sempre um próximo projeto, uma próxima viagem, um próximo desafio. '
     'O risco é que a intensidade do início pode ser difícil de sustentar, mas quando ambos crescem '
     'o suficiente para valorizar a constância, esta combinação se torna imbatível.'),
    ('Touro + Capricórnio', 'Terra + Terra · Fixo + Cardinal',
     'Touro e Capricórnio são dois construtores que se entendem profundamente. Ambos valorizam segurança '
     'material e emocional, ambos demonstram amor através de atos concretos, ambos pensam no longo prazo. '
     'Capricórnio encontra em Touro a estabilidade afetiva que raramente se permite buscar; '
     'Touro encontra em Capricórnio a ambição e a estrutura que admira. '
     'Esta é uma das combinações mais maduras do zodíaco, não é a mais apaixonante, mas é uma das '
     'que mais frequentemente constrói algo verdadeiramente sólido ao longo do tempo.'),
    ('Libra + Aquário', 'Ar + Ar · Cardinal + Fixo',
     'Libra e Aquário criam uma parceria de ideias, beleza e compromisso com algo maior que os dois. '
     'Libra traz elegância, cuidado com o relacionamento e a busca por harmonia; '
     'Aquário traz originalidade, visão de futuro e recusa em seguir o convencional. '
     'Ambos valorizam a liberdade dentro do relacionamento e entendem que amor não precisa ser '
     'aprisionamento. A admiração mútua é real: Libra vê em Aquário a originalidade que fascina; '
     'Aquário vê em Libra o equilíbrio que admira. Juntos, criam uma relação que inspira os dois.'),
    ('Câncer + Peixes', 'Água + Água · Cardinal + Mutável',
     'Câncer e Peixes se encontram em um nível emocional que parece mágico para os dois. '
     'Ambos sentem profundamente, ambos cuidam do outro de formas que o outro sequer precisou pedir, '
     'ambos criam juntos um mundo interior rico onde a realidade pragmática importa menos que a conexão. '
     'Câncer oferece a Peixes estrutura e cuidado prático; Peixes oferece a Câncer profundidade espiritual '
     'e criatividade. O risco é que os dois podem se proteger mutuamente da realidade ao invés de '
     'enfrentá-la juntos, mas quando equilibrados, criam uma das relações mais nutritivas do zodíaco.'),
]

DESAFIADORAS = [
    ('Áries + Câncer', 'Fogo + Água · Cardinal + Cardinal',
     'Áries e Câncer têm intenções parecidas, ambos são cardinais, ambos iniciam,mas expressam tudo '
     'de formas radicalmente diferentes. Áries é direto, rápido e frequentemente insensível sem perceber; '
     'Câncer é profundamente sensível, guarda tudo que sente e processa com lentidão. '
     'Áries pode ferir Câncer com palavras ditas sem cuidado; Câncer pode confundir Áries com '
     'comportamentos indiretos que Áries interpreta como manipulação. Para funcionar, Áries precisa '
     'aprender cuidado emocional; Câncer precisa aprender comunicação direta.'),
    ('Touro + Aquário', 'Terra + Ar · Fixo + Fixo',
     'Touro e Aquário são dois signos fixos com visões de mundo quase opostas. Touro precisa de '
     'previsibilidade, rotina e segurança; Aquário precisa de novidade, originalidade e ruptura com o '
     'convencional. Touro interpreta a imprevisibilidade de Aquário como falta de comprometimento; '
     'Aquário sente a necessidade de estabilidade de Touro como aprisionamento. Ambos são teimosos '
     'e resistem a ceder. Para funcionar, precisam respeitar genuinamente as diferenças do outro, '
     'o que exige maturidade considerável dos dois lados.'),
    ('Gêmeos + Escorpião', 'Ar + Água · Mutável + Fixo',
     'Gêmeos e Escorpião vivem em frequências emocionais completamente diferentes. Gêmeos é leve, '
     'adaptável e move-se rapidamente de uma coisa para a próxima; Escorpião é intenso, profundo e '
     'se fixa no que escolhe com uma totalidade que Gêmeos raramente experimenta. '
     'Escorpião sente que Gêmeos nunca está realmente presente; Gêmeos sente que Escorpião é '
     'possessivo e emocionalmente sufocante. A atração existe, o mistério de Escorpião fascina '
     'Gêmeos, e a versatilidade de Gêmeos intriga Escorpião, mas sustentar isso no longo prazo '
     'é um trabalho considerável.'),
    ('Leão + Escorpião', 'Fogo + Água · Fixo + Fixo',
     'Dois signos fixos com egos igualmente fortes. Leão precisa de admiração e protagonismo; '
     'Escorpião precisa de controle e profundidade. Nenhum dos dois cede facilmente. '
     'A atração é intensa: Leão é fascinado pelo mistério de Escorpião; Escorpião é atraído '
     'pelo brilho de Leão, mas a relação pode se tornar uma batalha de poder onde nenhum dos '
     'dois quer perder. Escorpião pode machucar o orgulho de Leão com sua capacidade de '
     'encontrar vulnerabilidades; Leão pode ignorar as profundezas emocionais de Escorpião. '
     'Quando ambos amadurecem, podem criar uma das relações mais intensas e transformadoras do zodíaco.'),
    ('Virgem + Sagitário', 'Terra + Fogo · Mutável + Mutável',
     'Virgem e Sagitário são ambos mutáveis, adaptáveis por natureza,mas adaptam-se de formas '
     'completamente diferentes. Virgem quer o detalhe, a precisão, o aperfeiçoamento constante; '
     'Sagitário quer o panorama, a expansão, o significado maior. Virgem acha Sagitário irresponsável '
     'e superficial; Sagitário acha Virgem excessivamente crítica e presa em detalhes que não importam. '
     'A comunicação é o maior desafio: Virgem escolhe as palavras com cuidado; Sagitário diz o que '
     'pensa sem filtro. Para funcionar, precisam aprender a valorizar a perspectiva oposta.'),
    ('Câncer + Aquário', 'Água + Ar · Cardinal + Fixo',
     'Câncer e Aquário têm necessidades emocionais quase opostas. Câncer precisa de proximidade, '
     'cuidado constante e segurança afetiva; Aquário precisa de distância, liberdade e '
     'relacionamentos que não sufoquem a individualidade. Câncer interpreta o desapego de Aquário '
     'como rejeição; Aquário interpreta a necessidade de Câncer como dependência emocional. '
     'A relação pode funcionar quando ambos entendem que as diferenças não são falhas, mas '
     'precisam de trabalho consciente considerável dos dois lados para isso.'),
    ('Capricórnio + Áries', 'Terra + Fogo · Cardinal + Cardinal',
     'Dois signos cardinais com formas completamente diferentes de iniciar. Capricórnio pensa, '
     'planeja e constrói devagar; Áries age antes de pensar e precisa de resultado imediato. '
     'Capricórnio acha Áries impulsivo e imaturamente impaciente; Áries acha Capricórnio lento, '
     'frio e controlador. A atração existe: Áries admira a competência de Capricórnio; '
     'Capricórnio secretamente aprecia a energia de Áries, mas construir algo juntos '
     'exige que os dois aprendam a respeitar o ritmo do outro.'),
    ('Peixes + Gêmeos', 'Água + Ar · Mutável + Mutável',
     'Peixes e Gêmeos são ambos mutáveis, ambos adaptáveis, e por isso a relação pode ter uma '
     'facilidade inicial que logo revela suas contradições. Peixes vive nas emoções e na intuição; '
     'Gêmeos vive na mente e na lógica. Peixes quer profundidade e conexão de alma; '
     'Gêmeos quer estimulação intelectual e liberdade. Peixes pode se sentir emocionalmente invisível '
     'com Gêmeos; Gêmeos pode se sentir emocionalmente sobrecarregado com Peixes. '
     'Para funcionar, Gêmeos precisa aprender a sentir; Peixes precisa aprender a articular.'),
]

TODAS = [
    # Áries com todos
    ('Áries + Touro', 'Fogo + Terra · Cardinal + Fixo',
     'Áries quer movimento imediato; Touro quer construção segura. A atração é real, a energia de Áries '
     'fascina Touro, e a solidez de Touro âncora Áries. O desafio é o ritmo: Áries se frustra com a '
     'lentidão de Touro, e Touro se cansa da impulsividade de Áries. Funciona quando ambos reconhecem '
     'que o ritmo do outro é uma força, não uma fraqueza.'),
    ('Áries + Gêmeos', 'Fogo + Ar · Cardinal + Mutável',
     'Uma das combinações mais energéticas e estimulantes. Gêmeos alimenta o fogo de Áries com ideias '
     'e conversas que nunca acabam; Áries dá a Gêmeos direção e a coragem de agir. Ambos precisam de '
     'novidade e movimento. O risco é que a profundidade emocional pode ser negligenciada quando os dois '
     'estão distraídos pela emoção do presente.'),
    ('Áries + Câncer', 'Fogo + Água · Cardinal + Cardinal',
     'Dois cardinais que iniciam de formas opostas. Áries age sem filtro; Câncer sente tudo profundamente '
     'e precisa de cuidado. Áries pode ferir Câncer sem perceber; Câncer pode confundir Áries com '
     'comportamentos indiretos. Exige paciência e aprendizado mútuo: Áries aprende cuidado emocional; '
     'Câncer aprende comunicação direta.'),
    ('Áries + Leão', 'Fogo + Fogo · Cardinal + Fixo',
     'Paixão, energia e entusiasmo em abundância. Ambos adoram a intensidade do outro. O desafio é '
     'o protagonismo: dois signos que querem brilhar podem competir ao invés de se complementar. '
     'Quando cada um sustenta o brilho do outro sem tentar ofuscá-lo, criam uma das relações '
     'mais vibrantes e apaixonantes do zodíaco.'),
    ('Áries + Virgem', 'Fogo + Terra · Cardinal + Mutável',
     'Áries age por impulso; Virgem age por análise. Esta diferença cria tensão e complementaridade ao '
     'mesmo tempo. Virgem pode ajudar Áries a refinar a execução de seus projetos; Áries pode ajudar '
     'Virgem a parar de analisar e simplesmente começar. A crítica de Virgem, porém, pode ferir '
     'o ego de Áries, e a impulsividade de Áries pode irritar a necessidade de ordem de Virgem.'),
    ('Áries + Libra', 'Fogo + Ar · Cardinal + Cardinal',
     'Opostos do zodíaco que se completam de formas poderosas. Áries age; Libra considera. Áries é direto; '
     'Libra é diplomático. A atração entre os dois é quase inevitável, cada um representa o que o '
     'outro precisa aprender. O desafio é que a impulsividade de Áries e a indecisão de Libra podem '
     'criar uma dança frustrante para os dois.'),
    ('Áries + Escorpião', 'Fogo + Água · Cardinal + Fixo',
     'Uma combinação de intensidade raramente igualada. Ambos têm Marte como regente (Escorpião '
     'compartilha Plutão), o que cria uma atração magnética e uma capacidade igual de conflito explosivo. '
     'Áries é aberto e direto; Escorpião é fechado e estratégico. A relação pode ser profundamente '
     'transformadora para os dois, se ambos aprenderem a não usar a intensidade como arma.'),
    ('Áries + Sagitário', 'Fogo + Fogo · Cardinal + Mutável',
     'Uma das combinações de fogo mais compatíveis. A honestidade de Sagitário e a coragem de Áries '
     'criam uma relação sem jogos, sem meias-palavras. Ambos adoram aventura e detestam estagnação. '
     'O risco é que a impulsividade combinada dos dois pode gerar decisões que ambos lamentam, '
     'mas raramente guardam rancor, porque ambos seguem em frente com a mesma rapidez.'),
    ('Áries + Capricórnio', 'Fogo + Terra · Cardinal + Cardinal',
     'Dois cardinais com abordagens opostas. Áries quer resultados imediatos; Capricórnio pensa no '
     'longo prazo. A ambição une os dois, mas o ritmo os divide. Áries vê Capricórnio como lento '
     'e controlador; Capricórnio vê Áries como impulsivo e imaturo. Quando respeitam os diferentes '
     'ritmos, podem construir coisas notáveis juntos.'),
    ('Áries + Aquário', 'Fogo + Ar · Cardinal + Fixo',
     'Aquário alimenta o fogo de Áries com originalidade e visão. Áries aprecia a liberdade que Aquário '
     'oferece; Aquário aprecia a ação direta de Áries. Ambos precisam de independência e detestam '
     'relacionamentos sufocantes. O desafio é o comprometimento emocional: nem Áries nem Aquário '
     'são os mais fáceis de alcançar em profundidade.'),
    ('Áries + Peixes', 'Fogo + Água · Cardinal + Mutável',
     'Áries e Peixes se atraem pela diferença que representa um mistério mútuo. Áries é atraído pela '
     'profundidade e sensibilidade de Peixes; Peixes é atraído pela coragem e vitalidade de Áries. '
     'O desafio é real: Áries pode ser diretamente cruel sem perceber, ferindo a profundidade '
     'emocional de Peixes. Peixes pode confundir Áries com comportamentos indiretos. '
     'Precisam aprender idiomas emocionais completamente diferentes.'),
    # Touro com os restantes
    ('Touro + Gêmeos', 'Terra + Ar · Fixo + Mutável',
     'Touro quer estabilidade e previsibilidade; Gêmeos quer variedade e movimento constante. '
     'Touro acha Gêmeos inconsistente e difícil de confiar; Gêmeos acha Touro previsível demais e sem '
     'estímulo intelectual suficiente. A atração existe, mas exige trabalho considerável. '
     'Touro pode oferecer a Gêmeos uma base sólida; Gêmeos pode oferecer a Touro leveza e novidade.'),
    ('Touro + Câncer', 'Terra + Água · Fixo + Cardinal',
     'Uma das combinações mais nutritivas do zodíaco. Touro oferece a Câncer a estabilidade material '
     'e emocional que ele tanto precisa; Câncer oferece a Touro o cuidado profundo e a intimidade '
     'afetiva que Touro raramente admite precisar. Ambos valorizam o lar, a segurança e o amor '
     'demonstrado em ações. Juntos, constroem um ambiente de conforto genuíno.'),
    ('Touro + Leão', 'Terra + Fogo · Fixo + Fixo',
     'Dois signos fixos que podem criar uma relação sólida ou um choque de vontades. Touro precisa de '
     'estabilidade e raramente demonstra admiração verbal; Leão precisa de reconhecimento constante. '
     'Touro pode sentir as exigências de atenção de Leão como excessivas; Leão pode sentir a frieza '
     'relativa de Touro como falta de amor. Quando se entendem, a lealdade de ambos cria algo duradouro.'),
    ('Touro + Virgem', 'Terra + Terra · Fixo + Mutável',
     'Uma das combinações mais naturalmente compatíveis. Touro e Virgem compartilham valores fundamentais '
     'e se entendem sem precisar de grandes explicações. Touro oferece estabilidade; Virgem oferece '
     'atenção e cuidado prático. Ambos demonstram amor em ações, não em palavras. '
     'O risco é a rigidez combinada dos dois, precisam de esforço consciente para não se tornarem '
     'uma parceria funcional mas emocionalmente fria.'),
    ('Touro + Libra', 'Terra + Ar · Fixo + Cardinal',
     'Ambos regidos por Vênus, o que cria uma apreciação compartilhada pela beleza, pelo conforto e '
     'pelo prazer. Mas Touro expressa isso de forma concreta e sensorial; Libra, de forma social e '
     'intelectual. Touro pode achar Libra superficial e indecisa; Libra pode achar Touro '
     'excessivamente possessivo e resistente a mudanças. A harmonia é possível quando cada um '
     'aprecia o modo de amar do outro.'),
    ('Touro + Escorpião', 'Terra + Água · Fixo + Fixo',
     'Opostos do zodíaco. A intensidade de Escorpião fascina Touro; a solidez de Touro ancora '
     'Escorpião. Ambos são leais de formas absolutas, e ambos são igualmente capazes de rancor '
     'prolongado quando se sentem traídos. Quando a confiança está estabelecida, esta relação tem '
     'uma profundidade difícil de encontrar em outras combinações. A teimosia compartilhada é '
     'o maior obstáculo.'),
    ('Touro + Sagitário', 'Terra + Fogo · Fixo + Mutável',
     'Touro quer segurança e rotina; Sagitário quer liberdade e expansão. A diferença de valores '
     'é real: Touro prioriza o construído, o sólido, o confiável; Sagitário prioriza a aventura, '
     'o crescimento, o novo horizonte. Para funcionar, Touro precisa dar espaço genuíno; '
     'Sagitário precisa oferecer consistência suficiente para Touro confiar.'),
    ('Touro + Capricórnio', 'Terra + Terra · Fixo + Cardinal',
     'Uma das combinações mais maduras e sólidas do zodíaco. Touro e Capricórnio entendem que '
     'amor é construção, não apenas sentimento. Ambos são leais, trabalham duro e constroem para '
     'o longo prazo. A relação pode se tornar excessivamente focada no funcional, perdendo a '
     'espontaneidade e o romance, mas a fundação que criam raramente se parte.'),
    ('Touro + Aquário', 'Terra + Ar · Fixo + Fixo',
     'Dois fixos com visões de mundo opostas. Touro valoriza tradição, segurança e o que já '
     'foi provado; Aquário valoriza inovação, liberdade e ruptura com o convencional. '
     'A teimosia combinada dos dois pode fazer a relação parecer uma negociação constante. '
     'Quando funcionam, o equilíbrio entre estabilidade (Touro) e evolução (Aquário) pode '
     'ser transformador para os dois.'),
    ('Touro + Peixes', 'Terra + Água · Fixo + Mutável',
     'Uma combinação naturalmente nutritiva. Touro oferece a Peixes a âncora e a estabilidade '
     'que ele precisa para não se perder; Peixes oferece a Touro sensibilidade emocional e '
     'profundidade que Touro raramente acessa sozinho. Ambos valorizam o conforto e a intimidade. '
     'O risco é que Touro pode se frustrar com a imprecisão de Peixes, e Peixes pode sentir '
     'a inflexibilidade de Touro como aprisionamento.'),
    # Gêmeos com os restantes
    ('Gêmeos + Câncer', 'Ar + Água · Mutável + Cardinal',
     'Gêmeos vive na mente; Câncer vive nas emoções. A atração existe, a vivacidade de Gêmeos '
     'anima Câncer; a profundidade emocional de Câncer fascina Gêmeos. O desafio: Gêmeos pode '
     'parecer emocionalmente ausente para Câncer; Câncer pode parecer excessivamente demandante '
     'para Gêmeos. Precisam aprender idiomas completamente diferentes para que a relação funcione.'),
    ('Gêmeos + Leão', 'Ar + Fogo · Mutável + Fixo',
     'Uma combinação de leveza e brilho. Gêmeos alimenta o ego de Leão com inteligência e humor; '
     'Leão dá a Gêmeos o calor e o entusiasmo que deixam a vida mais vibrante. Ambos são sociais, '
     'ambos adoram se divertir, ambos têm energia para novas experiências. O risco é a '
     'superficialidade: os dois podem se contentar com a diversão sem nunca aprofundar o que '
     'os conecta de verdade.'),
    ('Gêmeos + Virgem', 'Ar + Terra · Mutável + Mutável',
     'Ambos regidos por Mercúrio, o que cria uma linguagem intelectual compartilhada. Mas usam '
     'essa mente de formas diferentes: Gêmeos para explorar e se divertir; Virgem para analisar '
     'e aperfeiçoar. Gêmeos acha Virgem excessivamente crítica e limitante; Virgem acha Gêmeos '
     'inconsistente e superficial. Quando se entendem, criam uma das parcerias mais intelectualmente '
     'ricas do zodíaco.'),
    ('Gêmeos + Libra', 'Ar + Ar · Mutável + Cardinal',
     'Dois signos de ar que se entendem naturalmente. A conversa flui, a liberdade é respeitada '
     'mutuamente, e a estética compartilhada cria uma harmonia imediata. Ambos valorizam conexão '
     'intelectual e relacionamentos que não sufoquem. O risco desta combinação é que a leveza de '
     'ambos pode evitar a profundidade emocional necessária para uma relação duradoura.'),
    ('Gêmeos + Escorpião', 'Ar + Água · Mutável + Fixo',
     'Uma combinação de fascínio mútuo e frustração mútua. O mistério de Escorpião intriga '
     'Gêmeos; a versatilidade de Gêmeos intriga Escorpião. Mas a leveza de Gêmeos confronta '
     'a intensidade de Escorpião de formas difíceis. Escorpião quer profundidade e totalidade; '
     'Gêmeos quer variedade e leveza. Para funcionar, os dois precisam aprender a honrar '
     'a necessidade oposta do outro.'),
    ('Gêmeos + Sagitário', 'Ar + Fogo · Mutável + Mutável',
     'Opostos do zodíaco com uma atração poderosa. Ambos amam a liberdade, o aprendizado e a '
     'exploração de novas ideias. Sagitário busca o significado profundo; Gêmeos busca a '
     'variedade do conhecimento. A relação pode ser uma das mais estimulantes e aventureiras '
     'do zodíaco. O risco é que ambos são mutáveis, nenhum dos dois é particularmente '
     'comprometido com a estabilidade, o que pode fazer a relação nunca se aprofundar.'),
    ('Gêmeos + Capricórnio', 'Ar + Terra · Mutável + Cardinal',
     'Gêmeos vive no presente e nas possibilidades; Capricórnio vive no longo prazo e nas '
     'responsabilidades. A diferença de ritmo e de valores pode ser um obstáculo real. '
     'Capricórnio acha Gêmeos frivolo e pouco confiável; Gêmeos acha Capricórnio sério demais '
     'e sem senso de humor. Quando se entendem, Capricórnio traz estrutura à mente inquieta '
     'de Gêmeos; Gêmeos traz leveza à seriedade de Capricórnio.'),
    ('Gêmeos + Aquário', 'Ar + Ar · Mutável + Fixo',
     'Uma das combinações intelectualmente mais ricas do zodíaco. Ambos precisam de liberdade e '
     'estimulação mental constante. Aquário oferece a Gêmeos profundidade de visão; Gêmeos '
     'oferece a Aquário adaptabilidade e humor. A amizade é genuína e duradoura. '
     'O desafio é criar profundidade emocional além da camada intelectual que os dois '
     'dominam com facilidade.'),
    ('Gêmeos + Peixes', 'Ar + Água · Mutável + Mutável',
     'Dois mutáveis que se adaptam de formas completamente diferentes. Gêmeos processa pelo '
     'intelecto; Peixes processa pela emoção e pela intuição. A fascinação é mútua, cada um '
     'vê no outro algo que não consegue completamente entender. Mas a comunicação pode ser '
     'um desafio real: Gêmeos fala o que pensa; Peixes sente o que não consegue articular.'),
    # Câncer com os restantes
    ('Câncer + Leão', 'Água + Fogo · Cardinal + Fixo',
     'Câncer cuida; Leão brilha. Quando os dois se entendem, Câncer oferece a Leão o '
     'cuidado genuíno que ele raramente recebe; Leão oferece a Câncer a proteção e o '
     'calor que ele tanto precisa. O desafio: Câncer pode se sentir ignorado pelas '
     'demandas de atenção de Leão; Leão pode se sentir sufocado pela necessidade '
     'emocional de Câncer. O equilíbrio entre cuidar e brilhar é a chave.'),
    ('Câncer + Virgem', 'Água + Terra · Cardinal + Mutável',
     'Uma combinação de cuidado mútuo que pode criar uma das relações mais nutritivas do '
     'zodíaco. Câncer cuida emocionalmente; Virgem cuida praticamente. Ambos percebem '
     'necessidades sem precisar que o outro diga nada. O risco: a autocrítica de Virgem '
     'pode ferir a sensibilidade de Câncer; a demanda emocional de Câncer pode sobrecarregar '
     'a mente analítica de Virgem.'),
    ('Câncer + Libra', 'Água + Ar · Cardinal + Cardinal',
     'Dois cardinais com formas de iniciar completamente diferentes. Câncer inicia pelo '
     'cuidado emocional; Libra inicia pela busca de harmonia e conexão. A vontade de '
     'agradar de Libra e o cuidado profundo de Câncer podem criar muita beleza juntos. '
     'O desafio: a indecisão de Libra frustra a necessidade de segurança de Câncer; '
     'a intensidade emocional de Câncer pode sobrecarregar o equilíbrio que Libra busca.'),
    ('Câncer + Escorpião', 'Água + Água · Cardinal + Fixo',
     'Uma das combinações mais profundas e emocionalmente intensas do zodíaco. Câncer e '
     'Escorpião se entendem em um nível que poucos alcançam. A lealdade é absoluta nos dois. '
     'A intuição mútua cria uma intimidade raramente encontrada em outras combinações. '
     'O risco: os dois podem amplificar os medos e as inseguranças um do outro se não '
     'criarem ancoras individuais saudáveis.'),
    ('Câncer + Sagitário', 'Água + Fogo · Cardinal + Mutável',
     'A necessidade de lar e presença constante de Câncer confronta diretamente a '
     'necessidade de liberdade e movimento de Sagitário. Câncer quer enraizamento; '
     'Sagitário quer expansão. Para funcionar, Sagitário precisa oferecer a presença '
     'emocional que Câncer necessita; Câncer precisa dar liberdade genuína sem '
     'interpretar ausência como abandono. É um trabalho considerável para os dois.'),
    ('Câncer + Capricórnio', 'Água + Terra · Cardinal + Cardinal',
     'Opostos do zodíaco com uma complementaridade poderosa. Câncer oferece a Capricórnio '
     'o lar emocional que ele raramente se permite buscar; Capricórnio oferece a Câncer '
     'a estrutura e a estabilidade que ele precisa para se sentir seguro. '
     'O desafio é comunicar emoções: Câncer vive nelas; Capricórnio as guarda. '
     'Quando aprendem a linguagem um do outro, constroem algo muito sólido.'),
    ('Câncer + Aquário', 'Água + Ar · Cardinal + Fixo',
     'Uma das combinações mais desafiadoras do zodíaco. Câncer precisa de proximidade emocional '
     'constante; Aquário precisa de distância e independência. Câncer interpreta o desapego de '
     'Aquário como rejeição; Aquário interpreta a necessidade de Câncer como dependência. '
     'Para funcionar, precisam de um acordo consciente sobre o que cada um precisa, '
     'e de maturidade para honrá-lo sem ressentimento.'),
    ('Câncer + Peixes', 'Água + Água · Cardinal + Mutável',
     'Dois signos de água que se encontram em um nível emocional quase místico. Câncer e '
     'Peixes se cuidam, se compreendem sem palavras e criam juntos um mundo interior rico. '
     'Câncer oferece estrutura e cuidado prático; Peixes oferece profundidade criativa e '
     'espiritualidade. O risco é a falta de âncora à realidade, juntos podem se proteger '
     'do mundo ao invés de enfrentá-lo.'),
    # Leão com os restantes
    ('Leão + Virgem', 'Fogo + Terra · Fixo + Mutável',
     'Leão precisa de elogios e reconhecimento; Virgem tende a ver o que poderia ser melhorado '
     'ao invés do que está excelente. A crítica de Virgem pode ferir profundamente o orgulho '
     'de Leão; o drama de Leão pode exasperar a eficiência de Virgem. Quando se entendem, '
     'Virgem oferece a Leão a competência que ele admira; Leão oferece a Virgem o calor '
     'e o reconhecimento que raramente recebe.'),
    ('Leão + Libra', 'Fogo + Ar · Fixo + Cardinal',
     'Uma combinação de beleza, charme e sociabilidade natural. Libra adora a grandiosidade '
     'de Leão; Leão aprecia a elegância e a diplomacia de Libra. Ambos gostam de ambientes '
     'agradáveis, de relacionamentos onde o parceiro é alguém de quem se orgulham. '
     'O desafio: a indecisão de Libra pode frustrar Leão; a necessidade de protagonismo de '
     'Leão pode fazer Libra se sentir invisível.'),
    ('Leão + Escorpião', 'Fogo + Água · Fixo + Fixo',
     'Dois fixos com egos igualmente poderosos. A atração é intensa; a tensão é igualmente '
     'intensa. Leão quer admiração; Escorpião quer controle. Nenhum dos dois cede facilmente. '
     'Escorpião pode machucar o orgulho de Leão estrategicamente; Leão pode ignorar a '
     'profundidade emocional de Escorpião por considerá-la drama desnecessário. '
     'Quando amadurecem juntos, a transformação mútua é profunda.'),
    ('Leão + Sagitário', 'Fogo + Fogo · Fixo + Mutável',
     'Uma das combinações mais vibrantes e apaixonantes do zodíaco. Leão e Sagitário se '
     'alimentam mutuamente com energia e entusiasmo genuíno. A honestidade de Sagitário é '
     'algo que Leão aprecia após o impacto inicial; a grandiosidade de Leão inspira Sagitário. '
     'Quando o ego de Leão aprende a sustentar a liberdade que Sagitário precisa, '
     'esta relação se torna quase imbatível.'),
    ('Leão + Capricórnio', 'Fogo + Terra · Fixo + Cardinal',
     'A ambição une os dois, mas as motivações são diferentes. Leão quer brilhar e ser '
     'reconhecido; Capricórnio quer construir e ser respeitado. Capricórnio pode achar '
     'Leão desnecessariamente dramático; Leão pode achar Capricórnio frio e sem generosidade '
     'emocional. Quando se respeitam, a disciplina de Capricórnio e o brilho de Leão criam '
     'uma parceria poderosa.'),
    ('Leão + Aquário', 'Fogo + Ar · Fixo + Fixo',
     'Opostos do zodíaco com uma tensão criativa fascinante. Leão é individual e centrado no eu; '
     'Aquário é coletivo e centrado na humanidade. Leão quer ser único; Aquário quer ser '
     'original. A atração é real: cada um representa o que o outro precisa integrar. '
     'O ego de Leão e o desapego de Aquário criam choques frequentes, mas também '
     'crescimento significativo quando os dois se comprometem.'),
    ('Leão + Peixes', 'Fogo + Água · Fixo + Mutável',
     'Leão brilha externamente; Peixes brilha internamente. A generosidade de Leão encanta '
     'Peixes; a profundidade de Peixes fascina Leão. O desafio: Leão pode se sentir '
     'emocionalmente sobrecarregado pelas demandas de Peixes; Peixes pode se sentir '
     'emocionalmente invisível com o ego de Leão. Quando Leão aprende a cuidar da '
     'sensibilidade de Peixes, e Peixes aprende a admirar Leão sem se perder nele, '
     'a relação tem uma beleza única.'),
    # Virgem com os restantes
    ('Virgem + Libra', 'Terra + Ar · Mutável + Cardinal',
     'Virgem busca a perfeição no detalhe; Libra busca o equilíbrio no todo. Ambos têm '
     'altos padrões, mas os expressam de formas diferentes. Virgem pode achar Libra '
     'superficial e indecisa; Libra pode achar Virgem excessivamente crítica e '
     'perfeccionista. A elegância de Libra pode suavizar a rigidez de Virgem; '
     'a precisão de Virgem pode ajudar Libra a tomar decisões.'),
    ('Virgem + Escorpião', 'Terra + Água · Mutável + Fixo',
     'Uma combinação de profundidade e precisão que pode criar algo extraordinário. '
     'Escorpião aprecia a inteligência analítica de Virgem; Virgem é fascinada pela '
     'intensidade e profundidade de Escorpião. Ambos são observadores, discretos e '
     'valorizam a privacidade. O desafio: a crítica de Virgem pode ferir o orgulho '
     'de Escorpião; a intensidade emocional de Escorpião pode sobrecarregar Virgem.'),
    ('Virgem + Sagitário', 'Terra + Fogo · Mutável + Mutável',
     'Dois mutáveis com perspectivas opostas sobre o que importa. Virgem foca nos detalhes; '
     'Sagitário foca no panorama. Virgem escolhe as palavras com cuidado; Sagitário diz tudo '
     'sem filtro. A crítica de Virgem e a franqueza de Sagitário podem criar conflitos constantes. '
     'Mas quando se entendem, Sagitário expande o mundo de Virgem além dos detalhes; '
     'Virgem traz execução às grandes visões de Sagitário.'),
    ('Virgem + Capricórnio', 'Terra + Terra · Mutável + Cardinal',
     'Uma das combinações mais funcionalmente compatíveis do zodíaco. Ambos são práticos, '
     'trabalhadores e entendem o valor do esforço. Virgem oferece a Capricórnio atenção aos '
     'detalhes e cuidado meticuloso; Capricórnio oferece a Virgem visão de longo prazo e '
     'ambição estruturada. Precisam garantir que a relação não se torne apenas uma '
     'parceria funcional sem calor emocional.'),
    ('Virgem + Aquário', 'Terra + Ar · Mutável + Fixo',
     'Virgem quer precisão e ordem; Aquário quer inovação e ruptura. A mente de Virgem busca '
     'o que é comprovado e funcional; a mente de Aquário busca o que ainda não existe. '
     'Aquário pode achar Virgem excessivamente convencional; Virgem pode achar Aquário '
     'impraticável e caótico. Quando se entendem, a visão de Aquário e a execução de '
     'Virgem formam uma parceria poderosa.'),
    ('Virgem + Peixes', 'Terra + Água · Mutável + Mutável',
     'Opostos do zodíaco com uma complementaridade real. Virgem oferece a Peixes estrutura, '
     'precisão e âncora à realidade; Peixes oferece a Virgem profundidade emocional, '
     'criatividade e acesso ao que está além da análise. Virgem aprende a sentir mais; '
     'Peixes aprende a executar mais. O risco: a crítica de Virgem pode ferir Peixes; '
     'a imprecisão de Peixes pode frustrar Virgem.'),
    # Libra com os restantes
    ('Libra + Escorpião', 'Ar + Água · Cardinal + Fixo',
     'Libra busca harmonia e equilíbrio; Escorpião busca profundidade e transformação. '
     'A diplomacia de Libra e a intensidade de Escorpião criam uma tensão fascinante. '
     'Libra pode se sentir emocionalmente sobrecarregada com a intensidade de Escorpião; '
     'Escorpião pode sentir que Libra nunca é completamente autêntica, sempre ajustando '
     'a verdade para evitar conflitos. A confiança é o maior trabalho desta relação.'),
    ('Libra + Sagitário', 'Ar + Fogo · Cardinal + Mutável',
     'Uma combinação de leveza, aventura e generosidade mútua. Sagitário aprecia a '
     'elegância intelectual de Libra; Libra aprecia a honestidade e o entusiasmo de '
     'Sagitário. Ambos são sociáveis e adoram experiências novas. O desafio: '
     'a honestidade sem filtro de Sagitário pode ferir a sensibilidade social de Libra; '
     'a indecisão de Libra pode frustrar a necessidade de movimento de Sagitário.'),
    ('Libra + Capricórnio', 'Ar + Terra · Cardinal + Cardinal',
     'Dois cardinais com prioridades diferentes. Libra prioriza relacionamentos e harmonia; '
     'Capricórnio prioriza construção e responsabilidade. Libra pode achar Capricórnio '
     'frio e excessivamente focado no trabalho; Capricórnio pode achar Libra superficial '
     'e pouco prático. Quando se entendem, a elegância social de Libra e a disciplina '
     'de Capricórnio criam uma parceria admirável.'),
    ('Libra + Aquário', 'Ar + Ar · Cardinal + Fixo',
     'Uma combinação natural e estimulante. Libra e Aquário se entendem intelectualmente, '
     'respeitam a liberdade um do outro e compartilham valores de justiça e conexão. '
     'Aquário oferece a Libra originalidade e visão além do convencional; Libra oferece '
     'a Aquário elegância e capacidade de criar harmonia nas relações. '
     'O risco é a superficialidade emocional, ambos preferem o intelectual ao emocional profundo.'),
    ('Libra + Peixes', 'Ar + Água · Cardinal + Mutável',
     'Libra e Peixes compartilham uma sensibilidade estética e um desejo de harmonia que '
     'cria uma sintonia inicial bonita. Libra oferece clareza e estrutura racional; '
     'Peixes oferece profundidade emocional e criatividade. O desafio: a indecisão de '
     'Libra e a imprecisão de Peixes podem criar uma relação onde ninguém toma decisões. '
     'A comunicação clara é essencial para os dois.'),
    # Escorpião com os restantes
    ('Escorpião + Sagitário', 'Água + Fogo · Fixo + Mutável',
     'Escorpião é profundo e intenso; Sagitário é expansivo e livre. A atração existe, '
     'Escorpião é fascinado pela liberdade de Sagitário; Sagitário é fascinado pelo '
     'mistério de Escorpião. O desafio é real: a necessidade de profundidade de Escorpião '
     'confronta a necessidade de liberdade de Sagitário. Escorpião pode sentir que '
     'Sagitário nunca está totalmente presente; Sagitário pode sentir Escorpião '
     'excessivamente possessivo.'),
    ('Escorpião + Capricórnio', 'Água + Terra · Fixo + Cardinal',
     'Uma combinação de intensidade e disciplina que pode construir algo extraordinário. '
     'Escorpião oferece a Capricórnio profundidade emocional e percepção estratégica; '
     'Capricórnio oferece a Escorpião estrutura e visão de longo prazo. Ambos valorizam '
     'lealdade absoluta e trabalham com determinação. Juntos, raramente desistem do que '
     'começam, o que inclui a relação entre os dois.'),
    ('Escorpião + Aquário', 'Água + Ar · Fixo + Fixo',
     'Dois fixos com abordagens completamente diferentes para a intimidade. Escorpião quer '
     'profundidade total e fusão emocional; Aquário quer liberdade e distância como condição '
     'para permanecer. Escorpião interpreta o desapego de Aquário como indiferença; '
     'Aquário interpreta a intensidade de Escorpião como controle. Para funcionar, '
     'precisam de um contrato emocional muito claro, e maturidade para honrá-lo.'),
    ('Escorpião + Peixes', 'Água + Água · Fixo + Mutável',
     'Uma das combinações mais intuitivas e profundas do zodíaco. Escorpião e Peixes '
     'se entendem em um nível que raramente precisa de palavras. A lealdade de Escorpião '
     'dá a Peixes a segurança que ele precisa; a profundidade emocional de Peixes '
     'é uma das poucas que Escorpião genuinamente respeita. O risco: a intensidade '
     'de Escorpião pode sufocar a delicadeza de Peixes; os dois juntos podem se '
     'isolar do mundo exterior de formas pouco saudáveis.'),
    # Sagitário com os restantes
    ('Sagitário + Capricórnio', 'Fogo + Terra · Mutável + Cardinal',
     'Sagitário vive no presente e nas possibilidades futuras; Capricórnio vive na '
     'construção lenta e segura do futuro. Sagitário acha Capricórnio excessivamente '
     'sério e limitante; Capricórnio acha Sagitário irresponsável e sem comprometimento. '
     'Quando se entendem, a visão de Sagitário e a execução de Capricórnio criam uma '
     'parceria poderosa, se conseguirem tolerar os diferentes ritmos.'),
    ('Sagitário + Aquário', 'Fogo + Ar · Mutável + Fixo',
     'Uma combinação de liberdade, originalidade e entusiasmo compartilhado. Ambos '
     'precisam de espaço e detestam relacionamentos sufocantes. Sagitário alimenta '
     'o idealismo de Aquário com entusiasmo; Aquário oferece a Sagitário profundidade '
     'de visão e originalidade. A relação tem uma leveza natural que os dois apreciam. '
     'O desafio é criar raízes suficientes para que não se dissolvam na liberdade.'),
    ('Sagitário + Peixes', 'Fogo + Água · Mutável + Mutável',
     'Dois mutáveis com uma espiritualidade compartilhada: Sagitário busca o significado '
     'pela filosofia; Peixes busca pelo sentimento e pela intuição. A atração existe, '
     'mas as formas de processar o mundo são muito diferentes. Peixes pode confundir a '
     'liberdade de Sagitário com abandono; Sagitário pode se sentir sobrecarregado '
     'pela profundidade emocional de Peixes. Quando funcionam, criam uma relação '
     'de crescimento espiritual genuíno.'),
    # Capricórnio com os restantes
    ('Capricórnio + Aquário', 'Terra + Ar · Cardinal + Fixo',
     'Capricórnio e Aquário compartilham Saturno como regente (tradicional para Aquário), '
     'o que cria uma seriedade e um comprometimento que ambos reconhecem no outro. '
     'Mas Capricórnio busca estrutura e tradição; Aquário busca inovação e ruptura. '
     'Capricórnio pode achar Aquário rebelde demais; Aquário pode achar Capricórnio '
     'preso demais ao convencional. Quando se equilibram, criam algo que une '
     'estabilidade e visão de futuro.'),
    ('Capricórnio + Peixes', 'Terra + Água · Cardinal + Mutável',
     'Uma combinação de complementaridade real. Capricórnio oferece a Peixes a estrutura '
     'e a âncora à realidade que ele precisa desesperadamente; Peixes oferece a Capricórnio '
     'profundidade emocional e acesso ao que está além da lógica. Capricórnio aprende a '
     'sentir; Peixes aprende a executar. Quando funciona, cada um cobre a vulnerabilidade '
     'do outro de formas que criam uma relação extraordinariamente complementar.'),
    # Aquário com Peixes
    ('Aquário + Peixes', 'Ar + Água · Fixo + Mutável',
     'Aquário vive nas ideias e na mente; Peixes vive nas emoções e na intuição. '
     'A atração existe: Aquário é fascinado pela profundidade de Peixes; Peixes é '
     'fascinado pela originalidade de Aquário. Mas Peixes precisa de intimidade emocional '
     'que Aquário raramente oferece; Aquário precisa de liberdade que Peixes pode '
     'interpretar como abandono. Para funcionar, precisam de comunicação clara sobre '
     'o que cada um precisa, e respeito genuíno por essas diferenças.'),
]

# ══════════════════════════════════════════════════════════════════════════════
#  GERAÇÃO DO PDF
# ══════════════════════════════════════════════════════════════════════════════
def build():
    out = r'c:\Users\Heitor Melo\Desktop\Grana no Digital\Astrologia\O_Guia_Emocional_dos_Signos_PARTE3.pdf'
    doc = SimpleDocTemplate(
        out, pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=1.8*cm, bottomMargin=1.8*cm,
    )
    S = make_styles()
    story = []

    # ── CAPA DA PARTE 3 ──────────────────────────────────────────────────────
    story.append(DarkPage(
        'Os 12 Signos\nem Combinação',
        'Compatibilidade · As Melhores Combinações · As Mais Desafiadoras\nTodas as 66 Combinações do Zodíaco',
        'PARTE III'
    ))
    story.append(PageBreak())

    # ── CAP 6: COMPATIBILIDADE POR ELEMENTO ─────────────────────────────────
    story.append(Paragraph('CAPÍTULO 6', S['chapter_tag']))
    story.append(Paragraph('Compatibilidade por Elemento', S['chapter_title']))
    story.append(hr())
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(
        'Antes de entrar em cada combinação individual, é essencial entender como os quatro elementos '
        'interagem entre si. Essas dinâmicas de elemento são o pano de fundo de toda relação astrológica: '
        'elas revelam o nível de compatibilidade natural, os desafios estruturais e o potencial de crescimento '
        'de qualquer combinação. Conhecer o elemento do seu signo e o do signo de quem você ama já oferece '
        'uma visão poderosa do terreno em que a relação se desenvolve.',
        S['body']))
    story.append(Spacer(1, 0.3*cm))

    for nome, info in ELEMENTOS.items():
        story.append(KeepTogether([
            Paragraph(nome, S['section_title']),
            Paragraph(f"<i>{info['signos']}</i>", ParagraphStyle('sig', fontName='Georgia-Ital',
                fontSize=9.5, textColor=MID_GRAY, spaceAfter=6, leading=13)),
            hr(MID_GRAY, 0.3),
        ]))
        for para in info['texto'].split('\n\n'):
            story.append(Paragraph(para.strip(), S['body']))
        story.append(Spacer(1, 0.2*cm))

    story.append(PageBreak())

    # ── CAP 7: MELHORES COMBINAÇÕES ──────────────────────────────────────────
    story.append(Paragraph('CAPÍTULO 7', S['chapter_tag']))
    story.append(Paragraph('As Melhores\nCombinações do Zodíaco', S['chapter_title']))
    story.append(hr())
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(
        'Certas combinações têm uma compatibilidade que vai além do esforço, existe uma sintonia natural '
        'de valores, ritmo e linguagem emocional que faz a relação fluir com uma facilidade que outros pares '
        'raramente encontram. Isso não significa que essas combinações não têm desafios: toda relação tem. '
        'Mas o ponto de partida é significativamente mais fértil. Estas são as parcerias onde os dois '
        'tendem a crescer juntos de forma mais orgânica.',
        S['body']))
    story.append(Spacer(1, 0.3*cm))

    for titulo, subtitulo, texto in MELHORES:
        story.append(KeepTogether([
            Paragraph(titulo, S['section_title']),
            Paragraph(subtitulo, ParagraphStyle('sub2', fontName='Georgia-Ital',
                fontSize=9.5, textColor=MID_GRAY, spaceAfter=6, leading=13)),
            hr(GOLD, 0.4),
            Paragraph(texto, S['body']),
            Spacer(1, 0.15*cm),
        ]))

    story.append(PageBreak())

    # ── CAP 8: COMBINAÇÕES DESAFIADORAS ──────────────────────────────────────
    story.append(Paragraph('CAPÍTULO 8', S['chapter_tag']))
    story.append(Paragraph('As Combinações\nMais Desafiadoras', S['chapter_title']))
    story.append(hr())
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(
        'Existem combinações onde as diferenças são tão estruturais que o trabalho necessário para '
        'criar harmonia é considerável. Isso não significa que essas relações não funcionam, significa '
        'que exigem mais consciência, mais comunicação e mais disposição de ambas as partes para crescer '
        'além dos padrões mais automáticos. Frequentemente, são exatamente essas combinações mais difíceis '
        'que provocam o maior crescimento individual quando os dois decidem genuinamente se comprometer.',
        S['body']))
    story.append(Spacer(1, 0.3*cm))

    for titulo, subtitulo, texto in DESAFIADORAS:
        story.append(KeepTogether([
            Paragraph(titulo, S['section_title']),
            Paragraph(subtitulo, ParagraphStyle('sub3', fontName='Georgia-Ital',
                fontSize=9.5, textColor=MID_GRAY, spaceAfter=6, leading=13)),
            hr(colors.HexColor('#C09070'), 0.4),
            Paragraph(texto, S['body']),
            Spacer(1, 0.15*cm),
        ]))

    story.append(PageBreak())

    # ── CAP 9: TODAS AS COMBINAÇÕES ──────────────────────────────────────────
    story.append(Paragraph('CAPÍTULO 9', S['chapter_tag']))
    story.append(Paragraph('Todas as Combinações\nO que Cada Par Revela', S['chapter_title']))
    story.append(hr())
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(
        'O zodíaco tem 12 signos, o que resulta em 66 combinações únicas entre pares. '
        'Cada par revela uma dinâmica específica de linguagem emocional, valores, ritmo e potencial de '
        'crescimento. Esta seção apresenta todas as 66 combinações com uma análise direta do que '
        'acontece quando esses dois signos se encontram em uma relação íntima. '
        'Lembre-se: estas são tendências, não certezas. O mapa astral completo de cada pessoa, '
        'incluindo Lua, Ascendente e outros planetas, modifica profundamente qualquer combinação.',
        S['body']))
    story.append(Spacer(1, 0.4*cm))

    for titulo, subtitulo, texto in TODAS:
        story.append(KeepTogether([
            Paragraph(titulo, S['pair_title']),
            Paragraph(subtitulo, ParagraphStyle('sub4', fontName='Georgia-Ital',
                fontSize=9, textColor=MID_GRAY, spaceAfter=4, leading=12)),
            Paragraph(texto, S['body']),
            Spacer(1, 0.1*cm),
        ]))

    doc.build(story, onFirstPage=content_page, onLaterPages=content_page)
    print(f'PARTE3 gerada: {out}')

build()
