"""Genera el PDF del proyecto a partir de su guía Markdown."""

from html import escape
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

RAIZ = Path(__file__).resolve().parents[1]
AZUL = colors.HexColor("#17334D")
VERDE = colors.HexColor("#087F78")
ANCHO = A4[0] - 96
ESTILOS = {
    "texto": ParagraphStyle("Texto", fontName="Helvetica", fontSize=9.5, leading=14),
    "h1": ParagraphStyle(
        "Titulo",
        fontName="Helvetica-Bold",
        fontSize=29,
        leading=34,
        textColor=AZUL,
        spaceAfter=14,
        keepWithNext=True,
    ),
    "h2": ParagraphStyle(
        "Seccion",
        fontName="Helvetica-Bold",
        fontSize=19,
        leading=24,
        textColor=AZUL,
        spaceAfter=13,
        keepWithNext=True,
    ),
    "h3": ParagraphStyle(
        "Apartado",
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=17,
        textColor=VERDE,
        spaceBefore=8,
        spaceAfter=8,
        keepWithNext=True,
    ),
    "codigo": ParagraphStyle(
        "Codigo",
        fontName="Courier",
        fontSize=8,
        leading=12,
        backColor=colors.HexColor("#F0F4F7"),
        borderPadding=8,
        spaceBefore=5,
        spaceAfter=10,
    ),
    "celda": ParagraphStyle("Celda", fontSize=8, leading=11),
}


def tabla(lineas):
    filas = [linea.strip("| ").split("|") for linea in lineas]
    filas = [filas[0], *filas[2:]]  # La segunda fila delimita el encabezado Markdown.
    contenido = [
        [Paragraph(escape(celda.strip()), ESTILOS["celda"]) for celda in fila] for fila in filas
    ]
    resultado = Table(contenido, colWidths=[ANCHO / len(filas[0])] * len(filas[0]), repeatRows=1)
    resultado.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#DCEBEF")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F5F7F9")]),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    return resultado


def contenido_markdown(fuente):
    """Admite los encabezados, listas, tablas y bloques usados por esta guía."""
    lineas = fuente.splitlines()
    contenido = []
    indice = 0
    while indice < len(lineas):
        linea = lineas[indice]
        indice += 1
        if not linea.strip():
            continue
        if linea == "<!-- pagina -->":
            contenido.append(PageBreak())
        elif linea.startswith("```"):
            codigo = []
            while indice < len(lineas) and not lineas[indice].startswith("```"):
                codigo.append(lineas[indice])
                indice += 1
            if indice == len(lineas):
                raise ValueError("Bloque de código sin cierre en la guía.")
            indice += 1
            contenido.append(Preformatted("\n".join(codigo), ESTILOS["codigo"]))
        elif linea.startswith("|"):
            filas = [linea]
            while indice < len(lineas) and lineas[indice].startswith("|"):
                filas.append(lineas[indice])
                indice += 1
            contenido.extend([tabla(filas), Spacer(1, 10)])
        else:
            estilo = "texto"
            for prefijo, nombre in [("### ", "h3"), ("## ", "h2"), ("# ", "h1")]:
                if linea.startswith(prefijo):
                    linea, estilo = linea[len(prefijo) :], nombre
                    break
            if linea.startswith("- "):
                linea = "• " + linea[2:]
            contenido.extend([Paragraph(escape(linea), ESTILOS[estilo]), Spacer(1, 8)])
    return contenido


def marco(lienzo, documento):
    lienzo.saveState()
    lienzo.setFillColor(VERDE)
    lienzo.rect(0, A4[1] - 7, A4[0], 7, fill=1, stroke=0)
    lienzo.setFillColor(AZUL)
    lienzo.setFont("Helvetica-Bold", 8)
    lienzo.drawString(48, A4[1] - 35, "ACTIVIDAD NLP 2 / GUÍA DEL PROYECTO")
    lienzo.setFont("Helvetica", 8)
    lienzo.drawString(48, 30, "AlejandraSaldana/actividad-nlp-2")
    lienzo.drawRightString(A4[0] - 48, 30, str(documento.page))
    lienzo.restoreState()


def crear_guia(fuente, destino):
    contenido = contenido_markdown(Path(fuente).read_text(encoding="utf-8"))
    destino = Path(destino)
    destino.parent.mkdir(parents=True, exist_ok=True)
    SimpleDocTemplate(
        str(destino),
        pagesize=A4,
        leftMargin=48,
        rightMargin=48,
        topMargin=65,
        bottomMargin=55,
        title="Guía del proyecto - Calculadora en Python",
        author="Equipo actividad-nlp-2",
    ).build(contenido, onFirstPage=marco, onLaterPages=marco)
    return destino


def principal():
    destino = crear_guia(RAIZ / "GUIA_ALUMNOS.md", RAIZ / "material" / "GUIA_ALUMNOS.pdf")
    print(f"Guía generada: {destino}")


if __name__ == "__main__":
    principal()
