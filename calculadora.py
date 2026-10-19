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
        total = sum(self.numeros)
        if isinstance(total, float) and not math.isfinite(total):
            return sum(numero / len(self.numeros) for numero in self.numeros)
        return total / len(self.numeros)

    def potencia(self):
        if abs(self.numeros[1]) > 10000:
            raise ValueError("Usa un exponente entre -10000 y 10000")
        return self.numeros[0] ** self.numeros[1]

    def mayor(self):
        return max(self.numeros)

    def menor(self):
        return min(self.numeros)

    def _validar_entrada(self):
        operaciones_validas = {
            "suma", "resta", "multiplicacion", "division",
            "promedio", "potencia", "mayor", "menor",
        }
        if not isinstance(self.operacion, str) or self.operacion not in operaciones_validas:
            raise ValueError(f"Operación no válida: {self.operacion}")
        if not isinstance(self.numeros, list) or not self.numeros:
            raise ValueError("Debes escribir al menos un número")
        for numero in self.numeros:
            if type(numero) not in (int, float) or not math.isfinite(numero):
                raise ValueError("Solo se aceptan números reales y finitos")
        if self.operacion == "potencia" and len(self.numeros) != 2:
            raise ValueError("La potencia necesita dos números: base y exponente")

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
        self._validar_entrada()
        resultado = operaciones[self.operacion]()
        if type(resultado) not in (int, float) or not math.isfinite(resultado):
            raise ValueError("El resultado debe ser un número real y finito")
        return resultado


def solicitar_numero(mensaje):
    while True:
        try:
            return float(input(mensaje))
        except ValueError:
            print("Error: ingresa un número válido (puede ser decimal).")


def solicitar_lista_numeros():
    while True:
        try:
            cantidad = int(input("¿Cuántos números deseas utilizar? (mínimo 1): "))
            if cantidad < 1:
                print("Error: debes ingresar al menos un número.")
                continue
            break
        except ValueError:
            print("Error: ingresa un número entero válido.")

    numeros = []
    for i in range(cantidad):
        num = solicitar_numero(f"Ingresa el número {i + 1}: ")
        numeros.append(num)
    return numeros


def main():
    menu = """
CALCULADORA
1. Suma
2. Resta (primero menos segundo)
3. Multiplicación
4. División (primero entre segundo)
5. Promedio
6. Potencia (primero elevado al segundo)
7. Mayor
8. Menor
9. Salir
"""

    while True:
        print(menu)
        opcion = input("Elige una opción (1-9): ").strip()
        print(" ")

        if opcion == "9":
            print("¡Hasta luego!")
            break

        # Operaciones que requieren dos números en orden específico
        if opcion in ("2", "4", "6"):
            if opcion == "2":
                nombre = "resta"
                print("Resta: primero menos segundo.")
            elif opcion == "4":
                nombre = "division"
                print("División: primero entre segundo.")
            else:
                nombre = "potencia"
                print("Potencia: primero elevado al segundo.")

            x = solicitar_numero("Ingresa el primer número: ")
            y = solicitar_numero("Ingresa el segundo número: ")
            numeros = [x, y]

        # Operaciones con listas de números
        elif opcion in ("1", "3", "5", "7", "8"):
            nombres = {
                "1": "suma",
                "3": "multiplicacion",
                "5": "promedio",
                "7": "mayor",
                "8": "menor",
            }
            nombre = nombres[opcion]
            numeros = solicitar_lista_numeros()

        else:
            print("Error: opción no válida. Elige un número del 1 al 9.")
            continue

        try:
            calc = Calculadora(nombre, numeros)
            resultado = calc.resultado()
            print(f"Resultado de la {nombre}: {resultado}")
        except (ValueError, ZeroDivisionError, OverflowError) as e:
            print(f"Error: {e}")

        # Preguntar si desea continuar
        continuar = input("\n¿Deseas realizar otra operación? (s/n): ").strip().lower()
        if continuar != "s":
            print("¡Hasta luego!")
            break


if __name__ == "__main__":
    main()
