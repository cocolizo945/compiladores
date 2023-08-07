# Generated from C:/Users/massa/Documents/Universidad/quinto a�o/Segundo semestre/Compiladores/newBeggining\MyGrammar.g4 by ANTLR 4.10.1
from antlr4 import *

import Constants
import globalVariables
from cuadrupla import *
import cuadrupla
from TypeSystem import type_system
if __name__ is not None and "." in __name__:
    from .MyGrammarParser import MyGrammarParser
else:
    from MyGrammarParser import MyGrammarParser
from Errors import ett
from SymbolTable import *
from globalVariables import *



# tabla de simbolos
# lexema , semantica, linea, columna, tipo,  posicion, herencia, byte size,tipo semantica, no param


#operaciones de nodos hermanos
def getNodeIndex(node):
    if (node.parentCtx == None or node == None):
        return -1
    parent = node.parentCtx
    for i in range(len(parent.children)):
        if (parent.children[i] == node):
            return i


def getLeftSibling(node):
    index = getNodeIndex(node)
    if (index < 1):
        return None
    return node.parentCtx.children[index - 1]

def getRightSibling(node):
    index = getNodeIndex(node)
    if (index == -1 or index >= len(node.parentCtx.children) - 2):
        return -1
    return node.parentCtx.children[index + 2]

def getTable(name, list):
    for x in list:
        if x.name == name:
            return x


def getFather(name, list):
    for x in list:
        if x.name == name:
            return x.parent

