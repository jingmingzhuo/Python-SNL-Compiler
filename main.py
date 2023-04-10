import sys, os
import grammar.LL1 as grammar1
import grammar.recursiveDescent as grammar2
import morer.morer as morer 
import analyzer.semantic as analyzer
import argparse
from util.logger import log, set_debug
from util.config import get_cfg
from formula.formula import generater


if __name__ == '__main__':


  parser = argparse.ArgumentParser(description='Training segmentation network')
  parser.add_argument('--cfg',
                        help='experiment config file address',
                        default="configs/config.yaml",
                        type=str)
  args = parser.parse_args()
  cfg = get_cfg()
  cfg.merge_from_file(args.cfg)
  cfg.freeze()

  fileName = cfg.MORER.SNL_TEXT
  snlText = ''
  with open(fileName, encoding='utf-8') as file:
    snlText = file.read()

  # 运行 词法分析器 根据SNLText 获取 TokenList
  tokenList = morer.run(cfg,snlText)

  log('\n'.join(map(lambda x: str(x), tokenList)))

  # 运行 LL1或递归下降语法分析器 根据TokenList 获取 GrammarTree
  if cfg.GRAMMAR.GRAMMAR_METHOD=='LL1':
    tree = grammar1.run(cfg, tokenList)
  else:
    tree = grammar2.run(cfg, tokenList)
  
  # 通过 GrammarTree 和 Tokens 获取符号表信息、分析语义
  _analyzer = analyzer.Analyzer(tokenList, tree)
  _analyzer.analyze()

  # 中间代码优化
  output = cfg.FORMULA.OUT_ADDRESS
  generator = generater(tree)
  formula_list = generator.scan()
  if cfg.FORMULA.CHOOSE=='sample':
    formula_list.show2(output)
  else :
    formula_list.show(output)

  print('结果已生成在 dist 目录下')
