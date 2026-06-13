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
GOLD      = colors.HexColor('#C9A96E')
CREAM     = colors.HexColor('#FAF7F0')
DARK_TEXT = colors.HexColor('#2A2540')
MID_GRAY  = colors.HexColor('#8A8598')

W, H = A4
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
            sub_lines = []
            for part in self.subtitle.split('\n'):
                sub_lines.extend(part.split(' · '))
            for i, ln in enumerate(sub_lines):
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
    canvas.drawCentredString(W/2, 0.7*cm, 'O Guia Emocional dos Signos')
    canvas.drawRightString(W - 2*cm, 0.7*cm, str(doc.page))
    canvas.restoreState()

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
    s['sign_title'] = ParagraphStyle('sign_title',
        fontName='Georgia-Bold', fontSize=13, textColor=DARK_TEXT,
        spaceBefore=14, spaceAfter=4, alignment=TA_LEFT, leading=16)
    s['body'] = ParagraphStyle('body',
        fontName='Georgia', fontSize=10.5, textColor=DARK_TEXT,
        spaceAfter=8, alignment=TA_JUSTIFY, leading=16)
    s['label'] = ParagraphStyle('label',
        fontName='Georgia-Ital', fontSize=9.5, textColor=GOLD,
        spaceAfter=2, alignment=TA_LEFT, leading=12)
    s['sub'] = ParagraphStyle('sub',
        fontName='Georgia-Ital', fontSize=9.5, textColor=MID_GRAY,
        spaceAfter=6, alignment=TA_LEFT, leading=13)
    return s

def hr(color=GOLD, thickness=0.5):
    return HRFlowable(width='100%', thickness=thickness, color=color,
                      spaceAfter=10, spaceBefore=4)

# ══════════════════════════════════════════════════════════════════════════════
#  CAPÍTULO 10: POR QUE VOCÊ SE APAIXONA SEMPRE PELO MESMO TIPO
# ══════════════════════════════════════════════════════════════════════════════

CAP10_INTRO = (
    'A repetição nos relacionamentos não é coincidência, é estrutura. Você pode mudar de parceiro, '
    'de cidade, de estilo de vida, e ainda assim encontrar a mesma dinâmica emocional com pessoas '
    'diferentes. Isso acontece porque o que nos atrai não é aleatório: é moldado por nossa história, '
    'nossos medos, nossas partes reprimidas e nosso mapa interno de amor.'
)
CAP10_INTRO2 = (
    'A astrologia oferece uma linguagem para compreender esses padrões. Não para criar fatalismo, '
    '"sempre vou me apaixonar pelo mesmo tipo", mas para iluminar o que está acontecendo abaixo '
    'da superfície, onde a consciência raramente chega. Quando você vê o padrão com clareza, '
    'ele perde o poder automático sobre você.'
)

CAP10_SECOES = [
    (
        'Vênus: o que você chama de amor',
        (
            'Vênus no mapa natal descreve o que você interpreta como amor, quais qualidades te '
            'magnetizam, que tipo de presença faz você sentir que "isso é o que estava procurando". '
            'Vênus em Áries tende a chamar de amor a intensidade e a espontaneidade. Vênus em '
            'Capricórnio pode interpretar como amor a confiabilidade e a ambição. Vênus em Escorpião '
            'frequentemente associa amor com profundidade, mistério e até tensão.'
        ),
        (
            'O problema surge quando o que você aprendeu a chamar de amor foi moldado por '
            'experiências emocionalmente carregadas, e não necessariamente saudáveis. Se você cresceu '
            'num ambiente onde amor significava ansiedade ou intensidade, seu sistema emocional aprendeu '
            'que essa textura é "real". O que é tranquilo e seguro pode parecer, estranhamente, '
            '"sem química".'
        )
    ),
    (
        'Marte: o que você persegue sem perceber',
        (
            'Marte descreve o que ativa seu desejo, não o que você escolheria conscientemente, '
            'mas o que literalmente te faz se mover em direção a alguém. É a atração antes do '
            'pensamento, o impulso antes da análise. Marte em Escorpião se sente magnetizado pelo '
            'que é proibido e pelo que precisa ser conquistado. Marte em Libra é ativado pela '
            'elegância e pela reciprocidade. Marte em Gêmeos se acende com a inteligência e o '
            'imprevisível.'
        ),
        (
            'Entender o seu Marte é essencial porque ele frequentemente aponta para o que você '
            'persegue antes de pensar, incluindo o que pode não ser bom para você. O desejo de '
            'Marte não filtra, não avalia compatibilidade de longo prazo: ele apenas persegue o '
            'que ativa.'
        )
    ),
    (
        'A Casa 7: o espelho da alma',
        (
            'A sétima casa no mapa natal revela o que você inconscientemente busca em um parceiro. '
            'Mas há uma camada mais profunda: ela também mostra qualidades que você reprimiu em si '
            'mesmo e projeta no outro. Se a sua sétima casa é em Escorpião, você pode atrair '
            'pessoas intensas, quando na verdade, parte dessa intensidade vive dentro de você '
            'e não encontrou expressão.'
        ),
        (
            'Isso não significa que o outro não tem aquelas qualidades. Significa que algo em você '
            'reconhece e é atraído por elas com uma força que vai além do razoável, porque o '
            'reconhecimento vem de dentro.'
        )
    ),
    (
        'Projeção: nos apaixonamos pelo que reprimimos',
        (
            'Carl Jung chamou de "sombra" as partes de nós que aprendemos a reprimir porque eram '
            'inaceitáveis, para nossas famílias, nossa cultura, nossa autoimagem. Essas partes não '
            'desaparecem: elas vão morar em outras pessoas. Quando nos apaixonamos intensamente, '
            'frequentemente estamos nos apaixonando por uma projeção, qualidades que pertencem à '
            'nossa sombra e que estamos "encontrando" no outro.'
        ),
        (
            'A astrologia pode ajudar a identificar sua sombra. Se você tem Leão como signo solar '
            'mas sua sétima casa em Áries, pode reprimir sua própria arrogância e a encontrar nos '
            'parceiros. Se você é Virgem mas tem Netuno em destaque, pode reprimir sua sensibilidade '
            'e projetá-la em parceiros "artísticos" pelos quais se sente atraído compulsivamente.'
        )
    ),
    (
        'O vínculo com o passado: repetindo o familiar',
        (
            'Nosso primeiro modelo de amor, geralmente a relação com os pais,cria um template '
            'emocional. Não estamos destinados a repetir exatamente esse template, mas nosso sistema '
            'nervoso aprendeu a reconhecer aquele tipo de dinâmica como "amor familiar". Se o amor '
            'parental era abundante mas inconsistente, o sistema aprende que amor inclui incerteza.'
        ),
        (
            'A Lua no mapa natal mostra essa herança emocional, a textura do amor que você recebeu '
            'e como isso moldou o que você interpreta como conexão real. Lua em Câncer pode ter '
            'aprendido que amor significa cuidado e presença constante. Lua em Aquário pode ter '
            'aprendido que amor é respeito à autonomia e à individualidade.'
        )
    ),
    (
        'Como sair do padrão',
        (
            'Reconhecer o padrão não é suficiente para quebrá-lo, mas é o primeiro passo '
            'indispensável. O padrão se quebra quando você consegue tolerar a desconfortável '
            'sensação de que algo é bom sem ser familiar. A segurança pode parecer "sem graça" '
            'quando você está acostumado à ansiedade. A disponibilidade pode parecer "sufocante" '
            'quando está acostumado ao distante.'
        ),
        (
            'O trabalho não é eliminar a atração pelo que é conhecido, mas expandir sua capacidade '
            'de estar com o que é saudável, mesmo quando ainda não parece "a coisa certa". Com o '
            'tempo, o sistema nervoso se recalibra. Novos padrões constroem novos templates. '
            'A astrologia oferece o mapa; a terapia, a prática e o tempo oferecem o caminho.'
        )
    ),
]

