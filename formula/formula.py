
import os
from analyzer.symbol import (ArrayType, BaseType, ProcedureSymbol, RecordType,
                             Symbol, SymbolTable, TypeSymbol, VarSymbol)
from grammar.GrammarTree import GrammarNode, GrammarTree
from grammar.LL1 import dfs
from util.logger import log

class arg(object):
    def __init__(self, form: str, value: str = None, datalevel: int = None, dataoff: int = None, access: str = None, name: str = None) -> None:
        self.form = form
        self.value = value
        self.label = name
        self.name = name
        self.datalevel = datalevel
        self.dataoff = dataoff
        self.access = access

    def message(self):
        if(self.form == "ValueForm"):
            return "ValueForm" + ' ' + str(self.value)
        elif(self.form == "TempForm"):
            return "TempForm" + ' ' + str(self.name)
        elif(self.form == "LabelForm"):
            return "LabelForm" + ' ' + str(self.name)
        elif(self.form == "AddrForm"):
            return "AddrForm" + ' ' + str(self.name) + ' ' + str(self.datalevel) + ' ' + str(self.dataoff) + ' ' + str(self.access)
        else:
            return "Error"


class formula(object):

    def __init__(self, codekind: str, index: int, last, next, arg1: arg = None, arg2: arg = None, arg3: arg = None) -> None:
        self.codekind = codekind
        self.arg1: arg = arg1
        self.arg2: arg = arg2
        self.arg3: arg = arg3
        self.last: formula = last
        self.next: formula = next
        self.index = index

    def getLast(self):
        return self.last

    def getNext(self):
        return self.next
    
    def sample(self):
        if (self.arg3 != None):
            return "(%s, %s, %s, %s )" % (self.codekind, self.arg1.name, self.arg2.name, self.arg3.name)
        elif(self.arg2 != None):
            return "(%s, %s, %s, _ ) " % (self.codekind, self.arg1.name, self.arg2.name)
        elif(self.arg1 != None):
            return "(%s, %s, _ , _ ) " % (self.codekind, self.arg1.name)
        else:
            return "(%s, _ , _ , _ )" % (self.codekind)

    def __str__(self) -> str:
        if (self.arg3 != None):
            arg1Message = self.arg1.message()
            arg2Message = self.arg2.message()
            arg3Message = self.arg3.message()
            return "(%s, %s, %s, %s ) || %s || %s || %s || " % (self.codekind, self.arg1.name, self.arg2.name, self.arg3.name, arg1Message, arg2Message, arg3Message)
        elif(self.arg2 != None):
            arg1Message = self.arg1.message()
            arg2Message = self.arg2.message()
            return "(%s, %s, %s, _ ) || %s || %s || " % (self.codekind, self.arg1.name, self.arg2.name, arg1Message, arg2Message)
        elif(self.arg1 != None):
            arg1Message = self.arg1.message()
            return "(%s, %s, _ , _ ) || %s || " % (self.codekind, self.arg1.name, arg1Message)
        else:
            return "(%s, _ , _ , _ )" % (self.codekind)

    def __repr__(self) -> str:
        if (self.arg3 != None):
            arg1Message = self.arg1.message()
            arg2Message = self.arg2.message()
            arg3Message = self.arg3.message()
            return "(%s, %s, %s, %s || %s || %s || %s )" % (self.codekind, self.arg1.name, self.arg2.name, self.arg3.name, arg1Message, arg2Message, arg3Message)
        elif(self.arg2 != None):
            arg1Message = self.arg1.message()
            arg2Message = self.arg2.message()
            return "(%s, %s, %s, _ || %s || %s )" % (self.codekind, self.arg1.name, self.arg2.name, arg1Message, arg2Message)
        elif(self.arg1 != None):
            arg1Message = self.arg1.message()
            return "(%s, %s, _ , _ || %s )" % (self.codekind, self.arg1.name, arg1Message)
        else:
            return "(%s, _ , _ , _ )" % (self.codekind)


