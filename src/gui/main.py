import customtkinter as ctk
from gui.font_settings import default_font
from gui.start_screen import start_screen
from gui.game_screen import game_screen, update_num_string
from classes.display_tree import display_tree
from classes.node import Node
from config import COMPUTER_SLEEP, RULES



tree_data = None
game_head = None
current_node = None
game_frame = None
player_score = None
comp_score = None
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

app = ctk.CTk()
app.geometry("1100x900")
app.title("Ciparu spēle")
player_score = ctk.IntVar(value=0)
comp_score = ctk.IntVar(value=0)


def on_merge_numbers(idx : int):
  global current_node
  if not current_node:
    raise Exception("No current node")
  print("person move")
  cur_data = current_node.as_dict()
  cur_nums = cur_data["num_str"]
  if idx == len(cur_nums) - 1:
    raise ValueError("Incorrect index")
  merge_nums = (int(cur_nums[idx])), int(cur_nums[idx + 1])
  merge_sum = sum(merge_nums)
  if merge_sum > 7:
    score_diff = 1
    replace_with = 1
  elif merge_sum == 7:
    score_diff = 1
    replace_with = 2
  else:
    score_diff = -1
    replace_with = 3
  new_nums = cur_nums[:idx] + str(replace_with) + cur_nums[idx + 2:]
  if cur_data["player_1_move"]:
    score_a = cur_data["score_a"] + score_diff
    score_b = cur_data["score_b"]
  else:
    score_a = cur_data["score_a"]
    score_b = cur_data["score_b"] + score_diff
  make_move(new_nums, score_a, score_b)
  print(f"New nums: {new_nums}")
  if len(new_nums) > 1:
    computer_move()
    
    
def make_move(new_nums : str, score_a : int, score_b : int, slp_before : bool = False):
  global comp_score, player_score, game_frame, current_node, app
  if not current_node:
    raise Exception("No current node")
  if not comp_score or not player_score:
    raise Exception("No score")
  new_node = find_node(new_nums, score_a, score_b)
  current_node = new_node
  # Update score and board
  if current_node.is_terminal():
    rerender_game(new_nums, app, score_a, score_b, on_game_restart, on_show_rules, on_show_tree, on_merge_numbers, winner=current_node.is_win())
    return
  if slp_before:
    app.after(COMPUTER_SLEEP, lambda: rerender_game(new_nums, app, score_a, score_b, on_game_restart, on_show_rules, on_show_tree, on_merge_numbers))
  else:
    rerender_game(new_nums, app, score_a, score_b, on_game_restart, on_show_rules, on_show_tree, on_merge_numbers)
  

def rerender_game(new_nums, app, score_a, score_b, on_game_restart, on_show_rules, on_show_tree, on_merge_numbers, winner=None):
  global game_frame, player_score, comp_score
  comp_score.set(score_a)
  player_score.set(score_b)
  game_frame = update_num_string(new_nums, app, player_score, comp_score, on_game_restart, on_show_rules, on_show_tree, on_merge_numbers, winner)
  game_frame.pack(pady=30, padx=30, fill="both", expand=True)

  
def find_node(num_string : str, score_a : int, score_b : int):
  global current_node
  if not current_node:
    raise Exception("No game head")
  children = current_node.get_children()
  if not children:
    raise Exception("No children")
  for child in children:
    if child.num_string == num_string and child.score_a == score_a and child.score_b == score_b:
      return child
  raise Exception("No node found")


def computer_move():
  global current_node
  print("Computer move")
  if not current_node:
    raise Exception("No current node")
  best_move = current_node.get_best_move()
  if not best_move:
    raise Exception("No best move")
  best_data = best_move.as_dict()
  make_move(best_data["num_str"], best_data["score_a"], best_data["score_b"], slp_before=True)
  

def on_start_button_click(starting_nums : str, computer_starts : bool, start_frame):
  global app, tree_data, game_head, game_frame, current_node
  if len(starting_nums) < 3:
    return
  game_head = Node(num_string=starting_nums, player_1_move=computer_starts)
  game_head.expand()
  if computer_starts:
    game_head.maximize()
  else:
    game_head.minimize()
  current_node = game_head
  nodes, edges = game_head.build_tree()
  tree_data = {
    "nodes": nodes,
    "edges": edges,
  }
  start_frame.pack_forget()
  game_frame = game_screen(starting_nums, computer_starts, app, player_score, comp_score, on_game_restart, on_show_rules, on_show_tree, on_merge_numbers)
  game_frame.pack(pady=30, padx=30, fill="both", expand=True)
  if computer_starts:
    computer_move()
  

def on_game_over(winner : int):
  print("Game over")
  

def on_game_restart():
  global player_score, comp_score
  if not player_score:
    raise Exception("No player score")
  if not comp_score:
    raise Exception("No computer score")
  player_score.set(0)
  comp_score.set(0)
  print("Restarting game")
  if game_frame:
    game_frame.pack_forget()
  show_start()


def on_show_rules():
  print("Showing rules")
  rules = ctk.CTk()
  rules.geometry("650x900")
  rules.title("Noteikumi")
  rule_frame = ctk.CTkFrame(rules)
  rules_label = ctk.CTkLabel(rule_frame, text=RULES, font=default_font, wraplength=530, justify="left")
  rules_label.pack()
  rule_frame.pack(pady=30, padx=30, fill="both", expand=True)


def on_show_tree():
  print("Showing tree")
  if not tree_data:
    print("No tree data")
    return
  display_tree(tree_data["nodes"], tree_data["edges"])


def show_start():
  start_frame = start_screen(app, lambda *args: on_start_button_click(*args, start_frame=start_frame))
  start_frame.pack(pady=30, padx=30, fill="both", expand=True)


def main():
  global app
  show_start()
  app.mainloop()
