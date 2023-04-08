import grammar.getGrammar as gg
from util.logger import log

assetDir = 'assets/'

def getFirstLeft(grammar:dict,left:str)->set:
    leftSet=set()
    if left in grammar['VT'] or left == 'ε':
        leftSet.add(left)
        return leftSet
    else:
        leftP:dict=grammar['P'][left]
        for sub in leftP:
            # log(sub)
            if leftP[sub][0]=='ε':leftSet.add('ε')
            else:
                for item in range(len(leftP[sub])):
                    subSet=getFirstLeft(grammar,leftP[sub][item])
                    if 'ε' in subSet and len(leftP[sub])-1!=item:
                        subSet.remove('ε')
                        leftSet=leftSet.union(subSet)
                    else:
                        leftSet=leftSet.union(subSet)
                        break
    return leftSet

def getFirst(grammar:dict)->dict:
    firstSet={}
    for symbol in grammar['VT']:
        firstSet[symbol]=set()
        firstSet[symbol].add(symbol)
    for symbol in grammar['VN']:
        firstSet[symbol]=getFirstLeft(grammar,symbol)
    # f=open(assetDir + 'SNL_First.txt','w',encoding='utf-8')
    # for symbol in firstSet:
    #     f.write('First['+symbol+']:')
    #     for i in firstSet[symbol]:
    #         f.write(' '+i)
    #     f.write('\n')
    return firstSet

def getFollow(grammar:dict,firstSet:dict)->dict:
    followSet={}
    for symbol in grammar['VN']:
        followSet[symbol]=set()
    followSet[grammar['S']].add('#')
    followFlag=True
    while followFlag:
        preSet=[len(followSet[symbol]) for symbol in followSet]
        for symbol in grammar['P']:
            for i in grammar['P'][symbol]:
                production=grammar['P'][symbol][i]
                l=len(production)
                if l==1:
                    if production[0] in grammar['VN']:
                        followSet[production[0]]=followSet[production[0]].union(followSet[symbol])
                    continue
                for j in range(l-1,-1,-1):
                    if production[j] in grammar['VT']:continue
                    tmp=j+1
                    while tmp!=l:
                        followSet[production[j]]=followSet[production[j]].union(firstSet[production[tmp]])
                        if 'ε' in firstSet[production[tmp]]:
                            followSet[production[j]].remove('ε')
                            tmp=tmp+1
                        else:break
                    if tmp==l:followSet[production[j]]=followSet[production[j]].union(followSet[symbol])
        nowSet=[len(followSet[symbol]) for symbol in followSet]
        if nowSet==preSet:followFlag=False
    # f=open(assetDir + 'SNL_Follow.txt','w',encoding='utf-8')
    # for symbol in followSet:
    #     f.write('Follow['+symbol+']:')
    #     for i in followSet[symbol]:
    #         f.write(' '+i)
    #     f.write('\n')
    return followSet

def getPredict(grammar:dict)->dict:
    firstSet=getFirst(grammar)
    followSet=getFollow(grammar,firstSet)
    predictSet={}
    for symbol in grammar['VN']:
        predictSet[symbol]={}
        for i in grammar['P'][symbol]:
            predictSet[symbol][i]=set()
    for symbol in grammar['P']:
        for i in grammar['P'][symbol]:
            length=len(grammar['P'][symbol][i])
            if length==1 and grammar['P'][symbol][i][0]=='ε':
                predictSet[symbol][i]=followSet[symbol]
                continue
            tmp=0
            while tmp<length:
                predictSet[symbol][i]=predictSet[symbol][i].union(firstSet[grammar['P'][symbol][i][tmp]])
                if 'ε' not in firstSet[grammar['P'][symbol][i][tmp]]:
                    break
                else:
                    predictSet[symbol][i].remove('ε')
                    tmp=tmp+1
            if tmp==length:predictSet[symbol][i]=predictSet[symbol][i].union(followSet[symbol])
    return predictSet

def getAnalysisTable(grammar:dict)->dict:
    predictSet=getPredict(grammar)
    analysisTable={}
    for vn in grammar['VN']:
        analysisTable[vn]={}
        for vt in grammar['VT']:
            analysisTable[vn][vt]=-1
    for symbol in grammar['P']:
        for i in grammar['P'][symbol]:
            for vt in predictSet[symbol][i]:
                analysisTable[symbol][vt]=i
    return analysisTable

if __name__=='__main__':
    grammar={}
    grammar['S']='Program'
    assetDir = 'assets/'
    pAddress=assetDir + 'SNL_P.txt'
    vnAddress=assetDir + 'SNL_VN.txt'
    vtAddress=assetDir + 'SNL_VT.txt'
    grammar=gg.getGrammar(grammar,pAddress,vnAddress,vtAddress)
    # log(grammar['P'])
    analysisTable=getAnalysisTable(grammar)