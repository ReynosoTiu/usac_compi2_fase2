class Generador:
    
    def __init__(self):
        self.Temporal = 1
        self.Label = 1
        self.Code = []
        self.FuncCode = []
        self.Natives = []
        self.TempList = []
        self.MainCode = False
        self.PrintStringFlag = True
        self.FinalCode = ""
    #Generar un nuevo temporal
    def newTemp(self):
        temp = "t"+str(self.Temporal)
        self.Temporal += 1
        self.TempList.append(temp)
        return temp
    
    #Genera una nueva etiqueta
    def newLabel(self):
        temp = self.Label
        self.Label += 1
        return "L"+str(temp)

    # Agregando una instruccion if
    def AddIf(self,left, right, op, label):
        if self.MainCode:
            self.Code.append("if " + left + " " + op + " " + right + " { goto " + label + ";}\n")
        else:
            self.FuncCode.append("if " + left + " " + op + " " + right + " { goto " + label + ";}\n")
        
    # Agregando un salto
    def AddGoto(self,label):
        if self.MainCode:
            self.Code.append("goto " + label + ";\n")
        else:
            self.FuncCode.append("goto " + label + ";\n")

    # Agregando una expresion
    def AddExpression(self,target, left, right, op):
        if self.MainCode:
            self.Code.append(target + " = " + left + " " + op + " " + right + ";\n")
        else:
            self.FuncCode.append(target + " = " + left + " " + op + " " + right + ";\n")

    def AddExpressionPOT(self,target, left, right):
        if self.MainCode:
            self.Code.append(target + " = " + "math.Pow("+left+", "+right+");\n")
        else:
            self.FuncCode.append(target + " = " + "math.Pow("+left+", "+right+");\n")
            
    def AddExpressionMOD(self,target, left, right, op):
        if self.MainCode:
            self.Code.append(target + " = " + "float64(int("+left+") "+op+" int("+right+"));\n")
        else:
            self.FuncCode.append(target + " = " + "float64(int("+left+") "+op+" int("+right+"));\n")

    # Agregando una etiqueta
    def AddLabel(self,label):
        if self.MainCode:
            self.Code.append(label + ":\n")
        else:
            self.FuncCode.append(label + ":\n")

    # Agregando una asignacion
    def AddAssign(self,target, val):
        if self.MainCode:
            self.Code.append(target + " = " + val + ";\n")
        else:
            self.FuncCode.append(target + " = " + val + ";\n")


    # Agregando un comentario
    def AddComment(self,val):
        if  self.MainCode:
            self.Code.append("/* "+val+" */\n")
        else:
            self.FuncCode.append("// "+val+"\n")
    
    # Agregando inicia funcion
    def AddFunctionBegin(self,id_funtion):
        self.FuncCode.append("func "+id_funtion+"(){\n")

    # Agregando fin funcion
    def AddFunctionEnd(self):
        self.FuncCode.append("\nreturn;\n}\n")

    # Agregando una llamada
    def AddCall(self,target):
        if self.MainCode:
            self.Code.append(target+"();\n")
        else:
            self.FuncCode.append(target+"();\n")

    #set heap
    def AddSetHeap(self, index, value):
        if self.MainCode:
            self.Code.append("heap[" + index + "] = " + value + ";\n")
        else:
            self.FuncCode.append("heap[" + index + "] = " + value + ";\n")

    #set heap
    def AddSetStack(self,index, value):
        if self.MainCode:
            self.Code.append("stack[" + index + "] = " + value + ";\n")
        else:
            self.FuncCode.append("stack[" + index + "] = " + value + ";\n")
    

    #get heap
    def AddGetHeap(self,target, index):
        if self.MainCode:
            self.Code.append(target + " = heap[" + index + "];\n")
        else:
            self.FuncCode.append(target + " = heap[" + index + "];\n")

    #get stack
    def AddGetStack(self,target, index):
        if self.MainCode:
            self.Code.append(target + " = stack[" + index + "];\n")
        else:
            self.FuncCode.append(target + " = stack[" + index + "];\n")

    #agrega un salto de linea
    def AddBr(self):
        if self.MainCode:
            self.Code.append("\n")
        else:
            self.FuncCode.append("\n")
    
    #agrega un printf
    def AddPrintf(self,typePrint, value):
        if self.MainCode:
            self.Code.append("fmt.Printf(\"%" + typePrint + "\", " + value + ");\n")
        else:
            self.FuncCode.append("fmt.Printf(\"%" + typePrint + "\", " + value + ");\n")

    #Agrega un print del string
    def GeneratePrintString(self):
        if self.PrintStringFlag:
            #generando temporales y etiquetas
            newTemp1 = self.newTemp()
            newTemp2 = self.newTemp()
            newTemp3 = self.newTemp()
            newLvl1 = self.newLabel()
            newLvl2 = self.newLabel()
            #se genera la funcion printstring
            self.Natives.append("func printString() {\n")
            self.Natives.append("\t" + newTemp1 + " = P + 1;\n")
            self.Natives.append("\t" + newTemp2 + " = stack[int(" + newTemp1 + ")];\n")
            self.Natives.append("\t" + newLvl2 + ":\n")
            self.Natives.append("\t" + newTemp3 + " = heap[int(" + newTemp2 + ")];\n")
            self.Natives.append("\tif " + newTemp3 + " == -1 {goto " + newLvl1 + ";}\n")
            self.Natives.append("\tfmt.Printf(\"%c\", int(" + newTemp3 + "));\n")
            self.Natives.append("\t" + newTemp2 + " = " + newTemp2 + " + 1;\n")
            self.Natives.append("\tgoto " + newLvl2 + ";\n")
            self.Natives.append("\t" + newLvl1 + ":\n")
            self.Natives.append("\treturn;\n")
            self.Natives.append("}\n\n")
            self.PrintStringFlag = False
        
    

    #Generando codigo final
    def GenerateFinalCode(self):
        #creando cabecera
        self.FinalCode += "//****************** Compiladores C3D ******************\n\n"
        self.FinalCode += "package main\n"
        self.FinalCode += "import (\n\t\"fmt\"\n\t\"math\"\n)\n"
        self.FinalCode += "var stack[100000] float64;\n"
        self.FinalCode += "var heap[100000] float64;\n"
        self.FinalCode += "var P float64;\n"
        self.FinalCode += "var H float64;\n"
        #agregando temporales
        if len(self.TempList) > 0:
            tmpDec = "var " +self.TempList[0]
            for i in range(1,len(self.TempList)):
                tmpDec += ", "+self.TempList[i]
            tmpDec += " float64;\n\n"
            self.FinalCode += tmpDec

        #agregando funciones
        for i in range(len(self.FuncCode)):
            self.FinalCode += self.FuncCode[i]

        #agregando funciones nativas
        for i in range(len(self.Natives)):
            self.FinalCode += self.Natives[i]        
        
        #agregando main()
        self.FinalCode += "func main(){\n"
        for i in self.Code:
            self.FinalCode += "\t"
            self.FinalCode += i
        self.FinalCode += "\t\n}"
    



