from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, PageBreak,
                                  HRFlowable, KeepTogether)
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
DARK_PUR  = colors.HexColor('#14102B')   # capa do bônus: roxo escuro
GOLD      = colors.HexColor('#C9A96E')
PURPLE    = colors.HexColor('#9B5DE5')
CREAM     = colors.HexColor('#FAF7F0')
DARK_TEXT = colors.HexColor('#2A2540')
MID_GRAY  = colors.HexColor('#8A8598')
WARN      = colors.HexColor('#B84040')

W, H = A4
LEFT_MARGIN   = 2   * cm
BOTTOM_MARGIN = 1.8 * cm

# ── Capa especial do bônus (roxo + dourado) ────────────────────────────────
class BonusCoverPage(Flowable):
    def wrap(self, availWidth, availHeight):
        return (availWidth, availHeight)

    def draw(self):
        c = self.canv
        c.saveState()
        c.translate(-LEFT_MARGIN, -BOTTOM_MARGIN)

        # Fundo roxo-marinho profundo
        c.setFillColor(DARK_PUR)
        c.rect(0, 0, W, H, fill=1, stroke=0)

        # Textura: grade discreta
        c.setStrokeColor(colors.HexColor('#1E1535'))
        c.setLineWidth(0.3)
        for i in range(0, int(W), 28):
            c.line(i, 0, i, H)
        for j in range(0, int(H), 28):
            c.line(0, j, W, j)

        # Linha dourada horizontal topo/base
        c.setStrokeColor(GOLD)
        c.setLineWidth(0.8)
        c.line(2*cm, H - 1.5*cm, W - 2*cm, H - 1.5*cm)
        c.line(2*cm, 1.5*cm,     W - 2*cm, 1.5*cm)

        # Linha roxa acima do título
        c.setStrokeColor(PURPLE)
        c.setLineWidth(1.5)
        c.line(W/2 - 3*cm, H*0.65, W/2 + 3*cm, H*0.65)

        # Label BONUS / SECRETO
        c.setFillColor(PURPLE)
        c.setFont('Georgia', 9)
        c.drawCentredString(W/2, H*0.68, 'C A P Í T U L O   S E C R E T O')

        # Ícone cadeado (texto simulado)
        c.setFillColor(GOLD)
        c.setFont('Georgia-Bold', 20)
        c.drawCentredString(W/2, H*0.60, '🔒')

        # Título principal
        c.setFillColor(GOLD)
        c.setFont('Georgia-Bold', 34)
        c.drawCentredString(W/2, H*0.52, 'O Manual Proibido')
        c.setFont('Georgia-Bold', 34)
        c.drawCentredString(W/2, H*0.45, 'dos Signos')

        # Subtítulo
        c.setFillColor(MID_GRAY)
        c.setFont('Georgia-Ital', 12)
        c.drawCentredString(W/2, H*0.38,
            'Como a mente de cada signo realmente funciona')
        c.drawCentredString(W/2, H*0.35,
            'e como usar isso a seu favor')

        # Aviso
        c.setFillColor(WARN)
        c.setFont('Georgia-Ital', 9)
        c.drawCentredString(W/2, H*0.28, '⚠  Contém informações psicológicas diretas e sem filtro.')
        c.drawCentredString(W/2, H*0.25, 'Use com responsabilidade.')

        # Diamante base
        c.setFillColor(GOLD)
        cx, cy = W/2, 1.8*cm
        s = 5
        p = c.beginPath()
        p.moveTo(cx, cy+s); p.lineTo(cx+s, cy)
        p.lineTo(cx, cy-s); p.lineTo(cx-s, cy)
        p.close()
        c.drawPath(p, fill=1, stroke=0)

        c.restoreState()

