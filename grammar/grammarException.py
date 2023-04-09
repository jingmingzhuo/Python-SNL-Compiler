class TypeError(Exception):
    def __init__(self,lineNo:int,should:str,get:str) -> None:
        self.lineNo=lineNo
        self.should=should
        self.get=get
    def __str__(self) -> str:
        return "TypeError in line %d : must be %s here , not %s" % (self.lineNo,self.should,self.get)

class RedundancyError(Exception):
    def __init__(self,lineNo:int) -> None:
        self.lineNo=lineNo
    def __str__(self) -> str:
        return "RedundancyError in line %d : superfluous code after end_program" % self.lineNo