# This class defines a complete listener for a parse tree produced by MyGrammarParser.
class MyGrammarListener(ParseTreeListener):
    def __init__(self):
        self.ant = 0
        self.lt = None  # ultima tabla utilizada
        self.propiedad = ""
        self.cb = None # ultimo bloque de codigo utilizado
    # Enter a parse tree produced by MyGrammarParser#program.
    def enterProgram(self, ctx: MyGrammarParser.ProgramContext):

        self.ant += 1
        type_system.add_core_scopes()

        pass

    # Exit a parse tree produced by MyGrammarParser#program.
    def exitProgram(self, ctx: MyGrammarParser.ProgramContext):
        # print("hola desde EXIT PROGRAM: ", self.ant)
        if "Main" not in st.symbols.keys():
            print("ERROR: Class Main does not exist")
            ett.addError("ERROR: Class Main does not exist")

    # Enter a parse tree produced by MyGrammarParser#class.
    def enterClass(self, ctx: MyGrammarParser.ClassContext):
        self.ant += 1
        self.propiedad = "class"
        lex = ctx.children[1].symbol.text
        token = ctx.children[1].symbol.type
        line = ctx.children[0].getSymbol().line
        column = ctx.children[0].getSymbol().column
        inherits = ""
        byteSize = 0
        sem_type = "class"
        noParam = 0
        clean_error = True
        print("entering class: ", lex)
        # check Lex existance
        if lex in st.symbols.keys():
            clean_error = False
            print("ERROR: Class " + lex + " already exists in line " + str(line) + " column " + str(column))
            ett.addError("ERROR: Class " + lex + " already exists in line " + str(line) + " column " + str(column))

        # inherits
        for i in ctx.children:
            if i.getText() == "inherits":
                inherits = ctx.children[ctx.children.index(i) + 1].getText()
                if inherits not in st.symbols.keys():
                    clean_error = False
                    print(
                        "ERROR: Class " + inherits + " does not exist in line " + str(line) + " column " + str(column))
                    ett.addError(
                        "ERROR: Class " + inherits + " does not exist in line " + str(line) + " column " + str(column))
                if inherits == lex:
                    clean_error = False
                    print("ERROR: Class " + lex + " cannot inherit from itself in line " + str(line) + " column " + str(
                        column))
                    ett.addError(
                        "ERROR: Class " + lex + " cannot inherit from itself in line " + str(line) + " column " + str(
                            column))
                break

        if clean_error:
            st.insert(lex, [token, line, column, "", globalVariables.memPos, inherits, byteSize, sem_type, noParam])
            self.lt = st
            if st not in tableList:
                tableList.append(st)
            #st.insert(lex, [token, line, column, "", 0, inherits, byteSize, sem_type, noParam])
        pass

    # Exit a parse tree produced by MyGrammarParser#class.
    def exitClass(self, ctx: MyGrammarParser.ClassContext):
        print("exiting class")
        pass

    # Enter a parse tree produced by MyGrammarParser#feature.
    def enterFeature(self, ctx: MyGrammarParser.FeatureContext):
        print("entering feature")
        line = ctx.children[0].getSymbol().line
        column = ctx.children[0].getSymbol().column
        byteSize = 0
        sem_type = "null"
        noParam = 0

        #areas de pruebas de ctx



        # insertar feature
        parentName = ctx.parentCtx.children[1].getText()
        ID = ctx.children[0].getText()
        st2 = self.lt

        #Assignment check
        type_system.check_assignment(ctx)

        if ett.getError() == "":
            if self.lt.name == "global":
                st2 = ScopeSymbolTable(parentName, self.lt)
                #- Self Insertion
                st2.insert("self", [44, line, column, parentName, globalVariables.memPos, "", byteSize, "reference", noParam]) #sem_type

            # Type insertion
            type_ = ""
            for child in ctx.children:
                if child.getText() == ":":
                    type_ = ctx.children[ctx.children.index(child) + 1].getText()
                    sem_type = "Reference"
                    if type_ == "SELF_TYPE":
                        type_ = parentName
                    break
            if ctx.children[1].getText() == "(":
                sem_type = "method"
                # Method insertion (hypothetical)
                #noParam = len(ctx.children[3].children)
                #st2.insert(ID, [43, line, column, type_, globalVariables.memPos, "", byteSize, sem_type, noParam])
            #--------------------------------------------
            #define byteSize
            if type_ == "Int":
                byteSize = 4
            elif type_ == "Bool":
                byteSize = 1
            elif type_ == "String":
                byteSize = 50
            elif type_ == "SELF_TYPE" or st2.lookup(type_):
                byteSize = 100
            elif type_ == "Object":
                byteSize = 75
            elif type_ == "IO":
                byteSize = 100

            st2.insert(ID, [ctx.children[0].symbol.type, line, column, type_, globalVariables.memPos, "",byteSize,sem_type,noParam])
            self.lt = st2
            self.propiedad = "feature"
            if st2 not in tableList:
                tableList.append(st2)
        globalVariables.memPos = globalVariables.memPos + byteSize
        self.ant += 1

    # Exit a parse tree produced by MyGrammarParser#feature.
    def exitFeature(self, ctx: MyGrammarParser.FeatureContext):

        print("exiting feature: ", cuadrupla.patata_test)

        """
        for i in self.lt.symbols.keys():
            print("I: ",i)
            print("ID: ", ID)
            if i == ID:
                print("ERROR: Feature "+ID+ " already exists in line "+str(line)+" column "+str(column))
                ett.addError("ERROR: Feature "+ID+ " already exists in line "+str(line)+" column "+str(column))
                break
        ##print("hola desde exit feature: ", self.ant)
        pass
        """

    # Enter a parse tree produced by MyGrammarParser#formal.
    def enterFormal(self, ctx: MyGrammarParser.FormalContext):
        print("entering formal")
        line = ctx.children[0].getSymbol().line
        column = ctx.children[0].getSymbol().column
        ID = ctx.children[0].getText()
        parentName = ctx.parentCtx.children[0].getText()
        st3 = self.lt
        byteSize = 0
        sem_type = "null"
        noParam = 1

        #get no. of parameters
        for i in ctx.parentCtx.children:
            if i.getText() == ",":
                noParam = noParam + 1

        #inserting param number in parent
        if hasattr(st3.parent,"symbols") and  parentName in st3.parent.symbols.keys():

            #get parent current attributes
            parent = st3.parent.symbols[parentName]
            parent[8] = noParam
            st3.parent.insert(parentName, parent)

        if ett.getError() == "":
            if self.propiedad == "class" or self.propiedad == "feature":
                print("insertando formal: ", self.lt.name)
                st3 = ScopeSymbolTable(parentName, self.lt)

            # Type insertion - Amado
            type_ = ""
            for child in ctx.children:
                if child.getText() == ":":
                    type_ = ctx.children[ctx.children.index(child) + 1].getText() #revisar existencias del feature
                    if st3.lookupKey(type_) == True:
                        pass
                    else:
                        print("ERROR: Type " + type_ + " does not exist in line " + str(line) + " column " + str(column))
                        ett.addError("ERROR: Type " + type_ + " does not exist in line " + str(line) + " column " + str(column))
                    sem_type = "parameter"

                    break
            #--------------------------------------------  BYTE SIZE
            if type_ == "Int":
                byteSize = 4
            elif type_ == "Bool":
                byteSize = 1
            elif type_ == "String":
                byteSize = 50
            elif type_ == "SELF_TYPE" or st3.lookup(type_):
                byteSize = 100
            elif type_ == "Object":
                byteSize = 75
            elif type_ == "IO":
                byteSize = 100
            # --------------------------------------------
            st3.insert(ID, [ctx.children[0].symbol.type, line, column, type_, globalVariables.memPos, "", byteSize,sem_type,0])
            self.lt = st3
            self.propiedad = "formal"
            #insertar formal en cuadruplas
            type_system.checkFormalOp(ctx,ID,type_)
            if st3 not in tableList:
                tableList.append(st3)

        globalVariables.memPos = globalVariables.memPos + byteSize
        pass

    # Exit a parse tree produced by MyGrammarParser#formal.
    def exitFormal(self, ctx: MyGrammarParser.FormalContext):


        pass

    # Enter a parse tree produced by MyGrammarParser#expr.
    def enterExpr(self, ctx: MyGrammarParser.ExprContext):
        type_system.checkExprOp(ctx)
        type_system.if_statement(ctx)
        #type_system.checkSingleReturn(ctx)
        if globalVariables.is_if == True and len(ctx.children) > 1:
            type_system.check_comparison(ctx)
            print("entering if expr: ", ctx.children[0].getText())

            #cuadrupla.if_stack.append(cuadrupla.nextQuad())
            #cuadrupla.addCuadrupla("GOTOF", "t" + str(cuadrupla.tempCount - 1), "_", "_")
        pass

    # Exit a parse tree produced by MyGrammarParser#expr.
    def exitExpr(self, ctx: MyGrammarParser.ExprContext):
        self.ant += 1
        if ctx.children[-1] == "fi":
            is_if = False
            #cuadrupla.addCuadrupla("GOTO", "_", "_", "_")
            #cuadrupla.fill(cuadrupla.if_stack.pop(), cuadrupla.nextQuad())



del MyGrammarParser
