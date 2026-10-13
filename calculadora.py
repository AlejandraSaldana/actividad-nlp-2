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
    



