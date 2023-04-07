import enum
import os

from analyzer.symbol import (ArrayType, BaseType, ProcedureSymbol, RecordType,
                             Symbol, SymbolTable, TypeSymbol, VarSymbol)
from grammar.GrammarTree import GrammarNode, GrammarTree
from grammar.LL1 import dfs
from util.logger import log

class SemanticError():
  DuplicateDefine = '%s is duplicate defined'
  UndefinedVar = '%s is undefined variable'
  UndefinedType = '%s is undefined type'
  UndefinedField = '%s is undefined field'
  InvalidAssignLeft = 'invalid assignment %s is not variable'
  InvalidAssignRight = 'invalid assignment %s is not %s type'
  ParamTypeError = 'procedure param type do not match expect %s got %s'
  ParamNumError = 'procedure param number do not match expect %d params got %d params'
  ProcedureCallError  = 'can not be called'
  BoolError = 'condition must be an boolean value'
  TypeMatchError = 'incompatible type expect %s got %s'
  ArrayDefineError = 'invalid array define'
  KindMatchError = 'unexpected type expect %s got %s'

class State():
  START = 'start'
  TYPE_DEC = 'type-dec'
  VAR_DEC = 'var-dec'
  PROC_DEC = 'proc-dec'
  DONE = 'done'

