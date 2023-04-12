from graphviz import Digraph

def display_tree(nodes : list, edges : list):
  dot = Digraph()
  dot.engine = 'dot' # Set layout engine to 'dot'
  for node in nodes:
    dot.node(node)
  for edge in edges:
    dot.edge(edge[0], edge[1])
  dot.view()