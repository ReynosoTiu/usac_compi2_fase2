class Value:
    def __init__(self,valor,isTemp,tipo):
        self.valor = valor
        self.isTemp = isTemp
        self.tipo = tipo
        self.TrueLvl = []
        self.FalseLvl = []
    
    def imprimir(self):
        print("Valor:",self.valor)
        print("isTemp:",self.isTemp)
        print("tipo:",self.tipo)
        print("TrueLvl:",self.TrueLvl)
        print("FalseLvl:",self.FalseLvl)