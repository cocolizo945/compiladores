class Errors():
    def __init__(self):
        self.message = ""

    def addError(self, message):
        self.message += message + "\n"

    def getError(self):
        return self.message


ett = Errors()
# ett.addError("Error 1")
# ett.addError("Error 2")
# ett.addError("Error 3")

# print(ett.getError())
