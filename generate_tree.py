from graphviz import Digraph

class Node():
  def __init__(self, name, idd):
    self._name = name
    self._id = idd

  def __str__(self):
    return str(self._name) 

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

  # This method determines whether or not a given node should be merged with another to reduce redundancy
  #  Returns the node that should be used instead or None if we are all clear to add a new node
  def shouldMerge(self, parent, parent_label, name):
    ret = None
    for conn in self._conns:
      target = conn.getTarget()
      if target.getName() == name and conn.getLabel() == parent_label:
        ret = target
    return ret

  # This method will parse a given line and add it to the tree (note that order DOES matter when importing these lines from WEKA)
  def addLine(self, line):
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
    #if line_arr[-1] == 'recurrence-events' or line_arr[-1] == 'no-recurrence-events':
    if line_arr[-1] in classes:
      #print('leaf!')
      leaf = line_arr[-1]
    elif line_arr[-1] == 'null':
      return

    # If the depth has decreased, we need to pop off the unneeded elements
    while len(self._parent_stack) > cdepth:
      del self._parent_stack[-1]
      del self._label_stack[-1]

    # Switch changes to the tree based on whether we are dealing with a branch or a leaf
    if leaf:
      # This line is a leaf, which means we create more nodes
      #   Ex: `|  tumor-size = 0-4: no-recurrence-events`
      #print('Leaf!')

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
      #print('Branch!')

      new_branch = None

      # If there are nodes in the parent stack, point to me!
      if len(self._parent_stack) > 0:
        prnt = self._parent_stack[-1]
        plabel = self._label_stack[-1]        
        new_branch = self.shouldMerge(prnt, plabel, name)
        if not new_branch:
          # Create tumor-size node
          new_branch = Node(name, len(self._nodes))
          self._nodes.append(new_branch) # Adds the new node to the list of nodes
          prnt = self._parent_stack[-1]
          plabel = self._label_stack[-1]

          # Create connection
          conn = Connection(prnt, new_branch, plabel)
          self._conns.append(conn)
      else:
        # If the root node isn't already defined...
        if not self._root:
          # Create tumor-size node
          new_branch = Node(name, len(self._nodes))
          self._root = new_branch
          self._nodes.append(new_branch)
        # Otherwise, it is and we set the new branches
        else:
          new_branch = self._root

      # Append the tumor-size node to the parent_stack
      self._parent_stack.append(new_branch)

      # Append the tumor-size label (15-19) to the label_stack
      self._label_stack.append(val)


  # Creates a Graphviz DiGraph object and returns to the caller
  def createGraph(self):
    # Graph object
    graph = Digraph(comment='ID3 Tree on breast-cancer.arff')
    
    for node in self._nodes:
      #print('Adding node {}'.format(node))
      graph.node(node.getID(), node.getName())

    for conn in self._conns:
      #print('Addding conn {}'.format(conn))
      graph.edge( (conn.getOrigin()).getID(), (conn.getTarget()).getID(), label=conn.getLabel() )

    return graph
    

def create_tree():
  # Create tree object
  tree = Tree() 
  arr = ascii_tree.splitlines() 

  for line in arr:
    tree.addLine(line)

  #print(tree)

  graph = tree.createGraph()

  return graph

def main():
  tree = create_tree()

  tree.render('test-output.gv', format='png', view=True)



classes = ['diaporthe-stem-canker', 'charcoal-rot', 'rhizoctonia-root-rot', 'phytophthora-rot', 'brown-stem-rot', 'powdery-mildew', 'downy-mildew', 'brown-spot', 'bacterial-blight', 'bacterial-pustule', 'purple-seed-stain', 'anthracnose', 'phyllosticta-leaf-spot', 'alternarialeaf-spot', 'frog-eye-leaf-spot', 'diaporthe-pod-&-stem-blight', 'cyst-nematode', '2-4-d-injury', 'herbicide-injury']

