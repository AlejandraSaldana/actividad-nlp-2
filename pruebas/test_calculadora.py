import pytest

from calculadora import Calculadora


def test_suma():
    assert Calculadora("suma", [2, 3]).resultado() == 5


def test_suma_con_decimales_y_negativos():
    assert Calculadora("suma", [1.5, 2, -1]).resultado() == 2.5


def test_resta():
    assert Calculadora("resta", [3, 8]).resultado() == -5


def test_resta_varios_numeros():
    assert Calculadora("resta", [20, 5, 2.5]).resultado() == 12.5


def test_multiplicacion():
    assert Calculadora("multiplicacion", [2, 3, 0.5]).resultado() == 3


def test_multiplicacion_con_negativo():
    assert Calculadora("multiplicacion", [-4, 2.5]).resultado() == -10


def test_division():
    assert Calculadora("division", [9, 2]).resultado() == 4.5


def test_division_varios_numeros():
    assert Calculadora("division", [100, 5, -4]).resultado() == -5


def test_promedio():
    assert Calculadora("promedio", [8, 9, 10]).resultado() == 9


def test_promedio_con_decimales():
    assert Calculadora("promedio", [7.5, 8.5, 9.5]).resultado() == 8.5


def test_potencia():
    assert Calculadora("potencia", [2, 3]).resultado() == 8


def test_potencia_exponente_negativo():
    assert Calculadora("potencia", [2, -2]).resultado() == 0.25


def test_mayor():
    assert Calculadora("mayor", [4, -2, 8]).resultado() == 8


def test_menor():
    assert Calculadora("menor", [4, -2, 8]).resultado() == -2


# Prueba propia con datos diferentes a los ejemplos
def test_promedio_de_calificaciones():
    assert Calculadora("promedio", [70, 85.5, 92, 100]).resultado() == pytest.approx(86.875)


def test_division_entre_cero():
    with pytest.raises(ZeroDivisionError, match="cero"):
        Calculadora("division", [5, 0]).resultado()


def test_operacion_no_valida():
    with pytest.raises(ValueError, match="Operación no válida"):
        Calculadora("raiz", [4]).resultado()


def test_sin_numeros():
    with pytest.raises(ValueError, match="al menos un número"):
        Calculadora("suma", []).resultado()


def test_potencia_necesita_dos_numeros():
    with pytest.raises(ValueError, match="base y exponente"):
        Calculadora("potencia", [2, 3, 4]).resultado()


@pytest.mark.parametrize("valor", ["5", None, True, float("inf"), float("nan")])
def test_valores_no_numericos(valor):
    with pytest.raises(ValueError, match="reales y finitos"):
        Calculadora("suma", [1, valor]).resultado()
