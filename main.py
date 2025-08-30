# +----------------------------------------------------------------------------+
# | CARDUI WORKS v1.0.0
# +----------------------------------------------------------------------------+
# | Copyright (c) 2024 - 2025, CARDUI.COM (www.cardui.com)
# | Vanessa Reteguín <vanessa@reteguin.com>
# | Released under the MIT license
# | www.cardui.com/carduiframework/license/license.txt
# +----------------------------------------------------------------------------+
# | Author.......: Vanessa Reteguín <vanessa@reteguin.com>
# | First release: August 29th, 2025
# | Last update..: August 29th, 2025
# | WhatIs.......: Automotive Inference System - Main
# +----------------------------------------------------------------------------+

# ------------ Resources / Documentation involved -------------
# How to make Tkinter look modern? - How to use themes in Tkinter: https://www.reddit.com/r/Python/comments/lps11c/how_to_make_tkinter_look_modern_how_to_use_themes/

# ------------------------- Libraries -------------------------
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

# ---------------------------- GUI constraints ------------------------------- #
WHITE = "#ffffff"
BLACK = "#000000"
FONT = ("Arial", 12)

# -------------------------- GUI Functions ----------------------------- #
# Output Textbox (blue)
def printOutput(text):
    outputText.config(state=tk.NORMAL)
    outputText.insert(tk.END, f"{text}\n")
    print(text)
    outputText.config(state=tk.DISABLED)

def resetOutput():
    outputText.config(state=tk.NORMAL)
    outputText.delete("1.0", "end")
    outputText.config(state=tk.DISABLED)

# Result textbox (small right)
def printResult(text):
    resultOutput.configure(state="normal")
    resultOutput.delete(0, 'end')
    resultOutput.insert(0, text)
    resultOutput.configure(state="disabled", disabledbackground="white", disabledforeground="black")

# Learning radiobutton options
def selectLearning():
    printOutput(f"{opcion.get()}")


def resetLearningSelect():
    opcion.set(None)


# Goal Combobox
def printGoal(*arg):
    printOutput(var.get())
    print(var.get())


# ---------------------------- UI Set up ------------------------------- #
window = tk.Tk()
window.title("Agente inteligente")
window.config(padx=20, pady=20, background=WHITE)

# Barra de menu
barra_menus = tk.Menu()
menu_archivo = tk.Menu(barra_menus, tearoff=False)

dataBases = ["Base A", "Base B", "Base C"]

for i in dataBases:
    menu_archivo.add_command(
        label=f"{i}"
    )
barra_menus.add_cascade(menu=menu_archivo, label="Base de datos")

window.config(menu=barra_menus)

# Forward/Backward learning

opcion = IntVar()

ForwardChaining = Radiobutton(text="Forward chaining   ", font=FONT, fg=BLACK, bg=WHITE, variable=opcion, value=1,
                              command=selectLearning)
ForwardChaining.grid(column=0, row=0)

BackwardChaining = Radiobutton(text="Backward chaining", font=FONT, fg=BLACK, bg=WHITE, variable=opcion, value=2,
                               command=selectLearning, pady=10)
BackwardChaining.grid(column=0, row=1)

# Reset learning button
resetButton = Button(text="Reset options", highlightbackground=WHITE, command=resetLearningSelect)
resetButton.grid(column=0, row=2)

# Goal label
goalLabel = Label(text="Goal", fg=BLACK, font=FONT, bg=WHITE)
goalLabel.grid(column=1, row=0)

# Goal Combobox
style= ttk.Style()
style.theme_use('default')
style.configure("TCombobox", background= WHITE)
goalChoosen = ttk.Combobox(window, foreground=WHITE, state="readonly")
goalChoosen['values'] = (
    'Manzana',
    'Pera',
    'Limón')
goalChoosen.grid(column=1, row=1)

# Result label
resultLabel = Label(text="Result", fg=BLACK, font=FONT, bg=WHITE)
resultLabel.grid(column=2, row=0)

# Entry
resultOutput = Entry(width=21, highlightbackground=WHITE, fg=BLACK, bg=WHITE)
resultOutput.grid(column=2, row=1)
printResult("TestA")
printResult("TestB")

# TextBox
outputText = Text(window, height=20, width=100, bg="light blue")
outputText.grid(column=0, row=3, columnspan=3, pady=(20, 10))
printOutput("Lorem ipsum dolor sit amet, consectetur adipiscing elit.")  # Ejemplo

# Reset output button
resetButton = Button(text="Reset output", highlightbackground=WHITE, command=resetOutput)
resetButton.grid(column=0, row=4)

window.mainloop()