# ASCII Decision Tree retrieved from WEKA
ascii_tree = """canker-lesion = dna
|  leafspot-size = lt-1/8
|  |  leafspots-marg = w-s-marg
|  |  |  seed-size = norm
|  |  |  |  roots = norm: bacterial-blight
|  |  |  |  roots = rotted: bacterial-pustule
|  |  |  |  roots = galls-cysts: null
|  |  |  seed-size = lt-norm: bacterial-pustule
|  |  leafspots-marg = no-w-s-marg: bacterial-pustule
|  |  leafspots-marg = dna: null
|  leafspot-size = gt-1/8
|  |  date = april
|  |  |  temp = lt-norm: herbicide-injury
|  |  |  temp = norm: brown-spot
|  |  |  temp = gt-norm: brown-spot
|  |  date = may
|  |  |  fruit-pods = norm
|  |  |  |  precip = lt-norm: phyllosticta-leaf-spot
|  |  |  |  precip = norm
|  |  |  |  |  area-damaged = scattered: brown-spot
|  |  |  |  |  area-damaged = low-areas: null
|  |  |  |  |  area-damaged = upper-areas: brown-spot
|  |  |  |  |  area-damaged = whole-field: phyllosticta-leaf-spot
|  |  |  |  precip = gt-norm
|  |  |  |  |  leafspots-halo = absent: null
|  |  |  |  |  leafspots-halo = yellow-halos: downy-mildew
|  |  |  |  |  leafspots-halo = no-yellow-halos: brown-spot
|  |  |  fruit-pods = diseased: diaporthe-pod-&-stem-blight
|  |  |  fruit-pods = few-present: null
|  |  |  fruit-pods = dna: herbicide-injury
|  |  date = june
|  |  |  seed = norm
|  |  |  |  precip = lt-norm: phyllosticta-leaf-spot
|  |  |  |  precip = norm
|  |  |  |  |  hail = yes
|  |  |  |  |  |  plant-stand = normal: brown-spot
|  |  |  |  |  |  plant-stand = lt-normal: phyllosticta-leaf-spot
|  |  |  |  |  hail = no: brown-spot
|  |  |  |  precip = gt-norm
|  |  |  |  |  temp = lt-norm: herbicide-injury
|  |  |  |  |  temp = norm: brown-spot
|  |  |  |  |  temp = gt-norm: brown-spot
|  |  |  seed = abnorm
|  |  |  |  plant-growth = norm: downy-mildew
|  |  |  |  plant-growth = abnorm: cyst-nematode
|  |  date = july
|  |  |  seed = norm
|  |  |  |  precip = lt-norm: phyllosticta-leaf-spot
|  |  |  |  precip = norm: phyllosticta-leaf-spot
|  |  |  |  precip = gt-norm
|  |  |  |  |  area-damaged = scattered
|  |  |  |  |  |  crop-hist = diff-lst-year
|  |  |  |  |  |  |  hail = yes: alternarialeaf-spot
|  |  |  |  |  |  |  hail = no: frog-eye-leaf-spot
|  |  |  |  |  |  crop-hist = same-lst-yr: frog-eye-leaf-spot
|  |  |  |  |  |  crop-hist = same-lst-two-yrs: frog-eye-leaf-spot
|  |  |  |  |  |  crop-hist = same-lst-sev-yrs: frog-eye-leaf-spot
|  |  |  |  |  area-damaged = low-areas
|  |  |  |  |  |  crop-hist = diff-lst-year: null
|  |  |  |  |  |  crop-hist = same-lst-yr: null
|  |  |  |  |  |  crop-hist = same-lst-two-yrs: alternarialeaf-spot
|  |  |  |  |  |  crop-hist = same-lst-sev-yrs: brown-spot
|  |  |  |  |  area-damaged = upper-areas: frog-eye-leaf-spot
|  |  |  |  |  area-damaged = whole-field: brown-spot
|  |  |  seed = abnorm
|  |  |  |  plant-growth = norm: downy-mildew
|  |  |  |  plant-growth = abnorm: cyst-nematode
|  |  date = august
|  |  |  seed = norm
|  |  |  |  leaf-malf = absent
|  |  |  |  |  seed-tmt = none
|  |  |  |  |  |  area-damaged = scattered
|  |  |  |  |  |  |  crop-hist = diff-lst-year: null
|  |  |  |  |  |  |  crop-hist = same-lst-yr: alternarialeaf-spot
|  |  |  |  |  |  |  crop-hist = same-lst-two-yrs: frog-eye-leaf-spot
|  |  |  |  |  |  |  crop-hist = same-lst-sev-yrs: frog-eye-leaf-spot
|  |  |  |  |  |  area-damaged = low-areas
|  |  |  |  |  |  |  precip = lt-norm: null
|  |  |  |  |  |  |  precip = norm: frog-eye-leaf-spot
|  |  |  |  |  |  |  precip = gt-norm: alternarialeaf-spot
|  |  |  |  |  |  area-damaged = upper-areas
|  |  |  |  |  |  |  crop-hist = diff-lst-year: null
|  |  |  |  |  |  |  crop-hist = same-lst-yr
|  |  |  |  |  |  |  |  germination = 90-100: alternarialeaf-spot
|  |  |  |  |  |  |  |  germination = 80-89: frog-eye-leaf-spot
|  |  |  |  |  |  |  |  germination = lt-80: null
|  |  |  |  |  |  |  crop-hist = same-lst-two-yrs: alternarialeaf-spot
|  |  |  |  |  |  |  crop-hist = same-lst-sev-yrs: alternarialeaf-spot
|  |  |  |  |  |  area-damaged = whole-field: alternarialeaf-spot
|  |  |  |  |  seed-tmt = fungicide
|  |  |  |  |  |  germination = 90-100: frog-eye-leaf-spot
|  |  |  |  |  |  germination = 80-89
|  |  |  |  |  |  |  precip = lt-norm: null
|  |  |  |  |  |  |  precip = norm: frog-eye-leaf-spot
|  |  |  |  |  |  |  precip = gt-norm: alternarialeaf-spot
|  |  |  |  |  |  germination = lt-80
|  |  |  |  |  |  |  crop-hist = diff-lst-year: null
|  |  |  |  |  |  |  crop-hist = same-lst-yr: alternarialeaf-spot
|  |  |  |  |  |  |  crop-hist = same-lst-two-yrs: null
|  |  |  |  |  |  |  crop-hist = same-lst-sev-yrs
|  |  |  |  |  |  |  |  area-damaged = scattered: alternarialeaf-spot
|  |  |  |  |  |  |  |  area-damaged = low-areas: alternarialeaf-spot
|  |  |  |  |  |  |  |  area-damaged = upper-areas: null
|  |  |  |  |  |  |  |  area-damaged = whole-field: null
|  |  |  |  |  seed-tmt = other: frog-eye-leaf-spot
|  |  |  |  leaf-malf = present: phyllosticta-leaf-spot
|  |  |  seed = abnorm
|  |  |  |  plant-growth = norm
|  |  |  |  |  leaf-mild = absent: alternarialeaf-spot
|  |  |  |  |  leaf-mild = upper-surf: null
|  |  |  |  |  leaf-mild = lower-surf: downy-mildew
|  |  |  |  plant-growth = abnorm: cyst-nematode
|  |  date = september
|  |  |  mold-growth = absent
|  |  |  |  temp = lt-norm: null
|  |  |  |  temp = norm
|  |  |  |  |  leaf-shread = absent
|  |  |  |  |  |  crop-hist = diff-lst-year
|  |  |  |  |  |  |  precip = lt-norm: null
|  |  |  |  |  |  |  precip = norm: frog-eye-leaf-spot
|  |  |  |  |  |  |  precip = gt-norm: alternarialeaf-spot
|  |  |  |  |  |  crop-hist = same-lst-yr
|  |  |  |  |  |  |  hail = yes: frog-eye-leaf-spot
|  |  |  |  |  |  |  hail = no: alternarialeaf-spot
|  |  |  |  |  |  crop-hist = same-lst-two-yrs: alternarialeaf-spot
|  |  |  |  |  |  crop-hist = same-lst-sev-yrs: frog-eye-leaf-spot
|  |  |  |  |  leaf-shread = present: alternarialeaf-spot
|  |  |  |  temp = gt-norm: alternarialeaf-spot
|  |  |  mold-growth = present
|  |  |  |  temp = lt-norm: downy-mildew
|  |  |  |  temp = norm: downy-mildew
|  |  |  |  temp = gt-norm: diaporthe-pod-&-stem-blight
|  |  date = october
|  |  |  mold-growth = absent
|  |  |  |  precip = lt-norm: null
|  |  |  |  precip = norm
|  |  |  |  |  seed-tmt = none: null
|  |  |  |  |  seed-tmt = fungicide
|  |  |  |  |  |  crop-hist = diff-lst-year: null
|  |  |  |  |  |  crop-hist = same-lst-yr: null
|  |  |  |  |  |  crop-hist = same-lst-two-yrs: frog-eye-leaf-spot
|  |  |  |  |  |  crop-hist = same-lst-sev-yrs: alternarialeaf-spot
|  |  |  |  |  seed-tmt = other: alternarialeaf-spot
|  |  |  |  precip = gt-norm: alternarialeaf-spot
|  |  |  mold-growth = present
|  |  |  |  temp = lt-norm: downy-mildew
|  |  |  |  temp = norm: null
|  |  |  |  temp = gt-norm: diaporthe-pod-&-stem-blight
|  leafspot-size = dna
|  |  precip = lt-norm
|  |  |  leaf-mild = absent: brown-stem-rot
|  |  |  leaf-mild = upper-surf: powdery-mildew
|  |  |  leaf-mild = lower-surf: null
|  |  precip = norm: powdery-mildew
|  |  precip = gt-norm
|  |  |  plant-growth = norm
|  |  |  |  temp = lt-norm: powdery-mildew
|  |  |  |  temp = norm: 2-4-d-injury
|  |  |  |  temp = gt-norm: null
|  |  |  plant-growth = abnorm
|  |  |  |  date = april: herbicide-injury
|  |  |  |  date = may: herbicide-injury
|  |  |  |  date = june: herbicide-injury
|  |  |  |  date = july: diaporthe-stem-canker
|  |  |  |  date = august: diaporthe-stem-canker
|  |  |  |  date = september: diaporthe-stem-canker
|  |  |  |  date = october: null
canker-lesion = brown
|  fruit-spots = absent
|  |  fruiting-bodies = absent
|  |  |  date = april: anthracnose
|  |  |  date = may: anthracnose
|  |  |  date = june: anthracnose
|  |  |  date = july: null
|  |  |  date = august: frog-eye-leaf-spot
|  |  |  date = september: frog-eye-leaf-spot
|  |  |  date = october: null
|  |  fruiting-bodies = present: brown-spot
|  fruit-spots = colored
|  |  external-decay = absent: brown-spot
|  |  external-decay = firm-and-dry: frog-eye-leaf-spot
|  |  external-decay = watery: null
|  fruit-spots = brown-w/blk-specks
|  |  crop-hist = diff-lst-year: anthracnose
|  |  crop-hist = same-lst-yr: brown-spot
|  |  crop-hist = same-lst-two-yrs: anthracnose
|  |  crop-hist = same-lst-sev-yrs: null
|  fruit-spots = distort: null
|  fruit-spots = dna
|  |  temp = lt-norm: rhizoctonia-root-rot
|  |  temp = norm: diaporthe-stem-canker
|  |  temp = gt-norm: null
canker-lesion = dk-brown-blk
|  fruit-spots = absent
|  |  plant-stand = normal: anthracnose
|  |  plant-stand = lt-normal: phytophthora-rot
|  fruit-spots = colored: frog-eye-leaf-spot
|  fruit-spots = brown-w/blk-specks
|  |  precip = lt-norm: null
|  |  precip = norm: frog-eye-leaf-spot
|  |  precip = gt-norm: anthracnose
|  fruit-spots = distort: null
|  fruit-spots = dna: phytophthora-rot
canker-lesion = tan
|  int-discolor = none
|  |  severity = minor: purple-seed-stain
|  |  severity = pot-severe: null
|  |  severity = severe: brown-spot
|  int-discolor = brown: brown-stem-rot
|  int-discolor = black: charcoal-rot"""
main()
