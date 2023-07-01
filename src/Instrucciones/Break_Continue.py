from ..Abstract.abstract import Abstract
class Break(Abstract):
    def __init__(self, fila, columna):
        super().__init__(fila, columna)

    def interpretar(self, arbol, tabla):
        return self
class Continue(Abstract):
    def __init__(self, fila, columna):
        super().__init__(fila, columna)

    def interpretar(self, arbol, tabla):
        return self