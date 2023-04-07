from util.logger import log

def getGrammar(grammar:dict,pAddress:str,vnAddress:str,vtAddress:str)->dict:
    grammar=grammar
    readP=[]
    with open(pAddress,encoding='utf-8') as F:
        readP=F.read().split('\n')
    for i in range(len(readP)):
        readP[i]=readP[i].split('->')
        readP[i][1]=readP[i][1].split('|')
    for i in range(len(readP)):
        readP[i][0]=readP[i][0].strip(' ')
        for j in range(len(readP[i][1])):
            readP[i][1][j]=readP[i][1][j].strip().split(' ')

    grammar['P']={}
    for line in readP:
        grammar['P'][line[0]]={}
        count=0
        for subline in line[1]:
            grammar["P"][line[0]][count]=subline
            count=count+1

    grammar['VN']=[]
    with open(vnAddress,encoding='utf-8') as F:
        grammar['VN'].extend(F.read().split('\n'))
    grammar['VT']=[]

    with open(vtAddress,encoding='utf-8') as F:
        grammar['VT'].extend(F.read().split('\n'))
    return grammar

def run():
    grammar={}
    grammar['S']='E'
    assetDir='assets/'
    pAddress=assetDir + 'Grammar.txt'
    vnAddress=assetDir + 'non_termination_set.txt'
    vtAddress=assetDir + 'termination_set.txt'
    grammar=getGrammar(grammar,pAddress,vnAddress,vtAddress)
    log(grammar['S'])
    log(grammar['P'])
    log(grammar['VN'])
    log(grammar['VT'])

if __name__=='__main__':
    run()