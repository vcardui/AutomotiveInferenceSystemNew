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
# | Last update..: September 4th, 2025
# | WhatIs.......: Automotive Inference System - Main
# +----------------------------------------------------------------------------+

# ------------ Resources / Documentation involved -------------
# Sun Valley ttk theme: https://github.com/rdbende/Sun-Valley-ttk-theme

# ------------------------- Libraries -------------------------
import tkinter as tk
from tkinter import IntVar, Radiobutton, Button, Label, StringVar, Entry, Text, Menu
from tkinter import ttk

import sv_ttk

# ----------------------- GUI functions -----------------------

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

# Pop up
def open_popup():
    popup = tk.Toplevel()
    popup.title("Data")

    tk.Label(popup, text="Wheels:").grid(row=0, column=0, padx=5, pady=5)
    wheelsEntry = tk.Entry(popup)
    wheelsEntry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(popup, text="Doors:").grid(row=1, column=0, padx=5, pady=5)
    doorsEntry = tk.Entry(popup)
    doorsEntry.grid(row=1, column=1, padx=5, pady=5)

    def submit_data():
        print(f"Wheels: {wheelsEntry.get()}")
        print(f"Doors: {doorsEntry.get()}")
        popup.destroy()  # Close the pop-up after submission

    submit_button = tk.Button(popup, text="Submit", command=submit_data)
    submit_button.grid(row=2, column=0, columnspan=2, pady=10)

def yocsan():
    pass

# ------------------------- UI Set up ------------------------

window = tk.Tk()
window.title("Automotive Inference System")
window.config(padx=20, pady=20)

# Menubar
menubar = Menu(window)
window.config(menu=menubar)

# File menu
fileMenu = Menu(
    menubar,
    tearoff=0
)

fileMenuOptions = [["Start", ""], ["Reset", ""]]

for i in fileMenuOptions:
    fileMenu.add_command(
        label=f"{i[0]}",
        command=f"{i[1]}"
    )
    fileMenu.add_separator()

# Exit option
fileMenu.add_command(
    label='Exit',
    command=window.destroy
)

# Data menu
ruleBaseMenu = Menu(
    menubar,
    tearoff=0
)

ruleBaseMenuOptions = [["Vehicles", ""], ["Bugs", ""], ["Plants", ""], ["Motor", ""]]

for i in ruleBaseMenuOptions:
    ruleBaseMenu.add_command(
        label=f"{i[0]}",
        command=f"{i[1]}"
    )

# Data menu
dataMenu = Menu(
    menubar,
    tearoff=0
)

dataMenuOptions = [["Set value", open_popup], ["Load data", ""]]

for i in dataMenuOptions:
    dataMenu.add_command(
        label=f"{i[0]}",
        command= i[1]
    )


# Help menu
help_menu = Menu(
    menubar,
    tearoff=0
)
help_menu.add_command(label='Welcome')
help_menu.add_command(label='About...')

# Add menus to menubar
menubar.add_cascade(
    label="File",
    menu=fileMenu,
    underline=0
)

menubar.add_cascade(
    label="RuleBase",
    menu=ruleBaseMenu,
    underline=0
)

menubar.add_cascade(
    label="Data",
    menu=dataMenu,
    underline=0
)

menubar.add_cascade(
    label="Help",
    menu=help_menu,
    underline=0
)


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