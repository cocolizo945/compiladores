from TypeSystem import *
from prettytable import PrettyTable


class ScopeSymbolTable:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.symbols = {}
        self.children = []
        self.level = 0
        if parent:
            self.level = parent.level + 1
            parent.children.append(self)
        self.table = PrettyTable()

    # representa como cadena la tabla de simbolos
    def __str__(self):
        ret = "ScopeSymbolTable(%s) - level: %d\n" % (self.name, self.level)

        keys = self.symbols.keys()
        self.table.field_names = ["lexema", "semantica", "linea", "columna", "tipo", "posicion", "herencia",
                                  "byte size", "tipo semantica", "no param"]
        for key in keys:
            self.table.add_row(
                [key, self.symbols[key][0], self.symbols[key][1], self.symbols[key][2], self.symbols[key][3],
                 self.symbols[key][4], self.symbols[key][5], self.symbols[key][6], self.symbols[key][7],
                 self.symbols[key][8]])
        ret += str(self.table) + "\n"
        return ret

    # insertar elemento
    # lexema , semantica, linea, columna, tipo,  posicion, herencia, byte size,tipo semantica, no param,
    def insert(self, name, symbol):
        self.symbols[name] = symbol

    # funcion para encontrar elemento
    def lookup(self, name, current_scope_only=False):
        symbol = None
        if name in self.symbols:
            symbol = self.symbols[name]
        else:
            if current_scope_only:
                return None
            if self.parent:
                symbol = self.parent.lookup(name)
        return symbol

    # funcion para encontrar llave en una tabla o en todas las tablas hijas.
    def ChildrenlookupKey(self, key, current_scope_only=False):
        if key in self.symbols.keys():
            return True
        else:
            if current_scope_only:
                return None
            if self.children:
                for i in self.children:
                    if i.lookupKey(key):
                        return True
        return False
    def ChildrenGetSymbol(self, key, current_scope_only=False):
        symbol = None
        if key in self.symbols:
            symbol = self.symbols[key]
        else:
            if current_scope_only:
                return None
            if self.children:
                for i in self.children:
                    if i.ChildrenGetSymbol(key):
                        symbol = i.ChildrenGetSymbol(key)
        return symbol
    # funcion para encontrar llave en una tabla o en todas las tablas.
    def lookupKey(self, key, current_scope_only=False):
        if key in self.symbols.keys():
            return True
        else:
            if current_scope_only:
                return None
            if self.parent:
                if self.parent.lookupKey(key):
                    return True
        return False

    def lookup_current_scope(self, name):
        return self.lookup(name, True)

    def get_symbols(self):
        return self.symbols

    def get_children(self):
        return self.children

    def print_children(self):
        print(len(self.children))
        for child in self.children:
            print(child)
            if len(child.children) > 0:
                child.print_children()

    def get_parent(self):
        return self.parent

    # scope
    def get_level(self):
        return self.level

    def get_name(self):
        return self.name


st = ScopeSymbolTable("global")

"""
st.insert("a", [1,2,3])
st.insert("b", 2)
st.insert("c", 3)
"""
# get value inside list
# st.symbols.get("a")[0]

# print(st.symbols.get("a")[0])
