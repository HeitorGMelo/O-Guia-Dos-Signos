#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Guia Completo de Marketing Digital — Ebook de Astrologia
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

NAVY    = colors.HexColor('#0F1923')
GOLD    = colors.HexColor('#C9A96E')
RED     = colors.HexColor('#C0392B')
GREEN   = colors.HexColor('#27AE60')
BLUE    = colors.HexColor('#2980B9')
PURPLE  = colors.HexColor('#8E44AD')
CREAM   = colors.HexColor('#FAF7F0')
DARK    = colors.HexColor('#2A2540')
GRAY    = colors.HexColor('#8A8598')
LGRAY   = colors.HexColor('#F0EDE8')

W, H = A4
LM = 2*cm
BM = 1.8*cm


class CoverPage(Flowable):
    def wrap(self, aw, ah): return (aw, ah)
    def draw(self):
        c = self.canv
        c.saveState()
        c.translate(-LM, -BM)
        c.setFillColor(NAVY)
        c.rect(0, 0, W, H, fill=1, stroke=0)
        c.setFillColor(GOLD)
        c.setLineWidth(1)
        c.setStrokeColor(GOLD)
        c.line(2*cm, H-1.5*cm, W-2*cm, H-1.5*cm)
        c.line(2*cm, 1.5*cm,   W-2*cm, 1.5*cm)
        c.setFont('Georgia-Bold', 11)
        c.drawCentredString(W/2, H*0.75, 'GUIA COMPLETO DE MARKETING DIGITAL')
        c.setFont('Georgia-Bold', 36)
        c.drawCentredString(W/2, H*0.62, 'Vender muito:')
        c.setFont('Georgia-Bold', 34)
        c.drawCentredString(W/2, H*0.53, 'A Estratégia')
        c.setFont('Georgia-Ital', 14)
        c.setFillColor(GRAY)
        c.drawCentredString(W/2, H*0.44, 'Para o Guia Emocional dos Signos')
        c.drawCentredString(W/2, H*0.40, 'Funil · Conteúdo · Anúncios · Conversão')
        c.setFillColor(GOLD)
        cx, cy = W/2, 1.8*cm
        s = 5
        p = c.beginPath()
        p.moveTo(cx,cy+s); p.lineTo(cx+s,cy); p.lineTo(cx,cy-s); p.lineTo(cx-s,cy); p.close()
        c.drawPath(p, fill=1, stroke=0)
        c.restoreState()


def page_bg(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(CREAM)
    canvas.rect(0, 0, W, H, fill=1, stroke=0)
    canvas.setFillColor(NAVY)
    canvas.rect(0, H-0.35*cm, W, 0.35*cm, fill=1, stroke=0)
    canvas.setFont('Georgia', 8)
    canvas.setFillColor(GRAY)
    canvas.drawCentredString(W/2, 0.6*cm, 'Guia de Marketing — O Guia Emocional dos Signos')
    canvas.setFillColor(GOLD)
    canvas.drawRightString(W-2*cm, 0.6*cm, str(doc.page))
    canvas.restoreState()


def make_styles():
    s = {}
    s['h1'] = ParagraphStyle('h1', fontName='Georgia-Bold', fontSize=24,
        textColor=DARK, spaceAfter=6, leading=30)
    s['h2'] = ParagraphStyle('h2', fontName='Georgia-Bold', fontSize=15,
        textColor=DARK, spaceBefore=16, spaceAfter=4, leading=19)
    s['h3'] = ParagraphStyle('h3', fontName='Georgia-Bold', fontSize=12,
        textColor=DARK, spaceBefore=10, spaceAfter=3, leading=16)
    s['body'] = ParagraphStyle('body', fontName='Georgia', fontSize=10.5,
        textColor=DARK, spaceAfter=7, leading=16, alignment=TA_JUSTIFY)
    s['tag'] = ParagraphStyle('tag', fontName='Georgia', fontSize=8,
        textColor=GOLD, spaceAfter=4, leading=10)
    s['bullet'] = ParagraphStyle('bullet', fontName='Georgia', fontSize=10.5,
        textColor=DARK, spaceAfter=4, leading=16,
        leftIndent=14, firstLineIndent=-10)
    s['insight'] = ParagraphStyle('insight', fontName='Georgia-Ital', fontSize=11,
        textColor=DARK, spaceAfter=0, leading=16, alignment=TA_CENTER,
        leftIndent=16, rightIndent=16)
    s['warn'] = ParagraphStyle('warn', fontName='Georgia-Bold', fontSize=10.5,
        textColor=RED, spaceAfter=4, leading=15)
    s['green'] = ParagraphStyle('green', fontName='Georgia-Bold', fontSize=10.5,
        textColor=GREEN, spaceAfter=4, leading=15)
    s['label'] = ParagraphStyle('label', fontName='Georgia-Bold', fontSize=9,
        textColor=NAVY, spaceAfter=2, leading=11)
    s['center'] = ParagraphStyle('center', fontName='Georgia', fontSize=10.5,
        textColor=DARK, spaceAfter=7, leading=16, alignment=TA_CENTER)
    return s


def hr(color=GOLD):
    return HRFlowable(width='100%', thickness=0.5, color=color, spaceAfter=8, spaceBefore=4)

def box(text, S, bg=None, border=GOLD):
    bg = bg or colors.HexColor('#F5F0E8')
    p = Paragraph(text, S['insight'])
    t = Table([[p]], colWidths=[14.5*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0),(-1,-1), bg),
        ('BOX',        (0,0),(-1,-1), 1, border),
        ('LEFTPADDING', (0,0),(-1,-1), 14),
        ('RIGHTPADDING',(0,0),(-1,-1), 14),
        ('TOPPADDING',  (0,0),(-1,-1), 10),
        ('BOTTOMPADDING',(0,0),(-1,-1),10),
    ]))
    return t

