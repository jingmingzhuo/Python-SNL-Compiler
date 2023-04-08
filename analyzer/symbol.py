from util.logger import log

class BaseType(object):
  def __init__(self, size=1, kind=None):
    self.size = size
    self.type = kind
    self.element = None

  def __repr__(self) -> str:
    return self.type if type(self.type) == str else self.type.__str__()
  
  def __str__(self) -> str:
    return self.type if type(self.type) == str else self.type.__str__()


class ArrayType(object):
  def __init__(self, low=None, top=None, element=None) -> None:
    self.size = (top - low + 1) * element.size;
    self.kind = 'arrayType'
    self.low = low
    self.top = top
    self.element = element

  def __repr__(self) -> str:
    return 'array[%d .. %d] of %s' % (self.low, self.top, self.element.type)

  def __str__(self) -> str:
    return 'array[%d .. %d] of %s' % (self.low, self.top, self.element.type)


class RecordType(object):
  def __init__(self, size=None, fieldList=None) -> None:
    self.size = size
    self.kind = 'recordType'
    self.fieldList = fieldList

  def __repr__(self) -> str:
    return 'record %s' % (self.fieldList)

  def __str__(self) -> str:
    return 'recordType'

class Symbol(object):
  def __init__(self, name=None, kind=None, type=None) -> None:
    self.name = name
    self.decKind = kind
    self.typePtr = type

  def __repr__(self) -> str:
    return "%s\t\t\t%s\t\t%s" % (self.name, self.decKind, self.typePtr)

class VarSymbol(Symbol):
  def __init__(self, name=None, type=None, access=None, level=None, off=None, value=None) -> None:
    super().__init__(name, 'varDec', type)
    self.access = access
    # TODO
    self.level = level
    self.off = off
    self.value = value

  def __repr__(self) -> str:
    return "%s\t%s\t\t%s\t\t%s" % (
      super().__repr__(),
      self.access,
      self.level,
      self.off
    )

class TypeSymbol(Symbol):
  def __init__(self, name=None, type=None) -> None:
    super().__init__(name, 'typeDec', type)


class ProcedureSymbol(Symbol):
  def __init__(self, name=None, type=None, level=None, off=None, param=None, _class=None, code=None, size=None, forward=None) -> None:
    super().__init__(name, 'procDec', type)
    # TODO
    self.level = level
    self.off = off
    self.param = param
    self._class = _class
    self.code = code
    self.size = size
    self.forward = forward

  def __repr__(self):
    return "%s\t%s\t\t%s" % (
      super().__repr__(),
      self.level,
      self.off
    )


class SymbolTable(list):
  def add(self, symbol):
    self.append(symbol)
    log(f'[[symbol-table]] -- {self}')

  def top(self):
    return self[-1]

  def get(self, name):
    for sym in self[::-1]:
      if sym.name == name:
        return sym;
    return None

  def __repr__(self) -> str:
    return '\n\t'.join([''] + [str(i) for i in self])

  def __contains__(self, item: str) -> bool:
    for sym in self:
      if sym.name == item:
        return True
    return False

