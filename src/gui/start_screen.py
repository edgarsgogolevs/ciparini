import customtkinter as ctk
from gui.font_settings import default_font, title_font
from config import DEFUALT_STARTING_NUMS


def character_limit(entry_text):
  if entry_text.get()[-1] not in "0123456789":
    entry_text.set(entry_text.get()[:-1])
  if len(entry_text.get()) > 10:
    entry_text.set(entry_text.get()[:-1])


def start_screen(app, on_start_button_click):
  # Frame
  frame = ctk.CTkFrame(app)

  # Title
  title = ctk.CTkLabel(master=frame, text="Ciparu spēle", font=title_font)
  title.pack(pady=100, padx=10)

  # Starting nums
  entry_nums_label = ctk.CTkLabel(
    master=frame,
    text="Ciparu virkne spēlei:",
    font=default_font,
  )
  entry_nums_label.pack(pady=10, padx=10)
  nums_var = ctk.StringVar(value=DEFUALT_STARTING_NUMS)
  entry_nums = ctk.CTkEntry(master=frame, textvariable=nums_var, font=default_font)
  entry_nums.pack()
  nums_var.trace("w", lambda *args: character_limit(nums_var))

  # Computer starts checkbox
  comp_starts_var = ctk.BooleanVar(value=False)
  comp_starts_checkbox = ctk.CTkCheckBox(master=frame, text="Spēli sāk dators", variable=comp_starts_var, font=default_font)
  comp_starts_checkbox.pack(pady=10)

  # Start button
  start_button = ctk.CTkButton(
    master=frame,
    text="Sākt!",
    font=title_font,
    command=lambda: on_start_button_click(nums_var.get(), comp_starts_var.get())
  )
  start_button.pack(pady=50, padx=10)
  return frame