def table2(rows, widths, S, header_bg=NAVY):
    data = []
    for i, row in enumerate(rows):
        data.append([Paragraph(cell, S['label'] if i==0 else S['body']) for cell in row])
    t = Table(data, colWidths=widths)
    style = [
        ('BACKGROUND', (0,0),(-1,0), header_bg),
        ('TEXTCOLOR',  (0,0),(-1,0), colors.white),
        ('FONTNAME',   (0,0),(-1,0), 'Georgia-Bold'),
        ('FONTSIZE',   (0,0),(-1,0), 9),
        ('BACKGROUND', (0,1),(-1,-1), LGRAY),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[LGRAY, CREAM]),
        ('BOX',        (0,0),(-1,-1), 0.5, GRAY),
        ('INNERGRID',  (0,0),(-1,-1), 0.3, GRAY),
        ('LEFTPADDING', (0,0),(-1,-1), 6),
        ('RIGHTPADDING',(0,0),(-1,-1), 6),
        ('TOPPADDING',  (0,0),(-1,-1), 5),
        ('BOTTOMPADDING',(0,0),(-1,-1),5),
        ('VALIGN',     (0,0),(-1,-1), 'TOP'),
    ]
    t.setStyle(TableStyle(style))
    return t

def bul(text, S):
    return Paragraph(f'◆  {text}', S['bullet'])

