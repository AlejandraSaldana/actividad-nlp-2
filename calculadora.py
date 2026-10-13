class Calculadora:
        def __init__(self, x, y, operacion):
                self.x = x
                self.y = y
                self.operacion = operacion

        def suma(self):
                return self.x + self.y

        def resta(self):
                return self.x - self.y

        def multiplicacion(self):
                return self.x * self.y

        def division(self):
                return self.x / self.y

        def promedio(self):
                return (self.x + self.y) / 2

        def potencia(self):
                return self.x**self.y

        def mayor(self):
                return max(self.x, self.y)

        def menor(self):
                return min(self.x, self.y)

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
                return operaciones[self.operacion]()

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


def operar_lista(operacion, numeros):
    if operacion == "suma":
        return sum(numeros)
    elif operacion == "multiplicacion":
        resultado = 1
        for n in numeros:
            resultado *= n
        return resultado
    elif operacion == "promedio":
        return sum(numeros) / len(numeros)
    elif operacion == "mayor":
        return max(numeros)
    elif operacion == "menor":
        return min(numeros)
    else:
        raise ValueError(f"Operación no soportada para listas: {operacion}")


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

            if nombre == "division" and y == 0:
                print("Error: no se puede dividir entre cero.")
                continue

            try:
                calc = Calculadora(x, y, nombre)
                resultado = calc.resultado()
                print(f"Resultado de la {nombre}: {resultado}")
            except Exception as e:
                print(f"Error inesperado: {e}")

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

            try:
                resultado = operar_lista(nombre, numeros)
                print(f"Resultado de la {nombre}: {resultado}")
            except Exception as e:
                print(f"Error inesperado: {e}")

        else:
            print("Error: opción no válida. Elige un número del 1 al 9.")

        # Preguntar si desea continuar
        continuar = input("\n¿Deseas realizar otra operación? (s/n): ").strip().lower()
        if continuar != "s":
            print("¡Hasta luego!")
            break


if __name__ == "__main__":
    main()