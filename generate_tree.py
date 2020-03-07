from graphviz import Digraph

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

def create_tree():
  """graph = Digraph(comment='The Round Table')
  graph.node('A', 'King Arthur')
  graph.node('B', 'Sir who the fukc')
  graph.node('C', 'test 3')

  #graph.edges(['AB', 'AL'])
  graph.edge('A', 'B', label='test label!')
  graph.edge('A', 'L', label='test label 2!')
  graph.edge('B', 'L', constraint='false')
  
  print(graph.source)"""

  # Graph object
  graph = Digraph(comment='ID3 Tree on breast-cancer.arff')

  # Loop over the given tree and dynamically add the nodes to the tree
  arr = ascii_tree.splitlines() 
  depth = 0

  # The first line contains our root element
  first_line_arr = arr.pop(0).split(' ')  
  graph.node(first_line_arr[0], first_line_arr[0])

  # Keep track of current parent node
  parent1 = first_line_arr[0]
  label1 = first_line_arr[-1]
  parent_stack = [parent1]
  label_stack = [label1]

  #print('parent: {}'.format(parent))
  #print('first line arr: {}'.format(first_line_arr))

  counter = 0

  for line in arr:
    line_arr = line.split(' ')
    #line_arr.remove('')
    line_arr[:] = [val for val in line_arr if val != '']
    # Don't do this next step is we point to null
    if line_arr[-1] != 'null':

      # Figure out how deep we are into the tree
      new_depth = line.count('|')
      if new_depth > depth:
        # Add new connection from parent to current
        name = line_arr[depth + 1]
        print(line_arr)
        graph.node(name, name)
        graph.edge(parent_stack[-1], name, label=label_stack[-1])

        if line_arr[-1] == 'recurrence-events' or line_arr[-1] == 'no-recurrence-events':
          # Create connection from current node to classification
          classif = line_arr[-1]
          graph.node(classif + str(counter), classif)
          graph.edge(name, classif + str(counter), label=line_arr[depth + 3][:-1])
          counter += 1
        else:
          ## Push current info onto the stack
          label = line_arr[-1] #[:-1]
          label_stack.append(label)

        parent_stack.append(name)
        #print(parent_stack)
        #print(label_stack)

        depth = new_depth
        
      elif new_depth < depth:
        # Add a new node to the graph
        break

      else:
        if line_arr[-1] == 'recurrence-events' or line_arr[-1] == 'no-recurrence-events':
          # Create connection from current node to classification
          classif = line_arr[-1]
          graph.node(classif + str(counter), classif)
          graph.edge(name, classif + str(counter), label=line_arr[depth + 2][:-1])
          counter += 1
        else:
          ## Push current info onto the stack
          label = line_arr[-1]
          label_stack.append(label)

        """
        # We are on the same depth  
        name = line_arr[depth + 1]
        print(line_arr)
        graph.node(name, name)
        graph.edge(parent_stack[-1], name, label=label_stack[-1])

        if line_arr[-1] == 'recurrence-events' or line_arr[-1] == 'no-recurrence-events':
          # Create connection from current node to classification
          classif = line_arr[-1]
          graph.node(classif + str(counter), classif)
          graph.edge(name, classif + str(counter), label=line_arr[depth + 3][:-1])
          counter += 1
        """

      #depth = line.count('|')

    print(depth)
    
  
  return graph

def main():
  tree = create_tree()

  tree.render('test-output.gv', format='png', view=True)


main()
