from grammar.TokenProcessing import TokenProcessing
from grammar.GrammarTree import GrammarNode, GrammarTree
from grammar.Visualization import visualization
from grammar.getGrammar import getGrammar
def ActParamList(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()[0]
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'ActParamList','ActParamList','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token==')':
		node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'ε','ε','EPS',None))
		tree.addNodeNum()
	elif token=='(' or token=='INTC' or token=='ID':
		Exp(tree,node,tokenList)
		ActParamMore(tree,node,tokenList)
	else:
		Error()
def ActParamMore(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()[0]
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'ActParamMore','ActParamMore','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token==')':
		node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'ε','ε','EPS',None))
		tree.addNodeNum()
	elif token==',':
		Match(tree,node,tokenList,',')
		ActParamList(tree,node,tokenList)
	else:
		Error()
def AddOp(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()[0]
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'AddOp','AddOp','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token=='+':
		Match(tree,node,tokenList,'+')
	elif token=='-':
		Match(tree,node,tokenList,'-')
	else:
		Error()
def ArrayType(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()[0]
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'ArrayType','ArrayType','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token=='ARRAY':
		Match(tree,node,tokenList,'ARRAY')
		Match(tree,node,tokenList,'[')
		Low(tree,node,tokenList)
		Match(tree,node,tokenList,'..')
		Top(tree,node,tokenList)
		Match(tree,node,tokenList,']')
		Match(tree,node,tokenList,'OF')
		BaseType(tree,node,tokenList)
	else:
		Error()
def AssCall(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()[0]
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'AssCall','AssCall','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token==':=' or token=='.' or token=='[':
		AssignmentRest(tree,node,tokenList)
	elif token=='(':
		CallStmRest(tree,node,tokenList)
	else:
		Error()
def AssignmentRest(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()[0]
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'AssignmentRest','AssignmentRest','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token==':=' or token=='.' or token=='[':
		VariMore(tree,node,tokenList)
		Match(tree,node,tokenList,':=')
		Exp(tree,node,tokenList)
	else:
		Error()
def BaseType(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()[0]
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'BaseType','BaseType','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token=='INTEGER':
		Match(tree,node,tokenList,'INTEGER')
	elif token=='CHAR':
		Match(tree,node,tokenList,'CHAR')
	else:
		Error()
def CallStmRest(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()[0]
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'CallStmRest','CallStmRest','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token=='(':
		Match(tree,node,tokenList,'(')
		ActParamList(tree,node,tokenList)
		Match(tree,node,tokenList,')')
	else:
		Error()
def CmpOp(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()[0]
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'CmpOp','CmpOp','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token=='<':
		Match(tree,node,tokenList,'<')
	elif token=='=':
		Match(tree,node,tokenList,'=')
	else:
		Error()
def ConditionalStm(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()[0]
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'ConditionalStm','ConditionalStm','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token=='IF':
		Match(tree,node,tokenList,'IF')
		RelExp(tree,node,tokenList)
		Match(tree,node,tokenList,'THEN')
		StmList(tree,node,tokenList)
		Match(tree,node,tokenList,'ELSE')
		StmList(tree,node,tokenList)
		Match(tree,node,tokenList,'FI')
	else:
		Error()
def DeclarePart(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()[0]
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'DeclarePart','DeclarePart','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token=='VAR' or token=='TYPE' or token=='PROCEDURE' or token=='BEGIN':
		TypeDec(tree,node,tokenList)
		VarDec(tree,node,tokenList)
		ProcDec(tree,node,tokenList)
	else:
		Error()
def Exp(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()[0]
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'Exp','Exp','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token=='(' or token=='INTC' or token=='ID':
		Term(tree,node,tokenList)
		OtherTerm(tree,node,tokenList)
	else:
		Error()
def Factor(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()[0]
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'Factor','Factor','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token=='(':
		Match(tree,node,tokenList,'(')
		Exp(tree,node,tokenList)
		Match(tree,node,tokenList,')')
	elif token=='INTC':
		Match(tree,node,tokenList,'INTC')
	elif token=='ID':
		Variable(tree,node,tokenList)
	else:
		Error()
def FidMore(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()[0]
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'FidMore','FidMore','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token==';' or token==')':
		node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'ε','ε','EPS',None))
		tree.addNodeNum()
	elif token==',':
		Match(tree,node,tokenList,',')
		FormList(tree,node,tokenList)
	else:
		Error()
def FieldDecList(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()[0]
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'FieldDecList','FieldDecList','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token=='INTEGER' or token=='CHAR':
		BaseType(tree,node,tokenList)
		IdList(tree,node,tokenList)
		Match(tree,node,tokenList,';')
		FieldDecMore(tree,node,tokenList)
	elif token=='ARRAY':
		ArrayType(tree,node,tokenList)
		IdList(tree,node,tokenList)
		Match(tree,node,tokenList,';')
		FieldDecMore(tree,node,tokenList)
	else:
		Error()
def FieldDecMore(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()[0]
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'FieldDecMore','FieldDecMore','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token=='END':
		node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'ε','ε','EPS',None))
		tree.addNodeNum()
	elif token=='ARRAY' or token=='INTEGER' or token=='CHAR':
		FieldDecList(tree,node,tokenList)
	else:
		Error()
def FieldVar(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()[0]
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'FieldVar','FieldVar','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token=='ID':
		Match(tree,node,tokenList,'ID')
		FieldVarMore(tree,node,tokenList)
	else:
		Error()
def FieldVarMore(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()[0]
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'FieldVarMore','FieldVarMore','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token==':=' or token=='+' or token=='-' or token=='=' or token=='ELSE' or token=='ENDWH' or token=='<' or token==';' or token=='FI' or token==',' or token=='THEN' or token=='*' or token==']' or token=='/' or token==')' or token=='END' or token=='DO':
		node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'ε','ε','EPS',None))
		tree.addNodeNum()
	elif token=='[':
		Match(tree,node,tokenList,'[')
		Exp(tree,node,tokenList)
		Match(tree,node,tokenList,']')
	else:
		Error()
def FormList(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()[0]
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'FormList','FormList','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token=='ID':
		Match(tree,node,tokenList,'ID')
		FidMore(tree,node,tokenList)
	else:
		Error()
def IdList(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()[0]
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'IdList','IdList','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token=='ID':
		Match(tree,node,tokenList,'ID')
		IdMore(tree,node,tokenList)
	else:
		Error()
def IdMore(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()[0]
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'IdMore','IdMore','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token==';':
		node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'ε','ε','EPS',None))
		tree.addNodeNum()
	elif token==',':
		Match(tree,node,tokenList,',')
		IdList(tree,node,tokenList)
	else:
		Error()
def InputStm(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()[0]
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'InputStm','InputStm','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token=='READ':
		Match(tree,node,tokenList,'READ')
		Match(tree,node,tokenList,'(')
		Invar(tree,node,tokenList)
		Match(tree,node,tokenList,')')
	else:
		Error()
def Invar(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()[0]
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'Invar','Invar','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token=='ID':
		Match(tree,node,tokenList,'ID')
	else:
		Error()
def LoopStm(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()[0]
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'LoopStm','LoopStm','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token=='WHILE':
		Match(tree,node,tokenList,'WHILE')
		RelExp(tree,node,tokenList)
		Match(tree,node,tokenList,'DO')
		StmList(tree,node,tokenList)
		Match(tree,node,tokenList,'ENDWH')
	else:
		Error()
def Low(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()[0]
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'Low','Low','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token=='INTC':
		Match(tree,node,tokenList,'INTC')
	else:
		Error()
def MultOp(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()[0]
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'MultOp','MultOp','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token=='*':
		Match(tree,node,tokenList,'*')
	elif token=='/':
		Match(tree,node,tokenList,'/')
	else:
		Error()
def OtherFactor(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()[0]
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'OtherFactor','OtherFactor','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token=='+' or token=='-' or token=='=' or token=='ELSE' or token=='ENDWH' or token=='<' or token==';' or token=='FI' or token==',' or token=='THEN' or token==']' or token==')' or token=='END' or token=='DO':
		node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'ε','ε','EPS',None))
		tree.addNodeNum()
	elif token=='*' or token=='/':
		MultOp(tree,node,tokenList)
		Term(tree,node,tokenList)
	else:
		Error()
def OtherRelE(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()[0]
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'OtherRelE','OtherRelE','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token=='=' or token=='<':
		CmpOp(tree,node,tokenList)
		Exp(tree,node,tokenList)
	else:
		Error()
def OtherTerm(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()[0]
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'OtherTerm','OtherTerm','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token=='=' or token=='ELSE' or token=='ENDWH' or token=='<' or token==';' or token=='FI' or token==',' or token=='THEN' or token==']' or token==')' or token=='END' or token=='DO':
		node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'ε','ε','EPS',None))
		tree.addNodeNum()
	elif token=='+' or token=='-':
		AddOp(tree,node,tokenList)
		Exp(tree,node,tokenList)
	else:
		Error()
def OutputStm(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()[0]
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'OutputStm','OutputStm','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token=='WRITE':
		Match(tree,node,tokenList,'WRITE')
		Match(tree,node,tokenList,'(')
		Exp(tree,node,tokenList)
		Match(tree,node,tokenList,')')
	else:
		Error()
def Param(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()[0]
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'Param','Param','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token=='ARRAY' or token=='RECORD' or token=='INTEGER' or token=='ID' or token=='CHAR':
		TypeName(tree,node,tokenList)
		FormList(tree,node,tokenList)
	elif token=='VAR':
		Match(tree,node,tokenList,'VAR')
		TypeName(tree,node,tokenList)
		FormList(tree,node,tokenList)
	else:
		Error()
def ParamDecList(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()[0]
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'ParamDecList','ParamDecList','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token=='VAR' or token=='ARRAY' or token=='RECORD' or token=='INTEGER' or token=='ID' or token=='CHAR':
		Param(tree,node,tokenList)
		ParamMore(tree,node,tokenList)
	else:
		Error()
def ParamList(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()[0]
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'ParamList','ParamList','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token==')':
		node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'ε','ε','EPS',None))
		tree.addNodeNum()
	elif token=='VAR' or token=='ARRAY' or token=='RECORD' or token=='INTEGER' or token=='ID' or token=='CHAR':
		ParamDecList(tree,node,tokenList)
	else:
		Error()
def ParamMore(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()[0]
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'ParamMore','ParamMore','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token==')':
		node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'ε','ε','EPS',None))
		tree.addNodeNum()
	elif token==';':
		Match(tree,node,tokenList,';')
		ParamDecList(tree,node,tokenList)
	else:
		Error()
def ProcBody(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()[0]
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'ProcBody','ProcBody','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token=='BEGIN':
		ProgramBody(tree,node,tokenList)
	else:
		Error()
def ProcDec(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()[0]
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'ProcDec','ProcDec','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token=='BEGIN':
		node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'ε','ε','EPS',None))
		tree.addNodeNum()
	elif token=='PROCEDURE':
		ProcDeclaration(tree,node,tokenList)
	else:
		Error()
def ProcDecMore(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()[0]
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'ProcDecMore','ProcDecMore','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token=='BEGIN':
		node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'ε','ε','EPS',None))
		tree.addNodeNum()
	elif token=='PROCEDURE':
		ProcDeclaration(tree,node,tokenList)
	else:
		Error()
def ProcDecPart(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()[0]
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'ProcDecPart','ProcDecPart','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token=='VAR' or token=='TYPE' or token=='PROCEDURE' or token=='BEGIN':
		DeclarePart(tree,node,tokenList)
	else:
		Error()
def ProcDeclaration(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()[0]
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'ProcDeclaration','ProcDeclaration','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token=='PROCEDURE':
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
		Error()
def ProcName(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()[0]
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'ProcName','ProcName','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token=='ID':
		Match(tree,node,tokenList,'ID')
	else:
		Error()
def ProgramBody(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()[0]
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'ProgramBody','ProgramBody','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token=='BEGIN':
		Match(tree,node,tokenList,'BEGIN')
		StmList(tree,node,tokenList)
		Match(tree,node,tokenList,'END')
	else:
		Error()
def ProgramHead(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()[0]
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'ProgramHead','ProgramHead','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token=='PROGRAM':
		Match(tree,node,tokenList,'PROGRAM')
		ProgramName(tree,node,tokenList)
	else:
		Error()
def ProgramName(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()[0]
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'ProgramName','ProgramName','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token=='ID':
		Match(tree,node,tokenList,'ID')
	else:
		Error()
def RecType(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()[0]
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'RecType','RecType','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token=='RECORD':
		Match(tree,node,tokenList,'RECORD')
		FieldDecList(tree,node,tokenList)
		Match(tree,node,tokenList,'END')
	else:
		Error()
def RelExp(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()[0]
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'RelExp','RelExp','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token=='(' or token=='INTC' or token=='ID':
		Exp(tree,node,tokenList)
		OtherRelE(tree,node,tokenList)
	else:
		Error()
def ReturnStm(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()[0]
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'ReturnStm','ReturnStm','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token=='RETURN':
		Match(tree,node,tokenList,'RETURN')
		Match(tree,node,tokenList,'(')
		Exp(tree,node,tokenList)
		Match(tree,node,tokenList,')')
	else:
		Error()
def Stm(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()[0]
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'Stm','Stm','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token=='IF':
		ConditionalStm(tree,node,tokenList)
	elif token=='WHILE':
		LoopStm(tree,node,tokenList)
	elif token=='READ':
		InputStm(tree,node,tokenList)
	elif token=='WRITE':
		OutputStm(tree,node,tokenList)
	elif token=='RETURN':
		ReturnStm(tree,node,tokenList)
	elif token=='ID':
		Match(tree,node,tokenList,'ID')
		AssCall(tree,node,tokenList)
	else:
		Error()
def StmList(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()[0]
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'StmList','StmList','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token=='READ' or token=='RETURN' or token=='IF' or token=='ID' or token=='WRITE' or token=='WHILE':
		Stm(tree,node,tokenList)
		StmMore(tree,node,tokenList)
	else:
		Error()
def StmMore(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()[0]
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'StmMore','StmMore','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token=='FI' or token=='ELSE' or token=='ENDWH' or token=='END':
		node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'ε','ε','EPS',None))
		tree.addNodeNum()
	elif token==';':
		Match(tree,node,tokenList,';')
		StmList(tree,node,tokenList)
	else:
		Error()
def StructureType(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()[0]
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'StructureType','StructureType','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token=='ARRAY':
		ArrayType(tree,node,tokenList)
	elif token=='RECORD':
		RecType(tree,node,tokenList)
	else:
		Error()
def Term(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()[0]
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'Term','Term','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token=='(' or token=='INTC' or token=='ID':
		Factor(tree,node,tokenList)
		OtherFactor(tree,node,tokenList)
	else:
		Error()
def Top(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()[0]
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'Top','Top','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token=='INTC':
		Match(tree,node,tokenList,'INTC')
	else:
		Error()
def TypeDec(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()[0]
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'TypeDec','TypeDec','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token=='VAR' or token=='PROCEDURE' or token=='BEGIN':
		node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'ε','ε','EPS',None))
		tree.addNodeNum()
	elif token=='TYPE':
		TypeDeclaration(tree,node,tokenList)
	else:
		Error()
def TypeDecList(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()[0]
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'TypeDecList','TypeDecList','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token=='ID':
		TypeId(tree,node,tokenList)
		Match(tree,node,tokenList,'=')
		TypeName(tree,node,tokenList)
		Match(tree,node,tokenList,';')
		TypeDecMore(tree,node,tokenList)
	else:
		Error()
def TypeDecMore(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()[0]
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'TypeDecMore','TypeDecMore','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token=='VAR' or token=='PROCEDURE' or token=='BEGIN':
		node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'ε','ε','EPS',None))
		tree.addNodeNum()
	elif token=='ID':
		TypeDecList(tree,node,tokenList)
	else:
		Error()
def TypeDeclaration(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()[0]
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'TypeDeclaration','TypeDeclaration','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token=='TYPE':
		Match(tree,node,tokenList,'TYPE')
		TypeDecList(tree,node,tokenList)
	else:
		Error()
def TypeId(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()[0]
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'TypeId','TypeId','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token=='ID':
		Match(tree,node,tokenList,'ID')
	else:
		Error()
def TypeName(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()[0]
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'TypeName','TypeName','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token=='INTEGER' or token=='CHAR':
		BaseType(tree,node,tokenList)
	elif token=='ARRAY' or token=='RECORD':
		StructureType(tree,node,tokenList)
	elif token=='ID':
		Match(tree,node,tokenList,'ID')
	else:
		Error()
def VarDec(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()[0]
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'VarDec','VarDec','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token=='PROCEDURE' or token=='BEGIN':
		node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'ε','ε','EPS',None))
		tree.addNodeNum()
	elif token=='VAR':
		VarDeclaration(tree,node,tokenList)
	else:
		Error()
def VarDecList(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()[0]
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'VarDecList','VarDecList','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token=='ARRAY' or token=='RECORD' or token=='INTEGER' or token=='ID' or token=='CHAR':
		TypeName(tree,node,tokenList)
		VarIdList(tree,node,tokenList)
		Match(tree,node,tokenList,';')
		VarDecMore(tree,node,tokenList)
	else:
		Error()
def VarDecMore(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()[0]
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'VarDecMore','VarDecMore','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token=='PROCEDURE' or token=='BEGIN':
		node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'ε','ε','EPS',None))
		tree.addNodeNum()
	elif token=='ARRAY' or token=='RECORD' or token=='INTEGER' or token=='ID' or token=='CHAR':
		VarDecList(tree,node,tokenList)
	else:
		Error()
def VarDeclaration(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()[0]
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'VarDeclaration','VarDeclaration','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token=='VAR':
		Match(tree,node,tokenList,'VAR')
		VarDecList(tree,node,tokenList)
	else:
		Error()
def VarIdList(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()[0]
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'VarIdList','VarIdList','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token=='ID':
		Match(tree,node,tokenList,'ID')
		VarIdMore(tree,node,tokenList)
	else:
		Error()
def VarIdMore(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()[0]
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'VarIdMore','VarIdMore','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token==';':
		node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'ε','ε','EPS',None))
		tree.addNodeNum()
	elif token==',':
		Match(tree,node,tokenList,',')
		VarIdList(tree,node,tokenList)
	else:
		Error()
def VariMore(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()[0]
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'VariMore','VariMore','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token==':=' or token=='+' or token=='-' or token=='=' or token=='ELSE' or token=='ENDWH' or token=='<' or token==';' or token=='FI' or token==',' or token=='THEN' or token=='*' or token==']' or token=='/' or token==')' or token=='END' or token=='DO':
		node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'ε','ε','EPS',None))
		tree.addNodeNum()
	elif token=='[':
		Match(tree,node,tokenList,'[')
		Exp(tree,node,tokenList)
		Match(tree,node,tokenList,']')
	elif token=='.':
		Match(tree,node,tokenList,'.')
		FieldVar(tree,node,tokenList)
	else:
		Error()
def Variable(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing)->None:
	token=tokenList.getNowToken()[0]
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),-1,'Variable','Variable','VN',None))
	tree.addNodeNum()
	node=node.getChild(node.getChildNum()-1)
	if token=='ID':
		Match(tree,node,tokenList,'ID')
		VariMore(tree,node,tokenList)
	else:
		Error()




def Program(tokenList:TokenProcessing)->GrammarTree:
	tree=GrammarTree(GrammarNode(None,None,0,-1,'Program','Program','VN',None))
	node:GrammarNode=tree.getRoot()
	token=tokenList.getNowToken()[0]
	if token=='PROGRAM':
		ProgramHead(tree,node,tokenList)
		DeclarePart(tree,node,tokenList)
		ProgramBody(tree,node,tokenList)
		Match(tree,node,tokenList,'.')
	else:
		Error()
	return tree
def Match(tree:GrammarTree,node:GrammarNode,tokenList:TokenProcessing,symbol:str)->None:
	token=tokenList.getNowToken()
	node.addChild(GrammarNode(node,None,tree.getNodeNum(),token[2],token[0],token[1],'VT',None))
	tree.addNodeNum()
	tokenList.next()
def Error():
	pass
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
    print(token.getNowToken())
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

