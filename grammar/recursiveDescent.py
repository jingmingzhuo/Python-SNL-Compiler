import sys,os
from grammar.TokenProcessing import TokenProcessing
from grammar.GrammarTree import GrammarNode, GrammarTree
from grammar.Visualization import visualization
from grammar.getGrammar import getGrammar
from grammar.grammarException import TypeError,RedundancyError
def ActParamList(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'ActParamList','ActParamList','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token[0]==')':
		node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'ε','ε','EPS',None))
		tree.addNodeNum()
	elif token[0]=='ID' or token[0]=='(' or token[0]=='INTC':
		Exp(tree,node,tokenList)
		ActParamMore(tree,node,tokenList)
	else:
		Error(token[2],'ActParamList',token[0])
def ActParamMore(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'ActParamMore','ActParamMore','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token[0]==')':
		node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'ε','ε','EPS',None))
		tree.addNodeNum()
	elif token[0]==',':
		Match(tree,node,tokenList,',')
		ActParamList(tree,node,tokenList)
	else:
		Error(token[2],'ActParamMore',token[0])
def AddOp(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'AddOp','AddOp','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token[0]=='+':
		Match(tree,node,tokenList,'+')
	elif token[0]=='-':
		Match(tree,node,tokenList,'-')
	else:
		Error(token[2],'AddOp',token[0])
def ArrayType(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'ArrayType','ArrayType','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token[0]=='ARRAY':
		Match(tree,node,tokenList,'ARRAY')
		Match(tree,node,tokenList,'[')
		Low(tree,node,tokenList)
		Match(tree,node,tokenList,'..')
		Top(tree,node,tokenList)
		Match(tree,node,tokenList,']')
		Match(tree,node,tokenList,'OF')
		BaseType(tree,node,tokenList)
	else:
		Error(token[2],'ArrayType',token[0])
def AssCall(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'AssCall','AssCall','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token[0]=='.' or token[0]=='[' or token[0]==':=':
		AssignmentRest(tree,node,tokenList)
	elif token[0]=='(':
		CallStmRest(tree,node,tokenList)
	else:
		Error(token[2],'AssCall',token[0])
def AssignmentRest(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'AssignmentRest','AssignmentRest','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token[0]=='.' or token[0]=='[' or token[0]==':=':
		VariMore(tree,node,tokenList)
		Match(tree,node,tokenList,':=')
		Exp(tree,node,tokenList)
	else:
		Error(token[2],'AssignmentRest',token[0])
def BaseType(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'BaseType','BaseType','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token[0]=='INTEGER':
		Match(tree,node,tokenList,'INTEGER')
	elif token[0]=='CHAR':
		Match(tree,node,tokenList,'CHAR')
	else:
		Error(token[2],'BaseType',token[0])
def CallStmRest(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'CallStmRest','CallStmRest','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token[0]=='(':
		Match(tree,node,tokenList,'(')
		ActParamList(tree,node,tokenList)
		Match(tree,node,tokenList,')')
	else:
		Error(token[2],'CallStmRest',token[0])
def CmpOp(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'CmpOp','CmpOp','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token[0]=='<':
		Match(tree,node,tokenList,'<')
	elif token[0]=='=':
		Match(tree,node,tokenList,'=')
	else:
		Error(token[2],'CmpOp',token[0])
def ConditionalStm(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'ConditionalStm','ConditionalStm','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token[0]=='IF':
		Match(tree,node,tokenList,'IF')
		RelExp(tree,node,tokenList)
		Match(tree,node,tokenList,'THEN')
		StmList(tree,node,tokenList)
		Match(tree,node,tokenList,'ELSE')
		StmList(tree,node,tokenList)
		Match(tree,node,tokenList,'FI')
	else:
		Error(token[2],'ConditionalStm',token[0])
def DeclarePart(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'DeclarePart','DeclarePart','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token[0]=='PROCEDURE' or token[0]=='VAR' or token[0]=='BEGIN' or token[0]=='TYPE':
		TypeDec(tree,node,tokenList)
		VarDec(tree,node,tokenList)
		ProcDec(tree,node,tokenList)
	else:
		Error(token[2],'DeclarePart',token[0])
def Exp(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'Exp','Exp','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token[0]=='ID' or token[0]=='(' or token[0]=='INTC':
		Term(tree,node,tokenList)
		OtherTerm(tree,node,tokenList)
	else:
		Error(token[2],'Exp',token[0])
def Factor(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'Factor','Factor','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token[0]=='(':
		Match(tree,node,tokenList,'(')
		Exp(tree,node,tokenList)
		Match(tree,node,tokenList,')')
	elif token[0]=='INTC':
		Match(tree,node,tokenList,'INTC')
	elif token[0]=='ID':
		Variable(tree,node,tokenList)
	else:
		Error(token[2],'Factor',token[0])
def FidMore(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'FidMore','FidMore','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token[0]==')' or token[0]==';':
		node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'ε','ε','EPS',None))
		tree.addNodeNum()
	elif token[0]==',':
		Match(tree,node,tokenList,',')
		FormList(tree,node,tokenList)
	else:
		Error(token[2],'FidMore',token[0])
def FieldDecList(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'FieldDecList','FieldDecList','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token[0]=='INTEGER' or token[0]=='CHAR':
		BaseType(tree,node,tokenList)
		IdList(tree,node,tokenList)
		Match(tree,node,tokenList,';')
		FieldDecMore(tree,node,tokenList)
	elif token[0]=='ARRAY':
		ArrayType(tree,node,tokenList)
		IdList(tree,node,tokenList)
		Match(tree,node,tokenList,';')
		FieldDecMore(tree,node,tokenList)
	else:
		Error(token[2],'FieldDecList',token[0])
def FieldDecMore(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'FieldDecMore','FieldDecMore','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token[0]=='END':
		node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'ε','ε','EPS',None))
		tree.addNodeNum()
	elif token[0]=='INTEGER' or token[0]=='CHAR' or token[0]=='ARRAY':
		FieldDecList(tree,node,tokenList)
	else:
		Error(token[2],'FieldDecMore',token[0])
def FieldVar(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'FieldVar','FieldVar','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token[0]=='ID':
		Match(tree,node,tokenList,'ID')
		FieldVarMore(tree,node,tokenList)
	else:
		Error(token[2],'FieldVar',token[0])
def FieldVarMore(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'FieldVarMore','FieldVarMore','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token[0]=='<' or token[0]=='ELSE' or token[0]==')' or token[0]=='ENDWH' or token[0]=='/' or token[0]==':=' or token[0]==']' or token[0]=='FI' or token[0]==';' or token[0]=='=' or token[0]=='END' or token[0]=='DO' or token[0]=='-' or token[0]=='*' or token[0]==',' or token[0]=='THEN' or token[0]=='+':
		node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'ε','ε','EPS',None))
		tree.addNodeNum()
	elif token[0]=='[':
		Match(tree,node,tokenList,'[')
		Exp(tree,node,tokenList)
		Match(tree,node,tokenList,']')
	else:
		Error(token[2],'FieldVarMore',token[0])
def FormList(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'FormList','FormList','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token[0]=='ID':
		Match(tree,node,tokenList,'ID')
		FidMore(tree,node,tokenList)
	else:
		Error(token[2],'FormList',token[0])
def IdList(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'IdList','IdList','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token[0]=='ID':
		Match(tree,node,tokenList,'ID')
		IdMore(tree,node,tokenList)
	else:
		Error(token[2],'IdList',token[0])
def IdMore(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'IdMore','IdMore','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token[0]==';':
		node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'ε','ε','EPS',None))
		tree.addNodeNum()
	elif token[0]==',':
		Match(tree,node,tokenList,',')
		IdList(tree,node,tokenList)
	else:
		Error(token[2],'IdMore',token[0])
def InputStm(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'InputStm','InputStm','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token[0]=='READ':
		Match(tree,node,tokenList,'READ')
		Match(tree,node,tokenList,'(')
		Invar(tree,node,tokenList)
		Match(tree,node,tokenList,')')
	else:
		Error(token[2],'InputStm',token[0])
def Invar(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'Invar','Invar','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token[0]=='ID':
		Match(tree,node,tokenList,'ID')
	else:
		Error(token[2],'Invar',token[0])
def LoopStm(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'LoopStm','LoopStm','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token[0]=='WHILE':
		Match(tree,node,tokenList,'WHILE')
		RelExp(tree,node,tokenList)
		Match(tree,node,tokenList,'DO')
		StmList(tree,node,tokenList)
		Match(tree,node,tokenList,'ENDWH')
	else:
		Error(token[2],'LoopStm',token[0])
def Low(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'Low','Low','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token[0]=='INTC':
		Match(tree,node,tokenList,'INTC')
	else:
		Error(token[2],'Low',token[0])
def MultOp(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'MultOp','MultOp','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token[0]=='*':
		Match(tree,node,tokenList,'*')
	elif token[0]=='/':
		Match(tree,node,tokenList,'/')
	else:
		Error(token[2],'MultOp',token[0])
def OtherFactor(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'OtherFactor','OtherFactor','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token[0]=='<' or token[0]=='ELSE' or token[0]==')' or token[0]=='ENDWH' or token[0]==']' or token[0]=='FI' or token[0]==';' or token[0]=='=' or token[0]=='END' or token[0]=='DO' or token[0]=='-' or token[0]==',' or token[0]=='THEN' or token[0]=='+':
		node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'ε','ε','EPS',None))
		tree.addNodeNum()
	elif token[0]=='*' or token[0]=='/':
		MultOp(tree,node,tokenList)
		Term(tree,node,tokenList)
	else:
		Error(token[2],'OtherFactor',token[0])
def OtherRelE(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'OtherRelE','OtherRelE','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token[0]=='<' or token[0]=='=':
		CmpOp(tree,node,tokenList)
		Exp(tree,node,tokenList)
	else:
		Error(token[2],'OtherRelE',token[0])
def OtherTerm(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'OtherTerm','OtherTerm','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token[0]=='<' or token[0]=='ELSE' or token[0]==')' or token[0]=='ENDWH' or token[0]==']' or token[0]=='FI' or token[0]==';' or token[0]=='=' or token[0]=='END' or token[0]=='DO' or token[0]==',' or token[0]=='THEN':
		node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'ε','ε','EPS',None))
		tree.addNodeNum()
	elif token[0]=='-' or token[0]=='+':
		AddOp(tree,node,tokenList)
		Exp(tree,node,tokenList)
	else:
		Error(token[2],'OtherTerm',token[0])
def OutputStm(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'OutputStm','OutputStm','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token[0]=='WRITE':
		Match(tree,node,tokenList,'WRITE')
		Match(tree,node,tokenList,'(')
		Exp(tree,node,tokenList)
		Match(tree,node,tokenList,')')
	else:
		Error(token[2],'OutputStm',token[0])
def Param(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'Param','Param','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token[0]=='INTEGER' or token[0]=='RECORD' or token[0]=='ID' or token[0]=='CHAR' or token[0]=='ARRAY':
		TypeName(tree,node,tokenList)
		FormList(tree,node,tokenList)
	elif token[0]=='VAR':
		Match(tree,node,tokenList,'VAR')
		TypeName(tree,node,tokenList)
		FormList(tree,node,tokenList)
	else:
		Error(token[2],'Param',token[0])
def ParamDecList(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'ParamDecList','ParamDecList','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token[0]=='INTEGER' or token[0]=='RECORD' or token[0]=='VAR' or token[0]=='ID' or token[0]=='CHAR' or token[0]=='ARRAY':
		Param(tree,node,tokenList)
		ParamMore(tree,node,tokenList)
	else:
		Error(token[2],'ParamDecList',token[0])
def ParamList(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'ParamList','ParamList','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token[0]==')':
		node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'ε','ε','EPS',None))
		tree.addNodeNum()
	elif token[0]=='INTEGER' or token[0]=='RECORD' or token[0]=='VAR' or token[0]=='ID' or token[0]=='CHAR' or token[0]=='ARRAY':
		ParamDecList(tree,node,tokenList)
	else:
		Error(token[2],'ParamList',token[0])
def ParamMore(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'ParamMore','ParamMore','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token[0]==')':
		node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'ε','ε','EPS',None))
		tree.addNodeNum()
	elif token[0]==';':
		Match(tree,node,tokenList,';')
		ParamDecList(tree,node,tokenList)
	else:
		Error(token[2],'ParamMore',token[0])
def ProcBody(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'ProcBody','ProcBody','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token[0]=='BEGIN':
		ProgramBody(tree,node,tokenList)
	else:
		Error(token[2],'ProcBody',token[0])
def ProcDec(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'ProcDec','ProcDec','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token[0]=='BEGIN':
		node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'ε','ε','EPS',None))
		tree.addNodeNum()
	elif token[0]=='PROCEDURE':
		ProcDeclaration(tree,node,tokenList)
	else:
		Error(token[2],'ProcDec',token[0])
def ProcDecMore(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'ProcDecMore','ProcDecMore','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token[0]=='BEGIN':
		node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'ε','ε','EPS',None))
		tree.addNodeNum()
	elif token[0]=='PROCEDURE':
		ProcDeclaration(tree,node,tokenList)
	else:
		Error(token[2],'ProcDecMore',token[0])
def ProcDecPart(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'ProcDecPart','ProcDecPart','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token[0]=='PROCEDURE' or token[0]=='VAR' or token[0]=='BEGIN' or token[0]=='TYPE':
		DeclarePart(tree,node,tokenList)
	else:
		Error(token[2],'ProcDecPart',token[0])
def ProcDeclaration(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'ProcDeclaration','ProcDeclaration','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token[0]=='PROCEDURE':
		Match(tree,node,tokenList,'PROCEDURE')
		ProcName(tree,node,tokenList)
		Match(tree,node,tokenList,'(')
		ParamList(tree,node,tokenList)
		Match(tree,node,tokenList,')')
		Match(tree,node,tokenList,';')
		ProcDecPart(tree,node,tokenList)
		ProcBody(tree,node,tokenList)
		ProcDecMore(tree,node,tokenList)
	else:
		Error(token[2],'ProcDeclaration',token[0])
def ProcName(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'ProcName','ProcName','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token[0]=='ID':
		Match(tree,node,tokenList,'ID')
	else:
		Error(token[2],'ProcName',token[0])
def ProgramBody(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'ProgramBody','ProgramBody','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token[0]=='BEGIN':
		Match(tree,node,tokenList,'BEGIN')
		StmList(tree,node,tokenList)
		Match(tree,node,tokenList,'END')
	else:
		Error(token[2],'ProgramBody',token[0])
def ProgramHead(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'ProgramHead','ProgramHead','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token[0]=='PROGRAM':
		Match(tree,node,tokenList,'PROGRAM')
		ProgramName(tree,node,tokenList)
	else:
		Error(token[2],'ProgramHead',token[0])
def ProgramName(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'ProgramName','ProgramName','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token[0]=='ID':
		Match(tree,node,tokenList,'ID')
	else:
		Error(token[2],'ProgramName',token[0])
def RecType(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'RecType','RecType','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token[0]=='RECORD':
		Match(tree,node,tokenList,'RECORD')
		FieldDecList(tree,node,tokenList)
		Match(tree,node,tokenList,'END')
	else:
		Error(token[2],'RecType',token[0])
def RelExp(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'RelExp','RelExp','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token[0]=='ID' or token[0]=='(' or token[0]=='INTC':
		Exp(tree,node,tokenList)
		OtherRelE(tree,node,tokenList)
	else:
		Error(token[2],'RelExp',token[0])
def ReturnStm(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'ReturnStm','ReturnStm','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token[0]=='RETURN':
		Match(tree,node,tokenList,'RETURN')
		Match(tree,node,tokenList,'(')
		Exp(tree,node,tokenList)
		Match(tree,node,tokenList,')')
	else:
		Error(token[2],'ReturnStm',token[0])
def Stm(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'Stm','Stm','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token[0]=='IF':
		ConditionalStm(tree,node,tokenList)
	elif token[0]=='WHILE':
		LoopStm(tree,node,tokenList)
	elif token[0]=='READ':
		InputStm(tree,node,tokenList)
	elif token[0]=='WRITE':
		OutputStm(tree,node,tokenList)
	elif token[0]=='RETURN':
		ReturnStm(tree,node,tokenList)
	elif token[0]=='ID':
		Match(tree,node,tokenList,'ID')
		AssCall(tree,node,tokenList)
	else:
		Error(token[2],'Stm',token[0])
def StmList(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'StmList','StmList','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token[0]=='RETURN' or token[0]=='READ' or token[0]=='ID' or token[0]=='IF' or token[0]=='WRITE' or token[0]=='WHILE':
		Stm(tree,node,tokenList)
		StmMore(tree,node,tokenList)
	else:
		Error(token[2],'StmList',token[0])
def StmMore(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'StmMore','StmMore','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token[0]=='ELSE' or token[0]=='ENDWH' or token[0]=='END' or token[0]=='FI':
		node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'ε','ε','EPS',None))
		tree.addNodeNum()
	elif token[0]==';':
		Match(tree,node,tokenList,';')
		StmList(tree,node,tokenList)
	else:
		Error(token[2],'StmMore',token[0])
def StructureType(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'StructureType','StructureType','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token[0]=='ARRAY':
		ArrayType(tree,node,tokenList)
	elif token[0]=='RECORD':
		RecType(tree,node,tokenList)
	else:
		Error(token[2],'StructureType',token[0])
def Term(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'Term','Term','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token[0]=='ID' or token[0]=='(' or token[0]=='INTC':
		Factor(tree,node,tokenList)
		OtherFactor(tree,node,tokenList)
	else:
		Error(token[2],'Term',token[0])
def Top(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'Top','Top','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token[0]=='INTC':
		Match(tree,node,tokenList,'INTC')
	else:
		Error(token[2],'Top',token[0])
def TypeDec(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'TypeDec','TypeDec','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token[0]=='PROCEDURE' or token[0]=='VAR' or token[0]=='BEGIN':
		node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'ε','ε','EPS',None))
		tree.addNodeNum()
	elif token[0]=='TYPE':
		TypeDeclaration(tree,node,tokenList)
	else:
		Error(token[2],'TypeDec',token[0])
def TypeDecList(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'TypeDecList','TypeDecList','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token[0]=='ID':
		TypeId(tree,node,tokenList)
		Match(tree,node,tokenList,'=')
		TypeName(tree,node,tokenList)
		Match(tree,node,tokenList,';')
		TypeDecMore(tree,node,tokenList)
	else:
		Error(token[2],'TypeDecList',token[0])
def TypeDecMore(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'TypeDecMore','TypeDecMore','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token[0]=='PROCEDURE' or token[0]=='VAR' or token[0]=='BEGIN':
		node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'ε','ε','EPS',None))
		tree.addNodeNum()
	elif token[0]=='ID':
		TypeDecList(tree,node,tokenList)
	else:
		Error(token[2],'TypeDecMore',token[0])
def TypeDeclaration(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'TypeDeclaration','TypeDeclaration','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token[0]=='TYPE':
		Match(tree,node,tokenList,'TYPE')
		TypeDecList(tree,node,tokenList)
	else:
		Error(token[2],'TypeDeclaration',token[0])
def TypeId(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'TypeId','TypeId','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token[0]=='ID':
		Match(tree,node,tokenList,'ID')
	else:
		Error(token[2],'TypeId',token[0])
def TypeName(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'TypeName','TypeName','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token[0]=='INTEGER' or token[0]=='CHAR':
		BaseType(tree,node,tokenList)
	elif token[0]=='RECORD' or token[0]=='ARRAY':
		StructureType(tree,node,tokenList)
	elif token[0]=='ID':
		Match(tree,node,tokenList,'ID')
	else:
		Error(token[2],'TypeName',token[0])
def VarDec(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'VarDec','VarDec','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token[0]=='PROCEDURE' or token[0]=='BEGIN':
		node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'ε','ε','EPS',None))
		tree.addNodeNum()
	elif token[0]=='VAR':
		VarDeclaration(tree,node,tokenList)
	else:
		Error(token[2],'VarDec',token[0])
def VarDecList(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'VarDecList','VarDecList','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token[0]=='INTEGER' or token[0]=='RECORD' or token[0]=='ID' or token[0]=='CHAR' or token[0]=='ARRAY':
		TypeName(tree,node,tokenList)
		VarIdList(tree,node,tokenList)
		Match(tree,node,tokenList,';')
		VarDecMore(tree,node,tokenList)
	else:
		Error(token[2],'VarDecList',token[0])
def VarDecMore(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'VarDecMore','VarDecMore','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token[0]=='PROCEDURE' or token[0]=='BEGIN':
		node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'ε','ε','EPS',None))
		tree.addNodeNum()
	elif token[0]=='INTEGER' or token[0]=='RECORD' or token[0]=='ID' or token[0]=='CHAR' or token[0]=='ARRAY':
		VarDecList(tree,node,tokenList)
	else:
		Error(token[2],'VarDecMore',token[0])
def VarDeclaration(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'VarDeclaration','VarDeclaration','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token[0]=='VAR':
		Match(tree,node,tokenList,'VAR')
		VarDecList(tree,node,tokenList)
	else:
		Error(token[2],'VarDeclaration',token[0])
def VarIdList(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'VarIdList','VarIdList','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token[0]=='ID':
		Match(tree,node,tokenList,'ID')
		VarIdMore(tree,node,tokenList)
	else:
		Error(token[2],'VarIdList',token[0])
def VarIdMore(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'VarIdMore','VarIdMore','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token[0]==';':
		node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'ε','ε','EPS',None))
		tree.addNodeNum()
	elif token[0]==',':
		Match(tree,node,tokenList,',')
		VarIdList(tree,node,tokenList)
	else:
		Error(token[2],'VarIdMore',token[0])
def VariMore(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'VariMore','VariMore','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token[0]=='<' or token[0]=='ELSE' or token[0]==')' or token[0]=='ENDWH' or token[0]=='/' or token[0]==':=' or token[0]==']' or token[0]=='FI' or token[0]==';' or token[0]=='=' or token[0]=='END' or token[0]=='DO' or token[0]=='-' or token[0]=='*' or token[0]==',' or token[0]=='THEN' or token[0]=='+':
		node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'ε','ε','EPS',None))
		tree.addNodeNum()
	elif token[0]=='[':
		Match(tree,node,tokenList,'[')
		Exp(tree,node,tokenList)
		Match(tree,node,tokenList,']')
	elif token[0]=='.':
		Match(tree,node,tokenList,'.')
		FieldVar(tree,node,tokenList)
	else:
		Error(token[2],'VariMore',token[0])
def Variable(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'Variable','Variable','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token[0]=='ID':
		Match(tree,node,tokenList,'ID')
		VariMore(tree,node,tokenList)
	else:
		Error(token[2],'Variable',token[0])





def Program(tokenList:TokenProcessing)->GrammarTree:
	tree=GrammarTree(GrammarNode(None,None,0,-1,'Program','Program','VN',None))
	node:GrammarNode=tree.getRoot()
	token=tokenList.getNowToken()
	if token[0]=='PROGRAM':
		ProgramHead(tree,node,tokenList)
		DeclarePart(tree,node,tokenList)
		ProgramBody(tree,node,tokenList)
		Match(tree,node,tokenList,'.')
	else:
		Error(token[2],'Program',token[0])
	try:
		if not tokenList.isEnd():
			raise RecursionError(tokenList.getNowToken()[2])
	except RecursionError as e:
		print(e)
		os._exit(0)
	return tree

def Match(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing,symbol:str)->None:
	token=tokenList.getNowToken()
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),token[2],token[0],token[1],'VT',None))
	tree.addNodeNum()
	tokenList.next()
def Error(lineNo:int,should:str,get:str):
	try:
		raise TypeError(lineNo,should,get)
	except TypeError as e:
		print(e)
		os._exit(0)

def dfs(now:GrammarNode,cnt:int)->int:
    cnt=cnt+1
    if now.getChildNum()==0:print(now.getNodeVal())
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

    # 生成 tokens 以及 ast
    token=TokenProcessing(model='list', tokenList=tokenList)
    # token=TokenProcessing('list', 'out.txt')
    tree=Program(token)
    tree.goRoot()
    visualization(grammar,tree)
    # log(tree.getRoot())

    return tree

if __name__=='__main__':
	token=TokenProcessing('read','LL1token.txt')
	tree=Program(token)
	tree.goRoot()
	cnt=dfs(tree.getNow(),0)
	print(cnt)

