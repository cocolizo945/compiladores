import sys
from antlr4 import *
import PySimpleGUI as pg
import os

import Constants
import Object_code
import cuadrupla
from TypeSystem import type_system
from yapl import *
from yapl.MyGrammarErrorListener import MyGrammarErrorListener

from yapl.MyGrammarLexer import MyGrammarLexer
from yapl.MyGrammarListener import MyGrammarListener
from yapl.MyGrammarParser import MyGrammarParser
from SymbolTable import st
from Errors import ett
from globalVariables import *
from cuadrupla import *
from Object_code import *

def UI(code):
    #print(Constants.tokens)
    #file = open("./if_estatement.yapl")
    #code = ""
    #for x in file:
    #    code += x
    #print(code)
    input_stream = InputStream(code)
    lexer = MyGrammarLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = MyGrammarParser(stream)
    parser.removeErrorListeners()
    parser.addErrorListener(MyGrammarErrorListener.instance)
    tree = parser.program()
    walker = ParseTreeWalker()
    walker.walk(MyGrammarListener(), tree)
    # print tableList
    print(st)
    if (st.get_children() != []):
        st.print_children()
    #print quadruples
    print("cuadruplas: ")
    for i in cuadrupla.basic_blocks:
        i.printQuadruples()
    # for table in st.children:
    #     print(table)
    # if ett.getError() == "":
    #     print("No errors found")
    print(" -------------- object code -------------")
    return Object_code.al.write()


if __name__ == '__main__':

    # tema
    pg.theme("DarkPurple4")

    # pg.theme_previewer()
    # layout
    file_list = [
        [
            pg.Text("Folder:"),
            pg.In(size=(30, 1), enable_events=True, key="-FOLDER-"),
            pg.FolderBrowse(),
        ],
        [
            pg.Listbox(
                values=[],
                enable_events=True,
                size=(50, 20),
                key="-FILE_LIST-"
            )
        ],
        [
            pg.Button("Compile")
        ]
    ]
    file_viewer_column = [
        [pg.Text("Choose a file", size=(50, 1))],
        [pg.Text("File name: ", size=(70, 3), key="-TOUT-")],
        [pg.Multiline(size=(70, 20), key="-TEXT-")],
        [pg.Text("Compilation results:")],
        [pg.Multiline(size=(70, 10), key="-COMPILED-")]
    ]

    layout = [
        [
            pg.Column(file_list),
            pg.VSeparator(),
            pg.Column(file_viewer_column)
        ]
    ]
    # window
    window = pg.Window("YAPL Compiler", layout)

    # event loop
    folder_location = ""
    selected_file = ""
    while True:
        event, values = window.read()
        if event == pg.WIN_CLOSED:
            break
        elif event == "-FOLDER-":
            folder_location = values["-FOLDER-"]
            try:
                files = os.listdir(folder_location)
            except:
                files = []
            file_names = [
                file for file in files
                if os.path.isfile(os.path.join(folder_location, file))
                   and file.lower().endswith(".yapl")
            ]
            window["-FILE_LIST-"].update(file_names)
        elif event == "-FILE_LIST-" and len(values["-FILE_LIST-"]) > 0:
            selected_file = values["-FILE_LIST-"][0]
            with open(os.path.join(folder_location, selected_file)) as file:
                contents = file.read()
                window["-TOUT-"].update(os.path.join(folder_location, selected_file))
                window["-TEXT-"].update(contents)
        if event == "Compile":
            with open(os.path.join(folder_location, selected_file)) as file:
                code = ""
                for x in file:
                    code += x
                window["-COMPILED-"].update(UI(code))
    # close window
    window.close()

