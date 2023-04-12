import customtkinter as ctk
from gui.font_settings import button_font, small_btn_font

COMPUTER_SLEEP = 0.8

WINNER_TEXT = {
  0: "Neizšķirts!",
  -1: "Tu uzvarēji!",
  1: "Dators uzvarēja!"
}

frame = None
buttons_container = None

def game_screen(num_string, computer_starts : bool, app, player_score, comp_score, on_game_restart, on_show_rules, on_show_tree, on_merge_numbers, winner=None):
  global frame, buttons_container
  frame = ctk.CTkFrame(app)
  buttons_container = ctk.CTkFrame(frame)
  game_elements = []
  for i,ch in enumerate(num_string):
    label = ctk.CTkLabel(master=buttons_container, text=ch, font=button_font, width=3, height=1)
    game_elements.append(label)
    if i == len(num_string) - 1:
      continue
    button = ctk.CTkButton(master=buttons_container, text="-> <-", font=small_btn_font, width=3, height=0, command=lambda idx=i: on_merge_numbers(idx))
    game_elements.append(button)
  for i, element in enumerate(game_elements):
    element.grid(row=0, column=i, padx=5)
  buttons_container.pack(pady=50)
  board = score_board(player_score, comp_score, winner)
  buttons = buttons_row(on_game_restart, on_show_rules, on_show_tree)
  board.pack(pady=30, padx=30)
  buttons.pack(pady=30, padx=30)
  return frame


def update_num_string(num_string, app, player_score, comp_score, on_game_restart, on_show_rules, on_show_tree, on_merge_numbers, winner=None):
  global frame
  if not frame:
    raise Exception("No frame")
  for widget in frame.winfo_children():
    widget.destroy()
  frame.pack_forget()
  return game_screen(num_string, False, app, player_score, comp_score, on_game_restart, on_show_rules, on_show_tree, on_merge_numbers, winner)


def score_board(player_score, comp_score, winner=None):
  board = ctk.CTkFrame(frame)
  player_label = ctk.CTkLabel(master=board, text="Spēlētājs:", font=button_font)
  player_score_display = ctk.CTkLabel(master=board, textvariable=player_score, font=button_font)
  comp_label = ctk.CTkLabel(master=board, text="Dators:", font=button_font)
  comp_score_display = ctk.CTkLabel(master=board, textvariable=comp_score, font=button_font)
  player_label.grid(row=0, column=0, padx=10, sticky="w")
  player_score_display.grid(row=0, column=1, padx=10, sticky="w")
  comp_label.grid(row=0, column=2, padx=10, sticky="e")
  comp_score_display.grid(row=0, column=3, padx=10, sticky="e")
  if winner is not None:
    winner_text = WINNER_TEXT[winner]
    winner_label = ctk.CTkLabel(master=board, text=winner_text, font=button_font)
    winner_label.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")
  return board


def buttons_row(startover_callback, rules_callback, show_tree_callback):
  global frame
  button_container = ctk.CTkFrame(frame)
  start_over_btn = ctk.CTkButton(master=button_container, text="Sākt no jauna", font=small_btn_font, command=startover_callback)
  rules_btn = ctk.CTkButton(master=button_container, text="Spēles noteikumi", font=small_btn_font, command=rules_callback)
  show_tree_btn = ctk.CTkButton(master=button_container, text="Parādīt koku", font=small_btn_font, command=show_tree_callback)
  start_over_btn.grid(row=0, column=0, padx=10, pady=10)
  rules_btn.grid(row=0, column=1, padx=10, pady=10)
  show_tree_btn.grid(row=0, column=2, padx=10, pady=10)
  return button_container
