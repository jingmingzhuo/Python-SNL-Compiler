from grammar.GrammarTree import GrammarTree
from graphviz import Digraph
def visualization(config,grammar:dict,tree:GrammarTree)->None:
    visual=Digraph(name='GrammarTree',comment='GrammarTree',format='png')
    generator=tree.nextNode()
    flag=True
    while flag:
        color=config.GRAMMAR.VISUAL_VN_COLOR
        name='node'+str(tree.getNow().getNodeID())
        if tree.getNow().getNodeKind() in grammar['VT']:
            color=config.GRAMMAR.VISUAL_VT_COLOR
        if tree.getNow().getNodeKind()=='ε':
            color=config.GRAMMAR.VISUAL_EPS_COLOR
        label=tree.getNow().getNodeVal()
        visual.node(name=name,label=label,color=color)
        for item in range(tree.getNow().getChildNum()):
            sonName='node'+str(tree.getNow().getChild(item).getNodeID())
            visual.edge(name,sonName)
        flag=next(generator)
    visualAddress=config.GRAMMAR.VISUAL_ADDRESS
    visual.render(visualAddress,view=True)