# ══════════════════════════════════════════════════════════════════════════════
#  CAPÍTULO 11: ESTILOS DE APEGO POR SIGNO
# ══════════════════════════════════════════════════════════════════════════════

CAP11_INTRO = (
    'Nos anos 1960, o psicólogo John Bowlby descreveu o estilo de apego como a forma como nos '
    'vinculamos às pessoas que amamos, é como respondemos quando esse vínculo é ameaçado. '
    'Pesquisadores identificaram quatro padrões principais: seguro, ansioso, evitativo e desorganizado.'
)
CAP11_INTRO2 = (
    'A posição da Lua, de Vênus e de Marte no mapa natal, combinados com o signo solar e o '
    'elemento dominante, podem indicar tendências naturais de cada signo. O que se segue são '
    'padrões frequentes, não certezas absolutas, mas tendências que merecem reconhecimento.'
)

ESTILOS_APEGO = [
    (
        'Áries', 'Evitativo com traços ansiosos',
        (
            'Áries carrega uma contradição interna: quer ser escolhido, mas resiste a depender. '
            'Quando se sente emocionalmente exposto demais, recua, não por frieza, mas por medo '
            'de perder o controle da situação. A independência de Áries não é apenas personalidade; '
            'é defesa.'
        ),
        (
            'Em relacionamentos, isso pode se manifestar como o clássico ciclo de perseguição e '
            'fuga. Quando o parceiro se aproxima demais, Áries abre espaço; quando o parceiro '
            'recua, Áries reaparece. O que parece manipulação muitas vezes é simplesmente a '
            'regulação de uma ansiedade que ele mesmo não reconhece totalmente.'
        ),
        'Sentir que perdeu a liberdade ou que o parceiro o considera garantido.',
        'Espaço físico sem ruptura emocional; saber que pode voltar.',
        'Aprender que vulnerabilidade pode coexistir com autonomia.'
    ),
    (
        'Touro', 'Ansioso com tendência ao apego estável',
        (
            'Touro é o signo que mais teme a perda depois de ter investido. Quando se entrega, '
            'entrega completamente, o que significa que a ameaça de perda cria uma ansiedade '
            'proporcional ao investimento. No início dos relacionamentos, pode parecer seguro e '
            'tranquilo. Com o tempo, à medida que o apego aprofunda, a ansiedade pode emergir.'
        ),
        (
            'O apego ansioso de Touro se manifesta principalmente como necessidade de consistência. '
            'Mudanças abruptas, inconsistência emocional no parceiro, ou sinais de distanciamento '
            'ativam um estado de alerta que pode levá-lo a se tornar possessivo ou excessivamente '
            'controlador do ambiente compartilhado.'
        ),
        'Incerteza e inconsistência; qualquer sinal de afastamento do parceiro.',
        'Rotinas estáveis, clareza nas intenções, presença física consistente.',
        'Desenvolver segurança interna que não dependa inteiramente da previsibilidade do outro.'
    ),
    (
        'Gêmeos', 'Evitativo',
        (
            'Gêmeos raramente admite que teme a intimidade, mesmo para si mesmo. O movimento '
            'constante, a necessidade de estimulação intelectual e a multiplicidade de interesses '
            'são, em parte, estratégias inconscientes para não ficar parado tempo suficiente para '
            'sentir o peso de um vínculo profundo. A leveza de Gêmeos é real, mas também funciona '
            'como escudo.'
        ),
        (
            'Em relacionamentos, isso se traduz em dificuldade com comprometimento, mudanças '
            'frequentes de humor em relação ao parceiro, e uma tendência de intelectualizar o que '
            'sente em vez de simplesmente senti-lo. Quando a intimidade aprofunda, Gêmeos pode '
            'criar distância, às vezes sem perceber.'
        ),
        'Sentir-se preso ou que o relacionamento exige mais emoção do que consegue dar.',
        'Liberdade intelectual; parceiro que respeita o espaço mental.',
        'Aprender que ficar, física e emocionalmente,não significa perder a si mesmo.'
    ),
    (
        'Câncer', 'Ansioso',
        (
            'Câncer é o signo mais propenso ao apego ansioso. Sua sensibilidade emocional é '
            'extraordinária, mas essa mesma sensibilidade o torna altamente reativo a mudanças '
            'de temperatura no relacionamento. Um parceiro levemente mais distante do que ontem '
            'pode ativar em Câncer uma onda de preocupação e necessidade de reasseguramento.'
        ),
        (
            'Isso não é fraqueza, é a natureza de uma inteligência emocional que capta o que '
            'os outros perdem. O desafio é que Câncer frequentemente age a partir do medo '
            'antes de ter certeza de que o medo é justificado. Isso pode gerar dinâmicas '
            'sufocantes mesmo em relacionamentos genuinamente seguros.'
        ),
        'Qualquer sinal de frieza, distância ou falta de reciprocidade emocional.',
        'Reasseguramento verbal e físico; clareza sobre o estado do relacionamento.',
        'Construir uma base emocional interna que não dependa inteiramente da resposta do outro.'
    ),
    (
        'Leão', 'Ansioso com traços seguros',
        (
            'Leão tem uma contradição interessante: sua autoconfiança aparente coexiste com uma '
            'necessidade intensa de afirmação. Quando amado e admirado, é generoso, expansivo e '
            'seguro. Quando ignorado ou diminuído, a ansiedade emerge, e pode se manifestar como '
            'drama ou demandas de atenção que os outros percebem como ego inflado.'
        ),
        (
            'No fundo, o apego ansioso de Leão vem de um medo de não ser suficiente, de que, '
            'sem a admiração do outro, não tem valor real. O trabalho emocional de Leão é construir '
            'uma fonte interna de autoestima que não precise ser constantemente reabastecida '
            'pelo parceiro.'
        ),
        'Ser ignorado, diminuído ou tratado como comum.',
        'Reconhecimento genuíno, tempo de qualidade com atenção plena.',
        'Aprender a se admirar independente da plateia; encontrar valor além do olhar do outro.'
    ),
    (
        'Virgem', 'Evitativo',
        (
            'Virgem raramente admite quanto precisa, para si mesmo e para os outros. Sua '
            'autossuficiência é real, mas também funciona como proteção contra a vulnerabilidade '
            'que intimidade exige. Ao manter o controle sobre si mesmo e sua rotina, Virgem cria '
            'uma distância segura que o protege de ser decepcionado.'
        ),
        (
            'Em relacionamentos, isso se manifesta como dificuldade em pedir, em mostrar '
            'necessidade, e em confiar que o outro cuida bem sem supervisão. A crítica constante '
            'de si mesmo e do parceiro, frequentemente mascara o medo de se abrir completamente.'
        ),
        'Sentir que perdeu o controle da situação ou que é visto como necessitado.',
        'Clareza, consistência e tempo para processar, sem pressão emocional.',
        'Aprender que pedir ajuda é força; que ser visto em suas imperfeições não é catastrófico.'
    ),
    (
        'Libra', 'Ansioso com tendência à complacência',
        (
            'Libra precisa de paz, e isso inclui a paz do relacionamento. Sua tendência ao apego '
            'ansioso se manifesta não como intensidade emocional visível, mas como adaptação '
            'excessiva. Libra frequentemente reprime suas próprias necessidades para manter a '
            'harmonia, criando um acúmulo silencioso que eventualmente explode.'
        ),
        (
            'O medo de Libra é a rejeição e o conflito. Para evitá-los, concorda quando deveria '
            'discordar, cede quando deveria manter, e frequentemente perde o fio de quem '
            'realmente é dentro do relacionamento. O parceiro pode interpretar isso como falta de '
            'caráter; o que é, na verdade, ansiedade disfarçada de diplomacia.'
        ),
        'Conflito, desarmonia, a sensação de que o parceiro está descontente.',
        'Conversas abertas e respeitosas; clareza sobre a relação sem drama.',
        'Aprender que a própria voz, quando usada com cuidado, fortalece o relacionamento.'
    ),
    (
        'Escorpião', 'Ansioso / Desorganizado',
        (
            'Escorpião ocupa um espaço único: é ao mesmo tempo intensamente apegado e profundamente '
            'desconfiante. Quer a fusão total com o outro, mas teme que essa fusão o deixe '
            'completamente vulnerável a uma traição que considera, em algum nível, inevitável. '
            'Essa ambivalência cria um padrão onde Escorpião testa constantemente o parceiro.'
        ),
        (
            'O estilo desorganizado emerge quando a ferida de confiança é profunda. Pode '
            'simultaneamente querer mais proximidade e criar situações que afastem o parceiro. '
            'O caminho de Escorpião é o mais difícil: aprender a confiar sabendo que pode ser '
            'machucado, e perceber que sobrevive.'
        ),
        'Qualquer suspeita de traição, segredo ou deslealdade.',
        'Transparência total, consistência de longo prazo, honestidade mesmo quando dói.',
        'Aprender que confiança não é ingenuidade, é coragem; a intimidade real exige vulnerabilidade.'
    ),
    (
        'Sagitário', 'Evitativo',
        (
            'Sagitário evita o comprometimento com a mesma energia com que persegue a liberdade, '
            'e para ele, as duas coisas são quase sinônimos. Não é que Sagitário não queira amor; '
            'é que o amor que conhece parece sempre vir com condições e restrições ao movimento. '
            'Então escolhe o movimento.'
        ),
        (
            'Em relacionamentos, isso se traduz em uma tendência de desaparecer quando as coisas '
            'ficam sérias demais, de redefinir o que "comprometido" significa para caber na '
            'própria agenda, e de usar o humor ou a filosofia para evitar conversas '
            'emocionalmente exigentes.'
        ),
        'Sentir que o relacionamento ameaça sua liberdade ou exige que abandone sua busca.',
        'Parceiro que tem sua própria vida vibrante; espaço para aventura dentro do relacionamento.',
        'Entender que o comprometimento não é uma prisão, é uma forma de liberdade mais sofisticada.'
    ),
    (
        'Capricórnio', 'Evitativo',
        (
            'Capricórnio trata emoções com a mesma eficiência com que trata projetos: prefere ter '
            'controle, planejar, e não depender de variáveis imprevisíveis. O afeto de Capricórnio '
            'é real e profundo, mas raramente visível, especialmente no início. Sua reserva '
            'emocional frequentemente é interpretada como frieza, quando é proteção.'
        ),
        (
            'O medo de Capricórnio é o fracasso, incluindo o fracasso relacional. Investir '
            'emocionalmente e perder pode ser vivido como uma derrota pessoal. Então não investe '
            'até ter alguma garantia, e raramente sente que tem garantia suficiente.'
        ),
        'Vulnerabilidade forçada, dependência emocional visível, instabilidade no parceiro.',
        'Construção gradual de confiança; clareza sobre intenções de longo prazo.',
        'Aprender que sentir e mostrar não é fraqueza, é o que torna os relacionamentos sustentáveis.'
    ),
    (
        'Aquário', 'Evitativo',
        (
            'Aquário é o signo mais filosoficamente confortável com a ideia de não precisar de '
            'ninguém, o que pode ser libertador ou uma profecia que ele mesmo cumpre. Sua '
            'necessidade de autonomia é genuína, mas frequentemente usada como razão para manter '
            'todos a uma distância segura. O paradoxo: genuinamente ama a humanidade, mas têm '
            'dificuldade com a pessoa específica à sua frente.'
        ),
        (
            'Em relacionamentos, isso aparece como distanciamento emocional, dificuldade em '
            'priorizar o parceiro frente a causas maiores, é uma tendência de intelectualizar o '
            'afeto em vez de simplesmente expressá-lo. O parceiro de Aquário frequentemente se '
            'sente amado em teoria mas sozinho na prática.'
        ),
        'Sentir que o relacionamento exige que abandone sua individualidade ou suas causas.',
        'Parceiro que valoriza independência; espaço para os dois crescerem individualmente.',
        'Aprender que profundidade emocional com uma pessoa não contradiz sua visão de mundo.'
    ),
    (
        'Peixes', 'Ansioso / Desorganizado',
        (
            'Peixes é o signo dos limites borrados, e isso se estende aos vínculos emocionais. '
            'Sente as emoções do outro como se fossem suas, o que pode criar laços intensos mas '
            'também confusão profunda sobre onde termina e onde o outro começa. Essa porosidade '
            'emocional frequentemente o leva a se perder no relacionamento.'
        ),
        (
            'O estilo ansioso-desorganizado de Peixes emerge quando as fronteiras são inexistentes: '
            'pode sacrificar suas necessidades completamente para não perder o outro, e ao mesmo '
            'tempo se ressentir silenciosamente desse sacrifício. Alternativamente, pode fugir '
            'para um mundo interior quando a realidade do relacionamento se torna pesada demais.'
        ),
        'Frieza, lógica excessiva, parceiro que não valida suas emoções.',
        'Gentileza, espaço para sentir, limite saudável vindo do parceiro.',
        'Aprender que fronteiras protegem o amor; que dizer não é um ato de cuidado.'
    ),
]

