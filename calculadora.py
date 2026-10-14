import math


class Calculadora:
    def __init__(self, operacion, numeros):
        self.operacion = operacion
        self.numeros = numeros

    def suma(self):
        return sum(self.numeros)

    def resta(self):
        return self.numeros[0] - sum(self.numeros[1:])

    def multiplicacion(self):
        resultado = 1
        for numero in self.numeros:
            resultado *= numero
        return resultado

    def division(self):
        resultado = self.numeros[0]
        for numero in self.numeros[1:]:
            if numero == 0:
                raise ZeroDivisionError("No se puede dividir entre cero")
            resultado /= numero
        return resultado

    def promedio(self):
        return sum(self.numeros) / len(self.numeros)

    def potencia(self):
        return self.numeros[0] ** self.numeros[1]

    def mayor(self):
        return max(self.numeros)

    def menor(self):
        return min(self.numeros)

    def resultado(self):
        operaciones = {
            "suma": self.suma,
            "resta": self.resta,
            "multiplicacion": self.multiplicacion,
            "division": self.division,
            "promedio": self.promedio,
            "potencia": self.potencia,
            "mayor": self.mayor,
            "menor": self.menor,
        }
        if self.operacion not in operaciones:
            raise ValueError(f"Operación no válida: {self.operacion}")
        if not isinstance(self.numeros, list) or not self.numeros:
            raise ValueError("Debes escribir al menos un número")
        for numero in self.numeros:
            if type(numero) not in (int, float) or not math.isfinite(numero):
                raise ValueError("Solo se aceptan números reales y finitos")
        if self.operacion == "potencia" and len(self.numeros) != 2:
            raise ValueError("La potencia necesita dos números: base y exponente")
        return operaciones[self.operacion]()


def menu():
    while True:
        print("\nOperaciones: suma, resta, multiplicacion, division,")
        print("promedio, potencia, mayor, menor")
        operacion = input("Escribe la operación (o 'salir'): ").strip().lower()
        if operacion == "salir":
            print("Adiós")
            break

        try:
            texto = input("Escribe los números separados por espacios: ")
            try:
                numeros = [float(n) for n in texto.split()]
            except ValueError:
                raise ValueError("Escribe solo números") from None
            print("Resultado:", Calculadora(operacion, numeros).resultado())
        except (ValueError, ZeroDivisionError, OverflowError) as error:
            print("Error:", error)

        otra = input("¿Otra operación? (s/n): ").strip().lower()
        if otra != "s":
            print("Adiós")
            break


if __name__ == "__main__":
    menu()
