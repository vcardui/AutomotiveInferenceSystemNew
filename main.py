# +----------------------------------------------------------------------------+
# | CARDUI WORKS v1.0.0
# +----------------------------------------------------------------------------+
# | Copyright (c) 2024 - 2025, CARDUI.COM (www.cardui.com)
# | Vanessa Reteguín <vanessa@reteguin.com>
# | Released under the MIT license
# | www.cardui.com/carduiframework/license/license.txt
# +----------------------------------------------------------------------------+
# | Author.......: Vanessa Reteguín <vanessa@reteguin.com>
# | Author.......: Yocsan Luevano <https://github.com/yocsan15>
# | Author.......: Eduardo Isaí López <https://github.com/VendosPan>
# | First release: August 29th, 2025
# | Last update..: September 7th, 2025
# | WhatIs.......: Automotive Inference System - Main
# +----------------------------------------------------------------------------+

# ------------ Resources / Documentation involved -------------
# Sun Valley ttk theme: https://github.com/rdbende/Sun-Valley-ttk-theme

# ------------------------- Libraries -------------------------
# app.py

from Forward import cargar_reglas, cargar_hechos, forward_chaining
from Backward import cargar_reglas as cargar_reglas_b, cargar_hechos as cargar_hechos_b, run_backward
import tkinter as tk
from tkinter import IntVar, Radiobutton, Button, Label, StringVar, Entry, Text, Menu
from tkinter import ttk
import sv_ttk

# Variables globales para almacenar reglas y hechos cargados
reglas_cargadas = []
hechos_cargados = {}
hechos_temporales = {}
archivo_modificado = False
HECHOS_ORIGINALES = """num_wheels=4
motor=yes
size=medium
num_doors=3
"""

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