class formulaList(object):

    def __init__(self) -> None:
        self.firstCode: formula = None
        self.lastCode: formula = None
        self.current: formula = None
        self.num: int = 0
        self.label_table: labelTable = labelTable()

    def isEmpty(self):
        return self.num == 0

    def addFormula(self, nextFormula: formula):
        if(self.isEmpty()):
            self.firstCode = nextFormula
            self.lastCode = nextFormula
            self.current = nextFormula
        else:
            nextFormula.last = self.current
            self.current.next = nextFormula
            self.lastCode = nextFormula
            self.current = nextFormula
        self.num += 1

    def goNext(self):
        self.current = self.current.getNext()

    def goLast(self):
        self.current = self.current.getLast()

    def show(self, output):
        f = open(output, 'w')
        self.current = self.firstCode
        while(self.current != None):
            print(self.current, file=f)
            self.goNext()
        print(str(self.label_table.labeldict), file=f)
        f.close()

    def show2(self):
        f = open('formulaout.txt', 'w')
        self.current = self.firstCode
        while(self.current != None):
            print(self.current.sample(), file=f)
            self.goNext()
        print(str(self.label_table.labeldict), file=f)
        f.close()
            

class labelTable(object):
    def __init__(self) -> None:
        self.labeldict: dict = {}
        self.labelLen: int = 0

    def addLabel(self, labelName: str, labelValue: int):
        self.labeldict[labelName] = labelValue

    def findLabel(self, labelName: str):
        if(labelName in self.labeldict):
            pass
        else:
            self.labeldict[labelName] = -1
    
    def show(self):
        f = open('formulaout.txt', 'w')
        print(str(self.labeldict), file=f)

class proStack(object):
    def __init__(self) -> None:
        self.proList: list = []
        self.proLen: int = -1
    
    def pop(self):
        if(self.proLen >= 0):
            self.proLen -= 1
            self.proList.pop()
    
    def top(self):
        if(self.proLen >= 0):
            return self.proList[self.proLen]
        
    def push(self, proSem):
        self.proLen += 1
        self.proList.append(proSem)

    def isEmpty(self):
        return self.proLen < 0


