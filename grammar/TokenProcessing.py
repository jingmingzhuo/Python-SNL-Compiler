from util.logger import log

class TokenProcessing(object):
    def __init__(self,model:str='read',address:str=None,tokenList:list=None) -> None:
        self.pointer=0
        self.tokenList=[]
        if model=='read':
            with open(address) as F:
                self.tokenList=F.read().split('\n')
                while self.tokenList[-1] == '':
                    self.tokenList.pop()
            for line in range(len(self.tokenList)):
                self.tokenList[line]=self.tokenList[line].strip('<>').split('|')
                self.tokenList[line][2]=int(self.tokenList[line][2])
        else:
            # tokenList = tokenList[1::]
            self.tokenList=tokenList
    def getNowToken(self)->list:
        return self.tokenList[self.pointer]
    def next(self)->int:
        if self.pointer!=len(self.tokenList):
            self.pointer=self.pointer+1
            return self.pointer
        else :return -1
    def isEnd(self)->bool:
        if self.pointer==len(self.tokenList):
            return True
        else:
            return False

if __name__=='__main__':
    token=tokenProcessing('read','tokenList.txt')
    token.next()
    print(token.getNowToken())



