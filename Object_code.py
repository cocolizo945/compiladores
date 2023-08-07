import globalVariables


class object_code_writer:
    def __init__(self):
        self.archivo= open("inter_code.txt", "r+")
        self.temp = 0
        self.there_is_string = False
    def write_body(self):
        lines = self.archivo.readlines()
        for line in lines:
            temp = self.rewrite_body(line)
            globalVariables.body += temp

    def rewrite_body(self, line):
        chunk = line.split()
        is_int = False

        #rvisar si algunparametro es un entero
        try:
            if len(chunk) >= 4:
                int(chunk[3])
                is_int = True
        except ValueError:
            pass
        if chunk[0] == "+":
            if is_int:
                return "    addi " + chunk[1] + ", " + chunk[2] + ", " + chunk[3] + "\n"

            else:
                return "    add " + chunk[1] + ", " + chunk[2] + ", " + chunk[3] + "\n"

        elif chunk[0] == "-":
            return "    sub " + chunk[1] + ", " + chunk[2] + ", " + chunk[3] + "\n"

        elif chunk[0] == "*":
            return "    mul " + chunk[1] + ", " + chunk[2] + ", " + chunk[3] + "\n"

        elif chunk[0] == "/":
            return "    div " + chunk[2] + ", " + chunk[3] + "\n"

        elif chunk[0] == "=i":
            if len(chunk) == 3:
                return "    li " + chunk[1] + ", " + chunk[2] + "\n"
            else:
                return "    li " + chunk[1] + ", " + str(0) + "\n"

        elif chunk[0] == "==":
            return "    beq " + chunk[1] + ", " + chunk[2] + ", " + chunk[3] + "\n"

        elif chunk[0] == "ri":
            if chunk[1] == "+":
                return "    add $a0"+ ", " + chunk[2] + ", " + chunk[3] + "\n"+ "    li $v0, 1\n" + "    syscall\n"
            elif chunk[1] == "-":
                return "    sub $a0"+ ", " + chunk[2] + ", " + chunk[3] + "\n"+ "    li $v0, 1\n" + "    syscall\n"
            elif chunk[1] == "*":
                return "    mul $a0"+ ", " + chunk[2] + ", " + chunk[3] + "\n"+ "    li $v0, 1\n" + "    syscall\n"
            elif len(chunk) == 2:
                return "    li $a0, " + chunk[1] + "\n" + "    li $v0, 1\n" + "    syscall\n"


        elif chunk[0] == "=b":
            if len(chunk) == 2:
                return "    li " + chunk[1] + ", " + str(0) + "\n"
            if chunk[2] == "true":
                return "    li " + chunk[1] + ", 1\n"
            else:
                return "    li " + chunk[1] + ", 0\n"
        elif chunk[0] == "=o":
            if self.there_is_string == False:
                globalVariables.header += ".data\n"
            if len(chunk) == 3:
                globalVariables.header += '    ' + chunk[1] + ': .asciiz ' + '"'+chunk[2] +'"'+ "\n"
                self.there_is_string = True
                return ""
            if len(chunk) == 2:
                globalVariables.header += '    ' + chunk[1] + ': .asciiz ' + '"Empty "' + "\n"
                self.there_is_string = True
                return ""
        elif chunk[0] == "=s":
            print("calling from string chunk")
            temp = ""
            for i in range(2, len(chunk)):
                temp += chunk[i]+" "
            if self.there_is_string == False:
                globalVariables.header += ".data\n"
            if len(chunk) >= 3:
                globalVariables.header += '    ' + chunk[1] + ': .asciiz ' + ''+temp +''+ "\n"
                self.there_is_string = True
                return ""
            if len(chunk) == 2:
                globalVariables.header += '    ' + chunk[1] + ': .asciiz ' + '"Empty "' + "\n"
                self.there_is_string = True
                return ""


            self.there_is_string = True
        return line
    def write(self):
        self.write_body()
        output = globalVariables.header + "\n" +globalVariables.pre_body+"\n"+ globalVariables.body + "\n" + globalVariables.footer
        globalVariables.console_output = output
        print(output)
        return output



al = object_code_writer()



