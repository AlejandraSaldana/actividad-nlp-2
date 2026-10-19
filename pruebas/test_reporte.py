import json
from pathlib import Path
from unittest.mock import Mock

import pytest
import requests
from pypdf import PdfReader

from herramientas import reporte_sonarqube as reporte


def datos_de_ejemplo():
    return {
        "project": "team02_actividad02",
        "analysis_id": "analisis",
        "revision": "commit",
        "date": "2026-10-18T18:00:00+00:00",
        "metrics": {"coverage": "95", "new_coverage": "96"},
        "quality_gate": {
            "status": "OK",
            "conditions": [
                {
                    "metricKey": "new_coverage",
                    "actualValue": "96",
                    "errorThreshold": "90",
                    "comparator": "LT",
                    "status": "OK",
                }
            ],
        },
        "overall_issues": [],
        "new_issues": [],
        "dashboard": f"{reporte.SERVIDOR}/dashboard?id=team02_actividad02",
    }


def test_crear_reportes(tmp_path):
    datos = datos_de_ejemplo()
    reporte.guardar_reportes(datos, tmp_path)
    documento = PdfReader(tmp_path / "sonarqube.pdf")
    texto = "\n".join(pagina.extract_text() for pagina in documento.pages)
    assert len(documento.pages) == 2
    for esperado in ("APROBADO", "team02_actividad02", "95 %", "96 %", "commit", "analisis"):
        assert esperado in texto
    assert json.loads((tmp_path / "sonarqube.json").read_text(encoding="utf-8")) == datos
    assert "Issues abiertos nuevos: **0**" in (tmp_path / "sonarqube.md").read_text(
        encoding="utf-8"
    )


def test_reporte_sin_mediciones_y_con_hallazgos(tmp_path):
    datos = datos_de_ejemplo()
    datos["metrics"] = {"coverage": "N/D"}
    datos["date"] = "2026-10-18"
    datos["quality_gate"] = {"status": "NONE", "conditions": []}
    datos["overall_issues"] = [{"message": "A < B & C", "severity": "MAJOR"}]
    datos["new_issues"] = datos["overall_issues"]
    reporte.guardar_reportes(datos, tmp_path)
    texto = "\n".join(p.extract_text() for p in PdfReader(tmp_path / "sonarqube.pdf").pages)
    assert "N/D" in texto
    assert "SIN EVALUAR" in texto
    assert "A < B & C" in texto
    assert "Issues abiertos totales: **1**" in reporte.resumen(datos)


def test_conexion_y_autenticacion(monkeypatch):
    monkeypatch.setenv("SONAR_TOKEN", "prueba")
    respuesta = Mock(status_code=200)
    respuesta.json.return_value = {"estado": "correcto"}
    peticion = Mock(return_value=respuesta)
    monkeypatch.setattr(reporte.requests, "get", peticion)
    assert reporte.consultar("system/status") == {"estado": "correcto"}
    peticion.assert_called_once_with(
        f"{reporte.SERVIDOR}/api/system/status",
        params={},
        headers={"Authorization": "Bearer prueba"},
        timeout=30,
        allow_redirects=False,
    )
    respuesta.status_code = 403
    with pytest.raises(PermissionError, match="lectura"):
        reporte.consultar("system/status")
    respuesta.status_code = 302
    with pytest.raises(RuntimeError, match="datos esperados"):
        reporte.consultar("system/status")
    respuesta.status_code = 401
    respuesta.raise_for_status.side_effect = requests.HTTPError()
    with pytest.raises(requests.HTTPError):
        reporte.consultar("system/status")


def test_errores_de_red(monkeypatch):
    monkeypatch.setenv("SONAR_TOKEN", "prueba")
    monkeypatch.setattr(reporte.requests, "get", Mock(side_effect=requests.Timeout()))
    with pytest.raises(requests.Timeout):
        reporte.consultar("system/status")


@pytest.mark.parametrize(
    "estado,error",
    [("PENDING", TimeoutError), ("FAILED", RuntimeError), ("CANCELED", RuntimeError)],
)
def test_analisis_no_completado(monkeypatch, estado, error):
    monkeypatch.setattr(reporte.time, "sleep", lambda segundos: None)
    monkeypatch.setattr(reporte, "consultar", Mock(return_value={"task": {"status": estado}}))
    with pytest.raises(error):
        reporte.esperar_analisis("tarea")


def test_espera_hasta_terminar(monkeypatch):
    pausa = Mock()
    monkeypatch.setattr(reporte.time, "sleep", pausa)
    consulta = Mock(
        side_effect=[
            {"task": {"status": "IN_PROGRESS"}},
            {"task": {"status": "SUCCESS", "analysisId": "analisis"}},
        ]
    )
    monkeypatch.setattr(reporte, "consultar", consulta)
    assert reporte.esperar_analisis("tarea") == "analisis"
    pausa.assert_called_once_with(5)