# ══════════════════════════════════════════════════════════════════════════════
#  CAPÍTULO 12: LINGUAGENS DO AMOR DOS 12 SIGNOS
# ══════════════════════════════════════════════════════════════════════════════

CAP12_INTRO = (
    'Em 1992, o conselheiro Gary Chapman propôs que as pessoas expressam e recebem amor de '
    'cinco formas primárias, às quais chamou de linguagens do amor. A teoria revelou algo '
    'fundamental: quando você expressa amor de uma forma e o outro recebe de outra, ambos '
    'podem sentir que não são amados, mesmo que os dois estejam tentando.'
)
CAP12_INTRO2 = (
    'O signo solar, a posição de Vênus é o elemento dominante influenciam fortemente qual '
    'linguagem cada pessoa usa naturalmente. Conhecer sua linguagem ajuda você a pedir o que '
    'precisa. Conhecer a do outro ajuda você a dar o que realmente importa.'
)
CAP12_LINGUAGENS = (
    'As 5 linguagens: Palavras de afirmação · Tempo de qualidade · Presentes · '
    'Atos de serviço · Toque físico'
)

LINGUAGENS_AMOR = [
    (
        'Áries', 'Toque físico + Palavras de afirmação',
        (
            'Áries demonstra amor com ação imediata, aparece, se move em direção ao outro, '
            'inicia o contato físico. Também expressa amor com afirmações diretas e entusiasmadas: '
            'não faz rodeios para dizer que admira o parceiro.'
        ),
        (
            'Precisa de reconhecimento verbal claro, que digam, sem rodeios, o que significa '
            'para o outro. Também responde muito ao contato físico iniciado pelo parceiro; ser '
            'procurado físicamente é uma declaração de desejo que ressoa mais fundo do que flores. '
            'Pode se sentir não amado quando o parceiro é verbal mas não físico.'
        )
    ),
    (
        'Touro', 'Toque físico + Presentes',
        (
            'Touro demonstra amor através do corpo, toque prolongado, abraços, contato físico '
            'constante e sem urgência. Também expressa amor materialmente: presentes '
            'cuidadosamente escolhidos, comida preparada com atenção, o ambiente organizado '
            'para o bem-estar do outro.'
        ),
        (
            'Precisa de toque físico consistente e presença real, videoconferências não '
            'satisfazem. Também responde a gestos materiais concretos que demonstrem que o '
            'parceiro pensou nele. A falta de toque pode ser interpretada como falta de '
            'interesse, mas Touro raramente pede diretamente.'
        )
    ),
    (
        'Gêmeos', 'Palavras de afirmação + Tempo de qualidade',
        (
            'Gêmeos ama com a mente, conversas longas e estimulantes, mensagens criativas, '
            'piadas privadas, referências que só fazem sentido entre os dois. Também expressa '
            'amor compartilhando seu mundo intelectual: livros, ideias, descobertas.'
        ),
        (
            'Precisa de conversação real, não check-ins de rotina, mas diálogo genuíno onde '
            'se sente escutado e estimulado. Pode se sentir não amado quando o parceiro é '
            'físicamente presente mas mentalmente ausente. O silêncio prolongado é '
            'emocionalmente pesado para Gêmeos.'
        )
    ),
    (
        'Câncer', 'Tempo de qualidade + Atos de serviço',
        (
            'Câncer demonstra amor cuidando, prepara a refeição favorita, lembra de detalhes, '
            'aparece quando o parceiro está mal sem precisar ser chamado. Ama com presença total: '
            'tempo compartilhado em casa, rituais cotidianos, criar um espaço que pertence '
            'aos dois.'
        ),
        (
            'Precisa de presença, não apenas companhia física, mas atenção emocional genuína. '
            'Responde profundamente a atos de serviço que demonstrem cuidado com seus estados '
            'internos. Raramente pede o que precisa diretamente, espera que o parceiro perceba, '
            'e quando não percebe, interpreta como falta de amor.'
        )
    ),
    (
        'Leão', 'Palavras de afirmação + Presentes',
        (
            'Leão ama de forma grandiosa, planejamento elaborado, surpresas teatrais, gestos '
            'que tornam o outro o centro do mundo. Expressa amor com elogios generosos e '
            'afirmações frequentes sobre o que torna o parceiro especial.'
        ),
        (
            'Precisa de reconhecimento verbal genuíno, não elogios genéricos, mas '
            'reconhecimento específico do que o faz único. Também responde a presentes e '
            'gestos que mostram que o parceiro investiu criatividade. Para Leão, a qualidade '
            'do elogio importa mais do que a quantidade.'
        )
    ),
    (
        'Virgem', 'Atos de serviço + Tempo de qualidade',
        (
            'Virgem demonstra amor sendo útil, resolve o problema que ninguém mais viu, '
            'organiza o que estava caótico, aparece com a solução antes do pedido. Seu cuidado '
            'é prático e concreto, não poético.'
        ),
        (
            'Precisa de atos de serviço que mostrem atenção aos detalhes do dia a dia, não '
            'grandes gestos, mas pequenas consistências. Responde ao tempo de qualidade que '
            'inclui conversa focada e presença real. Frequentemente expressa amor da forma que '
            'gostaria de receber, por isso pode se sentir não amado quando o parceiro é '
            'verbal mas não prático.'
        )
    ),
    (
        'Libra', 'Palavras de afirmação + Tempo de qualidade',
        (
            'Libra demonstra amor com elegância verbal, escolhe as palavras certas, no '
            'momento certo, com o tom certo. Também expressa amor criando experiências '
            'compartilhadas belas: jantares cuidadosamente escolhidos, atividades que '
            'os dois desfrutam.'
        ),
        (
            'Precisa de afirmação verbal consistente, não apenas "te amo" mas "aqui está '
            'o que eu amo em você". Também precisa de tempo de qualidade onde o parceiro '
            'está presente de verdade. Pode sustentar a harmonia por muito tempo sem '
            'revelar o que precisa, até que o acúmulo explode.'
        )
    ),
    (
        'Escorpião', 'Toque físico + Tempo de qualidade',
        (
            'Escorpião demonstra amor com presença intensa, olhar fixo, toque cheio de '
            'intenção, atenção total ao outro. Sua forma de amar exclui o resto do mundo. '
            'Também expressa amor com conversas profundas que revelam camadas normalmente '
            'escondidas.'
        ),
        (
            'Precisa de presença total, não de alguém que está lá mas com a mente em '
            'outro lugar. O toque físico significativo, não casual,é fundamental. '
            'Detecta quando o parceiro está físicamente presente mas emocionalmente '
            'ausente, e interpreta isso como desonestidade.'
        )
    ),
    (
        'Sagitário', 'Tempo de qualidade + Palavras de afirmação',
        (
            'Sagitário demonstra amor convidando o outro para suas aventuras, viagens, '
            'novas experiências, conversas que expandem perspectivas. Também expressa amor '
            'com generosidade intelectual: compartilha o que sabe, o que descobriu, '
            'o que o entusiasma.'
        ),
        (
            'Precisa de parceiro que queira explorar o mundo junto. Responde a afirmações '
            'que reconhecem sua originalidade e sua visão de mundo específica. Pode '
            'interpretar um parceiro repetitivo ou caseiro como alguém que não quer crescer, '
            'criando distância gradual sem conflito explícito.'
        )
    ),
    (
        'Capricórnio', 'Atos de serviço + Tempo de qualidade',
        (
            'Capricórnio demonstra amor sendo confiável, aparece quando prometeu, resolve '
            'o que precisa ser resolvido, suporta o peso prático da vida compartilhada. '
            'Seu amor é construído, não declarado.'
        ),
        (
            'Precisa de consistência e comprometimento de longo prazo, ações que demonstrem '
            'que o parceiro está sério. Não precisa de gestos poéticos, mas de evidências de '
            'que é uma prioridade real. Raramente declara o que precisa; prefere observar '
            'ações ao longo do tempo.'
        )
    ),
    (
        'Aquário', 'Tempo de qualidade + Palavras de afirmação',
        (
            'Aquário demonstra amor intelectualmente, compartilha ideias profundas, leva o '
            'parceiro para conversas que expandem, cria projetos comuns com significado '
            'além do casal.'
        ),
        (
            'Precisa de parceiro que respeite e verbalize respeito pela sua forma única de '
            'ser. Responde ao tempo de qualidade onde os dois exploram juntos. Pode confundir '
            'o parceiro que espera demonstrações convencionais, aprender a nomear o próprio '
            'afeto é uma habilidade que vale desenvolver.'
        )
    ),
    (
        'Peixes', 'Toque físico + Atos de serviço',
        (
            'Peixes demonstra amor com totalidade, entrega presença sem reservas, absorve '
            'o mundo emocional do outro, oferece cuidado que frequentemente vai além do '
            'que o outro pede.'
        ),
        (
            'Precisa de toque físico com presença emocional real, não contato mecânico, '
            'mas contato intencionado. Responde profundamente a atos de serviço que mostrem '
            'que o parceiro viu sua necessidade sem que precisasse pedi-la. Pode facilmente '
            'dar muito mais do que recebe, e raramente se queixa até estar exausto.'
        )
    ),
]

