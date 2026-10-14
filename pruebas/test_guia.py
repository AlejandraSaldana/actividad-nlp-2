from pathlib import Path

import pytest
from pypdf import PdfReader

from herramientas.guia_pdf import RAIZ, contenido_markdown, crear_guia


def test_guia_del_proyecto_generada(tmp_path):
    destino = crear_guia(RAIZ / "GUIA_ALUMNOS.md", tmp_path / "material" / "guia.pdf")
    lector = PdfReader(destino)
    texto = "\n".join(pagina.extract_text() for pagina in lector.pages)
    assert len(lector.pages) == 6
    for fragmento in (
        "AlejandraSaldana/actividad-nlp-2",
        "api:aplicacion",
        "team02_actividad02",
        "90 %",
        "0 issues",
        "sonarqube-report-pdf-json-md",
        "guia-para-alumnos-pdf",
        "86.875",
        "N/D",
        "6. Evidencia y entrega",
    ):
        assert fragmento in texto
    assert "<!-- pagina -->" not in texto
    assert lector.metadata.title == "Guía del proyecto - Calculadora en Python"


def test_guia_rechaza_codigo_sin_cierre():
    with pytest.raises(ValueError, match="sin cierre"):
        contenido_markdown("# Guía\n```text\npython calculadora.py")


def test_guia_no_requiere_directorio_actual_del_repo(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    destino = crear_guia(RAIZ / "GUIA_ALUMNOS.md", Path("salida") / "guia.pdf")
    assert destino.is_file()
    assert len(PdfReader(destino).pages) == 6