class generater(object):

    def __init__(self, tree: GrammarTree) -> None:
        self.head: formula = None
        self.tree: GrammarTree = tree
        self.current: GrammarNode = tree.getRoot()
        self.index = 0
        self.temp_index = 0
        self.label_index = 0
        self.formula_list: formulaList = formulaList()
        self.label_table: labelTable = labelTable()
        self.pro_stack: proStack = proStack()

    def step(self):
        if self.current.getChildNum() == 0:
            while self.current.getFather() != None and self.current.getSibling() == None:
                self.current = self.current.getFather()
            if self.current.getFather() != None:
                self.current = self.current.getSibling()
        else:
            self.current = self.current.getChild(0)

    def stepInto(self, tokenType):
        while not self.current.getNodeKind() == tokenType:
            self.step()

    def changeop(self, op: str):
        if(op == '-'):
            return "SUB"
        elif(op == '+'):
            return "ADD"
        elif(op == '*'):
            return "MULT"
        elif(op == '/'):
            return "DIV"
        elif(op == '<'):
            return "LTC"
        elif(op == '='):
            return "EQC"
        elif(op == 'AADD'):
            return "AADD"
        else:
            return "ERROR"

    def genCode(self, op: str, leftArg: arg, rightArg: arg):
        self.index += 1
        self.temp_index += 1
        op = self.changeop(op)
        tempName = 't' + str(self.temp_index)
        tempArg: arg = arg("TempForm", None, -1, self.temp_index, "dir", tempName)
        formu = formula(op, self.index, None, None, leftArg, rightArg, tempArg)
        self.formula_list.addFormula(formu)
        return tempArg

    def genBoolCode(self, op: str, leftArg: arg, rightArg: arg):
        self.index += 1
        self.temp_index += 1
        op = self.changeop(op)
        tempName = 't' + str(self.temp_index)
        tempArg = arg("TempForm", None, -1, self.temp_index, "dir", tempName)
        formu = formula(op, self.index, None, None, leftArg, rightArg, tempArg)
        self.formula_list.addFormula(formu)
        return tempArg

    def genAssign(self, varArg: arg, expArg: arg):
        self.index += 1
        formu = formula("ASSIGN", self.index, None, None, varArg, expArg, None)
        self.formula_list.addFormula(formu)

    def genJumpCon(self, op: str, boolArg: arg, labelArg: arg):
        self.index += 1
        formu = formula(op, self.index, None, None, boolArg, labelArg, None)
        self.formula_list.addFormula(formu)

    def genJump(self, op: str, labelArg: arg):
        self.index += 1
        formu = formula(op, self.index, None, None, labelArg, None, None)
        self.formula_list.addFormula(formu)

    def genLabel(self, op: str, labelArg: arg):
        self.index += 1
        self.label_table.addLabel(labelArg.name, self.index)
        formu = formula(op, self.index, None, None, labelArg, None, None)
        self.formula_list.addFormula(formu)

    def genRead(self, op: str, varArg: arg):
        self.index += 1
        formu = formula(op, self.index, None, None, varArg, None, None)
        self.formula_list.addFormula(formu)

    def genWrite(self, op: str, expArg: arg):
        self.index += 1
        formu = formula(op, self.index, None, None, expArg, None, None)
        self.formula_list.addFormula(formu)

    def genReturn(self, op: str):
        self.index += 1
        formu = formula(op, self.index, None, None, None, None, None)
        self.formula_list.addFormula(formu)
    
    def genProDec(self):
        self.index += 1
        proSem = self.pro_stack.top()
        self.pro_stack.pop()
        self.label_table.addLabel(proSem.name, self.index)
        argOne = arg("LabelForm", None, None, None, "indir", proSem.name)
        #proSize = proSem.size
        proSize = "Sizeof" + ' ' +proSem.name
        argTwo = arg("ValueForm", str(proSize), None, None, None, str(proSize))
        proLevel = proSem.level
        argThree = arg("ValueForm", str(proLevel), None, None, None, str(proLevel))
        op = ""
        if(self.pro_stack.isEmpty()):
            op = "MENTRY"
        else:
            op = "PENTRY"
        formu = formula(op, self.index, None, None, argOne, argTwo, argThree)
        self.formula_list.addFormula(formu)

    def genEndPro(self):
        self.index += 1
        formu = formula("ENDPROC", self.index, None, None, None, None, None)
        self.formula_list.addFormula(formu)

    def genAct(self, op: str, expArg: arg, off: int, size: int):
        self.index += 1
        offArg = arg("ValueForm", str(off), None, None, None, str(off))
        sizeArg = arg("ValueForm", str(size), None, None, None, str(size))
        formu = formula(op, self.index, None, None, expArg, offArg, sizeArg)
        self.formula_list.addFormula(formu)

    def genProCall(self, paramArgList: list, proSymbol):
        num = 0
        for paramArg in paramArgList:
            paramSem = proSymbol.get_param(num)
            op = ""
            if(paramSem.access == "indir"):
                op = "VARACT"
            else:
                op = "VALACT"
            self.genAct(op, paramArg, paramSem.off, paramSem.typePtr.size)
            num += 1
        self.index += 1
        self.label_table.findLabel(proSymbol.name)
        labelArg = arg("LabelForm", None, None, None, "indir", proSymbol.name)
        formu = formula("CALL", self.index, None, None, labelArg, None, None)
        self.formula_list.addFormula(formu)

    def genArray(self, arraySem):
        leftArg = self.expresion()
        arrayLow = arraySem.typePtr.low
        arrayEleSize = arraySem.typePtr.element.size
        rightArg = arg("ValueForm", str(arrayLow), None, None, None, str(arrayLow))
        leftArg = self.genCode("-", leftArg, rightArg)
        rightArg = arg("ValueForm", str(arrayEleSize),
                       None, None, None, str(arrayEleSize))
        rightArg = self.genCode("*", leftArg, rightArg)
        varArg = arg("AddrForm", None, arraySem.level,
                     arraySem.off, arraySem.access, arraySem.name)
        leftArg = self.genCode("AADD", varArg, rightArg)
        return leftArg

    def genFieldArray(self, recordSem, fieldSem, fieldName: str):
        leftArg = self.expresion()
        arrayLow = fieldSem.typePtr.low
        arrayEleSize = fieldSem.typePtr.element.size
        rightArg = arg("ValueForm", str(arrayLow), None, None, None, str(arrayLow))
        leftArg = self.genCode("-", leftArg, rightArg)
        rightArg = arg("ValueForm", str(arrayEleSize),
                       None, None, None, str(arrayEleSize))
        rightArg = self.genCode("*", leftArg, rightArg)
        varArg = arg("AddrForm", None, recordSem.level,
                     recordSem.level + fieldSem.off, fieldSem.access, fieldName)
        leftArg = self.genCode("AADD", varArg, rightArg)
        return leftArg

    def genField(self, recordSem):
        self.stepInto("FieldVar")
        self.stepInto("ID")
        fieldName = self.current.getNodeVal()
        fieldSem = recordSem.typePtr.get_field(fieldName)
        fieldName = recordSem.name + '.' + fieldName
        self.stepInto("FieldVarMore")
        self.step()
        if self.current.getNodeKind() == "ε":
            leftArg = arg("AddrForm", None, recordSem.level,
                          recordSem.off + fieldSem.off, recordSem.access, fieldName)
            return leftArg
        elif self.current.getNodeKind() == "[":
            leftArg = self.genFieldArray(recordSem, fieldSem, fieldName)
            return leftArg

    def scan(self):
        self.current = self.current.getChild(0)
        self.programHead()
        self.declarePart()
        self.programBody()
        self.formula_list.label_table = self.label_table
        return self.formula_list

    def programHead(self):
        self.stepInto("ProgramName")
        self.stepInto("ID")
        proSem = self.current.getNodeSemantic()
        self.pro_stack.push(proSem)

    def declarePart(self):
        self.stepInto("DeclarePart")
        self.procDec()

    def programBody(self):
        self.stepInto("BEGIN")
        self.genProDec()
        self.stmList()
        self.stepInto("END")
        self.genEndPro()

    def procDec(self):
        self.stepInto("ProcDec")
        self.step()
        if self.current.getNodeKind() == "ε":
            return
        else:
            while True:
                if self.current.getNodeKind() == "ProcDecMore" and self.current.getChild(0).getNodeKind() == "ε":
                    break
                else:
                    self.stepInto("ProcName")
                    self.stepInto("ID")
                    proSem = self.current.getNodeSemantic()
                    self.pro_stack.push(proSem)
                    self.stepInto("ParamList")
                    self.step()
                    self.stepInto("ProcDecPart")
                    self.declarePart()
                    self.stepInto("ProcBody")
                    self.programBody()
                    self.stepInto("ProcDecMore")

    def stmList(self):
        self.stepInto("Stm")
        while True:
            if self.current.getNodeKind() == "StmMore" and self.current.getChild(0).getNodeKind() == "ε":
                break
            else:
                self.stepInto("Stm")
                curStm = self.current.getChild(0).getNodeKind()
                if curStm == "ConditionalStm":
                    self.conditionalStm()
                elif curStm == "LoopStm":
                    self.loopStm()
                elif curStm == "InputStm":
                    self.inputStm()
                elif curStm == "OutputStm":
                    self.outputStm()
                elif curStm == "ReturnStm":
                    self.returnStm()
                elif curStm == "ID":
                    self.stepInto("ID")
                    varSymbol = self.current.getNodeSemantic()
                    proSymbol = varSymbol
                    self.stepInto("AssCall")
                    self.step()
                    decision = self.current.getNodeKind()

                    if decision == "AssignmentRest":
                        self.stepInto("VariMore")
                        self.step()
                        leftArg = None
                        choice = self.current.getNodeKind()
                        if choice == "ε":
                            leftArg: arg = arg("AddrForm", None, varSymbol.level,
                                               varSymbol.off, varSymbol.access, varSymbol.name)
                        elif choice == "[":
                            leftArg = self.genArray(varSymbol)
                        elif choice == ".":
                            leftArg = self.genField(varSymbol)

                        self.stepInto(":=")
                        rightArg = self.expresion()
                        self.genAssign(rightArg, leftArg)

                    elif decision == "CallStmRest":
                        self.stepInto("ActParamList")
                        paramArgList = []
                        while True:
                            if self.current.getNodeKind() == "ActParamMore" and self.current.getChild(0).getNodeKind() == "ε":
                                break
                            elif self.current.getNodeKind() == "ActParamList" and self.current.getChild(0).getNodeKind() == "ε":
                                break
                            else:
                                expArg = self.expresion()
                                paramArgList.append(expArg)
                                self.stepInto("ActParamMore")
                        leftArg = self.genProCall(paramArgList, proSymbol)

                self.stepInto("StmMore")

        pass

    def conditionalStm(self):
        self.stepInto("IF")
        boolArg = self.boolExp()
        self.stepInto("THEN")
        self.label_index += 1
        elselabel = "L" + str(self.label_index)
        elseArg = arg("LabelForm", None, None, None, "indir", elselabel)
        self.genJumpCon("JUMP0", boolArg, elseArg)
        self.stmList()
        self.stepInto("ELSE")
        self.label_index += 1
        outlabel = "L" + str(self.label_index)
        outArg = arg("LabelForm", None, None, None, "indir", outlabel)
        self.genJump("JUMP", outArg)
        self.genLabel("LABEL", elseArg)
        self.stmList()
        self.stepInto("FI")
        self.genLabel("LABEL", outArg)

    def loopStm(self):
        self.stepInto("WHILE")
        self.label_index += 1
        startlabel = "L" + str(self.label_index)
        startArg = arg("LabelForm", None, None, None, "indir", startlabel)
        self.genLabel("LABEL", startArg)
        boolArg = self.boolExp()
        self.stepInto("DO")
        self.label_index += 1
        outlabel = "L" + str(self.label_index)
        outArg = arg("LabelForm", None, None, None, "indir", outlabel)
        self.genJumpCon("JUMP0", boolArg, outArg)
        self.stmList()
        self.stepInto("ENDWH")
        self.genJump("JUMP", startArg)
        self.genLabel("LABEL", outArg)
        pass

    def inputStm(self):
        self.stepInto("InputStm")
        self.stepInto("READ")
        self.stepInto("Invar")
        self.stepInto("ID")
        varSem = self.current.getNodeSemantic()
        varArg = arg("AddrForm", None, varSem.level,
                     varSem.off, varSem.access, varSem.name)
        self.genRead("READC", varArg)

    def outputStm(self):
        self.stepInto("OutputStm")
        self.stepInto("WRITE")
        leftArg = self.expresion()
        self.genWrite("WRITEC", leftArg)

    def returnStm(self):
        self.stepInto("ReturnStm")
        self.stepInto("RETURN")
        self.expresion()
        self.genReturn("RETURNC")

    def boolExp(self):
        self.stepInto("RelExp")
        leftArg = self.expresion()
        self.stepInto("CmpOp")
        self.step()
        op = self.current.getNodeVal()
        rightArg = self.expresion()
        tempArg = self.genBoolCode(op, leftArg, rightArg)
        return tempArg

    def expresion(self):
        self.stepInto("Exp")
        leftArg = self.term()
        op = ''
        self.stepInto("OtherTerm")
        while True:
            if self.current.getNodeKind() == "OtherTerm" and self.current.getChild(0).getNodeKind() == "ε":
                break
            else:
                self.stepInto("AddOp")
                self.step()
                op = self.current.getNodeVal()
                self.stepInto("Exp")
                rightArg = self.expresion()
                leftArg = self.genCode(op, leftArg, rightArg)
                self.stepInto("OtherTerm")
        return leftArg

    def term(self):
        self.stepInto("Term")
        leftArg = self.factor()
        op = ''
        self.stepInto("OtherFactor")
        while True:
            if self.current.getNodeKind() == "OtherFactor" and self.current.getChild(0).getNodeKind() == "ε":
                break
            else:
                self.stepInto("MultOp")
                self.step()
                op = self.current.getNodeVal()
                self.stepInto("Term")
                rightArg = self.term()
                leftArg = self.genCode(op, leftArg, rightArg)
                self.stepInto("OtherFactor")
        return leftArg

    def factor(self):
        self.stepInto("Factor")
        self.step()
        choice = self.current.getNodeKind()
        if choice == "(":
            return self.expresion()
        elif choice == "INTC":
            value = self.current.getNodeVal()
            leftArg: arg = arg("ValueForm", value, None, None, None, value)
            return leftArg
        elif choice == "Variable":
            return self.variable()

    def variable(self):
        self.stepInto("Variable")
        self.stepInto("ID")
        varSymbol = self.current.getNodeSemantic()
        self.stepInto("VariMore")
        self.step()
        choice = self.current.getNodeKind()
        if choice == "ε":
            leftArg: arg = arg("AddrForm", None, varSymbol.level,
                               varSymbol.off, varSymbol.access, varSymbol.name)
            return leftArg
        elif choice == "[":
            leftArg = self.genArray(varSymbol)
            return leftArg
        elif choice == ".":
            leftArg = self.genField(varSymbol)
            return leftArg
