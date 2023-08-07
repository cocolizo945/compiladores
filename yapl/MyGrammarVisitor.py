# Generated from C:/Users/massa/Documents/Universidad/quinto año/Segundo semestre/Compiladores/newBeggining\MyGrammar.g4 by ANTLR 4.10.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .MyGrammarParser import MyGrammarParser
else:
    from MyGrammarParser import MyGrammarParser
from SymbolTable import st
# This class defines a complete generic visitor for a parse tree produced by MyGrammarParser.

class MyGrammarVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by MyGrammarParser#program.
    def visitProgram(self, ctx:MyGrammarParser.ProgramContext):
        print("holi: ",ctx.children[0].accept(self))
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyGrammarParser#class.
    def visitClass(self, ctx:MyGrammarParser.ClassContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyGrammarParser#feature.
    def visitFeature(self, ctx:MyGrammarParser.FeatureContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyGrammarParser#formal.
    def visitFormal(self, ctx:MyGrammarParser.FormalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyGrammarParser#expr.
    def visitExpr(self, ctx:MyGrammarParser.ExprContext):
        return self.visitChildren(ctx)



del MyGrammarParser