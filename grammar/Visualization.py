from grammar.GrammarTree import GrammarTree
from graphviz import Digraph
def visualization(grammar:dict,tree:GrammarTree)->None:
    visual=Digraph(name='GrammarTree',comment='GrammarTree',format='png')
    generator=tree.nextNode()
    flag=True
    while flag:
        color='black'
        name='node'+str(tree.getNow().getNodeID())
        if tree.getNow().getNodeKind() in grammar['VT']:
            color='red'
        if tree.getNow().getNodeKind()=='ε':
            color='yellow'
        label=tree.getNow().getNodeVal()
        visual.node(name=name,label=label,color=color)
        for item in range(tree.getNow().getChildNum()):
            sonName='node'+str(tree.getNow().getChild(item).getNodeID())
            visual.edge(name,sonName)
        flag=next(generator)
    visual.render('grammar/GrammarTree',view=True)