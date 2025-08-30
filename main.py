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
# Sun Valley ttk theme: https://github.com/rdbende/Sun-Valley-ttk-theme

# ------------------------- Libraries -------------------------
import tkinter as tk
from tkinter import IntVar, Radiobutton, Button, Label, StringVar, Entry, Text
from tkinter import ttk

import sv_ttk

# ---------------------------- GUI constraints ------------------------------- #
DARK_BLUE2 = "#OB3954"
DARK_BLUE = "#001111"
WHITE = "#ffffff"
BLACK = "#000000"

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
    resultOutput.configure(state="disabled")

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
window.title("Automotive Inference System")
window.config(padx=20, pady=20)
sv_ttk.set_theme("dark") # 'light' or 'dark'

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

ForwardChaining = Radiobutton(text="Forward chaining   ", variable=opcion, value=1,
                              command=selectLearning)
ForwardChaining.grid(column=0, row=0)

BackwardChaining = Radiobutton(text="Backward chaining", variable=opcion, value=2,
                               command=selectLearning, pady=10)
BackwardChaining.grid(column=0, row=1)

# Reset learning button
resetButton = ttk.Button(text="Reset options", command=resetLearningSelect)
resetButton.grid(column=0, row=2)

# Goal label
goalLabel = Label(text="Goal")
goalLabel.grid(column=1, row=0)

# Goal Combobox
var = StringVar()
goalChoosen = ttk.Combobox(window, textvariable=var, state="readonly")
goalChoosen['values'] = (
    'Manzana',
    'Pera',
    'Limón')
goalChoosen.grid(column=1, row=1)

# Result label
resultLabel = Label(text="Result")
resultLabel.grid(column=2, row=0)

# Entry
resultOutput = Entry(width=21)
resultOutput.grid(column=2, row=1)
printResult("TestB")

# TextBox
outputText = Text(window, height=20, width=100, highlightbackground="#A9A9A9")
outputText.grid(column=0, row=3, columnspan=3, pady=(20, 10))
var.trace('w', printGoal) # Favor de no mover esta linea de lugar
printOutput("Lorem ipsum dolor sit amet, consectetur adipiscing elit.")  # Ejemplo

# Reset output button
resetButton = ttk.Button(text="Reset output", command=resetOutput)
resetButton.grid(column=0, row=4)

window.mainloop()