#use graphviz to draw data structure
def draw_database_structure(root):
    g = Digraph(name='database_structure')
    g.node(name='d',label= root.name,color='red')
    g.node(name='t1',label = root.children[0].name)
    g.node(name='t2',label = root.children[1].name)
    g.edge('d','t1')
    g.edge('d','t2')
    for attribute in root.children[0].children:
        #g.node(name='att'+str(index),label = attribute,color='blue')
        g.edge('t1',attribute)

    for atribute in root.children[1].children:
        #g.node(name='att',label = atribute,color='blue')
        g.edge('t2',atribute)  
    g.view()