def build():
    out = (r'c:\Users\Heitor Melo\Desktop\Grana no Digital\Astrologia'
           r'\GUIA_MARKETING_EBOOK_ASTROLOGIA.pdf')
    doc = SimpleDocTemplate(out, pagesize=A4,
        leftMargin=LM, rightMargin=LM, topMargin=BM, bottomMargin=BM)
    S = make_styles()
    story = []

    # ════════════ CAPA ════════════
    story.append(CoverPage())
    story.append(PageBreak())

    # ════════════ SUMÁRIO ════════════
    story.append(Paragraph('ÍNDICE', S['tag']))
    story.append(Paragraph('O que está neste guia', S['h1']))
    story.append(hr())
    toc = [
        ('1.', 'O Mercado e o Público — quem compra e por quê'),
        ('2.', 'O Funil de Vendas — da descoberta à compra'),
        ('3.', 'Estratégia por Plataforma — onde e como estar'),
        ('4.', 'Posts que Convertem — formatos e scripts'),
        ('5.', 'WikiHow e SEO — tráfego orgânico que vende'),
        ('6.', 'Email Marketing — o ativo mais valioso'),
        ('7.', 'Anúncios Pagos — Meta Ads que retornam'),
        ('8.', 'Cronograma de Lançamento — 30 dias para vender'),
        ('9.', 'Métricas que importam — o que medir'),
        ('10.','Os erros que destroem conversão'),
    ]
    for num, titulo in toc:
        story.append(Paragraph(f'<b>{num}</b>  {titulo}', S['body']))
    story.append(PageBreak())

    # ════════════ CAP 1 — MERCADO E PÚBLICO ════════════
    story.append(Paragraph('CAPÍTULO 1', S['tag']))
    story.append(Paragraph('O Mercado e o Público', S['h1']))
    story.append(hr())
    story.append(Paragraph(
        'Antes de criar qualquer conteúdo ou anúncio, você precisa saber exatamente '
        'com quem está falando. Astrologia é um dos nichos de maior crescimento no '
        'digital: buscas por "mapa astral", "compatibilidade de signos" e "significado '
        'de ascendente" cresceram mais de 300% entre 2018 e 2024. O mercado já existe '
        'e está com fome. Sua tarefa é aparecer na frente dele.', S['body']))

    story.append(Paragraph('Quem é o comprador ideal', S['h2']))
    story.append(Paragraph(
        'O comprador do Guia Emocional dos Signos não é o "fã de astrologia" genérico. '
        'É uma pessoa específica, e você precisa conhecê-la melhor do que ela se conhece:', S['body']))
    for item in [
        'Mulher entre 18 e 38 anos (representa 70–80% do público de astrologia digital)',
        'Está em um momento de questionamento: relacionamento difícil, término recente, busca de identidade',
        'Já consumiu conteúdo de astrologia gratuitamente (Instagram, TikTok, YouTube)',
        'Crê que "tem algo a mais" que o horóscopo do jornal mas ainda não encontrou o quê',
        'Tem renda própria e gasta em autoconhecimento (livros, terapia, cursos, apps)',
        'Compartilha conteúdo de astrologia com amigas — é influenciadora informal do nicho',
        'Toma decisões de compra por impulso emocional validado por prova social',
    ]:
        story.append(bul(item, S))

    story.append(Paragraph('O que a faz comprar', S['h2']))
    story.append(Paragraph(
        'Ela não compra astrologia. Ela compra a sensação de ser completamente entendida. '
        'Compra a resposta para "por que eu sou assim" e "por que eu me apaixono sempre '
        'pelo mesmo tipo". O ebook resolve uma dor emocional real com uma linguagem que '
        'já é familiar para ela. Isso é ouro em marketing.', S['body']))
    story.append(box(
        '"Ela não quer aprender sobre Marte em Escorpião. Ela quer entender '
        'por que o ex dela era tão intenso e por que ela sempre cai nesse padrão." '
        'Quando você escreve para essa dor específica, a conversão explode.', S))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph('Tamanho do mercado no Brasil', S['h2']))
    story.append(table2([
        ['Indicador', 'Dado'],
        ['Buscas mensais: "mapa astral"', '~ 450.000 no Brasil'],
        ['Buscas mensais: "signos e amor"', '~ 200.000 no Brasil'],
        ['Seguidores top 10 perfis astro BR', '> 15 milhões combinados'],
        ['Apps de astrologia (downloads BR 2023)', '> 8 milhões'],
        ['Ticket médio de infoprodutos no nicho', 'R$ 27 – R$ 197'],
        ['Taxa de conversão típica (funil aquecido)', '2–5%'],
    ], [7*cm, 8*cm], S))
    story.append(PageBreak())

    # ════════════ CAP 2 — FUNIL ════════════
    story.append(Paragraph('CAPÍTULO 2', S['tag']))
    story.append(Paragraph('O Funil de Vendas', S['h1']))
    story.append(hr())
    story.append(Paragraph(
        'A maioria dos criadores de conteúdo tenta vender para pessoas frias — '
        'que nunca ouviram falar deles. Resultado: 0,1% de conversão. '
        'Um funil bem construído aquece o público antes de pedir o cartão.', S['body']))

    etapas = [
        ('TOPO — Descoberta (Frio)',
         GREEN,
         'O público ainda não te conhece. Seu trabalho é aparecer onde ele já está.',
         ['Posts virais de signo (Instagram Reels, TikTok)',
          'SEO: artigos tipo WikiHow sobre astrologia',
          'YouTube: vídeos sobre "seu signo na prática"',
          'Anúncios de engajamento com CPM baixo',
          'Compartilhamentos orgânicos de posts de valor']),
        ('MEIO — Consideração (Morno)',
         GOLD,
         'Já te conhece. Precisa confiar. Aqui você aprofunda o valor.',
         ['Stories diários com conteúdo de bastidores',
          'Depoimentos e provas sociais reais',
          'Lead magnet: PDF gratuito (demo do cap. 1)',
          'Sequência de emails de aquecimento (5 dias)',
          'Lives e Q&A sobre signos e relacionamentos']),
        ('FUNDO — Conversão (Quente)',
         RED,
         'Pronto para comprar. Precisa de um empurrão e zero fricção.',
         ['Link direto para a página de vendas',
          'Oferta com urgência real (vagas, prazo, bônus)',
          'Retargeting de quem visitou a página mas não comprou',
          'Email de carrinho abandonado',
          'Depoimentos específicos do produto']),
    ]
    for titulo, cor, desc, itens in etapas:
        story.append(KeepTogether([
            Paragraph(titulo, ParagraphStyle('etapa', fontName='Georgia-Bold',
                fontSize=13, textColor=cor, spaceBefore=12, spaceAfter=3, leading=17)),
            Paragraph(desc, S['body']),
        ]))
        for it in itens:
            story.append(bul(it, S))
        story.append(Spacer(1, 0.2*cm))

    story.append(Spacer(1, 0.3*cm))
    story.append(box(
        'Regra de ouro do funil: nunca peça o cartão para quem acabou de te conhecer. '
        'Primeiro entregue valor. Depois peça atenção. Depois peça o email. '
        'Só então peça o dinheiro. Cada etapa pulada reduz a conversão em 60–80%.', S))
    story.append(PageBreak())

    # ════════════ CAP 3 — PLATAFORMAS ════════════
    story.append(Paragraph('CAPÍTULO 3', S['tag']))
    story.append(Paragraph('Estratégia por Plataforma', S['h1']))
    story.append(hr())
    story.append(Paragraph(
        'Você não precisa estar em todas as plataformas. Precisa dominar duas ou três '
        'antes de expandir. A escolha depende do seu nível de energia e da plataforma '
        'onde seu público já está. Para astrologia no Brasil, o ranking é claro.', S['body']))

    plataformas = [
        ('INSTAGRAM — Prioridade 1', NAVY,
         'Público: 18–38 anos, majoritariamente feminino. Astrologia é um dos '
         'nichos mais ativos no Instagram brasileiro.',
         [('O que posta', 'Reels de 15–30s com revelações de signo. Carrosséis com "perfil emocional" de cada signo. '
           'Stories diários: enquetes ("qual é seu signo?"), caixinhas de perguntas, contagem regressiva de oferta.'),
          ('Frequência ideal', '1 Reel por dia + 5–7 Stories. Consistência bate qualidade nos primeiros 90 dias.'),
          ('O gancho que funciona', '"Se você é [signo], para tudo e lê isso." Personalização gera 3x mais salvamentos.'),
          ('Monetização direta', 'Link na bio + stories com "arrasta pra cima" / link sticker. Sempre CTA claro.'),
         ]),
        ('TIKTOK — Prioridade 2', PURPLE,
         'Crescimento orgânico mais fácil que qualquer outra plataforma. '
         '#AstroTok tem bilhões de visualizações. Algoritmo favorece nichos de identidade.',
         [('O que posta', 'Vídeos de 30–60s: "O que seu signo revela que você nunca quer admitir." '
           '"Por que [signo] e [signo] nunca funcionam." Tendências com áudios virais adaptados para astrologia.'),
          ('Frequência ideal', '2–3 vídeos por dia no início para testar. Depois 1 por dia com o que funciona.'),
          ('O gancho que funciona', 'Primeiros 2 segundos: afirmação polêmica ou pergunta que a pessoa não pode ignorar.'),
          ('Monetização direta', 'Bio com link. TikTok Shop ainda em expansão no BR — usar link externo por enquanto.'),
         ]),
        ('PINTEREST — Prioridade 3', RED,
         'Tráfego de altíssima intenção. Quem busca "perfil de Escorpião" no Pinterest '
         'está querendo consumir profundamente. Conteúdo dura meses, não horas.',
         [('O que posta', 'Infográficos: "Tudo sobre [signo] em um só lugar." Pins de compatibilidade. '
           'Links diretos para artigos ou página de vendas.'),
          ('Frequência ideal', '5–10 pins por dia usando agendador (Tailwind). Maior ROI por hora investida.'),
          ('O gancho que funciona', 'Título com palavra-chave + promessa: "Lua em Escorpião: o que isso revela sobre você."'),
          ('Monetização direta', 'Pin direto com link para página de vendas. Pinterest converte bem para e-books.'),
         ]),
        ('YOUTUBE — Investimento de longo prazo', BLUE,
         'Construção mais lenta, mas ativo permanente. Um vídeo sobre "mapa astral completo" '
         'pode gerar leads por anos. Complemento ideal após Instagram consolidado.',
         [('O que posta', 'Vídeos de 8–15 min: "Perfil completo de [signo]: amor, sombra e segredos." '
           '"Compatibilidade real entre [signo1] e [signo2]."'),
          ('Frequência ideal', '1 vídeo por semana. Consistência é mais importante que volume aqui.'),
          ('O gancho que funciona', 'Thumbnail com rosto + expressão + texto curto. Título com número ou promessa específica.'),
          ('Monetização direta', 'Card no vídeo + link na descrição + CTA verbal aos 60% do vídeo.'),
         ]),
    ]
    for titulo, cor, desc, itens in plataformas:
        story.append(Paragraph(titulo, ParagraphStyle('plat', fontName='Georgia-Bold',
            fontSize=14, textColor=cor, spaceBefore=14, spaceAfter=4, leading=18)))
        story.append(Paragraph(desc, S['body']))
        for label, texto in itens:
            story.append(KeepTogether([
                Paragraph(label, S['h3']),
                Paragraph(texto, S['body']),
            ]))
        story.append(hr(GRAY))
    story.append(PageBreak())

    # ════════════ CAP 4 — POSTS QUE CONVERTEM ════════════
    story.append(Paragraph('CAPÍTULO 4', S['tag']))
    story.append(Paragraph('Posts que Convertem', S['h1']))
    story.append(hr())
    story.append(Paragraph(
        'Existem padrões de conteúdo que consistentemente geram mais engajamento, '
        'salvamentos e cliques em astrologia. A seguir, os formatos validados por '
        'milhares de criadores do nicho, com scripts prontos para adaptar.', S['body']))

    story.append(Paragraph('Os 7 formatos de maior conversão', S['h2']))

    formatos = [
        ('1. O Post de Identidade',
         '"Você é [signo] e isso significa que..."',
         'O maior motor de compartilhamento. Pessoas compartilham o que as faz sentir vistas.',
         ['Legenda: "Se você é Escorpião, você provavelmente já amou alguém em silêncio '
          'por meses sem dizer nada. Você sente tudo em profundidades que a maioria nunca vai conhecer. '
          'Mas por fora parece que não liga. Se isso é você, salva esse post."',
          'CTA: "Marca alguém que é [signo]" → engajamento explosivo',
          'Métrica alvo: taxa de salvamento > 8% (excelente) e compartilhamento > 3%']),
        ('2. O Carrossel de Revelação',
         '"O lado que ninguém te conta sobre [signo]"',
         'Carrosséis geram 3x mais alcance que fotos estáticas. Estrutura: gancho → desenvolvimento '
         '→ revelação surpreendente → CTA. Mínimo 7 slides.',
         ['Slide 1 (gancho): "Tudo que você acredita sobre [signo] é incompleto"',
          'Slides 2–6: revelações específicas do signo (amor, sombra, medo, segredo)',
          'Slide 7: "Quer o perfil completo? Link na bio → [nome do ebook]"',
          'Dica: use fundo escuro com texto em dourado — esteticamente consistente com o ebook']),
        ('3. O Reel de Polêmica Controlada',
         '"[Signo1] e [Signo2] nunca deveriam namorar"',
         'Polêmica gera comentários. Comentários geram alcance. Mas a polêmica deve ser resolvida '
         'com inteligência, não com agressividade.',
         ['"Áries e Câncer parecem incompatíveis. E são — se nenhum dos dois se conhece. '
          'O problema não é o signo: é o nível de autoconhecimento. Aqui está o porquê..."',
          'Esse formato converte para o ebook porque a solução é: entenda você e o outro com profundidade',
          'Final: "No guia eu explico exatamente por que essas combinações funcionam ou explodem"']),
        ('4. O Post de Dor Específica',
         '"Por que você sempre se apaixona pelo mesmo tipo?"',
         'Dor específica converte muito mais que conteúdo genérico. As melhores dores para o nicho:',
         ['"Por que sinto tudo tão intensamente?" (água: Câncer, Escorpião, Peixes)',
          '"Por que começo tudo mas não termino nada?" (ar/mutável)',
          '"Por que prefiro ficar sozinha a me decepcionar de novo?" (universal)',
          '"Por que ele/ela age assim?" (compatibilidade, enorme)',
          'Esses posts terminam com: "Tem um capítulo inteiro sobre isso no guia. Link na bio."']),
        ('5. O Depoimento Visualizado',
         '"Ela comprou o guia e disse isso..."',
         'Prova social é o gatilho de conversão mais forte. Um depoimento real supera '
         'qualquer copy. Formate o depoimento como imagem com citação.',
         ['"Nunca tinha me sentido tão entendida lendo sobre o meu signo. Li em uma noite." — @usuario',
          'Peça depoimento para cada comprador (email pós-compra automático)',
          'Stories com depoimentos: reposta, salva nos destaques em "O que estão dizendo"',
          'Frequência: pelo menos 2 depoimentos por semana nas primeiras 4 semanas']),
        ('6. O Comparativo de Signos',
         '"Como [signo1] e [signo2] lidam com [situação]"',
         'Gera identificação em dois públicos ao mesmo tempo e incentiva marcações.',
         ['"Escorpião vs Áries num término: Escorpião corta contato total e processa em silêncio. '
          'Áries fica com raiva por 3 dias e segue em frente. Nenhum está errado — são linguagens diferentes."',
          'Tag um amigo que é [signo] / Me marca se você é [signo]',
          'Adaptar para todos os 66 pares de signos = 66 posts de alto engajamento garantido']),
        ('7. O Countdown de Oferta',
         '"Últimas horas com o preço especial"',
         'Urgência real converte. Urgência falsa destrói credibilidade. Use prazos reais.',
         ['Stories countdown (contagem regressiva nativa do Instagram) nos últimos 3 dias',
          '"Ontem 47 pessoas compraram. Hoje encerra o preço de lançamento."',
          'Email de última hora: "Encerra hoje à meia-noite. Sem prorrogação."',
          'Pós-encerramento: honre o prazo. Sua credibilidade vale mais que uma venda extra.']),
    ]

    for titulo, sub, desc, itens in formatos:
        story.append(KeepTogether([
            Paragraph(titulo, S['h2']),
            Paragraph(sub, ParagraphStyle('sub', fontName='Georgia-Ital', fontSize=11,
                textColor=GOLD, spaceAfter=3, leading=14)),
            Paragraph(desc, S['body']),
        ]))
        for it in itens:
            story.append(bul(it, S))
        story.append(Spacer(1, 0.3*cm))

    story.append(PageBreak())

    # ════════════ CAP 5 — WIKIHOW E SEO ════════════
    story.append(Paragraph('CAPÍTULO 5', S['tag']))
    story.append(Paragraph('WikiHow, SEO e Tráfego Orgânico', S['h1']))
    story.append(hr())
    story.append(Paragraph(
        'SEO é o ativo de marketing mais subestimado por criadores de astrologia. '
        'Enquanto todo mundo briga por atenção no Instagram, o Google entrega '
        'tráfego qualificado e gratuito 24 horas por dia para quem posicionou '
        'um artigo bem. A pergunta: vale a pena?', S['body']))

    story.append(Paragraph('WikiHow funciona para astrologia?', S['h2']))
    story.append(Paragraph(
        'Sim — com ressalvas importantes. O modelo WikiHow (artigo longo, estruturado '
        'em passos, objetivo prático) funciona bem para buscas de intenção alta como '
        '"como descobrir meu ascendente", "como calcular mapa astral", '
        '"como saber se sou compatível com [signo]". Essas buscas têm volume real '
        'e intenção de aprender, que é um passo antes da intenção de comprar.', S['body']))
    story.append(Paragraph(
        'Mas SEO leva de 3 a 6 meses para mostrar resultado. Não substitui redes sociais '
        'no curto prazo. A estratégia ideal é: redes sociais geram venda agora; '
        'SEO constrói um canal que alimenta o funil sem custo futuro.', S['body']))

    story.append(Paragraph('Os 10 artigos de maior conversão para o nicho', S['h2']))
    artigos = [
        ('"Como descobrir seu signo lunar (e o que ele revela sobre você)"',
         '450.000+ buscas/mês combinadas. Alta intenção. CTA natural: "Entenda o que sua Lua '
         'revela em profundidade — Capítulo 15 do Guia Emocional dos Signos."'),
        ('"Compatibilidade de signos: o guia completo"',
         'Enorme. Cada par de signos é uma variante de busca. Um artigo-mãe com links internos '
         'para cada combinação pode capturar dezenas de longas-caudas.'),
        ('"[Signo] no amor: o que ninguém te conta" (12 artigos)',
         'Um por signo. Volume médio de 20.000–80.000 buscas/mês cada. Total: potencial massivo. '
         'Cada artigo termina com CTA para o guia completo.'),
        ('"Por que [signo] e [signo] brigam tanto"',
         'Buscas de dor emocional real. Pessoa que busca isso está num relacionamento difícil. '
         'Alta intenção de consumo de solução.'),
        ('"O lado sombrio de [signo]: o que eles nunca mostram"',
         'Curiosidade + identificação = compartilhamento. Alta taxa de retorno ao site.'),
        ('"Como cada signo age num término"',
         'Busca de quem acabou de terminar. Momento emocional alto = receptividade alta.'),
        ('"Ascendente em [signo]: significado completo"',
         'Busca técnica com profundidade. Quem chega aqui já conhece astrologia e quer mais.'),
        ('"Mapa astral: como interpretar o seu"',
         'Volume enorme. Busca de iniciantes. Artigo de porta de entrada para o funil.'),
        ('"Linguagens do amor por signo"',
         'Muito compartilhado. Relaciona o conceito popular de Gary Chapman com astrologia.'),
        ('"Por que me apaixono sempre pelo mesmo tipo" + astrologia',
         'Busca emocional de alta intenção. Responde exatamente ao que o Capítulo 10 do guia cobre.'),
    ]
    for i, (titulo, desc) in enumerate(artigos, 1):
        story.append(KeepTogether([
            Paragraph(f'{i}. {titulo}', S['h3']),
            Paragraph(desc, S['body']),
        ]))

    story.append(Spacer(1, 0.3*cm))
    story.append(box(
        'Estrutura de cada artigo SEO: Título com palavra-chave → Introdução com a dor → '
        '5–8 seções com subtítulos → CTA para o ebook no meio e no final → '
        'Imagem compartilhável (Pinterest). Mínimo 1.500 palavras. Ideal: 2.500+.', S))
    story.append(PageBreak())

    # ════════════ CAP 6 — EMAIL MARKETING ════════════
    story.append(Paragraph('CAPÍTULO 6', S['tag']))
    story.append(Paragraph('Email Marketing — o ativo mais valioso', S['h1']))
    story.append(hr())
    story.append(Paragraph(
        'Seguidores não são seus. A plataforma pode te banir amanhã. '
        'Uma lista de emails é o único ativo de marketing que você realmente possui. '
        'No nicho de astrologia, uma lista aquecida converte entre 3% e 8% em cada '
        'lançamento — muito acima da média de redes sociais.', S['body']))

    story.append(Paragraph('O lead magnet perfeito para astrologia', S['h2']))
    story.append(Paragraph(
        'O melhor lead magnet é o Capítulo 1 do seu guia — que você já tem. '
        'Uma página de captura simples: "Receba gratuitamente o perfil emocional '
        'completo do seu signo. Email + nome → PDF instantâneo." '
        'Taxa de conversão esperada: 25–45% dos visitantes.', S['body']))

    story.append(Paragraph('A sequência de 5 emails que vende', S['h2']))
    emails = [
        ('Email 1 — Entrega (imediato)',
         'Entrega o PDF. Nada mais. Linha de assunto: "Aqui está o seu guia, [Nome]". '
         'Curto, direto. Um link. Cria o hábito de abrir seus emails.'),
        ('Email 2 — Valor puro (Dia 2)',
         'Um insight profundo sobre o signo deles que não está no PDF gratuito. '
         'Exemplo: "Uma coisa sobre [signo] que ninguém fala." Sem CTA de venda. '
         'Constrói confiança e expectativa.'),
        ('Email 3 — A história (Dia 4)',
         'Conte uma história de identificação. "Uma leitora de Escorpião me escreveu '
         'dizendo que leu o capítulo sobre sombra e chorou porque finalmente entendeu '
         'por que repetia os mesmos padrões." História real ou composta com permissão.'),
        ('Email 4 — A oferta (Dia 6)',
         'Apresenta o guia completo. Não como um produto, mas como a continuação natural '
         'do que ela já leu. "O PDF que você recebeu foi apenas o Capítulo 1. '
         'O guia completo tem 5 partes e um capítulo secreto sobre como a mente de '
         'cada signo realmente funciona — e como usar isso." Inclui depoimento real.'),
        ('Email 5 — Urgência (Dia 8)',
         '"Amanhã o preço de lançamento encerra." CTA direto e único. '
         'Linha de assunto: "Última chance — [Nome]" — usar primeiro nome aumenta abertura em 30%.'),
    ]
    for titulo, texto in emails:
        story.append(KeepTogether([
            Paragraph(titulo, S['h3']),
            Paragraph(texto, S['body']),
        ]))

    story.append(box(
        'Taxas de referência para saber se está indo bem: '
        'Taxa de abertura > 30% = boa. > 45% = excelente. '
        'Taxa de clique > 3% = boa. > 8% = excelente. '
        'Taxa de conversão no email de oferta > 2% = boa. > 5% = excelente.', S))
    story.append(PageBreak())

    # ════════════ CAP 7 — META ADS ════════════
    story.append(Paragraph('CAPÍTULO 7', S['tag']))
    story.append(Paragraph('Anúncios Pagos — Meta Ads que retornam', S['h1']))
    story.append(hr())
    story.append(Paragraph(
        'Anúncio pago é um acelerador, não um substituto para conteúdo orgânico. '
        'Com um produto de R$39,90 e uma margem de 90%+, você pode gastar até '
        'R$15 para adquirir um cliente e ainda ter lucro. Entender esse número '
        'muda tudo na forma de pensar em tráfego pago.', S['body']))

    story.append(Paragraph('A estrutura de campanha que funciona', S['h2']))
    campanhas = [
        ('Campanha 1 — Geração de leads (topo de funil)',
         'Objetivo: gerar emails para a lista. '
         'Anúncio: "Receba gratuitamente o perfil emocional completo do seu signo." '
         'Segmentação: Interesses em astrologia, horóscopo, espiritualidade, autoajuda. '
         'Mulheres 18–40. Brasil. '
         'Orçamento sugerido: R$20/dia. Meta: CPL (custo por lead) < R$3.'),
        ('Campanha 2 — Retargeting (fundo de funil)',
         'Público: visitantes da página de vendas que não compraram (pixel). '
         'Anúncio: depoimento em vídeo + preço + botão de compra. '
         'Orçamento: R$15/dia. Meta: ROAS (retorno sobre investimento) > 3x.'),
        ('Campanha 3 — Lookalike de compradores',
         'Após as primeiras 100 vendas, criar audiência lookalike dos compradores. '
         'É o público mais qualificado possível — pessoas parecidas com quem já comprou. '
         'Escalar gradualmente: R$30 → R$60 → R$100/dia conforme ROAS.'),
    ]
    for titulo, texto in campanhas:
        story.append(KeepTogether([
            Paragraph(titulo, S['h3']),
            Paragraph(texto, S['body']),
        ]))

    story.append(Paragraph('O anúncio que converte no nicho de astrologia', S['h2']))
    story.append(Paragraph(
        'Criativos de maior performance no nicho são vídeos de 15–30 segundos com '
        'o seguinte roteiro:', S['body']))
    for linha in [
        '0–3s (gancho): "Você é [signo]? Então você precisa ver isso."',
        '3–12s (valor): Revele um insight surpreendente e específico do signo',
        '12–20s (prova): "37 pessoas de [signo] leram isso ontem e disseram que nunca se sentiram tão entendidas."',
        '20–30s (CTA): "Clique no link e leia o perfil completo do seu signo agora."',
        'Legenda: Fundo escuro, texto em branco e dourado. Sem som necessário (75% vê sem áudio).',
    ]:
        story.append(bul(linha, S))

    story.append(Spacer(1, 0.3*cm))
    story.append(box(
        'Dica avançada: rode 3–5 variações do mesmo anúncio com apenas o gancho '
        'diferente. Deixe o algoritmo identificar qual converte mais e pause os demais. '
        'Esse teste simples pode reduzir o CAC (custo por aquisição) em até 40%.', S))
    story.append(PageBreak())

    # ════════════ CAP 8 — CRONOGRAMA 30 DIAS ════════════
    story.append(Paragraph('CAPÍTULO 8', S['tag']))
    story.append(Paragraph('Cronograma de Lançamento — 30 Dias', S['h1']))
    story.append(hr())
    story.append(Paragraph(
        'Um lançamento bem executado em 30 dias pode gerar de 50 a 500 vendas '
        'dependendo do tamanho do público aquecido. Abaixo, o plano semana a semana.', S['body']))

    semanas = [
        ('SEMANA 1 — Construção de audiência (Dias 1–7)', [
            'Dia 1: Crie ou otimize perfis: bio clara, link na bio para captura de email, foto de perfil reconhecível',
            'Dias 1–7: Post diário de valor puro — sem falar do produto. Objetivo: alcance e seguidores',
            'Post tipo "identidade" de cada signo (12 posts planejados para as 2 primeiras semanas)',
            'Instale o Pixel do Meta na página de captura e de vendas',
            'Configure o lead magnet: página de captura + entrega automática do PDF por email',
            'Campanha de tráfego para o lead magnet: R$20/dia a partir do dia 3',
        ]),
        ('SEMANA 2 — Aquecimento (Dias 8–14)', [
            'Continue os posts de valor. Introduza stories com enquetes e caixinhas',
            'Compartilhe bastidores: "Estou finalizando algo sobre signos e amor..."',
            'Comece a sequência de email para quem capturou (email 1 e 2)',
            'Colete depoimentos de betas/leitores iniciais — mesmo que gratuitos',
            'Anúncio de engajamento nos posts que mais performaram organicamente',
            'Dia 14: "Semana que vem tem uma novidade sobre [signo]..." — crie expectativa',
        ]),
        ('SEMANA 3 — Lançamento (Dias 15–21)', [
            'Dia 15: LANÇAMENTO. Email 4 para a lista. Post de lançamento. Stories com contagem',
            'Preço de lançamento com prazo real (ex: R$29,90 por 7 dias, depois R$39,90)',
            'Lives no Instagram/TikTok respondendo perguntas sobre signos — sem vender diretamente',
            'Retargeting ativado para visitantes da página que não compraram',
            'Emails 3 e 4 para novos leads que entraram durante o lançamento',
            'Monitorar: conversão da página de vendas (meta > 1,5%), custo por venda, ROAS',
        ]),
        ('SEMANA 4 — Fechamento e evergreen (Dias 22–30)', [
            'Dia 24: "Últimas 48 horas no preço de lançamento" — stories + email',
            'Dia 26: Email de urgência final. "Encerra hoje à meia-noite. Sem prorrogação."',
            'Dia 27: Encerramento do preço especial. Comunicar com seriedade.',
            'Dias 28–30: Transição para estratégia evergreen — produto ativo a R$39,90 permanentemente',
            'Campanha de anúncios contínua: leads + retargeting em escala menor (R$30/dia)',
            'Inicio do próximo ciclo: criar conteúdo para o próximo "lançamento" em 45 dias',
        ]),
    ]
    for titulo, itens in semanas:
        story.append(Paragraph(titulo, S['h2']))
        for it in itens:
            story.append(bul(it, S))
        story.append(Spacer(1, 0.2*cm))
    story.append(PageBreak())

    # ════════════ CAP 9 — MÉTRICAS ════════════
    story.append(Paragraph('CAPÍTULO 9', S['tag']))
    story.append(Paragraph('Métricas que Importam', S['h1']))
    story.append(hr())
    story.append(Paragraph(
        'Medir tudo é a forma mais rápida de não medir nada. '
        'Foque nas métricas que têm impacto direto em vendas.', S['body']))
    story.append(table2([
        ['Métrica', 'O que é', 'Meta realista'],
        ['Taxa de conversão da página', '% de visitantes que compram', '1–3%'],
        ['Custo por lead (CPL)', 'Quanto paga por email capturado', '< R$3,00'],
        ['Custo por aquisição (CAC)', 'Quanto paga por venda', '< R$12,00'],
        ['ROAS (retorno sobre anúncios)', 'Receita / gasto em anúncios', '> 2,5x'],
        ['Taxa de abertura de email', '% que abre o email', '> 30%'],
        ['Taxa de clique no email', '% que clica no link', '> 3%'],
        ['Taxa de salvamento (Instagram)', '% de salvamentos por alcance', '> 5%'],
        ['Taxa de compartilhamento', '% de compartilhamentos por alcance', '> 2%'],
        ['LTV (valor por cliente)', 'Receita total por comprador', 'Aumentar com upsell'],
    ], [4.5*cm, 5.5*cm, 4.5*cm], S))
    story.append(PageBreak())

    # ════════════ CAP 10 — ERROS FATAIS ════════════
    story.append(Paragraph('CAPÍTULO 10', S['tag']))
    story.append(Paragraph('Os Erros que Destroem Conversão', S['h1']))
    story.append(hr())
    story.append(Paragraph(
        'Esses erros são responsáveis por 90% das vendas que não acontecem. '
        'Leia com atenção porque todos eles parecem razoáveis antes de destruir seu resultado.', S['body']))

    erros = [
        ('Falar do produto antes de entregar valor',
         'Se o primeiro contato que alguém tem com você é um anúncio pedindo dinheiro, '
         'a taxa de conversão é próxima de zero. Entregue antes de pedir. Sempre.'),
        ('CTA fraco ou inexistente',
         '"Link na bio" não é um CTA. "Clique no link na bio e receba agora o perfil '
         'emocional completo do seu signo — é gratuito" é um CTA. Seja específico sobre '
         'o que a pessoa deve fazer e o que vai ganhar fazendo.'),
        ('Página de vendas com muita informação',
         'Uma página de vendas boa tem: headline que captura a dor, descrição do que a '
         'pessoa vai sentir (não o que vai ler), depoimentos, preço, botão. '
         'Descrição de 12 parágrafos sobre o conteúdo do PDF mata a conversão.'),
        ('Urgência falsa',
         '"Oferta por tempo limitado" que se renova eternamente. O público percebe. '
         'Uma vez destruída, a credibilidade leva meses para ser reconstruída.'),
        ('Não construir lista de email',
         'Contar apenas com seguidores é contar com o algoritmo. Em 2024, alcance orgânico '
         'no Instagram era de 3–8% dos seguidores. Uma lista de email entrega 100%.'),
        ('Tentar vender para todo mundo',
         'Quanto mais específico o público, maior a conversão. '
         '"Mulheres de 25–35 que saíram de um relacionamento nos últimos 6 meses" '
         'converte muito mais que "pessoas interessadas em astrologia".'),
        ('Desistir antes do mês 3',
         'A maioria dos criadores abandona a estratégia antes de o algoritmo '
         'aprender e antes de a lista ter volume suficiente. 90 dias de consistência '
         'fazem mais diferença do que o melhor post isolado.'),
        ('Não fazer retargeting',
         '97% das pessoas que visitam uma página de vendas não compram na primeira visita. '
         'Sem retargeting, você perde 97% do dinheiro que gastou para trazer tráfego.'),
    ]
    for titulo, texto in erros:
        story.append(KeepTogether([
            Paragraph(f'✗  {titulo}', S['warn']),
            Paragraph(texto, S['body']),
        ]))

    story.append(Spacer(1, 0.5*cm))
    story.append(box(
        'A estratégia perfeita é simples: entregue valor diariamente, '
        'construa uma lista de email, ative retargeting, seja consistente por 90 dias. '
        'Qualquer pessoa que fizer isso com disciplina vende. O mercado existe. '
        'O produto é bom. O que falta é aparecer com consistência.', S,
        bg=colors.HexColor('#EAF4EA'), border=GREEN))

    doc.build(story, onFirstPage=page_bg, onLaterPages=page_bg)
    print(f'[OK] Guia de marketing gerado: {out}')

build()