# ══════════════════════════════════════════════════════════════════════════════
#  CAPÍTULO 13: COMO CADA SIGNO LIDA COM TÉRMINOS E REJEIÇÃO
# ══════════════════════════════════════════════════════════════════════════════

CAP13_INTRO = (
    'O fim de um relacionamento é um dos momentos mais psicologicamente reveladores da vida. '
    'Nele, as defesas caem, os padrões de apego ficam visíveis, e o signo faz jus, ou não, '
    'à sua natureza mais profunda. Não existe uma forma certa de lidar com a perda afetiva, '
    'mas cada signo tem tendências características que, quando reconhecidas, podem ser '
    'trabalhadas de forma mais consciente.'
)
CAP13_INTRO2 = (
    'O que importa não é a velocidade da recuperação, mas a qualidade dela: o que você aprende '
    'sobre si mesmo no processo, e como esse conhecimento muda o que você busca a seguir.'
)

TERMINOS = [
    (
        'Áries',
        (
            'Áries reage à rejeição com intensidade imediata, raiva, movimento, ação. '
            'Pode enviar mensagens que depois lamenta, confrontar o ex, ou mergulhar em '
            'projetos com energia que impressiona e assusta ao mesmo tempo. O luto de '
            'Áries é ativo: não consegue ficar parado enquanto dói.'
        ),
        (
            'A recuperação costuma ser mais rápida do que a de outros signos, não porque '
            'sente menos, mas porque transforma a dor em movimento. O risco é que a '
            'rapidez máscara processamento que ainda não aconteceu. Novos relacionamentos '
            'iniciados cedo demais como forma de evitar o luto real são o principal '
            'perigo de Áries no pós-término.'
        )
    ),
    (
        'Touro',
        (
            'Touro reage ao término com silêncio e negação. Pode demorar para aceitar que '
            'acabou, especialmente se investiu muito. Nos primeiros dias, pode tentar '
            'restabelecer a rotina como se nada tivesse mudado, ou persistir em manter '
            'contato esperando uma reversão que não vem.'
        ),
        (
            'O processo de recuperação é lento e profundo. Touro não apaga; acumula. '
            'Mudar o ambiente físico, a casa, a rotina, os hábitos compartilhados,é '
            'frequentemente o que sinaliza o início real do luto interno. A ruminação '
            'prolongada e a dificuldade de aceitar que o outro já seguiu em frente são '
            'os maiores riscos.'
        )
    ),
    (
        'Gêmeos',
        (
            'Gêmeos processa pela palavra, fala com todos, escreve, analisa. Pode '
            'parecer recuperado muito antes de realmente estar, porque tem facilidade de '
            'criar narrativas convincentes sobre o que aconteceu. A racionalização é '
            'eficiente mas pode deixar a emoção não processada.'
        ),
        (
            'Precisa encontrar novos estímulos para substituir o vazio deixado pelo '
            'outro. Livros, viagens, novas amizades, tudo que alimenta a mente. '
            'O risco é usar o intelecto para evitar a dor emocional, iniciando '
            'relacionamentos novos precocemente sem ter entendido o que terminou.'
        )
    ),
    (
        'Câncer',
        (
            'Câncer sente profundamente, e demonstra. Chora, recolhe-se, revisita '
            'memórias. Pode entrar em modo de cuidado excessivo com outros como forma '
            'de evitar o próprio luto. Ou fazer o oposto: isolar-se completamente '
            'na concha protetora que conhece tão bem.'
        ),
        (
            'O processo é não-linear. Pode parecer superado, depois uma música ou um '
            'objeto traz tudo de volta. Aceitar essa não-linearidade é parte do caminho. '
            'O maior risco é idealizar o ex ou retornar a relacionamentos que já '
            'terminaram por medo do desconhecido.'
        )
    ),
    (
        'Leão',
        (
            'A rejeição fere o orgulho de Leão de forma particularmente profunda. '
            'A primeira reação pode ser dramática, postagens que demonstram o quanto '
            'está bem (quando não está), ou uma queda súbita no que parece ser '
            'confiança inabalável. Por baixo, a pergunta que tortura: "O que tem '
            'de errado comigo?"'
        ),
        (
            'Leão se recupera quando encontra espaços onde pode voltar a brilhar. '
            'Projetos criativos, reconhecimento externo, não para substituir, mas '
            'para relembrar quem é além do relacionamento. O risco é encobrir a dor '
            'com uma fachada de superação, ou iniciar novos relacionamentos por '
            'necessidade de plateia, não de conexão real.'
        )
    ),
    (
        'Virgem',
        (
            'Virgem analisa. Imediatamente, meticulosamente, exaustivamente. Tenta '
            'entender cada etapa de onde deu errado, o que poderia ter feito diferente, '
            'qual foi o erro. Essa análise pode ser útil, ou pode se tornar uma forma '
            'sofisticada de autopunição.'
        ),
        (
            'Virgem se recupera reconstruindo a rotina e o senso de controle. O trabalho '
            'e os projetos práticos são âncoras. O maior risco é a autocrítica excessiva: '
            'ficar preso no loop de "o que eu fiz de errado" sem chegar a conclusões '
            'que realmente movem para frente.'
        )
    ),
    (
        'Libra',
        (
            'A primeira resposta de Libra pode surpreender: frequentemente fica em cima '
            'do muro por muito tempo, tentando manter uma relação amigável com o ex '
            'enquanto ainda sente dor. Evita o conflito mesmo quando a separação ocorre '
            'e pode demorar para nomear o quanto está sofrendo.'
        ),
        (
            'Libra processa relacionalmente, precisa de pessoas próximas com quem '
            'compartilhar e refletir. O isolamento não funciona para este signo. '
            'O risco principal é iniciar um novo relacionamento antes de processar o '
            'anterior, ou tender a culpar apenas a si mesmo pelo que terminou.'
        )
    ),
    (
        'Escorpião',
        (
            'Escorpião não mostra a dor, mas ela existe com uma intensidade que poucos '
            'outros signos conhecem. A reação externa pode variar: retraimento total, '
            'frieza calculada, ou, nos casos mais difíceis, comportamentos que beiram '
            'a obsessão. Internamente, o luto de Escorpião é alquímico: transforma.'
        ),
        (
            'O processo é longo e não-linear, mas quando Escorpião completa, emerge '
            'diferente, mais sábio, mais profundo, mais inteiro. O desafio é atravessar '
            'o processo sem destruir o ex, a si mesmo ou ambos. Cortar o contato '
            'completamente por um período é quase sempre necessário.'
        )
    ),
    (
        'Sagitário',
        (
            'Sagitário foge, literalmente, se possível. Uma viagem, um projeto novo, '
            'uma filosofia que explica por que tudo aconteceu como deveria. A primeira '
            'resposta é movimento e ressignificação, não sempre sentimento genuíno '
            'do que se perdeu.'
        ),
        (
            'A recuperação é rápida na superfície, mais lenta na profundidade. Sagitário '
            'pode estar em outro país antes de ter realmente processado o luto. A leveza '
            'genuína retorna quando encontra novamente o senso de propósito e expansão, '
            'mas o risco é romantizar o futuro antes de entender o passado.'
        )
    ),
    (
        'Capricórnio',
        (
            'Capricórnio internaliza. Raramente vai ao choro ou ao drama, o que os '
            'outros veem é uma máscara de continuidade funcional. Trabalha mais, produz '
            'mais, é mais eficiente. Por baixo, carrega o peso em silêncio e sozinho.'
        ),
        (
            'A recuperação é gradual e estruturada. A dor não desaparece mais rápido, '
            'mas vai sendo integrada lentamente junto à rotina. O risco é usar o '
            'trabalho como anestésico sem jamais processar o luto, e se fechar para '
            'novos relacionamentos por um período longo demais.'
        )
    ),
    (
        'Aquário',
        (
            'Aquário se destaca, às vezes literalmente. Pode demonstrar uma frieza que '
            'surpreende o próprio parceiro: "já analisei e concluí que é o melhor para '
            'os dois". Pode ser verdade. Mas frequentemente é uma dissociação intelectual '
            'da dor que ainda não foi processada.'
        ),
        (
            'Aquário processa em solidão e a seu próprio ritmo. Causas, projetos e '
            'grupos de interesse são âncoras importantes. O risco é convencer a si '
            'mesmo de que está bem quando ainda não está, é uma desconexão emocional '
            'que pode durar mais do que necessário.'
        )
    ),
    (
        'Peixes',
        (
            'Peixes dissolve, nas emoções, no choro, na música, nos sonhos. A dor '
            'não tem contornos claros: é uma onda que envolve tudo. Pode cair na '
            'fantasia: idealizar o ex, reimaginar como poderia ter sido, criar mundos '
            'alternativos onde o relacionamento não terminou.'
        ),
        (
            'O processo é não-linear e frequentemente longo. Peixes precisa de tempo '
            'real, não de conselhos para "seguir em frente", mas de espaço para sentir '
            'sem ser apressado. O risco é o retorno a relacionamentos que terminaram por '
            'medo do vazio, ou o uso de comportamentos escapistas como anestesia.'
        )
    ),
]

