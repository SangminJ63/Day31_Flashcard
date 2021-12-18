from tkinter import *
import random
import pandas as pd

BACKGROUND_COLOR = "#B1DDC6"

# Load data file -------------------------

try:
    data = pd.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pd.read_csv("data/french_words.csv")
    words_to_learn = original_data.to_dict('records')
else:
    words_to_learn = data.to_dict('records')
card = {}


def next_card():
    global card, flip_timer
    window.after_cancel(flip_timer)
    card = random.choice(words_to_learn)
    canvas.itemconfig(card_image, image=image_card_front)
    canvas.itemconfigure(title_text, text="French", fill="black")
    canvas.itemconfigure(french_text, text=card['French'], fill="black")
    flip_timer = window.after(3000, flip_card)

def flip_card():
    canvas.itemconfig(title_text, text="English", fill="white")
    canvas.itemconfig(french_text, text=card['English'], fill="white")
    canvas.itemconfig(card_image, image=image_card_back)

def card_learned():
    words_to_learn.remove(card)
    data = pd.DataFrame(words_to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_card()

# UI Setup -------------------------------

window = Tk()
window.title("Flash Cards")
window.config(padx=25, pady=25, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

image_card_front = PhotoImage(file="images/card_front.png")
image_card_back = PhotoImage(file="images/card_back.png")
image_right_button = PhotoImage(file="images/right.png")
image_wrong_button = PhotoImage(file="images/wrong.png")

canvas = Canvas(bg=BACKGROUND_COLOR, width=800, height=526, highlightthickness=0)
card_image = canvas.create_image(400, 250, image=image_card_front)
title_text = canvas.create_text(400, 150, text="", font=("Ariel", 25, "bold"))
french_text = canvas.create_text(400, 250, text="", font=("Ariel", 40, "bold"))
canvas.grid(column=0,row=0, columnspan=2)

wrong_button = Button(image=image_wrong_button, highlightthickness=0, command=next_card)
wrong_button.grid(column=0, row=1)
right_button = Button(image=image_right_button, highlightthickness=0, command=card_learned)
right_button.grid(column=1, row=1)

next_card()


window.mainloop()
