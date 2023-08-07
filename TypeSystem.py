import cuadrupla
import globalVariables
from Constants import core_scopes, core_scopes_types, tokens, byte_sizes, operands
from Errors import ett
from cuadrupla import *
from SymbolTable import ScopeSymbolTable, st
from yapl.MyGrammarParser import MyGrammarParser
from globalVariables import *

#obtener nodos hermanos

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
#funcion para obtener la variable temporal o el valor asigando a cada llave
def eq_map(key):
    value = None
    if isinstance(key, int):
        value = key
        pass
    else:
        if key in cuadrupla.equivalencias.keys():
            value = cuadrupla.equivalencias[key]
        else:
            value = "$t"+str(cuadrupla.tempvar)
            cuadrupla.equivalencias[key] = value
            cuadrupla.tempvar += 1

    return value

def check_List(list):
    operandos = ["+", "-", "*", "/"]
    op  = 0
    validate = False
    for i in list:
        if i.getText() in operandos:
            op = i.getText()
            validate = True
        return validate, op
def commonChar(str1,str2):
    for i in str1:
        for j in str2:
            if i == j:
                return True

def operator_reducer(ctx, first_key, last_key, last_opertor):
    operandos = ["+", "-", "*", "/"]
    value = None
    is_op = False
    current_list = ctx
    arg1 = None
    arg2 = None
    result = None
    cont = 0
    cant = 0
    done = False
    op = None
    temp_result = None
    validate = False
    while not done:

        for i in current_list:
            if i in operandos:
                op = i
                is_op = True


        if is_op:
            if cont == 0:
                arg1 = ctx[0]
                arg2 = ctx[2]
                result = "$t"+str(cuadrupla.tempvar)
                cuadrupla.tempvar += 1
                cuadrupla.current_block.addQuadruple(Quadruple(op, result, arg1, arg2))
                temp_result = result
                current_list = current_list[3:]
                cont += 1
            elif cont == 1:
                arg2 = current_list[1]
                result = temp_result
                cuadrupla.tempvar += 1
                op = current_list[0]
                cuadrupla.current_block.addQuadruple(Quadruple(op, result, result, arg2))
                current_list = current_list[2:]
        else:
            done = True

        is_op = False
    #verificar si es entero
    try:  # verificar si es un int
        last_key= int(last_key)
    except ValueError:
        pass
    first_key = eq_map(first_key)
    last_key = eq_map(last_key)
    #inserción de cuadruplas
    cuadrupla.current_block.addQuadruple(Quadruple(last_opertor, temp_result, temp_result, last_key))
    cuadrupla.current_block.addQuadruple(Quadruple("+", first_key, first_key, temp_result))