# ══════════════════════════════════════════════════════════════════════════════
#  CAPÍTULO 14: GATILHOS EMOCIONAIS POR ELEMENTO
# ══════════════════════════════════════════════════════════════════════════════

CAP14_INTRO = (
    'Um gatilho emocional é aquilo que, de fora, parece desproporcional, mas que, por dentro, '
    'ativa uma camada de vulnerabilidade antiga. Entender seus gatilhos não significa eliminá-los: '
    'significa reconhecê-los antes que controlem sua resposta.'
)
CAP14_INTRO2 = (
    'Cada elemento tem sensibilidades características, situações, comportamentos ou dinâmicas que '
    'disparam uma reação emocional intensa. Conhecê-los permite separar o que é reação automática '
    'do que é resposta consciente.'
)

GATILHOS = [
    (
        'Fogo: Áries, Leão e Sagitário',
        (
            'Os signos de fogo são ativados quando sua autonomia, seu senso de identidade '
            'ou sua liberdade são ameaçados. Ser controlado, limitado ou tratado como se '
            'não fosse capaz de decidir por si mesmo é intolerável para o fogo. A reação '
            'é intensa e imediata, explosão verbal, confronto direto, ou abandono da '
            'situação. O fogo precisa sentir que têm espaço para ser ele mesmo; quando '
            'esse espaço é tirado, responde como uma chama pressionada: ela aumenta.'
        ),
        (
            'Ser ignorado, tratado como comum, ou ter suas contribuições minimizadas '
            'também ativa o fogo de forma profunda, especialmente Leão. O fogo '
            'fundamentalmente precisa sentir que sua presença importa. Quando sente que '
            'não importa, a reação varia entre uma performance maior (para garantir '
            'atenção) é um recuo orgulhoso. Como apoiar: dar espaço físico imediato; '
            'não pressionar por análise emocional no momento da crise; reconhecer a '
            'intensidade sem amplificá-la; retornar ao diálogo quando a temperatura baixar.'
        )
    ),
    (
        'Terra: Touro, Virgem e Capricórnio',
        (
            'Os signos de terra são ativados quando seu senso de segurança, controle ou '
            'competência é ameaçado. Terra precisa de chão firme, literalmente. Mudanças '
            'abruptas de planos, inconsistência emocional no parceiro, ou qualquer situação '
            'que tire o controle da terra de sua própria vida ativa um estado de alarme '
            'silencioso mas intenso. A reação raramente é dramática; é contida, e '
            'justamente por isso pode durar mais.'
        ),
        (
            'Ter a competência questionada ou ser tratado como se não soubesse o que está '
            'fazendo é profundamente desestabilizador para terra, especialmente Virgem e '
            'Capricórnio. Sua identidade está ancorada em grande parte na capacidade de '
            'fazer as coisas bem. Quando isso é atacado, a resposta pode ser defensividade '
            'ou retraimento prolongado. Como apoiar: respeitar o silêncio sem interpretá-lo '
            'como rejeição; oferecer estabilidade concreta; não forçar conversa imediata; '
            'reconhecer o esforço e a competência.'
        )
    ),
    (
        'Ar: Gêmeos, Libra e Aquário',
        (
            'Os signos de ar são ativados quando sua liberdade mental, sua racionalidade '
            'ou sua independência são ameaçadas. O ar precisa de espaço para pensar. '
            'Quando é bombardeado com demandas emocionais intensas, com parceiros que '
            'precisam de constante reasseguramento, ou com situações onde se espera que '
            'abandone a análise em favor do sentimento, o ar entra em modo de evasão. '
            'Não é frieza, é sobrecarga de um tipo específico.'
        ),
        (
            'Situações que parecem injustas ou irracionais também são ativadoras profundas, '
            'especialmente para Libra e Aquário. O ar não suporta bem a arbitrariedade: '
            'decisões tomadas por pura emoção sem lógica, regras que não fazem sentido, '
            'comportamentos que contradizem o que foi acordado. Como apoiar: dar espaço '
            'físico e mental; oferecer explicações lógicas; não exigir expressão emocional '
            'imediata; manter o tom conversacional, não confrontacional.'
        )
    ),
    (
        'Água: Câncer, Escorpião e Peixes',
        (
            'Os signos de água são ativados quando sua segurança emocional, sua confiança '
            'ou seu sentido de pertencimento são ameaçados. Para a água, especialmente '
            'Escorpião e Câncer, a traição não precisa ser explícita para ativar uma '
            'resposta intensa. Uma pequena inconsistência, uma meia-verdade, um segredo '
            'descoberto: tudo isso aciona o sistema de alarme de forma que parece '
            'desproporcional para quem está de fora, mas completamente proporcional '
            'para quem está dentro. A água tem memória emocional longa.'
        ),
        (
            'Ser tratado com frieza quando está vulnerável, ter suas emoções minimizadas '
            '("você é muito sensível"), ou sentir que o outro não está realmente presente '
            'emocionalmente, tudo isso ativa a água de forma profunda. A resposta pode '
            'ser retraimento completo (Escorpião na defensiva, Câncer na concha) ou '
            'dissolução emocional (Peixes). Como apoiar: presença emocional real, não '
            'apenas física; validação do sentimento antes de qualquer análise; contato '
            'físico gentil; paciência com o tempo de processamento; não pressionar '
            'por resolução rápida.'
        )
    ),
]

