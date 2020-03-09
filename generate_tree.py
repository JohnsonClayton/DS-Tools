from graphviz import Digraph

class Node():
  def __init__(self, name, idd):
    self._name = name
    self._id = idd

  def __str__(self):
    return str(self._name) #+ str(self._id)

  def getID(self):
    return str(self._id)

  def getName(self):
    return self._name

class Connection():
  def __init__(self, origin, target, label):
    self._origin = origin
    self._target = target
    self._label = label

  def __str__(self):
    return str(self._origin) + ' -> ' + str(self._target) + ' (' + str(self._label) + ')'

  def getConn(self):
    return [ self._origin, self._target, self._label ]

  def getTarget(self):
    return self._target

  def getOrigin(self):
    return self._origin

  def getLabel(self):
    return str(self._label)


class Tree():
  def __init__(self):
    self._conns = []
    self._nodes = []
    self._root = None
    self._current_parent = None
    self._last_added = None
    self._depth = 0
    self._node_count = 0
    self._parent_stack = []
    self._label_stack = []

  def __str__(self):
    # Print the tree's connections
    out = ''
    for conn in self._conns:
      out += str(conn) + '\n'
    return out 

  def shouldMerge(self, parent, parent_label, name):
    ret = None
    for conn in self._conns:
      target = conn.getTarget()
      if target.getName() == name and conn.getLabel() == parent_label:
        ret = target
    return ret

  def addLine(self, line):
    #print('Stack: ')
    #for node in self._parent_stack:
    #  print(node)
    #print('-------------')

    # Convert line to an array with no empty strings
    line_arr = line.split(' ')
    line_arr[:] = [val for val in line_arr if val != ''] 
   
    # Get current depth
    cdepth = line_arr.count('|')

    # We know these will be in the same place every time
    name = line_arr[cdepth]
    val = ''
    if line_arr[cdepth + 2][-1] == ':':
      val = line_arr[cdepth + 2][:-1]
    else:
      val = line_arr[cdepth + 2]

    # This will let us figure out if we are at a leaf node or not
    leaf = None
    if line_arr[-1] == 'recurrence-events' or line_arr[-1] == 'no-recurrence-events':
      #print('leaf!')
      leaf = line_arr[-1]
    elif line_arr[-1] == 'null':
      return

    # Switch changes to the tree based on whether we are dealing with a branch or a leaf
    if leaf:
      # This line is a leaf, which means we create more nodes
      #   Ex: `|  tumor-size = 0-4: no-recurrence-events`
      print('Leaf!')

      # Create no-recurrence-events node
      new_leaf = Node(leaf, len(self._nodes))
      self._nodes.append(new_leaf)

      # Create conn from parent with parent label -> tumor-size
      # Get the parent information
      plabel = self._label_stack[-1]
      prnt  = self._parent_stack[-1]

      # If the parent points to another node with the same name as this one (tumor-size) and the same value (0-4), then don't create a new node or connection
      new_branch = self.shouldMerge(prnt, plabel, name)
      if not new_branch:
        # Create tumor-size node
        new_branch = Node(name, len(self._nodes))
        self._nodes.append(new_branch) # Adds the new node to the list of nodes

        # Create the connection
        conn = Connection(prnt, new_branch, plabel)
        self._conns.append(conn)


      # Create conn from tumor-size with tumor-size label (0-4) -> no-recurrence-events
      conn = Connection(new_branch, new_leaf, val)
      self._conns.append(conn)

    else:
      # This line is a branch, which requires more work for the stack
      #   Ex: `|  tumor-size = 15-19`
      print('Branch!')

      # Create tumor-size node
      new_branch = Node(name, len(self._nodes))
      self._nodes.append(new_branch)

      # Append the tumor-size node to the parent_stack
      self._parent_stack.append(new_branch)

      # Append the tumor-size label (15-19) to the label_stack
      self._label_stack.append(val)


  # Creates a Graphviz DiGraph object and returns to the caller
  def createGraph(self):
    # Graph object
    graph = Digraph(comment='ID3 Tree on breast-cancer.arff')
    
    for node in self._nodes:
      print('Adding node {}'.format(node))
      graph.node(node.getID(), node.getName())

    for conn in self._conns:
      print('Addding conn {}'.format(conn))
      graph.edge( (conn.getOrigin()).getID(), (conn.getTarget()).getID(), label=conn.getLabel() )

    return graph
    

