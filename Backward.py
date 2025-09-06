import tkinter as tk
from tkinter import simpledialog, ttk
def cargar_reglas(archivo):
    reglas = []
    with open(archivo, "r", encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if not linea:
                continue
            try:
                nombre, resto = linea.split(":", 1)
                nombre = nombre.strip()
                condiciones_str, conclusion_str = resto.split("THEN")
                condiciones_str = condiciones_str.replace("IF", "").strip()
                condiciones = [tuple(cond.strip().split("=")) for cond in condiciones_str.split("AND")]
                condiciones = [(var.strip(), val.strip()) for var, val in condiciones]
                var_concl, val_concl = conclusion_str.strip().split("=")
                conclusion = (var_concl.strip(), val_concl.strip())
                reglas.append({"nombre": nombre, "condiciones": condiciones, "conclusion": conclusion})
            except ValueError as e:
                print(f"Error en la linea: {linea} ->{e}")
    return reglas

def cargar_hechos(archivo):
    hechos = {}
    try:
        with open(archivo, "r", encoding="utf-8") as f:
            for linea in f:
                if "=" in linea:
                    var, val = linea.strip().split("=")
                    hechos[var.strip()] = val.strip()
    except FileNotFoundError:
        pass
    return hechos

def ask_option(variable, opciones, title="Requerimiento"):
    """
    Muestra un Toplevel modal con un Combobox (readonly).
    Devuelve la opción elegida (str) o None si se cancela/cierra.
    """
    parent = tk._default_root  # usa la raíz existente creada en main.py
    if parent is None:
        # Si por alguna razón no existe, último recurso: crea una raíz temporal
        parent = tk.Tk()
        parent.withdraw()

    win = tk.Toplevel(parent)
    win.title(title)
    win.transient(parent)
    win.grab_set()  # modal

    # Centrar sobre la ventana principal
    win.update_idletasks()
    x = parent.winfo_rootx() + (parent.winfo_width() // 2) - 150
    y = parent.winfo_rooty() + (parent.winfo_height() // 2) - 60
    try:
        win.geometry(f"+{x}+{y}")
    except Exception:
        pass

    frame = ttk.Frame(win, padding=12)
    frame.pack(fill="both", expand=True)

    ttk.Label(frame, text=f"Seleccione un valor para '{variable}':").pack(pady=(0,8))

    var = tk.StringVar(value=opciones[0])
    combo = ttk.Combobox(frame, textvariable=var, values=opciones, state="readonly")
    combo.pack(fill="x")
    combo.focus_set()

    result = {"value": None}

    def on_ok():
        result["value"] = var.get()
        win.destroy()

    def on_cancel():
        result["value"] = None
        win.destroy()

    btns = ttk.Frame(frame)
    btns.pack(pady=(12,0), fill="x")
    ttk.Button(btns, text="Aceptar", command=on_ok).pack(side="left", expand=True)
    ttk.Button(btns, text="Cancelar", command=on_cancel).pack(side="right", expand=True)

    win.bind("<Return>", lambda e: on_ok())
    win.bind("<Escape>", lambda e: on_cancel())

    win.wait_window()  # bloquea hasta cerrar
    return result["value"]


def backward_chain(meta, reglas, respuestas, print_callback=print, pop_up = True, visitados=None):
    if visitados is None:
        visitados = set()

    if meta in visitados:
        return False
    visitados.add(meta)

    if meta[0] in respuestas:
        return respuestas[meta[0]] == meta[1]
    
    for regla in reglas:
        if regla["conclusion"] == meta:
            valido = True
            for cond in regla["condiciones"]:
                if not backward_chain(cond, reglas, respuestas, print_callback, pop_up, visitados):
                    valido = False
                    break
            if valido:
                respuestas[meta[0]] = meta[1]
                print_callback(f"Reglas que se aplicaron: {regla['nombre']} -> {meta[0]}={meta[1]}")
                return True
    
        caracteristicas_basicas = ["num_wheels", "motor", "size", "num_doors"]

    if meta[0] in caracteristicas_basicas and pop_up:
        opciones_dict = {
            "num_wheels": ["2", "3", "4"],
            "motor": ["yes", "no"],
            "size": ["small", "medium", "large"],
            "num_doors": ["2", "3", "4"]
        }

        if meta[0] in opciones_dict:
            respuesta = ask_option(meta[0], opciones_dict[meta[0]])
            if respuesta is None:
                return False

            if meta[0] in ("motor", "size"):
                respuesta = respuesta.strip().lower()
            else:
                respuesta = respuesta.strip()

            respuestas[meta[0]] = respuesta

            try:
                print_callback(f"Entrada usuario: {meta[0]}={respuesta}")
            except Exception:
                pass

            return respuestas[meta[0]] == meta[1]

    
    return False

def run_backward(reglas, archivo_hechos = None, print_callback = print, result_callback = None):
    hechos = cargar_hechos(archivo_hechos) if archivo_hechos else{}
    respuestas = dict(hechos)

    print_callback("Inciando sistema")
    encontrado = False

    # vehicleType solo se usa como apoyo, no activa 'encontrado'
    for meta in [r["conclusion"] for r in reglas if r["conclusion"][0] == "vehicleType"]:
        backward_chain(meta, reglas, respuestas, print_callback)

    # ahora sí: solo vehicle cuenta como encontrado
    for meta in [r["conclusion"] for r in reglas if r["conclusion"][0] == "vehicle"]:
        if backward_chain(meta, reglas, respuestas, print_callback):
            print_callback(f"\nVehiculo identificado: {meta[1]}")
            respuestas[meta[0]] = meta[1]
            if result_callback:
                result_callback(meta[1])
            encontrado = True
            break

    if not encontrado:
        print_callback("\n No se encontro el vehiculo buscado")
        if result_callback:
            result_callback("NULL")


    hechos_temporales = {k: v for k, v in respuestas.items() if k not in hechos}
    return hechos_temporales