class TypeSystem:
    def __init__(self):
        self.current_block = None
        pass

    @staticmethod
    def add_core_scopes():
        for core_scope in core_scopes:
            symbol_table = ScopeSymbolTable(core_scope, st)
            st.insert(core_scope, [tokens['TYPE'], 0, 0, "", globalVariables.memPos, "", byte_sizes[core_scope], "class", 0])
            if core_scope == "Int":
                globalVariables.memPos += 4
            elif core_scope == "Bool":
                globalVariables.memPos += 1
            for core_scopes_type in core_scopes_types[core_scope]:
                symbol_table.insert(core_scopes_type[0], [tokens['TYPE'], 0, 0, core_scopes_type[1], globalVariables.memPos, "",
                                                          byte_sizes[core_scopes_type[1]], "class", 0])
                if core_scope == "String":
                    globalVariables.memPos += 50
                elif core_scope == "Object":
                    globalVariables.memPos += 75
                elif core_scope == "IO":
                    globalVariables.memPos += 100


    def get_children(self, child, arr, ctx):
        token_keys = list(tokens.keys())
        for c in child.children:
            if isinstance(c, MyGrammarParser.ExprContext):
                self.get_children(c, arr, ctx)
            else:
                if hasattr(child.children[0], 'symbol') and\
                        token_keys[list(tokens.values()).index(child.children[0].symbol.type)] != 'INTEGER' \
                        and c.getText() != '+' and c.getText() != '-' and c.getText() != '*' and c.getText() != '/':
                    print("ERROR: Invalid Arithmetic types in " + str(child.children[0].getSymbol().line)
                          + " column " + str(child.children[0].getSymbol().column))
                    ett.addError(
                        "ERROR: Invalid Arithmetic types in  " + str(child.children[0].getSymbol().line)
                        + " column " + str(child.children[0].getSymbol().column))

                arr.append(c.getText())

    def check_arithmetic(self, ctx, expected_type):
        expr = ctx.children[-1]
        arr = []

        for child in expr.children:
            if isinstance(child, MyGrammarParser.ExprContext):
                self.get_children(child, arr, ctx)
            else:
                if child.symbol.type != 41:
                    print("ERROR call from check_arithmetic: ", ctx.children[0].getText())
                    print("ERROR: Invalid Arithmetic operation in " + str(ctx.children[0].getSymbol().line)
                          + " column " + str(ctx.children[0].getSymbol().column))
                    ett.addError(
                        "ERROR: Invalid Arithmetic operation in  " + str(ctx.children[0].getSymbol().line)
                        + " column " + str(ctx.children[0].getSymbol().column))
                    return
                else:
                    arr.append(child.getText())

        is_previous_operand = False
        for element in arr:
            if element == '+' or element == '-' or element == '*' or element == '/':
                if is_previous_operand:
                    print("ERROR: Invalid Arithmetic operation in " + str(ctx.children[0].getSymbol().line)
                          + " column " + str(ctx.children[0].getSymbol().column))
                    ett.addError(
                        "ERROR: Invalid Arithmetic operation in  " + str(ctx.children[0].getSymbol().line)
                        + " column " + str(ctx.children[0].getSymbol().column))
                is_previous_operand = True
            else:
                is_previous_operand = False

    def check_assignment(self, ctx):

        expected_type = ''
        expected_typeL = ''
        for child in ctx.children:
            if child.getText() == ":":
                expected_type = ctx.children[ctx.children.index(child) + 1].getText().upper()
                expected_typeL = ctx.children[ctx.children.index(child) + 1].getText()
        token_keys = list(tokens.keys())
        if isinstance(ctx.children[-1], MyGrammarParser.ExprContext) \
                and len(ctx.children[-1].children) > 1 \
                and ctx.children[-1].children[1].getText() in operands:
            self.check_arithmetic(ctx, expected_type)
        elif expected_type == 'BOOLEAN':
            self.check_boolean_assignment(ctx, token_keys)
        elif expected_type == 'INT':
            self.check_int_assignment(ctx, token_keys)
        elif expected_type == 'STRING':
            self.check_string_assignment(ctx, token_keys)
        elif expected_type == 'SELF_TYPE':
            self.check_self_type_assignment(ctx, token_keys)
        elif st.ChildrenlookupKey(expected_typeL):
            self.check_object_assignment(ctx, token_keys, expected_typeL)


    def check_boolean_assignment(self, ctx, token_keys):
        error = False
        if token_keys[list(tokens.values()).index(ctx.children[-1].children[0].symbol.type)] != 'INTEGER':
            if ctx.children[-1].getText() != 'true' and ctx.children[-1].getText() != 'false':
                self.type_mismatch_error(ctx)
                error = True
        elif token_keys[list(tokens.values()).index(ctx.children[-1].children[0].symbol.type)] == 'INTEGER' \
                and ctx.children[-1].children[0].getText() != '1' \
                and ctx.children[-1].children[0].getText() != '0':
            self.type_mismatch_error(ctx)
            error = True
        if not error:
            arg1 = eq_map(ctx.children[0].getText())
            if ctx.children[-1].getText() != "}":
                print("calling from booleanT: ", ctx.children[0].getText())
                if len(ctx.children) == 3:
                    cuadrupla.qb.addQuadruple(Quadruple("=b", arg1, "", ""))
                if len(ctx.children) == 5:
                    cuadrupla.qb.addQuadruple(Quadruple("=b", arg1, ctx.children[-1].getText(), ""))

    def check_int_assignment(self, ctx, token_keys):
        arg1 = None
        arg2 = None
        if hasattr(ctx.children[-1], 'children') and hasattr(ctx.children[-1].children[0], 'symbol') and \
                token_keys[list(tokens.values()).index(ctx.children[-1].children[0].symbol.type)] != 'INTEGER':
            self.type_mismatch_error(ctx)
        elif ctx.children[-1].getText() != "}":

            arg1 = eq_map(ctx.children[0].getText())
            if len(ctx.children) == 3:
                cuadrupla.qb.addQuadruple(Quadruple("=i", arg1, "", ""))
            if len(ctx.children) == 5:
                arg2 = eq_map(int(ctx.children[4].children[0].getText()))
                cuadrupla.qb.addQuadruple(Quadruple("=i", arg1, arg2, ""))
                print("calling from integer: ", getRightSibling(ctx))
                if str(getRightSibling(ctx)) == "}":
                    cuadrupla.qb.addQuadruple(Quadruple("ri", arg1, "", ""))

    def check_string_assignment(self, ctx, token_keys):
        arg1 = None
        arg2 = None
        if hasattr(ctx.children[-1], 'children') and hasattr(ctx.children[-1].children[0], 'symbol') and \
                token_keys[list(tokens.values()).index(ctx.children[-1].children[0].symbol.type)] != 'STRING':
            self.type_mismatch_error(ctx)
        elif ctx.children[-1].getText() != "}":
            arg1 = ctx.children[0].getText()
            print("calling from String: ", ctx.children[0].getText())
            if len(ctx.children) == 3:
                print("calling from string: ", ctx.children[-1].getText())

                cuadrupla.qb.addQuadruple(Quadruple("=s", arg1, "", ""))
            if len(ctx.children) == 5:
                print("calling from string: ", ctx.children[-1].getText())
                cuadrupla.qb.addQuadruple(Quadruple("=s", arg1, ctx.children[4].children[0], ""))
                if str(getRightSibling(ctx)) == "}":
                    cuadrupla.qb.addQuadruple(Quadruple("rs", arg1, "", ""))

    def check_self_type_assignment(self, ctx, token_keys):
        if hasattr(ctx.children[-1], 'children') and hasattr(ctx.children[-1].children[0], 'symbol') and \
                token_keys[list(tokens.values()).index(ctx.children[-1].children[0].symbol.type)] != 'SELF_TYPE':
            self.type_mismatch_error(ctx)

        pass

    def check_object_assignment(self, ctx, token_keys, expected_type):

        if hasattr(ctx.children[-1], 'children') and hasattr(ctx.children[-1].children[0], 'symbol') and \
                token_keys[list(tokens.values()).index(ctx.children[-1].children[0].symbol.type)] != expected_type:
            self.type_mismatch_error(ctx)

        elif ctx.children[-1].getText() != "}":
            print("calling from integer: ", ctx.children[0].getText())
            if len(ctx.children) == 3:
                print("calling from object: ", ctx.children[-1].getText())
                cuadrupla.qb.addQuadruple(Quadruple("=o", ctx.children[0], "", ""))
            if len(ctx.children) == 5:
                obj = ctx.children[4].children[0].children[1].children[1].getText()
                print("calling from object: ", ctx.children[-1].getText())
                if st.ChildrenlookupKey(obj) == True:
                    cuadrupla.qb.addQuadruple(Quadruple("=o", ctx.children[0], str(obj)+"["+str(st.ChildrenGetSymbol(obj)[4])+"]", ""))
                else:
                    print("ERROR: Trying to make an object out of a non existing class in line " + str(ctx.children[0].getSymbol().line) + " column " + str(
                        ctx.children[0].getSymbol().column))
                    ett.addError(
                        "ERROR: Trying to make an object out of a non existing class in line " + str(ctx.children[0].getSymbol().line) + " column " + str(
                            ctx.children[0].getSymbol().column))

    @staticmethod
    def type_mismatch_error(ctx):
        print("ERROR: Type mismatch in line " + str(ctx.children[0].getSymbol().line) + " column " + str(
            ctx.children[0].getSymbol().column))
        ett.addError("ERROR: Type mismatch in line " + str(ctx.children[0].getSymbol().line) + " column " + str(
            ctx.children[0].getSymbol().column))




    def getMemorySize(self, type, tree):
        if type == "Int":
            globalVariables.memPos += 4
        elif type == "Bool":
            globalVariables.memPos += 1
        elif type == "String":
            globalVariables.memPos += 50
        elif type == "Object":
            globalVariables.memPos += 75
        elif type == "IO":
            globalVariables.memPos += 100
        elif type == "SELF_TYPE" or tree.lookupKey(type):
            globalVariables.memPos += 100

    @staticmethod
    def checkSingleReturn(ctx):
        arg = ctx.children[0].getText()
        if len(ctx.parentCtx.children) == 4 and st.ChildrenlookupKey(ctx.children[0].getText()) == True:
            type_ = st.ChildrenGetSymbol(ctx.children[0].getText())[3]
            if type_ == "Int":
                arg = eq_map(arg)
                cuadrupla.ob.addQuadruple(Quadruple("ri", arg, "", ""))
    @staticmethod
    def checkFormalOp(ctx, ID, type_):
        operand = ""
        arg = ""
        if type_ == "Int":
            operand = "=i"
        elif type_ == "Bool":
            operand = "=b"
        elif type_ == "String":
            operand = "=s"
        elif type_ == "Object":
            operand = "=o"
        if len(ctx.children) == 5:
            arg = ctx.children[4].getText()
        ID = eq_map(ID)
        cuadrupla.qb.addQuadruple(Quadruple(operand, ID, arg, ""))
    @staticmethod
    def checkExprOp(ctx):
        is_op = False
        operator = ""
        operands = ["+", "-", "*", "/"]
        index = 0
        contador = 0

        brother = str(getLeftSibling(ctx)) #determinar si estamos en un then

        # contar cantidad de operaciones
        if globalVariables.is_if and brother == "then":
            for i in cuadrupla.basic_blocks:
                if i.label == "L"+str(cuadrupla.current_label)+":": #buscar el bloque actual
                    cuadrupla.current_block = i
                    break

        if globalVariables.is_if and brother == "else":
            cuadrupla.current_block = cuadrupla.ob

        #que bloque escribir con base a si es un if


        # operator, arg1, arg2, result
        for i in ctx.children:
            if i.getText() in operands:
                is_op = True
                operator = i.getText()
                index = ctx.children.index(i)
                break

        if is_op:

            arg1 = ctx.children[index - 1].getText()
            arg2 = ctx.children[index + 1].getText()
            rst = ctx.parentCtx.children[0].getText()

            if ("+" in ctx.children[index - 1].getText() or "-" in ctx.children[index - 1].getText() or "*" in \
                    ctx.children[index - 1].getText() or "/" in ctx.children[index - 1].getText()) and not (arg2  in cuadrupla.balanza):
                cuadrupla.balanza = ctx.children[index - 1].getText()
                contador += 1
                #take care of expressions with multiple operators
                operator_reducer(ctx.children[index - 1].getText(),rst,arg2,ctx.children[index])
            else:
                try:  # verificar si es un int
                    arg1 = int(arg1)
                except ValueError:
                    pass
                try:
                    arg2 = int(arg2)
                except ValueError:
                    pass
                arg1 = eq_map(arg1)
                arg2 = eq_map(arg2)
                rst = eq_map(rst)
                if operator == "+":
                    if ctx.parentCtx.children[1].getText() == "=":
                        cuadrupla.current_block.addQuadruple(
                            Quadruple("+", rst, arg1, arg2))
                        print(cuadrupla.equivalencias)
                    else:
                        name = ctx.parentCtx.parentCtx.children[0].getText()
                        print("calling form return assignment", str(getLeftSibling(ctx.parentCtx)))
                        if (st.ChildrenlookupKey(name)):
                            if st.ChildrenGetSymbol(name)[7] == "method":
                                cuadrupla.ob.addQuadruple(Quadruple("ri", ctx.children[index].getText(), arg1, arg2))
                        if (str(getLeftSibling(ctx.parentCtx))=="else"):
                            cuadrupla.ob.addQuadruple(Quadruple("ri", ctx.children[index].getText(), arg1, arg2))
                        if (str(getLeftSibling(ctx.parentCtx))== "then"):
                            cuadrupla.current_block.addQuadruple(Quadruple("ri", ctx.children[index].getText(), arg1, arg2))
                if operator == "-":
                    if ctx.parentCtx.children[1].getText() == "=":
                        cuadrupla.current_block.addQuadruple(
                            Quadruple("-", rst, arg1, arg2))
                        print(cuadrupla.equivalencias)
                    else:
                        name = ctx.parentCtx.parentCtx.children[0].getText()
                        print("calling form return assignment", str(getLeftSibling(ctx.parentCtx)))
                        if (st.ChildrenlookupKey(name)):
                            if st.ChildrenGetSymbol(name)[7] == "method":
                                cuadrupla.ob.addQuadruple(Quadruple("ri", ctx.children[index].getText(), arg1, arg2))
                        if (str(getLeftSibling(ctx.parentCtx))=="else"):
                            cuadrupla.ob.addQuadruple(Quadruple("ri", ctx.children[index].getText(), arg1, arg2))
                        if (str(getLeftSibling(ctx.parentCtx))== "then"):
                            cuadrupla.current_block.addQuadruple(Quadruple("ri", ctx.children[index].getText(), arg1, arg2))
                if operator == "*":
                    if ctx.parentCtx.children[1].getText() == "=":
                        cuadrupla.current_block.addQuadruple(
                            Quadruple("*", rst, arg1, arg2))
                        print(cuadrupla.equivalencias)
                    else:
                        name = ctx.parentCtx.parentCtx.children[0].getText()
                        print("calling form return assignment", str(getLeftSibling(ctx.parentCtx)))
                        if (st.ChildrenlookupKey(name)):
                            if st.ChildrenGetSymbol(name)[7] == "method":
                                cuadrupla.ob.addQuadruple(Quadruple("ri", ctx.children[index].getText(), arg1, arg2))
                        if (str(getLeftSibling(ctx.parentCtx))=="else"):
                            cuadrupla.ob.addQuadruple(Quadruple("ri", ctx.children[index].getText(), arg1, arg2))
                        if (str(getLeftSibling(ctx.parentCtx))== "then"):
                            cuadrupla.current_block.addQuadruple(Quadruple("ri", ctx.children[index].getText(), arg1, arg2))
                if operator == "/":
                    if ctx.parentCtx.children[1].getText() == "=":
                        cuadrupla.current_block.addQuadruple(
                            Quadruple("/", rst, arg1, arg2))
                        print(cuadrupla.equivalencias)
                    else:
                        name = ctx.parentCtx.parentCtx.children[0].getText()
                        print("calling form return assignment", str(getLeftSibling(ctx.parentCtx)))
                        if (st.ChildrenlookupKey(name)):
                            if st.ChildrenGetSymbol(name)[7] == "method":
                                cuadrupla.ob.addQuadruple(Quadruple("ri", ctx.children[index].getText(), arg1, arg2))
                        if (str(getLeftSibling(ctx.parentCtx))=="else"):
                            cuadrupla.ob.addQuadruple(Quadruple("ri", ctx.children[index].getText(), arg1, arg2))
                        if (str(getLeftSibling(ctx.parentCtx))== "then"):
                            cuadrupla.current_block.addQuadruple(Quadruple("ri", ctx.children[index].getText(), arg1, arg2))



    def check_comparison(self,ctx):
        #print("check comparison:", ctx.children[0].g)
        sibling = str(getLeftSibling(ctx))

        print("sibling:", sibling)
        if sibling == "if":
            if ctx.children[1].getText() == "=":
                arg1 = ctx.children[0].getText()
                arg2 = ctx.children[2].getText()
                try:
                    arg1 = int(arg1)
                except ValueError:
                    pass
                try:
                    arg2 = int(arg2)
                except ValueError:
                    pass
                arg1 = eq_map(arg1)
                arg2 = eq_map(arg2)

                cuadrupla.ob.addQuadruple(Quadruple("==", arg1, arg2, "L" + str(cuadrupla.current_label)))
            if ctx.children[1].getText() == "<":
                arg1 = ctx.children[0].getText()
                arg2 = ctx.children[2].getText()
                try:
                    arg1 = int(arg1)
                except ValueError:
                    pass
                try:
                    arg2 = int(arg2)
                except ValueError:
                    pass
                arg1 = eq_map(arg1)
                arg2 = eq_map(arg2)
                cuadrupla.ob.addQuadruple(Quadruple("<", arg1, arg2, "L" + str(cuadrupla.current_label)))
                cuadrupla.temp_counter += 1
            if ctx.children[1].getText() == ">":
                arg1 = ctx.children[0].getText()
                arg2 = ctx.children[2].getText()
                try:
                    arg1 = int(arg1)
                except ValueError:
                    pass
                try:
                    arg2 = int(arg2)
                except ValueError:
                    pass
                arg1 = eq_map(arg1)
                arg2 = eq_map(arg2)
                cuadrupla.ob.addQuadruple(Quadruple(">", arg1, arg2, "L" + str(cuadrupla.current_label)))
                cuadrupla.temp_counter += 1
            if ctx.children[1].getText() == "<=":
                arg1 = ctx.children[0].getText()
                arg2 = ctx.children[2].getText()
                try:
                    arg1 = int(arg1)
                except ValueError:
                    pass
                try:
                    arg2 = int(arg2)
                except ValueError:
                    pass
                arg1 = eq_map(arg1)
                arg2 = eq_map(arg2)
                cuadrupla.ob.addQuadruple(Quadruple("<=", arg1, arg2, "L" + str(cuadrupla.current_label)))

    @staticmethod
    def if_statement(ctx):
        if ctx.children[0].getText() == "if":
            if ctx.children[2].getText() == "then":
                if ctx.children[4].getText() == "else":
                    if ctx.children[6].getText() == "fi":
                        globalVariables.is_if = True
                        cuadrupla.current_label += 1
                        truelist = qBlock("L"+str(cuadrupla.current_label)+":")
                        cuadrupla.basic_blocks.append(truelist)
                        """
                        ype_system.check_assignment(ctx.children[1])
                        type_system.check_assignment(ctx.children[3])
                        type_system.check_assignment(ctx.children[5])
                        """
                    else:

                        return "error"
                else:

                    return "error"
            else:

                return "error"
        else:
            return "error"



type_system = TypeSystem()

