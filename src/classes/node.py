
class Node:
  """
    Virsotne spēles kokā.
  """
  
  def __init__(self, num_string: str, player_1_move: bool = True, score_a: int = 0, score_b: int = 0, parent = None) -> None:
    self.num_string= num_string
    self.score_a = score_a
    self.score_b = score_b
    self.player_1_move = player_1_move
    self.children : list[Node] = []
    self.parent = parent if parent and isinstance(parent, Node) else None
    self.minimax_score = None
    
    
  def add_child(self, child) -> None:
    if not isinstance(child, Node):
      raise ValueError("Incorrect value for Child")
    self.children.append(child)
  
  
  def as_dict(self) -> dict:
    """
      Node to dict.
    """
    return {
      "score_a": self.score_a,
      "score_b": self.score_b,
      "num_str": self.num_string,
      "max_score": self.minimax_score,
      "player_1_move": self.player_1_move,
    }
  
  
  def get_children(self):
    return self.children
  
  def get_hash(self) -> str:
    return f"{self.score_a}  |  {self.num_string}  |  {self.score_b} |  {self.minimax_score}"
  
  
  def get_best_move(self):
    best_move = None
    for child in self.children:
      if not best_move:
        best_move = child
      else:
        if not child.minimax_score:
          raise Exception("No minimax score")
        if child.minimax_score > best_move.minimax_score:
          best_move = child
    return best_move
  
  
  def expand(self):
    """
      Ģenerē visus pēctečus
    """
    if len(self.num_string) == 1:
      return
    available_moves = len(self.num_string) - 1
    whos_next_move = not self.player_1_move
    children = []
    for i in range(available_moves):
      move = self.calculate_move(i)
      node_data = {
        "num_string": move["num_str"],
        "parent": self,
        "player_1_move": whos_next_move,
        "score_a": self.score_a + move["score"] if self.player_1_move else self.score_a,
        "score_b": self.score_b + move["score"] if not self.player_1_move else self.score_b
      }
      new_child = Node(**node_data)
      new_child.expand()
      children.append(new_child)
    self.children = children
  
  
  def calculate_move(self, move_idx : int) -> dict:
    if move_idx >= len(self.num_string) - 1:
      raise ValueError("Incorrect move index")
    ret = {}
    operands = [int(self.num_string[move_idx]), int(self.num_string[move_idx + 1])]
    summa = sum(operands)
    if summa > 7:
      ret["score"] = 1
      ret["num_str"] = self.get_replaced_num_string(move_idx, 1)
      return ret
    if summa == 7:
      ret["score"] = 1
      ret["num_str"] = self.get_replaced_num_string(move_idx, 2)
      return ret
    ret["score"] = -1
    ret["num_str"] = self.get_replaced_num_string(move_idx, 3)
    return ret
  
  
  def is_terminal(self) -> bool:
    """
      Checks if the current node is a terminal node.
    """
    if len(self.num_string) == 1:
      return True
    return False
  
  
  def is_win(self) -> int:
    """
      Checks if the current node is a winning node. Returns 1 if player 1 wins,
      0 if it's a draw and -1 if player 2 wins.
    """
    if self.score_a > self.score_b:
      return 1
    if self.score_a == self.score_b:
      return 0
    return -1
  
  
  def get_replaced_num_string(self, move_idx : int, new_num : int) -> str:
    return self.num_string[:move_idx] + str(new_num) + self.num_string[move_idx + 2:]
  
  
  def build_tree(self):
    """
      Returns a list of nodes and a list of edges with self as root.
    """
    if not self.children:
      return [], []
    nodes = [self.get_hash()]
    edges = []
    for child in self.children:
      edges.append((self.get_hash(), child.get_hash()))
      new_nodes, new_edges = child.build_tree()
      for node in new_nodes:
        if node not in nodes:
          nodes.append(node)
      for edge in new_edges:
        if edge not in edges:
          edges.append(edge)
    return nodes, edges
    
  
  def maximize(self) -> int:
    """
      Returns the maximum score that can be obtained from the current node
      using the minimax algorithm.
    """
    if not self.children:
      # Leaf node, return the result
      self.minimax_score = self.is_win()
      return self.minimax_score

    max_score = -1
    for child in self.children:
      child_score = child.minimize()  # Recursively minimize the child node
      max_score = max(max_score, child_score)
    self.minimax_score = max_score
    return max_score


  def minimize(self) -> int:
    """
      Returns the minimum score that can be obtained from the current node
      using the minimax algorithm.
    """
    if not self.children:
      # Leaf node, return the result
      self.minimax_score = self.is_win()
      return self.minimax_score

    min_score = 1
    for child in self.children:
      child_score = child.maximize()  # Recursively maximize the child node
      min_score = min(min_score, child_score)
    self.minimax_score = min_score
    return min_score
  
  
  def print_tree(self, depth: int = 0) -> None:
    """
      Prints the tree with self as root.
    """
    print("  " * depth, self.as_dict())
    for child in self.children:
      child.print_tree(depth + 1)
    