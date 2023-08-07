#List of all the Table declared in the project
tableList = []
i = 0
lTable = None
memPos = 0
is_if = False
current_flow = None

header = """
.globl variables
"""
pre_body = ".text"
body = ""

footer = """
end:
li $v0, 10
syscall
"""

console_output = ""