class Analyzer(object):
  root: GrammarTree 
  ptr: GrammarTree

  def __init__(self, tokens, root: GrammarTree):
    self.state = State.START

    self.index = 0
    self.tokens = tokens
    self.root = root
    
    root.goRoot()
    self.ptr = root.nextNode()

    self.tbSym = SymbolTable()
    self.scope = [self.tbSym]
    self.exp = None
    self.level = None

    self.varType = None
    self.varKind = None
    self.varValue = None

    self.shouldPrintErr = None
    self.isErr = False 
    self.msgErr = None
    self.lineErr = -1

    self.levelCurrent = 0
    self.offsetCurrent = [0]

    cnt = dfs(root.now, 0)
    log(f'[[treeNodeCount]] -- {cnt}')

  def __len__(self):
    return len(self.tbSym)
  
  def __repr__(self) -> str:
    return str(self.tbSym)

  def step(self):
    next(self.ptr)
    if self.root.now.symbol == 'VT': 
      log(f'[[now-is-VT]] --- {self.root.now.getNodeVal()}')
      self.index += 1
    log(f'[[to]] -- {self.root.now.getNodeKind()}')
    pass

  def step_into(self, token_type):
    while not self.root.isNodeKind(token_type):
      self.step()
  
  def pre_token(self):
    return self.tokens[self.index - 2][1] if self.index > 2 else None
  
  def next_token(self):
    return self.tokens[self.index][1] if self.index < len(self.tokens) else None
  
  def current_line(self):
    return self.tokens[self.index - 1][-1] if self.index > 1 else None
    
  def current_token(self):
    return self.tokens[self.index - 1][1] if self.index - 1 > 0 else None
  
  def print_error(self, var:Symbol=None):
    print(self.tokens[self.index - 1])
    if self.shouldPrintErr or self.tokens[self.index - 1][-1] != self.lineErr:
      if var is not None:
        print('Error in line %d: %s' % (self.tokens[self.index - 1][-1], self.msgErr))
        os._exit(1)
      else:
        print('Error in line %d: %s' % (self.tokens[self.index - 1][-1], self.msgErr))
        os._exit(1)

  def assign_type_check(self, type_left, type_right):
    log(f'[[left-type]] --- {type(str(type_left))}')
    if str(type_left) == 'INTEGER':
      log(f'[[left-INTEGER]]')
      return str(type_right) == 'INTEGER' or str(type_right) == 'INTC'
    else:
      log(f'[[right-CHAR]]')
      return type_left == type_right
  
  # 开始分析
  def analyze(self):
    next(self.ptr)
    log(f'[[program_start]]')
    self.program_start()
    log(f'[[declare]]')
    self.declare()
    log(f'[[program_pending]]')
    self.program_pending()
    log(f'[[the-end]]')

  # 项目开始
  def program_start(self):
    self.step_into('ProgramName')
    self.step_into('ID')
    idName = self.root.now.getNodeVal()
    sym = ProcedureSymbol(
      name=idName, 
      type=BaseType(size=0, kind='procType'), 
      level=self.levelCurrent, 
      off=self.offsetCurrent[-1]
    )
    self.root.now.semantic = sym

  # 定义基本类型
  def declare(self):
    self.step_into('DeclarePart') # Declare
    self.type_dec()
    log(f'[[declare-type-finish]]')
    self.var_dec()
    log(f'[[declare-var-finish]]')
    self.proc_dec()
    log(f'[[declare-proc-finish]]')

  # 项目进行
  def program_pending(self):
    self.step_into('BEGIN')
    log(f'[[xxx]]')
    self.stm_list()
    log(f'[[program-pending]] --- almost end')
    self.step_into('END')

  # 定义类型
  def type_dec(self):
    self.step_into('TypeDec')
    self.step()

    if self.root.now.isNodeKind('ε'): return 

    self.step_into('TypeDecList')
    while True:
      if (
        self.root.now.isNodeKind('TypeDecMore') and
        self.root.now.getChild(0).isNodeKind('ε')
      ): break

      self.step_into('TypeId')
      self.step_into('ID')
      
      name = self.root.now.getNodeVal()
      typeName = self.type_name()
      sym = TypeSymbol(name=name, type=typeName)
      self.root.now.semantic = sym

      log(f'[[sym-type-name]] -- {name}')
      if typeName is not None:
        sym.typePtr = typeName
        if sym.name not in self.tbSym:
          self.tbSym.add(sym)
        else:
          self.isErr = True
          self.msgErr = SemanticError.DuplicateDefine % (sym.name)
          self.print_error()
      self.step_into('TypeDecMore')
  
  # 定义变量
  def var_dec(self):
    self.step_into('VarDec')
    self.step()
    if self.root.now.isNodeKind('ε'): return 
    
    self.step_into('VarDecList')
    while True:
      if (
        self.root.now.isNodeKind('VarDecMore') and 
        self.root.now.getChild(0).isNodeKind('ε')
      ): 
        log('[[var-dec]] --- break')
        break

      typeName = self.type_name()

      self.step_into('VarIdList')
      while True:
        if (
          self.root.now.isNodeKind('VarIdMore') and
          self.root.now.getChild(0).isNodeKind('ε')
        ):
          log('[[var-dec]] --- break')
          break

        sym: VarSymbol = VarSymbol(type=BaseType(kind=typeName, size=typeName.size))
        self.step_into('ID')
        sym.name = self.root.now.getNodeVal()
        sym.access = 'dir'
        sym.level = self.levelCurrent
        sym.off = self.offsetCurrent[-1]
        self.offsetCurrent[-1] += sym.typePtr.size
        log(f'[[sym-var-name]] -- {sym.name}')

        if sym.name in self.tbSym:
          self.isErr = True
          self.msgErr = SemanticError.DuplicateDefine % sym.name
          self.print_error()
        else:
          self.tbSym.add(sym)
          self.step_into('VarIdMore')

      self.step_into('VarDecMore')

  # 定义过程 / 函数
  def proc_dec(self):
    tbSymCur: SymbolTable = self.tbSym
    self.step_into('ProcDec')
    self.step()

    if self.root.now.isNodeKind('ε'): return 

    while True:
      if (
        self.root.now.isNodeKind('ProcDecMore') and 
        (
          self.root.isEmpty() or 
          self.root.now.getChild(0).isNodeKind('ε')
        )
      ): break

      self.step_into('ProcName')
      self.step()

      # 函数名存放在 ProcName 下一步的节点上（第一个子节点）
      procName = self.root.now.getNodeVal()
      # TODO
      proc: ProcedureSymbol = ProcedureSymbol(
        name=procName, 
        param=SymbolTable(),
        type=None,
        level=self.levelCurrent,
        off=self.offsetCurrent[-1],
      )
      self.levelCurrent += 1
      self.offsetCurrent.append(0)

      symTable = SymbolTable()
      symTable.add(proc)

      procError = False
      log(f'[[proc-name-in-symbol-table]] --- {procName in self.tbSym}')
      if procName in self.tbSym:
        procError = True
        self.isErr = True
        self.msgErr = SemanticError.DuplicateDefine % procName
        self.print_error()

      else:
        self.tbSym.add(proc)
        self.scope.append(symTable)
        self.tbSym = self.scope[-1]
      self.step_into('ParamList')
      self.step()
      
      if not self.root.isNodeKind('ε'):
        while True:
          if (
            self.root.isNodeKind('ParamMore') and 
            self.root.now.getChild(0).isNodeKind('ε')
          ): break

          self.step_into('Param')
          typeName = self.type_name()
          typeError = False
          if typeName is None: typeError = True

          self.step_into('FormList')
          while True:
            if (
              self.root.isNodeKind('FidMore') and 
              self.root.now.getChild(0).isNodeKind('ε')
            ): break

            self.step_into('ID')
            param = VarSymbol(
              name=self.root.now.getNodeVal(), 
              type=typeName, 
              access='dir', 
              level=self.levelCurrent, 
              off=self.offsetCurrent[-1]
            )
            proc.param.add(param)
            self.root.now.semantic = param
            self.offsetCurrent[-1] += param.typePtr.size

            if not procError and not typeError:
              if param.name not in self.tbSym:
                self.tbSym.add(param)
              else:
                self.isErr = True
                self.msgErr = SemanticError.DuplicateDefine % param.name
                self.print_error()
            self.step_into('FidMore')
          self.step_into('ParamMore')

      self.step_into('ProcDecPart')
      self.declare()
      self.step_into('ProcBody')
      self.program_pending()
      self.tbSym = tbSymCur
      self.step_into('ProcDecMore')
      
      self.levelCurrent -= 1
      self.offsetCurrent.pop()

  # 不同语法进行对应的分析
  def stm_list(self):
    self.step_into('Stm')
    while True:
      if (
        self.root.isNodeKind('StmMore') and 
        self.root.now.getChild(0).isNodeKind('ε')
      ): break
      self.step_into('Stm')
      curStm = self.root.now.getChild(0).getNodeKind()
      log(f'[[check-stm]] --- {curStm}')

      if curStm == 'ConditionalStm':
        self.conditional_stm()
      elif curStm == 'LoopStm':
        self.loop_stm()
      elif curStm == 'InputStm':
        self.input_stm()
      elif curStm == 'OutputStm':
        self.output_stm()
      elif curStm == 'ReturnStm':
        self.return_stm()
      elif curStm == 'ID':
        self.step_into('ID')
        # TODO
        # self.root.now.symbol = '[[???TODO]]' Symbol()
        idNode = self.root.now
        idName = idNode.getNodeVal()

        log(f'[[ass-call]]')

        self.step_into('AssCall')
        self.step()
        decision = self.root.now.getNodeVal()
        varError = True
        var: VarSymbol = None
        for symTable in self.scope[::-1]:
          if idName in symTable:
            varError = False
            var = symTable.get(idName)
            idNode.semantic = var

        if varError:
          self.isErr = True
          # TODO
          self.msgErr = SemanticError.UndefinedVar % idName
          self.print_error()
          
        if decision == 'AssignmentRest':
          log(f'[[assign-rest]]')
          varType = None
          self.step_into('VariMore')
          self.step()
          choice = self.root.now.getNodeKind()
          if choice == 'ε':
            log(f'[[choise-eps]] --- {var.typePtr}')
            if not varError: varType = var.typePtr

          elif choice == '[':
            indType, _ = self.expression()
            if indType not in ['INTEGER', 'INTC']:
              self.error = True
              self.msgErr = SemanticError.TypeMatchError % ('INTC', indType)
              self.print_error()
            else:
              varType = var.typePtr.element.type

          elif choice == '.':
            self.step_into('FieldVar')
            self.step_into('ID')
            fieldName = self.root.now.getNodeVal()
            
            if var.typePtr.type != 'recordType':
              self.isErr = True
              self.msgErr = SemanticError.TypeMatchError % (
                'recordType',
                var.typePtr.type
              )
              self.print_error()

            if fieldName not in var.typePtr.fieldList:
              self.isErr = True
              self.msgErr = SemanticError.UndefinedField % fieldName
              self.print_error()

            field = var.typePtr.fieldList.get(fieldName)
            self.root.now.semantic = field
            
            self.step_into('FieldVarMore')
            self.step()
            if self.root.isNodeKind('ε'):
              varType = field.typePtr.type

            elif self.root.isNodeKind('['):
              indType, indVal = self.expression()
              if indType not in ['INTEGER', 'INTC']:
                self.isErr = True
                self.msgErr = SemanticError.TypeMatchError % (
                  'INTC',
                  indType
                )
                self.print_error()

              else:
                varType = field.typePtr.element.type

          self.step_into(':=')
          rightType, _ = self.expression()
          log(f'[[assign-type-check]] --- {varType} - {rightType}')
          log(f'[[]] --- {self.assign_type_check(varType, rightType)}')
          if varType and not varError:
            if not self.assign_type_check(varType, rightType):
              self.isErr = True
              self.msgErr = SemanticError.TypeMatchError % (
                varType,
                rightType
              )
              self.print_error()

        elif decision == 'CallStmRest':
          self.step_into('ActParamList')
          actParamList = []
          while True:
            if (
              self.root.isNodeKind('ActParamMore') and 
              self.root.now.getChild(0).isNodeKind('ε')
            ): break

            if (
              self.root.isNodeKind('ActParamList') and 
              self.root.now.getChild(0).isNodeKind('ε')
            ): break

            expType, _ = self.expression()
            actParamList.append(expType)
            self.step_into('ActParamMore')

          actParamLen = len(actParamList)
          paramList = SymbolTable()
          if not varError:
            if var.decKind != 'procDec':
              self.isErr = True
              self.msgErr = SemanticError.ProcedureCallError
              self.print_error()

            else:
              paramList = var.param
              paramLen = len(paramList)
              if paramLen != actParamLen:
                self.isErr = True
                self.msgErr = SemanticError.ParamNumError % (
                  paramLen,
                  actParamLen
                )
                self.print_error()

              else:
                for i in range(paramLen):
                  if paramList[i].typePtr == None: continue

                  expect = paramList[i].typePtr.type
                  got = actParamList[i]
                  if not self.assign_type_check(expect, got):
                    self.isErr = True
                    self.msgErr = SemanticError.TypeMatchError % (
                      expect,
                      got
                    )
                    self.print_error()
                    
      self.step_into('StmMore')

  # 获取类型
  def type_name(self):
    log(f'[[type-name()]]')
    self.step_into('TypeName')

    choice = self.root.now.getChild().getNodeKind()
    log(f'[[type-name()-choice]] -- {choice}')
    self.step_into(choice)
    if choice == 'ID':
      idName = self.root.now.getNodeVal()
      if idName in self.tbSym:
        sym = self.tbSym.get(idName)
        return sym.typePtr

      else:
        self.isErr = True
        self.msgErr = SemanticError.UndefinedType % idName
        self.print_error()
        return None

    if choice == 'BaseType':
      return self.base_type()

    if choice == 'StructureType':
      structType = self.root.now.getChild().getNodeKind()
      self.step_into(structType)
      if structType == 'ArrayType':
        return self.array_type()

      elif structType == 'RecType':
        size = 0
        off = 0
        fieldList = SymbolTable()
        self.step_into('RECORD')
        while True:
          if (
            self.root.isNodeKind('FieldDecMore') and 
            self.root.now.getChild(0).isNodeKind('ε')
          ): break

          self.step_into('FieldDecList')
          fieldTypeKind = self.root.now.getChild(0).getNodeKind()
          fieldType = None
          if fieldTypeKind == 'BaseType': fieldType = self.base_type()
          elif fieldTypeKind == 'ArrayType': fieldType = self.array_type()

          while True:
            if (
              self.root.isNodeKind('IdMore') and 
              self.root.now.getChild(0).isNodeKind('ε')
            ): break

            self.step_into('IdList')
            self.step_into('ID')
            log(f'[[record-type-id]] --- {fieldType} ,{self.root.now.getNodeVal()}')
            sym = VarSymbol(
              type=fieldType, 
              name=self.root.now.getNodeVal(), 
              access='indir', 
              level=self.levelCurrent, 
              off=off,
            )
            off += sym.typePtr.size
            size += sym.typePtr.size

            if sym.name in fieldList:
              self.isErr = True
              self.msgErr = SemanticError.DuplicateDefine % (sym.name)
              self.print_error(sym)

            fieldList.add(sym)
            self.step_into('IdMore')
          self.step_into('FieldDecMore')
        self.step_into('END')

        recType = RecordType(
          fieldList=fieldList, 
          size=size
        )
        return recType

  # 分析数组类型
  def array_type(self):
    self.step_into('ArrayType')
    self.step_into('[')
    self.step_into('Low')
    self.step_into('INTC')
    low = self.root.now.getNodeVal()
    self.step_into('Top')
    self.step_into('INTC')
    top = self.root.now.getNodeVal()
    self.step_into(']')
    self.step_into('OF')
    self.step_into('BaseType')
    self.step()
    bType = BaseType(kind=self.root.getNodeKind())
    top, low = int(top), int(low)
    typePtr = ArrayType(size=(top - low) * bType.size, low=low, top=top, element=bType)
    if low < 0 or (low >= top):
      self.isErr = True
      self.msgErr = SemanticError.ArrayDefineError
      self.print_error()
      return None

    return typePtr
  
  # 分析基本类型
  def base_type(self):
    self.step_into('BaseType')
    self.step()
    typePtr = BaseType(kind=self.root.getNodeKind())
    return typePtr
  
  # 分析表达式
  def expression(self):
    self.step_into('Exp')
    leftType, leftVal = self.term()
    self.step_into('OtherTerm')
    expError = False
    while True:
      if (
        self.root.isNodeKind('OtherTerm') and 
        self.root.now.getChild(0).isNodeKind('ε')
      ): break

      self.step_into('Exp')
      rightType, _ = self.expression()
      if not self.assign_type_check(leftType, rightType):
        expError = True
        self.isErr = True
        self.msgErr = SemanticError.TypeMatchError % (
          leftType,
          rightType
        )
        self.print_error()
      self.step_into('OtherTerm')

    if expError:
      leftType, leftVal = None, None

    return leftType, leftVal

  # 分析运算项
  def term(self):
    self.step_into('Term')
    leftType, leftVal = self.factor()
    self.step_into('OtherFactor')
    termError = False
    while True:
      if (
        self.root.isNodeKind('OtherFactor') and 
        self.root.now.getChild(0).isNodeKind('ε')
      ): break
      
      self.step_into('Term')
      rightType, _ = self.factor()

      if not self.assign_type_check(leftType, rightType):
        termError = True
        self.isErr = True
        self.msgErr = SemanticError.TypeMatchError % (
          leftType,
          rightType
        )
        self.print_error()

      self.step_into('OtherFactor')
      
    if termError: leftType, leftVal = (None, None)

    return leftType, leftVal
  
  # 分析因子
  def factor(self):
    self.step_into('Factor')
    self.step()
    choice = self.root.getNodeKind()
    if choice == '(':
      return self.expression()
    if choice == 'INTC':
      return 'INTC', self.root.now.getNodeVal()
    if choice == 'Variable':
      return self.variable()
  
  # 分析变量
  def variable(self):
    self.step_into('Variable')
    self.step_into('ID')
    varName = self.root.now.getNodeVal()
    var: Symbol = None
    varError = False
    for symTable in self.scope[::-1]:
      if varName in symTable:
        var = symTable.get(varName)
        self.root.now.semantic = var
        break
    
    if var == None:
      varError = True
      self.isErr = True
      self.msgErr = SemanticError.UndefinedVar % varName
      self.print_error()

    self.step_into('VariMore')
    self.step()
    choice = self.root.getNodeKind()
    if choice == 'ε':
      if varError:
        return None, None
      return var.typePtr, var.value
    if choice == '[':
      return self.expression()
    if choice == '.':
      self.step_into('FieldVar')
      self.step_into('ID')
      fieldName = self.root.now.getNodeVal()

      log(f'[[check-record-type]] --- {type(var.typePtr)}')

      if str(var.typePtr.type) != 'recordType':
        self.isErr = True
        self.msgErr = SemanticError.TypeMatchError % (
          'recordType',
          var.typePtr
        )
        self.print_error(var)
      
      fieldList = var.typePtr.type.fieldList
      if fieldName not in fieldList:
        self.isErr = True
        self.msgErr = SemanticError.UndefinedField % fieldName
        self.print_error()

        # self.step_into('FieldVarMore')
        # self.step()
        # if self.root.isNodeKind('ε'):
        #   return None, None
        # if self.root.isNodeKind('['):
        #   self.expression()
        #   return None, None

      field = fieldList.get(fieldName)
      self.root.now.semantic = field

      self.step_into('FieldVarMore')
      self.step()
      if self.root.isNodeKind('ε'):
        return field.typePtr.type, field.value
      if self.root.isNodeKind('['):
        indType, indVal = self.expression()
        if indType not in ['INTEGER', 'INTC']:
          self.isErr = True
          self.msgErr = SemanticError.TypeMatchError % (
            'INTC',
            indType
          )
          self.print_error()
          return None, None
        return field.typePtr, None
  
  # 分析条件分支
  def conditional_stm(self):
    self.step_into('IF')
    condition = self.rel_exp()
    self.step_into('THEN')
    self.stm_list()
    self.step_into('ELSE')
    self.stm_list()
    self.stm_list()
    self.step_into('FI')
  
  # 分析循环
  def loop_stm(self):
    self.step_into('WHILE')
    condition = self.rel_exp()
    self.step_into('DO')
    self.stm_list()
    self.step_into('ENDWH')
  
  # 分析输入 
  def input_stm(self):
    self.step_into('InputStm')
    self.step_into('READ')
    self.step_into('Invar')
    self.step_into('ID')
    idName = self.root.now.getNodeVal()
    
    if idName not in self.tbSym:
      self.isErr = True
      self.msgErr = SemanticError.UndefinedVar % idName
      self.print_error()
    
    sym: Symbol = self.tbSym.get(idName)
    self.root.now.semantic = sym
  
  # 分析输出
  def output_stm(self):
    self.step_into('OutputStm')
    self.step_into('WRITE')
    self.expression()

  # 分析返回
  def return_stm(self):
    self.step_into('ReturnStm')
    self.step_into('RETURN')
    self.expression()
  
  # 分析条件表达式
  def rel_exp(self):
    self.step_into('RelExp')
    leftType, _ = self.expression()
    self.step_into('CmpOp')
    rightType, _ = self.expression()
    if not self.assign_type_check(leftType, rightType):
      self.isErr = True
      self.msgErr = SemanticError.TypeMatchError % (
        leftType,
        rightType
      )
      self.print_error()
      return False
    return True