def open_popup():
    popup = tk.Toplevel()
    popup.title("Set Boolean Rule Base Variables")

    rulbaseJson = {
        "vehicleType": ["cycle", "automobile"],
        "num_wheels": [2, 3, 4],
        "motor": ["no", "yes"],
        "size": ["small", "medium", "large"],
        "num_doors": [2, 3, 4]
    }

    listbox = tk.Listbox(popup)
    a = 1
    for i in rulbaseJson:
        listbox.insert(a, i)
        a += 1
    listbox.grid(row=0, column=0, padx=5, pady=5)

    popupselect = StringVar()
    goalChoosen = ttk.Combobox(popup, textvariable=popupselect, state="readonly")
    goalChoosen.grid(row=0, column=1, padx=5, pady=5)

    listboxItem = ""  # definida en el ámbito de open_popup

    def selected_item(chosenVar):
        nonlocal listboxItem
        if chosenVar != "":
            listboxItem = chosenVar
            goalChoosen['values'] = rulbaseJson[chosenVar]

    def callback(event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            data = event.widget.get(index)
            selected_item(data)

    listbox.bind("<<ListboxSelect>>", callback)

    def submit_data():
        global archivo_modificado
        variable = listboxItem
        valor = goalChoosen.get()

        if not (variable and valor):
            printOutput("⚠ No se seleccionó variable o valor")
            popup.destroy()
            return

        hechos_actuales = {}

        if not archivo_modificado:
            # Primer set después del reset: sobrescribir todo
            hechos_actuales = {variable: valor}
            archivo_modificado = True
        else:
            # Leer hechos existentes
            try:
                with open("Sistema_Experto/hechos.txt", "r") as f:
                    for line in f:
                        if "=" in line:
                            k, v = line.strip().split("=", 1)
                            hechos_actuales[k] = v
            except FileNotFoundError:
                pass

            # Actualizar o agregar el nuevo valor
            hechos_actuales[variable] = valor

        # Reescribir el archivo con todos los hechos
        with open("hechos.txt", "w") as f:
            for k, v in hechos_actuales.items():
                f.write(f"{k}={v}\n")

        printOutput(f"✔ Se guardó: {variable} = {valor} (hechos.txt actualizado)")
        popup.destroy()

    submit_button = tk.Button(popup, text="Guardar cambios", command=submit_data)
    submit_button.grid(row=2, column=0, columnspan=2, pady=10)


# ---------------------- FUNCIONES LÓGICAS ----------------------

def cargar_rulebase():
    global reglas_cargadas
    archivo_reglas = "base.txt"
    reglas_cargadas = cargar_reglas(archivo_reglas)
    resetOutput()
    printOutput("=== BASE DE REGLAS CARGADA ===")
    for r in reglas_cargadas:
        printOutput(f"{r['nombre']}: {r['condiciones']} -> {r['conclusion']}")

def cargar_datos():
    global hechos_cargados
    archivo_hechos = "hechos.txt"
    hechos_cargados = cargar_hechos(archivo_hechos)
    printOutput("\n=== HECHOS CARGADOS ===")
    for k, v in hechos_cargados.items():
        printOutput(f"{k} = {v}")

def run_inference():
    if  opcion.get() == 1:
        if not reglas_cargadas:
            printOutput("⚠ No hay base de reglas cargada.")
            return

        if not hechos_cargados:
            printOutput("⚠ No hay hechos cargados.")
            printResult("NULL")
            return

        resultado = forward_chaining(reglas_cargadas, hechos_cargados.copy())
        printOutput("\n=== RESULTADO INFERENCIA ===")
        for k, v in resultado.items():
            printOutput(f"{k} = {v}")

        if "vehicle" in resultado:
            printResult(resultado["vehicle"])
        else:
            printResult("No se pudo inferir vehículo")

    elif opcion.get() == 2:
        global hechos_temporales

        if not reglas_cargadas:
            printOutput("⚠ No hay base de reglas cargada.")
            return

        hechos_temporales = run_backward(reglas = reglas_cargadas, archivo_hechos =None if not hechos_cargados else "hechos.txt",
                                         print_callback = printOutput, result_callback = printResult)

    else:
        printOutput("⚠ Debe seleccionar un metodo de inferencia antes de continuar.")


def reset_all():
    global reglas_cargadas, hechos_cargados, hechos_temporales, archivo_modificado

    with open("hechos.txt", "w") as f:
        f.write(HECHOS_ORIGINALES)

    archivo_modificado = False  # <- reset del flag

    # Vaciar variables globales
    reglas_cargadas = []
    hechos_cargados = {}
    hechos_temporales = {}

    # Limpiar salidas
    resetOutput()
    printResult("")

    # (Opcional) limpiar la selección de Forward/Backward
    opcion.set(0)

    printOutput("=== Sistema reiniciado: reglas y datos borrados ===")

# ------------------------- UI Set up ------------------------

window = tk.Tk()
window.title("Automotive Inference System")
window.config(padx=20, pady=20)

sv_ttk.set_theme("light")  # Tema Sun Valley

# Menubar
menubar = Menu(window)
window.config(menu=menubar)

# File menu
fileMenu = Menu(menubar, tearoff=0)
fileMenu.add_command(label="Start", command=run_inference)
fileMenu.add_separator()
fileMenu.add_command(label="Reset", command=reset_all)
fileMenu.add_separator()
fileMenu.add_command(label="Exit", command=window.destroy)

# RuleBase menu
ruleBaseMenu = Menu(menubar, tearoff=0)
ruleBaseMenu.add_command(label="Vehicles", command=cargar_rulebase)
# ruleBaseMenu.add_command(label="Bugs", command=lambda: printOutput("Base Bugs no implementada"))
# ruleBaseMenu.add_command(label="Plants", command=lambda: printOutput("Base Plants no implementada"))
# ruleBaseMenu.add_command(label="Motor", command=lambda: printOutput("Base Motor no implementada"))

# Data menu
dataMenu = Menu(menubar, tearoff=0)


dataMenuOptions = [["Set value", open_popup], ["Load data", cargar_datos]]

for i in dataMenuOptions:
    dataMenu.add_command(
        label=f"{i[0]}",
        command= i[1]
    )

########## dataMenu.add_command(label="Set value", command=lambda: printOutput("Función Set value pendiente"))
########## dataMenu.add_command(label="Load data", command=cargar_datos)

# Help menu
help_menu = Menu(menubar, tearoff=0)
help_menu.add_command(label='Welcome')
help_menu.add_command(label='About...')

# Add menus to menubar
menubar.add_cascade(label="File", menu=fileMenu, underline=0)
menubar.add_cascade(label="RuleBase", menu=ruleBaseMenu, underline=0)
menubar.add_cascade(label="Data", menu=dataMenu, underline=0)
menubar.add_cascade(label="Help", menu=help_menu, underline=0)

# Forward/Backward learning
opcion = IntVar()
ForwardChaining = Radiobutton(text="Forward chaining   ", variable=opcion, value=1)
ForwardChaining.grid(column=0, row=0)

BackwardChaining = Radiobutton(text="Backward chaining", variable=opcion, value=2, pady=10)
BackwardChaining.grid(column=0, row=1)

# Reset learning button
#resetButton = ttk.Button(text="Reset options", command=lambda: opcion.set(None))
#resetButton.grid(column=0, row=2)

# Goal label
goalLabel = Label(text="Goal")
goalLabel.grid(column=1, row=0)

# Goal Combobox
var = StringVar()
goalChoosen = ttk.Combobox(window, textvariable=var, state="readonly")
goalChoosen['values'] = ('Vehicle')
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

# Reset output button
#resetButton = ttk.Button(text="Reset output", command=resetOutput)
#resetButton.grid(column=0, row=4)

window.mainloop()