def test_paginacion_de_hallazgos(monkeypatch):
    consulta = Mock(
        side_effect=[
            {"issues": [{"key": "a"}], "paging": {"total": 2}},
            {"issues": [{"key": "b"}], "paging": {"total": 2}},
        ]
    )
    monkeypatch.setattr(reporte, "consultar", consulta)
    assert reporte.obtener_problemas("team02_actividad02", nuevos=True) == [
        {"key": "a"},
        {"key": "b"},
    ]
    assert consulta.call_args.kwargs["p"] == 2
    assert consulta.call_args.kwargs["componentKeys"] == "team02_actividad02"
    assert consulta.call_args.kwargs["sinceLeakPeriod"] == "true"
    monkeypatch.setattr(
        reporte, "consultar", Mock(return_value={"issues": [], "paging": {"total": 10001}})
    )
    with pytest.raises(RuntimeError, match="demasiados"):
        reporte.obtener_problemas("team02_actividad02")


def respuestas_de_ejemplo():
    return {
        "ce/task": {"task": {"status": "SUCCESS", "analysisId": "analisis"}},
        "project_analyses/search": {
            "analyses": [{"key": "analisis", "revision": "commit", "date": "2026-10-18"}]
        },
        "measures/component": {
            "component": {
                "measures": [
                    {"metric": "coverage", "value": "95"},
                    {"metric": "new_coverage", "period": {"value": "96"}},
                ]
            }
        },
        "qualitygates/project_status": {"projectStatus": {"status": "OK", "conditions": []}},
        "issues/search": {"issues": [], "paging": {"total": 0}},
    }


def test_datos_del_commit_correcto(monkeypatch):
    monkeypatch.setenv("GITHUB_SHA", "commit")
    respuestas = respuestas_de_ejemplo()
    monkeypatch.setattr(reporte, "consultar", lambda ruta, **parametros: respuestas[ruta])
    datos = reporte.obtener_datos("analisis", "team02_actividad02")
    assert datos["metrics"] == {"coverage": "95", "new_coverage": "96"}
    assert datos["revision"] == "commit"
    assert "team02_actividad02" in datos["dashboard"]
    with pytest.raises(RuntimeError, match="commit"):
        reporte.obtener_datos("otro", "team02_actividad02")
    monkeypatch.setenv("GITHUB_SHA", "otro-commit")
    with pytest.raises(RuntimeError, match="commit"):
        reporte.obtener_datos("analisis", "team02_actividad02")


def test_no_mezcla_analisis(monkeypatch):
    monkeypatch.setenv("GITHUB_SHA", "commit")
    monkeypatch.setattr(reporte, "obtener_problemas", lambda project_key, nuevos=False: [])
    monkeypatch.setattr(
        reporte,
        "consultar",
        Mock(
            side_effect=[
                respuestas_de_ejemplo()["project_analyses/search"],
                {"component": {"measures": []}},
                {"projectStatus": {"status": "OK"}},
                {"analyses": [{"key": "otro"}]},
            ]
        ),
    )
    with pytest.raises(RuntimeError, match="Otro análisis"):
        reporte.obtener_datos("analisis", "team02_actividad02")


def test_ejecucion_y_evidencia_de_fallos(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("GITHUB_SHA", "commit")
    monkeypatch.setenv("GITHUB_STEP_SUMMARY", str(tmp_path / "resumen.md"))
    Path(".scannerwork").mkdir()
    Path(".scannerwork/report-task.txt").write_text(
        "ceTaskId=tarea\nprojectKey=team02_actividad02\n", encoding="utf-8"
    )
    respuestas = respuestas_de_ejemplo()
    monkeypatch.setattr(reporte, "consultar", lambda ruta, **parametros: respuestas[ruta])
    reporte.principal()
    assert Path("reports/sonarqube/sonarqube.pdf").is_file()
    assert "commit" in Path("resumen.md").read_text(encoding="utf-8")
    respuestas["qualitygates/project_status"]["projectStatus"]["status"] = "ERROR"
    monkeypatch.delenv("GITHUB_STEP_SUMMARY")
    with pytest.raises(SystemExit, match="Quality Gate"):
        reporte.principal()
    datos = json.loads(Path("reports/sonarqube/sonarqube.json").read_text(encoding="utf-8"))
    assert datos["quality_gate"]["status"] == "ERROR"
    respuestas["qualitygates/project_status"]["projectStatus"]["status"] = "OK"
    respuestas["issues/search"] = {
        "issues": [{"message": "Pendiente", "key": "uno"}],
        "paging": {"total": 1},
    }
    with pytest.raises(SystemExit, match="issues abiertos"):
        reporte.principal()
    datos = json.loads(Path("reports/sonarqube/sonarqube.json").read_text(encoding="utf-8"))
    assert len(datos["overall_issues"]) == 1