# ══════════════════════════════════════════════════════════════════════════════
#  BUILD
# ══════════════════════════════════════════════════════════════════════════════

def build():
    out = (r'c:\Users\Heitor Melo\Desktop\Grana no Digital\Astrologia'
           r'\O_Guia_Emocional_dos_Signos_PARTE4.pdf')
    doc = SimpleDocTemplate(
        out, pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=1.8*cm, bottomMargin=1.8*cm,
    )
    S = make_styles()
    story = []

    # ── CAPA DA PARTE 4 ──────────────────────────────────────────────────────
    story.append(DarkPage(
        'Padrões Emocionais\nProfundos',
        'Por que você se apaixona sempre pelo mesmo tipo\n'
        'Estilos de apego · Linguagens do amor\n'
        'Términos · Gatilhos emocionais',
        'PARTE IV'
    ))
    story.append(PageBreak())

    # ── CAP 10 ───────────────────────────────────────────────────────────────
    story.append(Paragraph('CAPÍTULO 10', S['chapter_tag']))
    story.append(Paragraph(
        'Por que Você se Apaixona\nSempre pelo Mesmo Tipo', S['chapter_title']))
    story.append(hr())
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(CAP10_INTRO,  S['body']))
    story.append(Paragraph(CAP10_INTRO2, S['body']))

    for titulo, p1, p2 in CAP10_SECOES:
        story.append(KeepTogether([
            Spacer(1, 0.2*cm),
            Paragraph(titulo, S['section_title']),
            Paragraph(p1, S['body']),
            Paragraph(p2, S['body']),
        ]))

    story.append(PageBreak())

    # ── CAP 11 ───────────────────────────────────────────────────────────────
    story.append(Paragraph('CAPÍTULO 11', S['chapter_tag']))
    story.append(Paragraph('Estilos de Apego por Signo', S['chapter_title']))
    story.append(hr())
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(CAP11_INTRO,  S['body']))
    story.append(Paragraph(CAP11_INTRO2, S['body']))
    story.append(Spacer(1, 0.3*cm))

    for signo, estilo, p1, p2, trigger, calmer, path in ESTILOS_APEGO:
        story.append(KeepTogether([
            Paragraph(signo, S['sign_title']),
            Paragraph(estilo, S['sub']),
            Paragraph(p1, S['body']),
            Paragraph(p2, S['body']),
            Paragraph('Gatilho principal: ' + trigger, S['label']),
            Paragraph('O que acalma: ' + calmer, S['label']),
            Paragraph('Caminho de crescimento: ' + path, S['label']),
            Spacer(1, 0.1*cm),
        ]))

    story.append(PageBreak())

    # ── CAP 12 ───────────────────────────────────────────────────────────────
    story.append(Paragraph('CAPÍTULO 12', S['chapter_tag']))
    story.append(Paragraph('Linguagens do Amor\ndos 12 Signos', S['chapter_title']))
    story.append(hr())
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(CAP12_INTRO,  S['body']))
    story.append(Paragraph(CAP12_INTRO2, S['body']))
    story.append(Paragraph(CAP12_LINGUAGENS, S['sub']))
    story.append(Spacer(1, 0.3*cm))

    for signo, linguagem, expressão, recepcao in LINGUAGENS_AMOR:
        story.append(KeepTogether([
            Paragraph(signo, S['sign_title']),
            Paragraph(linguagem, S['sub']),
            Paragraph('Como expressa amor: ' + expressão, S['body']),
            Paragraph('Como precisa receber: ' + recepcao, S['body']),
            Spacer(1, 0.1*cm),
        ]))

    story.append(PageBreak())

    # ── CAP 13 ───────────────────────────────────────────────────────────────
    story.append(Paragraph('CAPÍTULO 13', S['chapter_tag']))
    story.append(Paragraph(
        'Como Cada Signo Lida\ncom Términos e Rejeição', S['chapter_title']))
    story.append(hr())
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(CAP13_INTRO,  S['body']))
    story.append(Paragraph(CAP13_INTRO2, S['body']))
    story.append(Spacer(1, 0.3*cm))

    for signo, reação, recuperação in TERMINOS:
        story.append(KeepTogether([
            Paragraph(signo, S['sign_title']),
            Paragraph(reação,      S['body']),
            Paragraph(recuperação, S['body']),
            Spacer(1, 0.1*cm),
        ]))

    story.append(PageBreak())

    # ── CAP 14 ───────────────────────────────────────────────────────────────
    story.append(Paragraph('CAPÍTULO 14', S['chapter_tag']))
    story.append(Paragraph(
        'Gatilhos Emocionais\npor Elemento', S['chapter_title']))
    story.append(hr())
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(CAP14_INTRO,  S['body']))
    story.append(Paragraph(CAP14_INTRO2, S['body']))
    story.append(Spacer(1, 0.3*cm))

    for elemento, p1, p2 in GATILHOS:
        story.append(KeepTogether([
            Paragraph(elemento, S['section_title']),
            Paragraph(p1, S['body']),
            Paragraph(p2, S['body']),
            Spacer(1, 0.2*cm),
        ]))

    doc.build(story, onFirstPage=content_page, onLaterPages=content_page)
    print(f'PARTE4 gerada: {out}')

build()