# ── Página de conteúdo ─────────────────────────────────────────────────────
def content_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(CREAM)
    canvas.rect(0, 0, W, H, fill=1, stroke=0)
    canvas.setStrokeColor(PURPLE)
    canvas.setLineWidth(2)
    canvas.line(0, H - 0.4*cm, W, H - 0.4*cm)
    canvas.setFont('Georgia', 8)
    canvas.setFillColor(MID_GRAY)
    canvas.drawCentredString(W/2, 0.7*cm, 'O Guia Emocional dos Signos: Capítulo Secreto')
    canvas.drawRightString(W - 2*cm, 0.7*cm, str(doc.page))
    canvas.restoreState()

# ── Estilos ────────────────────────────────────────────────────────────────
def make_styles():
    s = {}
    s['chapter_tag'] = ParagraphStyle('chapter_tag',
        fontName='Georgia', fontSize=8, textColor=PURPLE,
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
    s['label'] = ParagraphStyle('label',
        fontName='Georgia-Bold', fontSize=9.5, textColor=PURPLE,
        spaceAfter=1, alignment=TA_LEFT, leading=12)
    s['label_val'] = ParagraphStyle('label_val',
        fontName='Georgia', fontSize=10, textColor=DARK_TEXT,
        spaceAfter=7, alignment=TA_JUSTIFY, leading=14)
    s['warn'] = ParagraphStyle('warn',
        fontName='Georgia-Ital', fontSize=10, textColor=WARN,
        spaceAfter=8, alignment=TA_CENTER, leading=14)
    s['sub'] = ParagraphStyle('sub',
        fontName='Georgia-Ital', fontSize=9.5, textColor=MID_GRAY,
        spaceAfter=8, alignment=TA_LEFT, leading=13)
    return s

def hr(color=PURPLE, thickness=0.5):
    return HRFlowable(width='100%', thickness=thickness, color=color,
                      spaceAfter=10, spaceBefore=4)

# ══════════════════════════════════════════════════════════════════════════════
#  CONTEÚDO: O MANUAL PROIBIDO DOS SIGNOS
# ══════════════════════════════════════════════════════════════════════════════

INTRO = (
    'Este capítulo existe porque há uma diferença entre entender astrologia e entender pessoas. '
    'O que você leu até aqui foi sobre você, seus padrões, suas emoções, seu interior. '
    'O que está a seguir é diferente: é sobre como cada signo funciona por fora, como processa '
    'influência, como toma decisões sob pressão, e onde estão suas brechas psicológicas.'
)
INTRO2 = (
    'Não vou fingir que esse conteúdo é neutro. Conhecimento sobre como influenciar pessoas pode '
    'ser usado para criar conexões genuínas, comunicar-se com mais eficiência, entender o outro '
    'antes de julgá-lo, ou pode ser usado para manipular. Essa escolha é sua, não minha. '
    'O que ofereço aqui é precisão, não julgamento.'
)
INTRO3 = (
    'Cada perfil a seguir cobre cinco pontos: como a mente do signo funciona internamente, '
    'como ganhar sua confiança, o que o faz ceder, seu ponto cego, e o erro fatal que '
    'imediatamente fecha sua porta.'
)

# estrutura por signo: (signo, símbolo, como_funciona, como_confiar, como_ceder, ponto_cego, erro_fatal)
MANUAL = [
    (
        'Áries ♈', 'Fogo Cardinal',
        (
            'Áries toma decisões pelo impulso e valida depois. A mente dele processa emoção e '
            'ação quase simultaneamente, não há espaço entre o sentir e o fazer. Isso o torna '
            'previsível: diga algo que ative seu orgulho ou sua competitividade, e ele reage '
            'antes de pensar. Sua necessidade de ser o primeiro é a força que move e o limite '
            'que cega.'
        ),
        (
            'Seja direto e nunca adulador. Áries detecta adulação imediatamente e o '
            'desprezará. Discorde dele na frente dos outros uma vez, de forma inteligente, '
            'ele vai te respeitar mais do que quem concorda com tudo. Desafios criam '
            'interesse; admiração passiva cria indiferença.'
        ),
        (
            'Crie urgência real ou aparente. Frame a decisão como algo que outra pessoa '
            'vai tomar antes dele. Apele ao orgulho, "não sei se você tem coragem pra isso" '
            'funciona mais do que qualquer argumento racional. Para Áries, ser o escolhido '
            'ou o primeiro é suficiente justificativa para qualquer decisão.'
        ),
        (
            'Seu ego é tão grande que o impede de recuar mesmo quando sabe que está errado. '
            'Isso cria situações onde persiste em decisões ruins para não "perder". '
            'Quem souber plantar a semente de que recuar é, na verdade, a atitude mais '
            'corajosa, tem Áries na mão.'
        ),
        (
            'Nunca tente controlá-lo, dar ordens ou parecer passivo-agressivo. '
            'Áries prefere um inimigo declarado a um aliado manipulador silencioso. '
            'Qualquer tentativa de cercá-lo indiretamente o faz sair da relação '
            'completamente, e sem aviso.'
        )
    ),
    (
        'Touro ♉', 'Terra Fixo',
        (
            'Touro processa o mundo pelos sentidos e pelo acúmulo. A mente de Touro é lenta '
            'por design, ela coleta dados, cria padrões, e só age quando tem certeza suficiente. '
            'O que parece teimosia é, internamente, um sistema de proteção contra mudanças que '
            'percebe como ameaças. Conforto e prazer não são desejos de Touro, são necessidades '
            'operacionais.'
        ),
        (
            'Seja consistente antes de ser interessante. Touro não confia em quem é brilhante '
            'mas imprevisível. Apareça nos momentos certos, mantenha o que promete, e não force '
            'o ritmo. Uma ação concreta de cuidado, a comida favorita, um detalhe lembrado,'
            'vale mais do que mil palavras.'
        ),
        (
            'Mostre permanência e qualidade. Nunca price-down com Touro, barato gera '
            'desconfiança. Dê a ele a sensação de que está fazendo o melhor negócio do mercado '
            'e de que a escolha vai durar. Para ceder numa decisão pessoal, use conforto como '
            'argumento: "vai ser mais fácil, mais estável, mais sólido."'
        ),
        (
            'Touro confunde teimosia com princípio. Pode se manter em posições prejudiciais '
            'simplesmente porque mudou de ideia uma vez e se sentiu fraco. Mostrar que a '
            'mudança que você propõe está na direção do que ele sempre quis, não contra,'
            'dissolve a resistência sem confronto.'
        ),
        (
            'Nunca pressione, force mudança, ou crie instabilidade emocional deliberadamente. '
            'Touro não esquece perturbações, ele arquiva. O que parece ter passado em aberto '
            'pode virar razão de distância permanente meses depois.'
        )
    ),
    (
        'Gêmeos ♊', 'Ar Mutável',
        (
            'Gêmeos processa o mundo pela linguagem e pela informação. A mente de Gêmeos está '
            'sempre dividida entre dois caminhos, daí o símbolo dos gêmeos. Ele decide '
            'impulsivamente depois de coletar informação rapidamente, e pode mudar de ideia '
            'com a mesma velocidade. Sua principal necessidade não é a resposta certa, '
            'mas a estimulação constante.'
        ),
        (
            'Seja interessante antes de ser útil. Gêmeos não confia em quem entedia, '
            'independente de quão confiável seja. Demonstre que tem múltiplas camadas, '
            'que não é previsível, que tem opiniões que ele não esperava de você. '
            'Flexibilidade intelectual cria conexão; consistência monótona cria invisibilidade.'
        ),
        (
            'Dê-lhe informação que ele não conhece e enquadre a decisão como algo intelectualmente '
            'estimulante. Gêmeos diz sim quando sente que descobriu algo, não quando foi '
            'convencido. Nunca apresente uma única opção. Dê duas ou três possibilidades, '
            'e deixe-o "escolher" o que você quer que ele escolha.'
        ),
        (
            'Gêmeos subestima a profundidade emocional do que sente, porque processa '
            'tudo pela análise. Isso cria uma brecha: ele pode ser convencido racionalmente '
            'de algo que emocionalmente não quer, e vice-versa. Quem souber falar simultaneamente '
            'para sua cabeça e para sua curiosidade, tem muito poder sobre Gêmeos.'
        ),
        (
            'Nunca seja repetitivo, didático ou previsível. Gêmeos encerra conversas e '
            'relacionamentos com a mesma velocidade que os inicia, é o principal gatilho '
            'é o tédio. Qualquer sinal de que você é igual a todo mundo fecha a janela '
            'imediatamente.'
        )
    ),
    (
        'Câncer ♋', 'Água Cardinal',
        (
            'Câncer decide pelo sentimento e valida depois com razão. A mente de Câncer está '
            'constantemente avaliando segurança emocional, toda interação é filtrada pela '
            'pergunta: "estou seguro aqui?" Memória afetiva é a moeda interna de Câncer: '
            'o que marcou positivamente tem crédito ilimitado; o que feriu fecha uma porta '
            'que raramente volta a abrir.'
        ),
        (
            'Faça-o sentir visto antes de fazer qualquer pedido. Câncer abre quando percebe '
            'que você se importa com o que ele sente, não com o que ele faz. Lembre detalhes '
            'que outros esquecem. Crie um ambiente onde ele não precisa se defender. '
            'A confiança de Câncer é total ou inexistente, não há meio-termo.'
        ),
        (
            'Apele à memória afetiva e ao senso de família e pertencimento. Frases como '
            '"isso fortalece o que temos construído juntos" ou "sei que você cuida de quem '
            'ama" ativam o sentido de cuidado de Câncer e o colocam em modo de cooperação. '
            'Para decisões difíceis, mostre que a escolha protege quem ele ama.'
        ),
        (
            'Câncer raramente é direto sobre o que o feriu. Arquiva, processa internamente, '
            'e distancia silenciosamente. Esse silêncio pode ser usado, mas com cuidado. '
            'Quem aprende a ler o humor de Câncer antes que ele o declare têm acesso às '
            'suas decisões antes que ele mesmo as tome.'
        ),
        (
            'Nunca minimize o que ele sente, seja indiferente nos momentos de vulnerabilidade, '
            'ou use contra ele algo que confiou a você. A traição emocional para Câncer não '
            'tem conciliação, é quando vai, vai em silêncio e para sempre.'
        )
    ),
    (
        'Leão ♌', 'Fogo Fixo',
        (
            'Leão decide pelo ego e justifica pela razão. A mente de Leão está sempre '
            'monitorando uma pergunta invisível: "como isso me faz parecer?" Isso não é '
            'vaidade superficial, é a estrutura pela qual Leão organiza sua realidade. '
            'Faça Leão se sentir especial e você tem sua atenção. Faça-o se sentir grande '
            'e você tem sua lealdade.'
        ),
        (
            'Demonstre admiração genuína, mas específica. Elogios genéricos Leão percebe '
            'e descarta. O que funciona é nomear uma qualidade específica de forma que '
            'mostre que você realmente prestou atenção. Depois de se sentir visto e admirado, '
            'Leão se torna extraordinariamente generoso e fácil de influenciar.'
        ),
        (
            'Enquadre a decisão como algo que só um líder tomaria. "Poucos teriam a visão '
            'de fazer isso" funciona melhor do que qualquer argumento lógico. Para que Leão '
            'ceda em algo difícil, certifique-se de que ele saberá que cedeu, porque Leão '
            'precisa ser visto fazendo a coisa certa, não apenas fazendo a coisa certa.'
        ),
        (
            'O ego de Leão o torna vulnerável à bajulação estratégica. Alguém disposto a '
            'inflar seu senso de grandeza consistentemente ganha influência desproporcional. '
            'O perigo para Leão é não perceber quando está sendo usado justamente porque '
            'está muito ocupado apreciando a admiração.'
        ),
        (
            'Nunca o envergonhe em público, o trate como comum, ou o ignore deliberadamente. '
            'Leão responde a insultos com fogo imediato, mas a indiferença é o que '
            'realmente o destrói por dentro. Não há forma mais rápida de perder Leão '
            'do que tratá-lo como se não fosse especial.'
        )
    ),
    (
        'Virgem ♍', 'Terra Mutável',
        (
            'Virgem decide pela análise e sente culpa se não o faz. A mente de Virgem está '
            'sempre em modo de auditoria, avaliando eficiência, identificando falhas, '
            'medindo distâncias entre o ideal e o real. Essa mente é poderosa e útil, '
            'mas também é um sistema que nunca descansa. A vulnerabilidade de Virgem '
            'é o perfeccionismo: ela jamais está completamente satisfeita, inclusive consigo.'
        ),
        (
            'Demonstre competência antes de demonstrar afeto. Virgem confia em quem faz '
            'as coisas bem, e desconfia de quem parece agradável mas desorganizado. '
            'Seja preciso, pontual, e nunca prometa o que não vai cumprir. Cada promessa '
            'cumprida é um tijolo na construção de credibilidade com Virgem.'
        ),
        (
            'Apresente argumentos com dados e lógica. Virgem não cede para apelos emocionais: '
            'ela cede quando a análise fecha. Mostre que pensou nos detalhes, que considerou '
            'os riscos, que tem um plano. Enquadre qualquer pedido como a solução mais '
            'eficiente para um problema que ela já identificou.'
        ),
        (
            'Virgem é seu próprio crítico mais severo, o que significa que ela responde '
            'bem a quem a aceita sem julgamento. Um ambiente de aceitação genuína deixa '
            'Virgem desarmada de formas que nenhuma outra estratégia consegue. '
            'Seu perfeccionismo é a armadura; a aceitação é o que a dissolve.'
        ),
        (
            'Nunca seja impreciso, descuidado, ou apresente soluções sem ter pensado nos '
            'detalhes. Virgem perde a confiança imediatamente em quem demonstra incompetência '
            'ou superficialidade, e raramente dá uma segunda chance para reabilitar '
            'a imagem.'
        )
    ),
    (
        'Libra ♎', 'Ar Cardinal',
        (
            'Libra decide pela harmonia e padece de indecisão estrutural. A mente de Libra '
            'está constantemente pesando lados, não porque seja fraca, mas porque sua '
            'inteligência genuinamente enxerga mérito em perspectivas opostas. Isso a torna '
            'justa e difícil de mover. A chave não é convencer Libra de que você está certo, '
            'mas de que a sua escolha cria mais harmonia do que a alternativa.'
        ),
        (
            'Crie um ambiente de beleza e equilíbrio ao redor da conversa. Libra não confia '
            'em pessoas que geram conflito ou que parecem parciais demais. Apresente-se como '
            'alguém equilibrado, que ouve os dois lados, que respeita. Depois de sentir que '
            'você é justo, Libra baixa a guarda completamente.'
        ),
        (
            'Elimine as alternativas uma por uma em vez de vender a sua opção. Libra cede '
            'quando as outras opções se tornam menos atraentes, não quando a sua se torna '
            'mais. Mostre os problemas das outras possibilidades com calma, e a sua escolha '
            'naturalmente emergirá como a mais equilibrada.'
        ),
        (
            'Libra evita conflito a tal ponto que frequentemente concorda com o que não quer. '
            'Isso pode ser explorado, uma pergunta direta em um momento de desconforto '
            'social pode arrancar um sim que não foi realmente considerado. Libra percebe '
            'isso depois, e o ressente profundamente.'
        ),
        (
            'Nunca force uma decisão imediata, crie pressão artificial, ou seja injusto '
            'visivelmente. Libra responde à injustiça com uma determinação surpreendente '
            'que contrasta completamente com sua indecisão habitual. Quando vê injustiça, '
            'decide, e a decisão costuma ser irreversível.'
        )
    ),
    (
        'Escorpião ♏', 'Água Fixo',
        (
            'Escorpião decide pelo poder e desconfia de todo o resto. A mente de Escorpião '
            'está sempre avaliando motivação oculta, sua pergunta constante é "o que essa '
            'pessoa realmente quer?" Isso o torna difícil de manipular diretamente. A única '
            'forma de influenciar Escorpião é sendo genuinamente honesto sobre suas intenções, '
            'incluindo as menos nobres. Paradoxalmente, a honestidade sobre o interesse '
            'próprio cria mais confiança do que a altruísmo encenado.'
        ),
        (
            'Seja transparente sobre quem você é, inclusive sobre o que quer. Escorpião '
            'respeita quem tem poder e honestidade suficientes para não fingir. Mostrar '
            'vulnerabilidade estratégica, revelar algo real sobre si mesmo,cria uma '
            'reciprocidade poderosa em Escorpião, que então sente que deve revelar também.'
        ),
        (
            'Apele ao senso de poder e exclusividade. Escorpião cede quando sente que '
            'a escolha o coloca em posição de força, acesso ou conhecimento privilegiado. '
            '"Poucas pessoas têm acesso a isso" ressoa mais do que qualquer benefício '
            'prático. Escorpião também cede por lealdade, mas essa lealdade precisa '
            'ter sido conquistada, não assumida.'
        ),
        (
            'A necessidade de controle de Escorpião pode levá-lo a superanalisar situações '
            'simples e criar conspirações onde não há nenhuma. Quem souber alimentar sua '
            'paranoia cuidadosamente, ou aliviá-la com transparência,tem influência '
            'significativa sobre o que Escorpião decide.'
        ),
        (
            'Nunca minta, omita algo importante, ou demonstre fraqueza de caráter. '
            'Escorpião testa constantemente, e percebe quando alguém falha no teste, '
            'mesmo que não diga nada. O silêncio de Escorpião depois de uma traição '
            'é mais definitivo do que qualquer confronto.'
        )
    ),
    (
        'Sagitário ♐', 'Fogo Mutável',
        (
            'Sagitário decide pela visão e se entedia com o prático. A mente de Sagitário '
            'está sempre no futuro, no horizonte, no maior propósito. Detalhes e limitações '
            'são obstáculos que prefere ignorar. Isso o torna entusiasmado e fácil de excitar, '
            'e difícil de comprometer. A chave para influenciar Sagitário é sempre começar '
            'pelo horizonte: mostre o destino antes de mostrar o caminho.'
        ),
        (
            'Seja um igual em amplitude de visão. Sagitário não se deixa influenciar por '
            'quem parece menor, intelectualmente, espiritualmente, ou em termos de '
            'experiência de mundo. Demonstre que viveu, que pensa além, que tem perspectivas '
            'que ele ainda não considerou. Isso imediatamente cria respeito e abertura.'
        ),
        (
            'Faça a decisão parecer uma aventura, não uma responsabilidade. Enquadre '
            'qualquer comprometimento como expansão, não como limitação. "Isso vai abrir "  '
            '"portas que você ainda não imagina" funciona. "Isso vai te dar estabilidade" '
            'fecha a porta imediatamente. Sagitário cede pelo entusiasmo, não pela lógica.'
        ),
        (
            'O otimismo estrutural de Sagitário o torna ingênuo em contextos práticos. '
            'Ele acredita que as coisas vão dar certo mesmo sem planejamento, o que o '
            'expõe a quem promete mundos e fundos com vocabulário visionário mas sem '
            'substância real. É o signo mais vulnerável a promessas grandes '
            'entregues com entusiasmo.'
        ),
        (
            'Nunca tente prendê-lo, dê-lhe ultimatos, ou pareça alguém que vai '
            'reduzir sua liberdade. Sagitário tem um reflexo imediato de fuga quando '
            'sente que a autonomia está ameaçada, e esse reflexo é mais forte do que '
            'qualquer apego que tenha construído.'
        )
    ),
    (
        'Capricórnio ♑', 'Terra Cardinal',
        (
            'Capricórnio decide pelo controle e pelo status de longo prazo. A mente de '
            'Capricórnio avalia toda decisão por uma pergunta: "isso me coloca em posição '
            'de força no futuro?" Imediatismo não funciona com ele, o que funciona é '
            'mostrar retorno a longo prazo, seja financeiro, de posição, de segurança '
            'ou de reputação. Capricórnio é o gerente da própria vida, e você precisa '
            'apresentar seu pedido como um investimento, não como um custo.'
        ),
        (
            'Demonstre resultados concretos antes de pedir confiança. Capricórnio não '
            'confia em potencial, confia em histórico. Mostre o que você já fez, não '
            'o que vai fazer. E seja paciente: a confiança de Capricórnio é construída '
            'em meses, não em encontros.'
        ),
        (
            'Mostre o ROI emocional ou prático da decisão. Capricórnio cede quando '
            'a análise de custo-benefício fecha, e quando percebe que a escolha fortalece '
            'sua posição ou segurança. Apresente dados, histórico, projeções. '
            'Enquadre como um movimento estratégico inteligente, não como um risco.'
        ),
        (
            'Capricórnio suprime emoção com tanta eficiência que frequentemente não '
            'percebe quando está emocionalmente exausto ou quando uma decisão "racional" '
            'é na verdade uma fuga emocional. Quem souber nomear isso, "parece que '
            'essa decisão também tem um componente emocional que você não está '
            'considerando", tem acesso a uma camada que poucos chegam.'
        ),
        (
            'Nunca seja improdutivo visivelmente, demonstre incompetência, ou tente '
            'acessar sua vulnerabilidade de forma forçada e pública. Capricórnio '
            'fecha completamente para quem o expõe, e pode levar anos para '
            'reabrir, se é que reabre.'
        )
    ),
    (
        'Aquário ♒', 'Ar Fixo',
        (
            'Aquário decide pelo princípio e resiste à autoridade. A mente de Aquário '
            'está sempre analisando sistemas, e identificando onde eles falham. '
            'Ele não segue regras por respeito às regras, mas porque decidiu que faz '
            'sentido. Isso o torna difícil de mover por autoridade direta. O que '
            'funciona é apresentar sua ideia como algo que desafia o sistema existente, '
            'não como algo que obedece a ele.'
        ),
        (
            'Trate-o como intelectual, não como seguidor. Aquário confia em quem o '
            'respeita como pensador independente, não em quem tenta ensiná-lo ou '
            'guiá-lo. Compartilhe ideias, provoque pensamento, e deixe-o chegar '
            'às suas próprias conclusões. Se a conclusão for a que você quer, '
            'Aquário a adotará com fervor.'
        ),
        (
            'Faça da decisão um ato de inconformidade inteligente. "Poucos têm '
            'a visão de fazer isso diferente" ou "esse é o caminho que a maioria '
            'evita porque exige pensar fora do padrão" funciona diretamente no '
            'sistema de valores de Aquário. Ele quer ser o que pensa à frente '
            'do seu tempo, use isso.'
        ),
        (
            'A fixidez de Aquário, o único signo de ar fixo,o torna surpreendentemente '
            'tão teimoso quanto Touro nas posições que adota como princípio. Uma vez que '
            'decidiu que algo é errado, dificilmente revisita. Quem souber plantar '
            'uma semente de dúvida antes que a posição se consolide tem muito mais '
            'espaço do que quem tenta mudar uma posição já formada.'
        ),
        (
            'Nunca tente controlá-lo, apelar para autoridade, ou mostrar que você '
            'precisa de conformidade dele. Aquário não obedece, ele coopera quando '
            'quer. Qualquer sinal de que você precisa que ele siga regras imediatamente '
            'cria resistência, mesmo que a regra em questão seja razoável.'
        )
    ),
    (
        'Peixes ♓', 'Água Mutável',
        (
            'Peixes decide pelo sentimento e raramente sabe explicar por quê. A mente '
            'de Peixes é fluida, intuitiva, e permeável, ela absorve o estado emocional '
            'de quem está ao redor como uma esponja absorve água. Isso o torna '
            'extraordinariamente empático e extraordinariamente influenciável. '
            'O estado emocional de quem está com Peixes é, muitas vezes, o estado '
            'que Peixes adota como próprio.'
        ),
        (
            'Crie um campo emocional de segurança e beleza. Peixes confia em quem o '
            'faz sentir que o mundo é menos brutal do que parece. Gentileza genuína, '
            'presença, e ausência de julgamento abrem Peixes mais do que qualquer '
            'argumento. Ele vai em direção ao que sente como lar.'
        ),
        (
            'Apele à imaginação e ao ideal. Peixes cede quando a decisão parece '
            'conectada com algo maior do que o prático, um sonho, um propósito, '
            'uma missão. Enquadre como uma oportunidade de criar algo significativo, '
            'de ajudar alguém, de viver algo que valerá a pena ter vivido. '
            'Peixes não age pela lógica, age pela poesia.'
        ),
        (
            'A porosidade emocional de Peixes é sua maior vulnerabilidade. Ele '
            'absorve culpa com facilidade, mesmo culpa que não é sua. Quem souber '
            'implantar a sensação de que Peixes está decepcionando alguém que ama, '
            'ou que não está cumprindo um propósito maior, tem poder significativo '
            'sobre suas decisões. Isso é manipulação emocional direta, e funciona '
            'demais com Peixes.'
        ),
        (
            'Nunca seja cínico, duro, ou completamente pragmático com Peixes. '
            'Ele fecha para quem não deixa espaço para o sonho. E nunca use '
            'sua compaixão contra ele: Peixes perdoa quase tudo, mas quando '
            'finalmente percebe que foi usado por quem confiava, o afastamento '
            'é total e sem possibilidade real de retorno.'
        )
    ),
]

# ══════════════════════════════════════════════════════════════════════════════
#  BUILD
# ══════════════════════════════════════════════════════════════════════════════

def build():
    out = (r'c:\Users\Heitor Melo\Desktop\Grana no Digital\Astrologia'
           r'\O_Guia_Emocional_dos_Signos_BONUS.pdf')
    doc = SimpleDocTemplate(
        out, pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=1.8*cm, bottomMargin=1.8*cm,
    )
    S = make_styles()
    story = []

    # ── CAPA DO BÔNUS ────────────────────────────────────────────────────────
    story.append(BonusCoverPage())
    story.append(PageBreak())

    # ── INTRO ────────────────────────────────────────────────────────────────
    story.append(Paragraph('CAPÍTULO SECRETO', S['chapter_tag']))
    story.append(Paragraph(
        'O Manual Proibido dos Signos\nComo a Mente de Cada Signo Funciona, e Como Usar Isso',
        S['chapter_title']))
    story.append(hr())
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(INTRO,  S['body']))
    story.append(Paragraph(INTRO2, S['body']))
    story.append(Paragraph(INTRO3, S['body']))
    story.append(Paragraph(
        '⚠  Este conteúdo é para autoconhecimento e comunicação estratégica. '
        'Use com ética e responsabilidade.',
        S['warn']))
    story.append(Spacer(1, 0.4*cm))

    LABELS = [
        'Como a mente funciona',
        'Como ganhar sua confiança',
        'Como fazê-lo ceder',
        'Seu ponto cego',
        'O erro fatal',
    ]

    for signo, subtitulo, *campos in MANUAL:
        bloco = [
            Paragraph(signo, S['sign_title']),
            Paragraph(subtitulo, S['sub']),
        ]
        for label, texto in zip(LABELS, campos):
            bloco.append(Paragraph(label, S['label']))
            bloco.append(Paragraph(texto, S['label_val']))
        bloco.append(Spacer(1, 0.15*cm))
        bloco.append(HRFlowable(width='100%', thickness=0.3,
                                color=colors.HexColor('#DDD8C8'),
                                spaceAfter=8, spaceBefore=4))
        story.append(KeepTogether(bloco))

    doc.build(story, onFirstPage=content_page, onLaterPages=content_page)
    print(f'BÔNUS gerado: {out}')

build()
