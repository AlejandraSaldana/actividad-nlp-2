import json
import subprocess
import sys

from fastapi.testclient import TestClient

from api import aplicacion
from calculadora import menu

cliente = TestClient(aplicacion)


def simular_menu(monkeypatch, capsys, entradas):
    respuestas = iter(entradas)
    monkeypatch.setattr("builtins.input", lambda mensaje: next(respuestas))
    menu()
    return capsys.readouterr().out


def test_programa_completo():
    respuesta = subprocess.run(
        [sys.executable, "calculadora.py"],
        input="promedio\n8 9 10\nn\n",
        text=True,
        capture_output=True,
        check=True,
        timeout=10,
    )
    assert "Resultado: 9.0" in respuesta.stdout


def test_menu_muestra_el_calculo(monkeypatch, capsys):
    casos = [
        (["suma", "2 3", "n"], "Resultado: 5.0"),
        (["resta", "3 8", "n"], "Resultado: -5.0"),
        (["multiplicacion", "2 3 0.5", "n"], "Resultado: 3.0"),
        (["division", "9 2", "n"], "Resultado: 4.5"),
        (["potencia", "2 3", "n"], "Resultado: 8.0"),
        (["MAYOR", "4 -2 8", "n"], "Resultado: 8.0"),
        (["menor", "4 -2 8", "n"], "Resultado: -2.0"),
    ]
    for entradas, esperado in casos:
        assert esperado in simular_menu(monkeypatch, capsys, entradas)


def test_menu_permite_continuar_y_salir(monkeypatch, capsys):
    salida = simular_menu(monkeypatch, capsys, ["suma", "1 1", "s", "resta", "5 2", "s", "salir"])
    assert "Resultado: 2.0" in salida
    assert "Resultado: 3.0" in salida
    assert salida.strip().endswith("Adiós")


def test_menu_maneja_entradas_incorrectas(monkeypatch, capsys):
    casos = [
        (["suma", "dos tres", "n"], "Error: Escribe solo números"),
        (["division", "8 0", "n"], "Error: No se puede dividir entre cero"),
        (["raiz", "4", "n"], "Error: Operación no válida: raiz"),
        (["suma", "", "n"], "Error: Debes escribir al menos un número"),
        (["potencia", "1e300 2", "n"], "Error:"),
    ]
    for entradas, esperado in casos:
        assert esperado in simular_menu(monkeypatch, capsys, entradas)


def test_menu_sigue_despues_de_un_error(monkeypatch, capsys):
    salida = simular_menu(monkeypatch, capsys, ["division", "1 0", "s", "suma", "4 4", "n"])
    assert "Error: No se puede dividir entre cero" in salida
    assert "Resultado: 8.0" in salida


def test_api():
    respuesta = cliente.post("/calcular", json={"operacion": "promedio", "numeros": [8, 9, 10]})
    assert respuesta.status_code == 200
    assert respuesta.json() == {"resultado": 9}
    assert cliente.get("/estado").json() == {"estado": "correcto"}
    assert respuesta.headers["Cross-Origin-Resource-Policy"] == "same-origin"
    assert respuesta.headers["Cache-Control"] == "no-store"


def test_api_con_errores():
    casos = [
        {"operacion": "division", "numeros": [5, 0]},
        {"operacion": "raiz", "numeros": [4]},
        {"operacion": "suma", "numeros": ["a"]},
        {"operacion": "suma", "numeros": [1] * 1001},
        {"operacion": "potencia", "numeros": [1e300, 2]},
        {},
    ]
    for datos in casos:
        respuesta = cliente.post(
            "/calcular",
            content=json.dumps(datos),
            headers={"Content-Type": "application/json"},
        )
        assert respuesta.status_code == 400
        assert "detail" in respuesta.json()
    assert cliente.post("/calcular", json=[1, 2]).status_code == 422
