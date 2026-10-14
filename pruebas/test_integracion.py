import json
import subprocess
import sys

from fastapi.testclient import TestClient

from api import aplicacion
from calculadora import main

cliente = TestClient(aplicacion)


def simular_menu(monkeypatch, capsys, entradas):
    respuestas = iter(entradas)
    monkeypatch.setattr("builtins.input", lambda mensaje: next(respuestas))
    main()
    return capsys.readouterr().out


def test_programa_completo():
    respuesta = subprocess.run(
        [sys.executable, "calculadora.py"],
        input="5\n3\n8\n9\n10\nn\n",
        text=True,
        capture_output=True,
        check=True,
        timeout=10,
    )
    assert "Resultado de la promedio: 9.0" in respuesta.stdout


def test_menu_muestra_el_calculo(monkeypatch, capsys):
    casos = [
        (["1", "2", "2", "3", "n"], "Resultado de la suma: 5.0"),
        (["2", "3", "8", "n"], "Resultado de la resta: -5.0"),
        (["3", "3", "2", "3", "0.5", "n"], "Resultado de la multiplicacion: 3.0"),
        (["4", "9", "2", "n"], "Resultado de la division: 4.5"),
        (["5", "3", "8", "9", "10", "n"], "Resultado de la promedio: 9.0"),
        (["6", "2", "3", "n"], "Resultado de la potencia: 8.0"),
        (["7", "3", "4", "-2", "8", "n"], "Resultado de la mayor: 8.0"),
        (["8", "3", "4", "-2", "8", "n"], "Resultado de la menor: -2.0"),
    ]
    for entradas, esperado in casos:
        assert esperado in simular_menu(monkeypatch, capsys, entradas)


def test_menu_permite_continuar_y_salir(monkeypatch, capsys):
    salida = simular_menu(monkeypatch, capsys, ["1", "2", "1", "1", "s", "2", "5", "2", "s", "9"])
    assert "Resultado de la suma: 2.0" in salida
    assert "Resultado de la resta: 3.0" in salida
    assert salida.strip().endswith("¡Hasta luego!")


def test_menu_maneja_entradas_incorrectas(monkeypatch, capsys):
    casos = [
        (["1", "dos", "1", "hola", "4", "n"], "ingresa un número entero válido"),
        (["1", "0", "1", "4", "n"], "debes ingresar al menos un número"),
        (["1", "1", "hola", "4", "n"], "ingresa un número válido"),
        (["4", "8", "0", "n"], "Error: No se puede dividir entre cero"),
        (["0", "9"], "opción no válida"),
        (["6", "1e300", "2", "n"], "Error:"),
    ]
    for entradas, esperado in casos:
        assert esperado in simular_menu(monkeypatch, capsys, entradas)


def test_menu_sigue_despues_de_un_error(monkeypatch, capsys):
    salida = simular_menu(monkeypatch, capsys, ["4", "1", "0", "s", "1", "2", "4", "4", "n"])
    assert "Error: No se puede dividir entre cero" in salida
    assert "Resultado de la suma: 8.0" in salida


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
