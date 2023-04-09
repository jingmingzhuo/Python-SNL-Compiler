from util.logger import log
from analyzer.symbol import Symbol

class GrammarNode(object):
    def __init__(
        self,
        father,
        sibling,
        nodeID: int,
        lineno: int,
        nodeKind: str,
        nodeVal: str,
        symbol: str,
        semantic: Symbol=None
    ) -> None:
        self.father:GrammarNode=father
        self.sibling:GrammarNode=sibling
        self.children:list=[]
        self.childNum:int=0    
        self.nodeID:int=nodeID

        self.lineNo:int=lineno
        self.symbol=symbol
        self.nodeKind:str=nodeKind
        self.nodeVal:str=nodeVal
        self.semantic = None

    def getFather(self):
        return self.father

    def getChild(self,num:int=0):
        return self.children[num]

    def getChildNum(self)->int:
        return self.childNum

    def getSibling(self):
        return self.sibling

    def getLineNo(self)->int:
        return self.lineNo

    def getNodeKind(self)->str:
        return self.nodeKind

    def getNodeVal(self)->str:
        return self.nodeVal

    def addChild(self,child)->None:
        self.children.append(child)
        self.childNum=self.childNum+1
        if self.childNum!=1:
            self.getChild(self.childNum-2).sibling=self.getChild(self.childNum-1)

    def isNodeKind(self, nodeKind: str):
        return self.nodeKind == nodeKind
    
    def getNodeID(self)->int:
        return self.nodeID

    def getNodeSemantic(self):
        return self.semantic

class GrammarTree(object):
    def __init__(self,root:GrammarNode)->None:
        self.root:GrammarNode=root
        self.now:GrammarNode=self.root
        self.nodeNum=1
        
    def getNow(self)->GrammarNode:
        return self.now

    def goRoot(self)->None:
        self.now=self.root

    def getRoot(self):
        return self.root

    def goFather(self)->None:
        self.now=self.now.getFather()

    def getFather(self):
        return self.now.getFather()

    def goBrother(self)->None:
        self.now=self.now.getSibling()

    def getBrother(self):
        return self.now.getSibling()

    def goChild(self,num:int=0)->None:
        self.now=self.now.getChild(num)

    def addChild(self,child:GrammarNode)->None:
        # log(f'[[child]] -- {child}')
        self.now.addChild(child)
        self.nodeNum=self.nodeNum+1

    def addNodeNum(self)->None:
        self.nodeNum=self.nodeNum+1
        
    def getNodeNum(self)->int:
        return self.nodeNum

    # 迭代器
    def nextNode(self)->bool:
        nextFlag=True
        while nextFlag:
            while self.getNow().getChildNum()!=0:
                self.goChild()
                yield True
            while self.getNow().getFather() is not None and self.getBrother() is None:
                self.goFather()
            if self.getBrother() is not None:
                self.goBrother()
                yield True
            else:
                nextFlag=False
                yield False

    # 判断当前的节点的类型
    def isNodeKind(self, nodeKind: str)->bool:
        return self.now.isNodeKind(nodeKind)
    
    # 获取当前节点的类型
    def getNodeKind(self)->str:
        return self.now.getNodeKind()

    def isEmpty(self)->bool:
        return self.getNow().childNum == 0