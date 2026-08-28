# -*- coding: utf-8 -*-
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors

OUT = "/home/user/Teste/declaracao-disponibilidade-voluntario-Luiz-Gustavo-Pereira-Uesato.pdf"

NOME = "Luiz Gustavo Pereira Uesato"
DIAS_SEMANA = "4 (quatro)"
DIAS_DISPONIVEIS = "4 dias por semana, a definir com a coordenacao"
HORARIOS = "das 14h as 16h e das 20h as 22h (2 horas por dia)"
LOCAL_DATA = "Sao Paulo, 28 de agosto de 2026"

# acentuacao
DIAS_DISPONIVEIS = "4 dias por semana, a definir com a coordenação"
HORARIOS = "das 14h às 16h e das 20h às 22h (2 horas por dia)"
LOCAL_DATA = "São Paulo, 28 de agosto de 2026"

titulo = ParagraphStyle("titulo", fontName="Helvetica-Bold", fontSize=13.5,
                        leading=18, alignment=TA_CENTER, spaceAfter=6)
corpo = ParagraphStyle("corpo", fontName="Helvetica", fontSize=11.5,
                       leading=19, alignment=TA_JUSTIFY, spaceAfter=12)
campo = ParagraphStyle("campo", fontName="Helvetica", fontSize=11.5, leading=19)
centro = ParagraphStyle("centro", fontName="Helvetica", fontSize=11, leading=15,
                        alignment=TA_CENTER)

doc = SimpleDocTemplate(OUT, pagesize=A4,
                        leftMargin=3*cm, rightMargin=3*cm,
                        topMargin=3*cm, bottomMargin=2.5*cm,
                        title="Declaração de Disponibilidade para Atuação Voluntária",
                        author=NOME)

S = []
S.append(Paragraph("DECLARAÇÃO DE DISPONIBILIDADE<br/>PARA ATUAÇÃO VOLUNTÁRIA", titulo))
S.append(Spacer(1, 4))

linha = Table([[""]], colWidths=[4*cm], rowHeights=[2])
linha.setStyle(TableStyle([("LINEBELOW", (0,0), (-1,-1), 1, colors.HexColor("#333333"))]))
S.append(linha)
S.append(Spacer(1, 22))

S.append(Paragraph(
    "Eu, <b>%s</b> (nome completo), declaro para os devidos fins que possuo "
    "disponibilidade para atuar como voluntário junto à Associação Mental Care "
    "Colômbia – Sede Brasil." % NOME, corpo))

S.append(Paragraph(
    "Informo que minha disponibilidade semanal é de <b>%s</b> dias, nos seguintes horários:"
    % DIAS_SEMANA, corpo))

dados = [
    [Paragraph("<b>Dias disponíveis:</b>", campo), Paragraph(DIAS_DISPONIVEIS, campo)],
    [Paragraph("<b>Horários disponíveis:</b>", campo), Paragraph(HORARIOS, campo)],
]
t = Table(dados, colWidths=[4.6*cm, 9.4*cm])
t.setStyle(TableStyle([
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("LEFTPADDING", (0,0), (-1,-1), 0),
    ("BOTTOMPADDING", (0,0), (-1,-1), 6),
    ("TOPPADDING", (0,0), (-1,-1), 2),
    ("LINEBELOW", (1,0), (1,-1), 0.6, colors.HexColor("#999999")),
]))
S.append(t)
S.append(Spacer(1, 18))

S.append(Paragraph(
    "Comprometo-me a dedicar carga horária mínima de 8 (oito) horas semanais, "
    "conforme pactuação com a coordenação da organização.", corpo))

S.append(Spacer(1, 34))
S.append(Paragraph("Local e data: <b>%s</b>" % LOCAL_DATA, campo))

S.append(Spacer(1, 60))
ass = Table([[""], [Paragraph(NOME, centro)],
             [Paragraph("Assinatura (manual ou eletrônica)", centro)]],
            colWidths=[10*cm], rowHeights=[2, None, None])
ass.setStyle(TableStyle([
    ("LINEABOVE", (0,1), (0,1), 0.8, colors.HexColor("#333333")),
    ("TOPPADDING", (0,1), (0,1), 6),
    ("BOTTOMPADDING", (0,1), (0,1), 2),
    ("TOPPADDING", (0,2), (0,2), 0),
    ("ALIGN", (0,0), (-1,-1), "CENTER"),
]))
ass.hAlign = "CENTER"
S.append(ass)

doc.build(S)
print("ok ->", OUT)
