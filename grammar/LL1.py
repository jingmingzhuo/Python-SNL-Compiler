from grammar.getGrammar import getGrammar 
from grammar.ThreeSet import getAnalysisTable
from grammar.TokenProcessing import TokenProcessing
from grammar.GrammarTree import GrammarNode, GrammarTree
from grammar.Visualization import visualization
from util.logger import log

def LL1(grammar:dict,analysisTable:dict,token:TokenProcessing)->GrammarTree:
    tree:GrammarTree=GrammarTree(GrammarNode(None,None,0,-1,grammar['S'],grammar['S'],'VN'))
    stack:list=[]
    stack.append(grammar['S'])
    # log(f'[[LL1]]')
    while not token.isEnd():
        # log(f'[[stack]] -- {stack}')    
        nowToken:list=token.getNowToken()
        # log(f'[[token]] -- {nowToken}')

        nowLeft=stack[-1]
        if nowLeft not in grammar['VN']:
            if nowLeft!='ε' and nowToken[0]!=nowLeft:
                print('ERROR1')
                return None

            if nowLeft!='ε':
                tree.getNow().nodeVal=nowToken[1]
                token.next()

            stack.pop()

            while (
                tree.getNow().getFather() is not None and 
                tree.getBrother() is None
            ): tree.goFather()

            if tree.getBrother() is not None: tree.goBrother()

        else:
            num=analysisTable[nowLeft][nowToken[0]]
            if num==-1:
                log('ERROR2')
                return None

            stack.pop()
            product=grammar['P'][nowLeft][num]
            length=len(product)
            for i in range(length):
                symbol:str='VN' if product[i] in grammar['VN'] else 'VT'
                if product[i]=='ε':symbol='EPS'

                # log(f'[[tree.now]] -- {tree.now}')

                kind:str=product[i]
                tree.addChild(GrammarNode(tree.getNow(),None,tree.getNodeNum(),-1,kind,kind,symbol,None))
            tree.goChild()
            for i in range(length-1,-1,-1):
                stack.append(product[i])
    return tree

def dfs(now:GrammarNode,cnt:int)->int:
    cnt=cnt+1
    # print(now.getNodeKind())
    num:int=0
    while num<now.getChildNum():
        cnt=dfs(now.getChild(num),cnt)
        num=num+1
    return cnt

def run(tokenList: list=None):
    grammar={}
    grammar['S']='Program'

    assetDir='assets/'
    pAddress=assetDir+'SNL_P.txt'
    vnAddress=assetDir+'SNL_VN.txt'
    vtAddress=assetDir+'SNL_VT.txt'

    # 初始化
    grammar=getGrammar(grammar,pAddress,vnAddress,vtAddress)
    analysisTable=getAnalysisTable(grammar)

    # 生成 tokens 以及 ast
    # token=TokenProcessing(model='list', tokenList=tokenList)
    token=TokenProcessing('read', 'out.txt')
    tree=LL1(grammar,analysisTable,token)
    tree.goRoot()
    visualization(grammar,tree)
    # log(tree.getRoot())

    return tree

if __name__=='__main__':
    run()
