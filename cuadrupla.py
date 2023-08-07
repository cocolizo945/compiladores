import globalVariables


class qBlock:
    def __init__(self, label, previous=None):
        self.label = label
        self.previous = previous
        self.nextQ = [] #aqui se agrega el siguiente bloque basico una vez se sepa cual es
        self.quadruples = []
        self.filed = open("inter_code.txt", "a+")
        if previous:
            previous.nextQ.append(self)
    def printQuadruples(self):
        print(self.label)
        self.filed.write(self.label + "\n")
        for quadruple in self.quadruples:
            print(quadruple)
            self.filed.write(str(quadruple) + "\n")
        self.filed.close()
    def addQuadruple(self, quadruple):
        #replace for new quadruple if exists
        #for i in range(len(self.quadruples)):
         #   if self.quadruples[i].result == quadruple.result:
          #      self.quadruples[i] = quadruple
        self.quadruples.append(quadruple)
class Quadruple:
    def __init__(self, operator, result, operand1, operand2):
        self.operator = operator
        self.operand1 = operand1
        self.operand2 = operand2
        self.result = result

    def __str__(self):
        return f'{self.operator}   {self.result}   {self.operand1}   {self.operand2} '
    def setOperator(self, operator):
        self.operator = operator
    def setOperand1(self, operand1):
        self.operand1 = operand1
    def setOperand2(self, operand2):
        self.operand2 = operand2
    def setResult(self, result):
        self.result = result

equivalencias = {}
qb = qBlock('variables:')
ob = qBlock('L1:', qb)
current_block = ob
current_label = 1
basic_blocks = [qb, ob]
tempvar = 0
terminado = True

patata_test = ""


#equivalencias["y"] = "t1"
balanza = "" # para validar si ejecutar Expr subsecuentes
#print(equivalencias.values())
print("x" in equivalencias.keys())