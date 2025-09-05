def cargar_reglas(archivo):
    reglas = []
    with open(archivo, "r", encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if not linea or linea.startswith("#"):
                continue
            try:
                nombre, resto = linea.split(":", 1)
                condiciones_str, conclusion_str = resto.split("THEN")
                condiciones_str = condiciones_str.replace("IF", "").strip()
                condiciones = [(var.strip(), val.strip()) for var, val in
                               (cond.split("=") for cond in condiciones_str.split("AND"))]
                var_concl, val_concl = conclusion_str.strip().split("=")
                conclusion = (var_concl.strip(), val_concl.strip())
                reglas.append({"nombre": nombre.strip(),
                               "condiciones": condiciones,
                               "conclusion": conclusion})
            except ValueError as e:
                print(f"Error en línea: {linea} -> {e}")
    return reglas


def cargar_hechos(archivo):
    hechos = {}
    with open(archivo, "r", encoding="utf-8") as f:
        for linea in f:
            if "=" in linea:
                var, val = linea.strip().split("=")
                hechos[var.strip()] = val.strip()
    return hechos


def forward_chaining(reglas, hechos):
    hechos_nuevos = True
    while hechos_nuevos:
        hechos_nuevos = False
        for regla in reglas:
            if all(hechos.get(var) == val for var, val in regla["condiciones"]):
                var_concl, val_concl = regla["conclusion"]
                if var_concl not in hechos:
                    hechos[var_concl] = val_concl
                    hechos_nuevos = True
    return hechos


if __name__ == "__main__":
    archivo_reglas = "base.txt"
    archivo_hechos = "hechos.txt"
    reglas = cargar_reglas(archivo_reglas)
    hechos = cargar_hechos(archivo_hechos)
    print("Reglas cargadas:", reglas)
    print("Hechos cargados:", hechos)
    resultado = forward_chaining(reglas, hechos)
    print("Resultado:", resultado)