def create_tree():
  # Create tree object
  tree = Tree() 
  arr = ascii_tree.splitlines() 

  counter = 0
  for line in arr:
    #print('-------------------------------------------------------------------')
    tree.addLine(line)
    #print(tree)
    if counter > 20:
      break
    counter += 1

  print(tree)

  graph = tree.createGraph()

  return graph

def main():
  tree = create_tree()

  tree.render('test-output.gv', format='png', view=True)

# ASCII Decision Tree retrieved from WEKA
ascii_tree = """deg-malig = 1
|  tumor-size = 0-4: no-recurrence-events
|  tumor-size = 5-9: no-recurrence-events
|  tumor-size = 10-14: no-recurrence-events
|  tumor-size = 15-19
|  |  age = 10-19: null
|  |  age = 20-29: null
|  |  age = 30-39
|  |  |  breast = left: no-recurrence-events
|  |  |  breast = right: recurrence-events
|  |  age = 40-49: null
|  |  age = 50-59: no-recurrence-events
|  |  age = 60-69: no-recurrence-events
|  |  age = 70-79: null
|  |  age = 80-89: null
|  |  age = 90-99: null
|  tumor-size = 20-24
|  |  breast-quad = left_up: recurrence-events
|  |  breast-quad = left_low: no-recurrence-events
|  |  breast-quad = right_up: no-recurrence-events
|  |  breast-quad = right_low: no-recurrence-events
|  |  breast-quad = central: null
|  tumor-size = 25-29
|  |  breast-quad = left_up: no-recurrence-events
|  |  breast-quad = left_low: no-recurrence-events
|  |  breast-quad = right_up: null
|  |  breast-quad = right_low: no-recurrence-events
|  |  breast-quad = central: no-recurrence-events
|  tumor-size = 30-34
|  |  age = 10-19: null
|  |  age = 20-29: null
|  |  age = 30-39: recurrence-events
|  |  age = 40-49
|  |  |  irradiat = yes: recurrence-events
|  |  |  irradiat = no: no-recurrence-events
|  |  age = 50-59: no-recurrence-events
|  |  age = 60-69: no-recurrence-events
|  |  age = 70-79: null
|  |  age = 80-89: null
|  |  age = 90-99: null
|  tumor-size = 35-39
|  |  breast = left: no-recurrence-events
|  |  breast = right: recurrence-events
|  tumor-size = 40-44
|  |  breast = left: recurrence-events
|  |  breast = right: no-recurrence-events
|  tumor-size = 45-49: recurrence-events
|  tumor-size = 50-54: no-recurrence-events
|  tumor-size = 55-59: null
deg-malig = 2
|  tumor-size = 0-4
|  |  age = 10-19: null
|  |  age = 20-29: null
|  |  age = 30-39: no-recurrence-events
|  |  age = 40-49: no-recurrence-events
|  |  age = 50-59: no-recurrence-events
|  |  age = 60-69: null
|  |  age = 70-79: null
|  |  age = 80-89: null
|  |  age = 90-99: null
|  tumor-size = 5-9: no-recurrence-events
|  tumor-size = 10-14: no-recurrence-events
|  tumor-size = 15-19
|  |  menopause = lt40: no-recurrence-events
|  |  menopause = ge40: no-recurrence-events
|  |  menopause = premeno
|  |  |  breast = left
|  |  |  |  age = 10-19: null
|  |  |  |  age = 20-29: null
|  |  |  |  age = 30-39: null
|  |  |  |  age = 40-49
|  |  |  |  |  breast-quad = left_up: recurrence-events
|  |  |  |  |  breast-quad = left_low: no-recurrence-events
|  |  |  |  |  breast-quad = right_up: null
|  |  |  |  |  breast-quad = right_low: null
|  |  |  |  |  breast-quad = central: null
|  |  |  |  age = 50-59: recurrence-events
|  |  |  |  age = 60-69: null
|  |  |  |  age = 70-79: null
|  |  |  |  age = 80-89: null
|  |  |  |  age = 90-99: null
|  |  |  breast = right: no-recurrence-events
|  tumor-size = 20-24
|  |  breast-quad = left_up
|  |  |  menopause = lt40: null
|  |  |  menopause = ge40
|  |  |  |  age = 10-19: null
|  |  |  |  age = 20-29: null
|  |  |  |  age = 30-39: null
|  |  |  |  age = 40-49: recurrence-events
|  |  |  |  age = 50-59
|  |  |  |  |  breast = left: recurrence-events
|  |  |  |  |  breast = right: no-recurrence-events
|  |  |  |  age = 60-69: no-recurrence-events
|  |  |  |  age = 70-79: null
|  |  |  |  age = 80-89: null
|  |  |  |  age = 90-99: null
|  |  |  menopause = premeno: no-recurrence-events
|  |  breast-quad = left_low
|  |  |  age = 10-19: null
|  |  |  age = 20-29: null
|  |  |  age = 30-39: recurrence-events
|  |  |  age = 40-49
|  |  |  |  breast = left
|  |  |  |  |  inv-nodes = 0-2: no-recurrence-events
|  |  |  |  |  inv-nodes = 3-5: recurrence-events
|  |  |  |  |  inv-nodes = 6-8: null
|  |  |  |  |  inv-nodes = 9-11: null
|  |  |  |  |  inv-nodes = 12-14: null
|  |  |  |  |  inv-nodes = 15-17: null
|  |  |  |  |  inv-nodes = 18-20: null
|  |  |  |  |  inv-nodes = 21-23: null
|  |  |  |  |  inv-nodes = 24-26: null
|  |  |  |  |  inv-nodes = 27-29: null
|  |  |  |  |  inv-nodes = 30-32: null
|  |  |  |  |  inv-nodes = 33-35: null
|  |  |  |  |  inv-nodes = 36-39: null
|  |  |  |  breast = right: no-recurrence-events
|  |  |  age = 50-59: no-recurrence-events
|  |  |  age = 60-69: recurrence-events
|  |  |  age = 70-79: null
|  |  |  age = 80-89: null
|  |  |  age = 90-99: null
|  |  breast-quad = right_up
|  |  |  inv-nodes = 0-2: no-recurrence-events
|  |  |  inv-nodes = 3-5: recurrence-events
|  |  |  inv-nodes = 6-8: null
|  |  |  inv-nodes = 9-11: null
|  |  |  inv-nodes = 12-14: null
|  |  |  inv-nodes = 15-17: null
|  |  |  inv-nodes = 18-20: null
|  |  |  inv-nodes = 21-23: null
|  |  |  inv-nodes = 24-26: null
|  |  |  inv-nodes = 27-29: null
|  |  |  inv-nodes = 30-32: null
|  |  |  inv-nodes = 33-35: null
|  |  |  inv-nodes = 36-39: null
|  |  breast-quad = right_low: no-recurrence-events
|  |  breast-quad = central
|  |  |  age = 10-19: null
|  |  |  age = 20-29: null
|  |  |  age = 30-39: no-recurrence-events
|  |  |  age = 40-49: no-recurrence-events
|  |  |  age = 50-59: recurrence-events
|  |  |  age = 60-69: null
|  |  |  age = 70-79: null
|  |  |  age = 80-89: null
|  |  |  age = 90-99: null
|  tumor-size = 25-29
|  |  breast-quad = left_up: no-recurrence-events
|  |  breast-quad = left_low
|  |  |  age = 10-19: null
|  |  |  age = 20-29: null
|  |  |  age = 30-39: no-recurrence-events
|  |  |  age = 40-49
|  |  |  |  menopause = lt40: null
|  |  |  |  menopause = ge40: no-recurrence-events
|  |  |  |  menopause = premeno
|  |  |  |  |  breast = left: recurrence-events
|  |  |  |  |  breast = right: recurrence-events
|  |  |  age = 50-59: no-recurrence-events
|  |  |  age = 60-69: no-recurrence-events
|  |  |  age = 70-79: null
|  |  |  age = 80-89: null
|  |  |  age = 90-99: null
|  |  breast-quad = right_up: recurrence-events
|  |  breast-quad = right_low: no-recurrence-events
|  |  breast-quad = central: no-recurrence-events
|  tumor-size = 30-34
|  |  breast-quad = left_up
|  |  |  inv-nodes = 0-2
|  |  |  |  age = 10-19: null
|  |  |  |  age = 20-29: null
|  |  |  |  age = 30-39: no-recurrence-events
|  |  |  |  age = 40-49: no-recurrence-events
|  |  |  |  age = 50-59: null
|  |  |  |  age = 60-69: no-recurrence-events
|  |  |  |  age = 70-79: null
|  |  |  |  age = 80-89: null
|  |  |  |  age = 90-99: null
|  |  |  inv-nodes = 3-5: recurrence-events
|  |  |  inv-nodes = 6-8: no-recurrence-events
|  |  |  inv-nodes = 9-11: recurrence-events
|  |  |  inv-nodes = 12-14: null
|  |  |  inv-nodes = 15-17: null
|  |  |  inv-nodes = 18-20: null
|  |  |  inv-nodes = 21-23: null
|  |  |  inv-nodes = 24-26: null
|  |  |  inv-nodes = 27-29: null
|  |  |  inv-nodes = 30-32: null
|  |  |  inv-nodes = 33-35: null
|  |  |  inv-nodes = 36-39: null
|  |  breast-quad = left_low: no-recurrence-events
|  |  breast-quad = right_up
|  |  |  inv-nodes = 0-2
|  |  |  |  age = 10-19: null
|  |  |  |  age = 20-29: null
|  |  |  |  age = 30-39: null
|  |  |  |  age = 40-49: no-recurrence-events
|  |  |  |  age = 50-59: null
|  |  |  |  age = 60-69: recurrence-events
|  |  |  |  age = 70-79: null
|  |  |  |  age = 80-89: null
|  |  |  |  age = 90-99: null
|  |  |  inv-nodes = 3-5: recurrence-events
|  |  |  inv-nodes = 6-8: no-recurrence-events
|  |  |  inv-nodes = 9-11: null
|  |  |  inv-nodes = 12-14: null
|  |  |  inv-nodes = 15-17: null
|  |  |  inv-nodes = 18-20: null
|  |  |  inv-nodes = 21-23: null
|  |  |  inv-nodes = 24-26: null
|  |  |  inv-nodes = 27-29: null
|  |  |  inv-nodes = 30-32: null
|  |  |  inv-nodes = 33-35: null
|  |  |  inv-nodes = 36-39: null
|  |  breast-quad = right_low
|  |  |  age = 10-19: null
|  |  |  age = 20-29: null
|  |  |  age = 30-39: null
|  |  |  age = 40-49: no-recurrence-events
|  |  |  age = 50-59: recurrence-events
|  |  |  age = 60-69: null
|  |  |  age = 70-79: null
|  |  |  age = 80-89: null
|  |  |  age = 90-99: null
|  |  breast-quad = central: recurrence-events
|  tumor-size = 35-39
|  |  breast-quad = left_up: no-recurrence-events
|  |  breast-quad = left_low: recurrence-events
|  |  breast-quad = right_up: no-recurrence-events
|  |  breast-quad = right_low: null
|  |  breast-quad = central: null
|  tumor-size = 40-44
|  |  age = 10-19: null
|  |  age = 20-29: null
|  |  age = 30-39: no-recurrence-events
|  |  age = 40-49: no-recurrence-events
|  |  age = 50-59: no-recurrence-events
|  |  age = 60-69
|  |  |  inv-nodes = 0-2: recurrence-events
|  |  |  inv-nodes = 3-5: no-recurrence-events
|  |  |  inv-nodes = 6-8: null
|  |  |  inv-nodes = 9-11: null
|  |  |  inv-nodes = 12-14: null
|  |  |  inv-nodes = 15-17: null
|  |  |  inv-nodes = 18-20: null
|  |  |  inv-nodes = 21-23: null
|  |  |  inv-nodes = 24-26: null
|  |  |  inv-nodes = 27-29: null
|  |  |  inv-nodes = 30-32: null
|  |  |  inv-nodes = 33-35: null
|  |  |  inv-nodes = 36-39: null
|  |  age = 70-79: null
|  |  age = 80-89: null
|  |  age = 90-99: null
|  tumor-size = 45-49: no-recurrence-events
|  tumor-size = 50-54
|  |  inv-nodes = 0-2
|  |  |  age = 10-19: null
|  |  |  age = 20-29: null
|  |  |  age = 30-39: null
|  |  |  age = 40-49
|  |  |  |  breast = left: no-recurrence-events
|  |  |  |  breast = right: recurrence-events
|  |  |  age = 50-59: no-recurrence-events
|  |  |  age = 60-69: no-recurrence-events
|  |  |  age = 70-79: null
|  |  |  age = 80-89: null
|  |  |  age = 90-99: null
|  |  inv-nodes = 3-5: null
|  |  inv-nodes = 6-8: null
|  |  inv-nodes = 9-11: recurrence-events
|  |  inv-nodes = 12-14: null
|  |  inv-nodes = 15-17: null
|  |  inv-nodes = 18-20: null
|  |  inv-nodes = 21-23: null
|  |  inv-nodes = 24-26: null
|  |  inv-nodes = 27-29: null
|  |  inv-nodes = 30-32: null
|  |  inv-nodes = 33-35: null
|  |  inv-nodes = 36-39: null
|  tumor-size = 55-59: null
deg-malig = 3
|  inv-nodes = 0-2
|  |  tumor-size = 0-4: no-recurrence-events
|  |  tumor-size = 5-9: null
|  |  tumor-size = 10-14: no-recurrence-events
|  |  tumor-size = 15-19
|  |  |  age = 10-19: null
|  |  |  age = 20-29: null
|  |  |  age = 30-39: no-recurrence-events
|  |  |  age = 40-49: recurrence-events
|  |  |  age = 50-59: null
|  |  |  age = 60-69: no-recurrence-events
|  |  |  age = 70-79: null
|  |  |  age = 80-89: null
|  |  |  age = 90-99: null
|  |  tumor-size = 20-24
|  |  |  age = 10-19: null
|  |  |  age = 20-29: null
|  |  |  age = 30-39
|  |  |  |  breast-quad = left_up: recurrence-events
|  |  |  |  breast-quad = left_low: null
|  |  |  |  breast-quad = right_up: null
|  |  |  |  breast-quad = right_low: null
|  |  |  |  breast-quad = central: no-recurrence-events
|  |  |  age = 40-49: no-recurrence-events
|  |  |  age = 50-59: no-recurrence-events
|  |  |  age = 60-69: recurrence-events
|  |  |  age = 70-79: no-recurrence-events
|  |  |  age = 80-89: null
|  |  |  age = 90-99: null
|  |  tumor-size = 25-29
|  |  |  breast = left
|  |  |  |  age = 10-19: null
|  |  |  |  age = 20-29: null
|  |  |  |  age = 30-39: null
|  |  |  |  age = 40-49: recurrence-events
|  |  |  |  age = 50-59: no-recurrence-events
|  |  |  |  age = 60-69: recurrence-events
|  |  |  |  age = 70-79: null
|  |  |  |  age = 80-89: null
|  |  |  |  age = 90-99: null
|  |  |  breast = right
|  |  |  |  age = 10-19: null
|  |  |  |  age = 20-29: null
|  |  |  |  age = 30-39: null
|  |  |  |  age = 40-49: no-recurrence-events
|  |  |  |  age = 50-59: recurrence-events
|  |  |  |  age = 60-69: no-recurrence-events
|  |  |  |  age = 70-79: null
|  |  |  |  age = 80-89: null
|  |  |  |  age = 90-99: null
|  |  tumor-size = 30-34
|  |  |  breast-quad = left_up
|  |  |  |  irradiat = yes: recurrence-events
|  |  |  |  irradiat = no: no-recurrence-events
|  |  |  breast-quad = left_low: no-recurrence-events
|  |  |  breast-quad = right_up
|  |  |  |  age = 10-19: null
|  |  |  |  age = 20-29: null
|  |  |  |  age = 30-39: null
|  |  |  |  age = 40-49
|  |  |  |  |  node-caps = yes: recurrence-events
|  |  |  |  |  node-caps = no: no-recurrence-events
|  |  |  |  age = 50-59: recurrence-events
|  |  |  |  age = 60-69: null
|  |  |  |  age = 70-79: null
|  |  |  |  age = 80-89: null
|  |  |  |  age = 90-99: null
|  |  |  breast-quad = right_low: null
|  |  |  breast-quad = central: recurrence-events
|  |  tumor-size = 35-39
|  |  |  age = 10-19: null
|  |  |  age = 20-29: null
|  |  |  age = 30-39: recurrence-events
|  |  |  age = 40-49: no-recurrence-events
|  |  |  age = 50-59: no-recurrence-events
|  |  |  age = 60-69: null
|  |  |  age = 70-79: null
|  |  |  age = 80-89: null
|  |  |  age = 90-99: null
|  |  tumor-size = 40-44: no-recurrence-events
|  |  tumor-size = 45-49: null
|  |  tumor-size = 50-54: recurrence-events
|  |  tumor-size = 55-59: null
|  inv-nodes = 3-5
|  |  tumor-size = 0-4: null
|  |  tumor-size = 5-9: null
|  |  tumor-size = 10-14: null
|  |  tumor-size = 15-19: null
|  |  tumor-size = 20-24: recurrence-events
|  |  tumor-size = 25-29
|  |  |  menopause = lt40: null
|  |  |  menopause = ge40: no-recurrence-events
|  |  |  menopause = premeno: recurrence-events
|  |  tumor-size = 30-34
|  |  |  age = 10-19: null
|  |  |  age = 20-29: null
|  |  |  age = 30-39: recurrence-events
|  |  |  age = 40-49: recurrence-events
|  |  |  age = 50-59: recurrence-events
|  |  |  age = 60-69: no-recurrence-events
|  |  |  age = 70-79: null
|  |  |  age = 80-89: null
|  |  |  age = 90-99: null
|  |  tumor-size = 35-39: null
|  |  tumor-size = 40-44
|  |  |  age = 10-19: null
|  |  |  age = 20-29: null
|  |  |  age = 30-39: no-recurrence-events
|  |  |  age = 40-49: no-recurrence-events
|  |  |  age = 50-59: null
|  |  |  age = 60-69: recurrence-events
|  |  |  age = 70-79: null
|  |  |  age = 80-89: null
|  |  |  age = 90-99: null
|  |  tumor-size = 45-49: null
|  |  tumor-size = 50-54: null
|  |  tumor-size = 55-59: null
|  inv-nodes = 6-8
|  |  tumor-size = 0-4: null
|  |  tumor-size = 5-9: null
|  |  tumor-size = 10-14: recurrence-events
|  |  tumor-size = 15-19: recurrence-events
|  |  tumor-size = 20-24: null
|  |  tumor-size = 25-29: recurrence-events
|  |  tumor-size = 30-34: recurrence-events
|  |  tumor-size = 35-39: recurrence-events
|  |  tumor-size = 40-44: recurrence-events
|  |  tumor-size = 45-49: no-recurrence-events
|  |  tumor-size = 50-54: null
|  |  tumor-size = 55-59: null
|  inv-nodes = 9-11: recurrence-events
|  inv-nodes = 12-14
|  |  tumor-size = 0-4: null
|  |  tumor-size = 5-9: null
|  |  tumor-size = 10-14: null
|  |  tumor-size = 15-19: no-recurrence-events
|  |  tumor-size = 20-24: null
|  |  tumor-size = 25-29: recurrence-events
|  |  tumor-size = 30-34: recurrence-events
|  |  tumor-size = 35-39: null
|  |  tumor-size = 40-44: null
|  |  tumor-size = 45-49: null
|  |  tumor-size = 50-54: null
|  |  tumor-size = 55-59: null
|  inv-nodes = 15-17
|  |  menopause = lt40: null
|  |  menopause = ge40: no-recurrence-events
|  |  menopause = premeno: recurrence-events
|  inv-nodes = 18-20: null
|  inv-nodes = 21-23: null
|  inv-nodes = 24-26: recurrence-events
|  inv-nodes = 27-29: null
|  inv-nodes = 30-32: null
|  inv-nodes = 33-35: null
|  inv-nodes = 36-39: null
"""

main()
