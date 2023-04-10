import yaml
from yacs.config import CfgNode as CN


_C = CN()

_C.MORER = CN()
_C.MORER.SNL_TEXT = 'test/test0.snl'
_C.MORER.OUT_ADDRESS = 'morer/out.txt'

_C.GRAMMAR = CN()
_C.GRAMMAR.GRAMMAR_METHOD = 'LL1'
_C.GRAMMAR.START = 'Program'
_C.GRAMMAR.PRODUCTION_ADDRESS = 'assets/SNL_P.txt'
_C.GRAMMAR.VT_ADDRESS = 'assets/SNL_VT.txt'
_C.GRAMMAR.VN_ADDRESS = 'assets/SNL_VN.txt'
_C.GRAMMAR.GRAMMAR_TREE_VISUALIZATION = True
_C.GRAMMAR.VISUAL_ADDRESS = 'grammar/GrammarTree'
_C.GRAMMAR.VISUAL_VN_COLOR = 'blue'
_C.GRAMMAR.VISUAL_VT_COLOR = 'red'
_C.GRAMMAR.VISUAL_EPS_COLOR= 'yellow'

_C.ANALYZER = CN()

_C.FORMULA = CN()
_C.FORMULA.OUT_ADDRESS = 'dist/a.out'
_C.FORMULA.CHOOSE = 'sample'

def get_cfg():
    return _C.clone()