from pulp import *
import tkinter as tk
import customtkinter as ct
from tkinter import filedialog
import webbrowser

# La siguiente librería solo funciona en windows
try:
    from ctype import windll, byref, sizeof, c_int
except:
    pass
# from ctype import windll, byref, sizeof, c_int

# ------------------- CONFIGURACIÓN DE LA VENTANA -------------------
# Crea la ventana del programa
root = tk.Tk()
# Tamaño de la ventana
root.geometry(str(int(root.winfo_screenwidth() / 2)) + "x" + str(int(root.winfo_screenheight() / 2)))
# Ventana maximizada
root.state("zoomed")
# Tamaño mínimo de la ventana
root.minsize(640, 360)
# Fondo de la ventana
root.configure(background="#172235")
# Título de la ventana
tk.Wm.wm_title(root, "OptiSolver")
# Logo de la ventana
try:
    root.iconphoto(True, tk.PhotoImage(file="Logo.png"))
except:
    pass
# Color de la barra de la ventana (solo funciona en Windows 11)
try:
    root.update()
    HWND = windll.user32.GetParent(root.winfo_id())
    windll.dwmapi.DwmSetWindowAttribute(HWND,
                                        35,
                                        byref(c_int(0x00352217)),
                                        sizeof(c_int))
    windll.dwmapi.DwmSetWindowAttribute(HWND,
                                        36,
                                        byref(c_int(0x00EEEEEE)),
                                        sizeof(c_int))
except:
    pass
# Fuerza la barra oscura cuando no se ha podido cambiar el color (Windows 10)
# (Hay que mover la ventana para verla cambiada, es un bug de Windows)
try:
    windll.dwmapi.DwmSetWindowAttribute(HWND,
                                        20,
                                        byref(c_int(1)),
                                        sizeof(c_int))
except:
    pass

# ---------------------------- VARIABLES ----------------------------
# Ruta del archivo a editar o resolver
rutaArchivo = ""


# ---------------------------- FUNCIONES ----------------------------
def cmdArchivoAbrir():
    global rutaArchivo

    rutaArchivoTemp = str(filedialog.askopenfilename(title="Abrir archivo",
                                                     filetypes=(
                                                         ("Archivos de texto", "*.txt"),
                                                         ("Todos los archivos", "*.*"))))
    if rutaArchivoTemp == "":
        return

    rutaArchivo = rutaArchivoTemp
    archivo = open(rutaArchivo, 'r')
    textBox.delete("1.0", tk.END)
    textBox.insert("1.0", archivo.read())
    archivo.close()


def cmdArchivoCerrar():
    global rutaArchivo

    textBox.delete("1.0", tk.END)
    rutaArchivo = ""


def cmdArchivoGuardar():
    global rutaArchivo
    if rutaArchivo == "":
        cmdArchivoGuardarComo()
    else:
        archivo = open(rutaArchivo, 'r+')
        archivo.seek(0)
        archivo.truncate()
        archivo.write(str(textBox.get("1.0", tk.END)))
        archivo.close()


def cmdArchivoGuardarComo():
    global rutaArchivo

    archivo = filedialog.asksaveasfile(title="Guardar como",
                                       defaultextension=".txt",
                                       filetypes=[("Archivo de texto", ".txt")])

    if archivo is None:
        return

    archivo.write(str(textBox.get("1.0", tk.END)))
    rutaArchivo = str(archivo.name)
    archivo.close()


def cmdAyuda():
    webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstley")


def keyCtrlO(e):
    cmdArchivoAbrir()


def keyCtrlW(e):
    cmdArchivoCerrar()


def keyCtrlS(e):
    cmdArchivoGuardar()


def keyCtrlShiftS(e):
    cmdArchivoGuardarComo()


def cmdGSolver():
    frameMenu.pack_forget()
    frameGSolver.pack(fill="both", expand="True")


def cmdTSolver():
    frameMenu.pack_forget()
    frameTSolver.pack(fill="both", expand="True")


def cmdGSCAtras():
    frameGSolver.pack_forget()
    frameMenu.pack(fill="none", expand=True)


def cmdGSCResolver():
    global rutaArchivo
    cmdArchivoGuardar()

    if rutaArchivo != "":
        file_path = rutaArchivo

        # Diccionarios para almacenar la información de las variables
        variable_names = {}
        variable_min = {}
        variable_max = {}
        variable_modo = {}

        # Bandera para indicar cuando se están leyendo las variables
        reading_variables = False

        # Leer el contenido del archivo input.txt

        # ---------------------LECTURA DE VARIABLES-------------------------#

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                NombreProblema = file.readline().strip()
                for line in file:
                    # Activar la bandera cuando se encuentra la línea que contiene "Variables:"
                    if "Variables:" in line:
                        reading_variables = True
                        continue

                    # Desactivar la bandera al llegar a la siguiente sección
                    if reading_variables and not line.strip():
                        reading_variables = False
                        break

                    # Si estamos leyendo las variables, extraer la información de cada variable
                    if reading_variables:
                        matches = re.findall(r'"([^"]*)" \s*(\S*)? \s*(\S*)? "([^"]*)"', line)

                        for i, match in enumerate(matches):
                            var_name = match[0]
                            var_min = float(match[1]) if match[1] else None
                            var_max = match[2] if match[2] else None
                            var_modo = match[3] if match[3] else None

                            # Utilizar el nombre del diccionario para la posición
                            index = len(variable_names) + 1

                            variable_names[f"var{index}_name"] = var_name
                            variable_min[f"var{index}_min"] = var_min
                            variable_max[f"var{index}_max"] = var_max
                            variable_modo[f"var{index}_modo"] = var_modo

            # Diccionarios para almacenar la información de las variables
            variable_maxmin = {}
            variable_eq = {}
            variable_eqname = {}

            # Bandera para indicar cuando se están leyendo las variables
            reading_variables = False

            # Leer el contenido del archivo input.txt

            # ---------------------LECTURA DE OBJETIVO-------------------------#

            with open(file_path, "r", encoding="utf-8") as file:
                for line in file:
                    # Activar la bandera cuando se encuentra la línea que contiene "Objetivo:"
                    if "Objetivo:" in line:
                        reading_variables = True
                        continue

                    # Desactivar la bandera al llegar a la siguiente sección
                    if reading_variables and not line.strip():
                        reading_variables = False
                        break

                    # Si estamos leyendo las Objetivo, extraer la información de cada variable
                    if reading_variables:
                        matches = re.findall(r'"([^"]*)" \s*(\S*)? "([^"]*)"', line)

                        for i, match in enumerate(matches):
                            var_maxmin = match[0]
                            var_eq = match[1] if match[1] else None
                            var_eqname = match[2] if match[2] else None

                            # Utilizar el nombre del diccionario para la posición
                            index = len(variable_maxmin) + 1

                            variable_maxmin[f"var{index}_maxmin"] = var_maxmin
                            variable_eq[f"var{index}_eq"] = var_eq
                            variable_eqname[f"var{index}_eqname"] = var_eqname

            # Diccionarios para almacenar la información de las variables
            variable_restric = {}
            variable_resname = {}

            # Bandera para indicar cuando se están leyendo las variables
            reading_variables = False

            # Leer el contenido del archivo .txt

            # ---------------------LECTURA DE RESTRICCIONES-------------------------#

            with open(file_path, "r", encoding="utf-8") as file:
                for line in file:
                    # Activar la bandera cuando se encuentra la línea que contiene "Restricciones:"
                    if "Restricciones:" in line:
                        reading_variables = True
                        continue

                    # Desactivar la bandera al llegar a la siguiente sección
                    if reading_variables and not line.strip():
                        reading_variables = False
                        break

                    # Si estamos leyendo las variables, extraer la información de cada variable
                    if reading_variables:
                        matches = re.findall(r'\s*(\S*)? "([^"]*)"', line)

                        for i, match in enumerate(matches):
                            var_res = match[0]
                            var_resname = match[1] if match[1] else None

                            # Utilizar el nombre del diccionario para la posición
                            index = len(variable_restric) + 1

                            variable_restric[f"var{index}_res"] = var_res
                            variable_resname[f"var{index}_resname"] = var_resname

            # Cambio de formato de las variables para poder integrarlas en el código de optimización

            variable_names = list(variable_names.values())
            variable_min = list(variable_min.values())
            variable_max = list(variable_max.values())
            variable_modo = list(variable_modo.values())

            variable_maxmin = list(variable_maxmin.values())
            variable_eq = list(variable_eq.values())
            variable_eqname = list(variable_eqname.values())

            variable_restric = list(variable_restric.values())
            variable_resname = list(variable_resname.values())

            # -----------------LECTURA DEL TXT---------------------------#

            ##############################################################

            # -----------------CÓDIGO DE OPTIMIZACIÓN--------------------#
            # Nombre del problema y elección de minimización o maximización
            prob = LpProblem(NombreProblema, eval(variable_maxmin[0]))

            # Las variables del problema
            for i in range(len(variable_names)):
                globals()[f'x{i + 1}'] = LpVariable(variable_names[i], variable_min[i], eval(variable_max[i]),
                                                    eval(variable_modo[i]))

            # La ecuación objetivo
            prob += eval(variable_eq[0]), variable_eqname[0]

            # Restricciones
            for i in range(len(variable_restric)):
                prob += eval(variable_restric[i]), variable_resname[i]

            # The problem data is written to an .lp file
            prob.writeLP(prob.name + ".lp")

            # Resolución del problema
            prob.solve()

            # Verificar el estado de la solución
            estado_solucion = LpStatus[prob.status]

            # Crear una etiqueta para mostrar la solución del problema
            texto_solucion_problema = "Solución del problema:\n"
            for v in prob.variables():
                texto_solucion_problema += f"{v.name} = {v.varValue}\n"

            if not frameGSResult.winfo_viewable():
                frameGSResult.grid()
                frameGSolver.columnconfigure((1, 2), weight=1)
            texto_solucion_objetivo = f"Solución objetivo: \n {variable_eqname[0]} {value(prob.objective)}"

            # Análisis de Sensibilidad
            if estado_solucion == "Optimal":
                sensibilidad_info = "\n\nAnálisis de Sensibilidad:\n"
                for name, c in prob.constraints.items():
                    dual_value = c.pi
                    sensibilidad_info += f"Shadow Price de {name}: {dual_value}\n"

                for v in prob.variables():
                    reduced_cost = v.dj
                    sensibilidad_info += f"Reduced Cost de {v.name}: {reduced_cost}\n"
            else:
                sensibilidad_info = "\n\nEl problema no tiene solución óptima."

            # Mostrar resultados
            textBoxResult.config(state="normal")
            textBoxResult.delete("1.0", tk.END)
            textBoxResult.insert("1.0", str(texto_solucion_problema) + "\n\n" + str(texto_solucion_objetivo) + str(
                sensibilidad_info))
            textBoxResult.config(state="disabled")

        except:
            textBoxResult.config(state="normal")
            textBoxResult.delete("1.0", tk.END)
            textBoxResult.insert("1.0", "Error al analizar los datos")
            textBoxResult.config(state="disabled")


def cmdGSCResultados():
    if frameGSResult.winfo_viewable():
        frameGSResult.grid_remove()
        frameGSolver.columnconfigure(2, weight=0)
    else:
        frameGSResult.grid()
        frameGSolver.columnconfigure((1, 2), weight=1)


def cmdTSCAtras():
    frameTSolver.pack_forget()
    frameMenu.pack(fill="none", expand=True)


def cmdTSCResolver():
    try:
        textBoxResultT.config(state="normal")
        textBoxResultT.delete("1.0", tk.END)
        textBoxResultT.insert("1.0", "Resolviendo...")
        textBoxResultT.config(state="disabled")

        num_almacenes = int(entryTSOpc1a.get())
        # capacidades_almacen = ""
        num_destinos = int(entryTSOpc1b.get())
        # demanda = ""

        capacidades_almacen = [int(input(f"Ingrese la capacidad del almacén {i}: ")) for i in
                               range(1, num_almacenes + 1)]
        demanda = [int(input(f"Ingrese la demanda para el destino {i}: ")) for i in range(1, num_destinos + 1)]

        costos_transporte = []
        for i in range(1, num_almacenes + 1):
            fila = [int(input(f"Ingrese el costo de transporte del almacén {i} al destino {j}: ")) for j in
                    range(1, num_destinos + 1)]
            costos_transporte.append(fila)

        Almacenes = [f"Almacen_{i}" for i in range(1, num_almacenes + 1)]
        Destinos = [f"Destino_{i}" for i in range(1, num_destinos + 1)]

        oferta = {a: capacidad for a, capacidad in zip(Almacenes, capacidades_almacen)}
        demanda = {d: d_ for d, d_ in zip(Destinos, demanda)}

        # Verificar si la oferta es mayor o igual a la demanda
        if sum(capacidades_almacen) < sum(demanda.values()):
            textBoxResultT.config(state="normal")
            textBoxResultT.delete("1.0", tk.END)
            textBoxResultT.insert("1.0", "No es posible satisfacer la demanda con la oferta actual.")
            textBoxResultT.config(state="disabled")
            return

        costos = makeDict([Almacenes, Destinos], costos_transporte, 0)

        prob = LpProblem("Problema_Distribucion_Cerveza", LpMinimize)

        Rutas = [(a, d) for a in Almacenes for d in Destinos]
        vars = LpVariable.dicts("Ruta", (Almacenes, Destinos), 0, None, LpInteger)

        prob += lpSum([vars[a][d] * costos[a][d] for (a, d) in Rutas]), "Suma_de_Costos_de_Transporte"

        for a in Almacenes:
            prob += lpSum([vars[a][d] for d in Destinos]) <= oferta[a], f"Suma_de_Productos_fuera_del_Almacen_{a}"

        for d in Destinos:
            prob += lpSum([vars[a][d] for a in Almacenes]) >= demanda[d], f"Suma_de_Productos_en_{d}"

        prob.solve()

        textBoxResultT.config(state="normal")
        textBoxResultT.delete("1.0", tk.END)

        textBoxResultT.insert("1.0", ("Estado:", LpStatus[prob.status]))
        textBoxResultT.insert(tk.END, "\n")

        for v in prob.variables():
            textBoxResultT.insert(tk.END,
                                  (v.name.replace('Ruta', 'Ruta').replace('Destino', 'Destino'), "=", v.varValue))
            textBoxResultT.insert(tk.END, "\n")

        textBoxResultT.insert(tk.END, ("\n" + "Costo Total de Transporte =" + str(value(prob.objective))))
        textBoxResultT.insert(tk.END, "\n")
        textBoxResultT.config(state="disabled")

    except:
        textBoxResultT.config(state="normal")
        textBoxResultT.delete("1.0", tk.END)
        textBoxResultT.insert("1.0", "Error en la lectura de los datos")
        textBoxResultT.config(state="disabled")


def cmdTSCResultados():
    if frameTSResult.winfo_viewable():
        frameTSResult.grid_remove()
        frameTSolver.columnconfigure(2, weight=0)
    else:
        frameTSResult.grid()
        frameTSolver.columnconfigure((1, 2), weight=1)


# ---------------------------- SHORTCUTS ----------------------------
root.bind("<Control-o>", keyCtrlO)
root.bind("<Control-w>", keyCtrlW)
root.bind("<Control-s>", keyCtrlS)
root.bind("<Control-S>", keyCtrlShiftS)

# --------------------- ELEMENTOS DE LA VENTANA ---------------------

# Barra de herramientas
# El color de la barra de herramientas no puede cambiarse en Windows
barraH = tk.Menu(root, background="#243654", fg="#EEEEEE")
# Submenús
submenu1 = tk.Menu(barraH, tearoff=0, bg="#243654", fg="#EEEEEE")
submenu2 = tk.Menu(barraH, tearoff=0, bg="#243654", fg="#EEEEEE")
submenu3 = tk.Menu(barraH, tearoff=0, bg="#243654", fg="#EEEEEE")
barraH.add_cascade(menu=submenu1, label="Archivo")
barraH.add_cascade(menu=submenu2, label="Opciones")
barraH.add_cascade(menu=submenu3, label="Ayuda")
# Submenú Archivo
submenu1.add_command(label="Abrir",
                     command=cmdArchivoAbrir,
                     underline=0,
                     compound=tk.LEFT,
                     accelerator="Ctrl+O"
                     )
submenu1.add_command(label="Cerrar",
                     command=cmdArchivoCerrar,
                     underline=0,
                     compound=tk.LEFT,
                     accelerator="Ctrl+W"
                     )
submenu1.add_command(label="Guardar",
                     command=cmdArchivoGuardar,
                     underline=0,
                     compound=tk.LEFT,
                     accelerator="Ctrl+S"
                     )
submenu1.add_command(label="Guardar como",
                     command=cmdArchivoGuardarComo,
                     underline=0,
                     compound=tk.LEFT,
                     accelerator="Ctrl+Shift+S"
                     )
submenu1.add_separator()
submenu1.add_command(label="Salir",
                     command=root.quit,
                     underline=0,
                     compound=tk.LEFT
                     )
# Submenú Opciones
# Submenú Ayuda
submenu3.add_command(label="Descanso...",
                     command=cmdAyuda,
                     underline=0,
                     compound=tk.LEFT)

# Frame del menú inicial
frameMenu = tk.Frame(
    root,
    bg="#243654",
    width=300,
    height=200,
)

# Frame de la sección de resolución por el método general
frameGSolver = tk.Frame(root, bg="#172235")

# Frame de la sección de resolución del problema de transportes
frameTSolver = tk.Frame(root, bg="#172235")

# Frame para darle tamaño a btnGSolver sin problemas
frameBtnGSolver = tk.Frame(frameMenu, width=250, height=50)

# Botón para pasar a la pantalla del método general
btnGSolver = tk.Button(
    frameBtnGSolver,
    text="Problema lineal general",
    font=("Aptos", 15),
    bg="#334B74",
    fg="#EEEEEE",
    activebackground="#425C8A",
    activeforeground="#FAFAFA",
    command=cmdGSolver,
    relief="flat",
    borderwidth=0
)

# Frame para darle tamaño a btnTSolver sin problemas
frameBtnTSolver = tk.Frame(frameMenu, width=250, height=50)

# Botón para pasar a la pantalla del problemas horarios
btnTSolver = tk.Button(
    frameBtnTSolver,
    text="Problema de logística",
    font=("Aptos", 15),
    bg="#334B74",
    fg="#EEEEEE",
    activebackground="#425C8A",
    activeforeground="#FAFAFA",
    command=cmdTSolver,
    relief="flat",
    borderwidth=0
)

# Frame del General Solver que contiene el menú de opciones
frameGSOpc = tk.Frame(
    frameGSolver,
    bg="#243654",
    width=300
)

# Frame del General Solver que contiene el menú de control
frameGSControl = tk.Frame(
    frameGSolver,
    bg="#243654",
    width=300,
    height=70
)

# Frame del General Solver que contiene el código
frameGSText = tk.Frame(
    frameGSolver,
    bg="#243654",
)

# Frame del General Solver que contiene los resultados
frameGSResult = tk.Frame(
    frameGSolver,
    bg="#243654",
)

# Textbox con scrollbar del GSolver
scrollbarTBV = tk.Scrollbar(frameGSText, orient=tk.VERTICAL)
scrollbarTBH = tk.Scrollbar(frameGSText, orient=tk.HORIZONTAL)
textBox = tk.Text(frameGSText,
                  wrap="none",
                  xscrollcommand=scrollbarTBH.set,
                  yscrollcommand=scrollbarTBV.set,
                  bg="#334B74",
                  fg="#EEEEEE",
                  font=("Aptos", 14),
                  selectbackground="#4F6A97",
                  undo=True
                  )
scrollbarTBV.configure(command=textBox.yview)
scrollbarTBH.configure(command=textBox.xview)

# Resultados del GSolver en textbox con scrollbar
scrollbarRV = tk.Scrollbar(frameGSResult, orient=tk.VERTICAL)
scrollbarRH = tk.Scrollbar(frameGSResult, orient=tk.HORIZONTAL)
textBoxResult = tk.Text(frameGSResult,
                        wrap="none",
                        xscrollcommand=scrollbarRH.set,
                        yscrollcommand=scrollbarRV.set,
                        bg="#243654",  # "#334B74",
                        fg="#EEEEEE",
                        font=("Aptos", 14),
                        selectbackground="#4F6A97",
                        undo=True,
                        state=tk.DISABLED
                        )
scrollbarRV.configure(command=textBoxResult.yview)
scrollbarRH.configure(command=textBoxResult.xview)

# Frame para darle tamaño a btnGSCAtras sin problemas
frameBtnGSCAtras = tk.Frame(frameGSControl, width=100, height=50)

# Botón para pasar a la pantalla del método general
btnGSCAtras = tk.Button(
    frameBtnGSCAtras,
    text="Atrás",
    font=("Aptos", 12),
    bg="#334B74",
    fg="#EEEEEE",
    activebackground="#425C8A",
    activeforeground="#FAFAFA",
    command=cmdGSCAtras,
    width=250,
    height=50,
    relief="flat",
    borderwidth=0
)

# Frame para darle tamaño a btnGSCResolver sin problemas
frameBtnGSCResolver = tk.Frame(frameGSControl, width=100, height=50)

# Botón para pasar a la pantalla del método general
btnGSCResolver = tk.Button(
    frameBtnGSCResolver,
    text="Resolver",
    font=("Aptos", 12),
    bg="#334B74",
    fg="#EEEEEE",
    activebackground="#425C8A",
    activeforeground="#FAFAFA",
    command=cmdGSCResolver,
    width=250,
    height=50,
    relief="flat",
    borderwidth=0
)

# Frame para darle tamaño a btnGSCAtras sin problemas
frameBtnGSCResultados = tk.Frame(frameGSControl, width=100, height=50)

# Botón para pasar a la pantalla del método general
btnGSCResultados = tk.Button(
    frameBtnGSCResultados,
    text="Resultados",
    font=("Aptos", 12),
    bg="#334B74",
    fg="#EEEEEE",
    activebackground="#425C8A",
    activeforeground="#FAFAFA",
    command=cmdGSCResultados,
    width=250,
    height=50,
    relief="flat",
    borderwidth=0
)

# CONTENIDO DEL PROBLEMA DE TRANSPORTES
# Frame del Transport Solver que contiene el menú de opciones
frameTSOpc = ct.CTkScrollableFrame(
    frameTSolver,
    fg_color="#243654",
    width=300
)

# Frame del Transport Solver que contiene el menú de control
frameTSControl = tk.Frame(
    frameTSolver,
    bg="#243654",
    width=320,
    height=70
)

# Frame del Transport Solver que contiene el código
frameTSText = tk.Frame(
    frameTSolver,
    bg="#243654",
)

# Frame del Transport Solver que contiene los resultados
frameTSResult = tk.Frame(
    frameTSolver,
    bg="#243654",
)

# Textbox con scrollbar del TSolver
scrollbarLBV = tk.Scrollbar(frameTSText, orient=tk.VERTICAL)
scrollbarLBH = tk.Scrollbar(frameTSText, orient=tk.HORIZONTAL)
textBoxT = tk.Text(frameTSText,
                   wrap="none",
                   xscrollcommand=scrollbarLBH.set,
                   yscrollcommand=scrollbarLBV.set,
                   bg="#334B74",
                   fg="#EEEEEE",
                   font=("Aptos", 14),
                   selectbackground="#4F6A97",
                   undo=True
                   )
scrollbarLBV.configure(command=textBoxT.yview)
scrollbarLBH.configure(command=textBoxT.xview)

# Resultados del TSolver en textbox con scrollbar
scrollbarLRV = tk.Scrollbar(frameTSResult, orient=tk.VERTICAL)
scrollbarLRH = tk.Scrollbar(frameTSResult, orient=tk.HORIZONTAL)
textBoxResultT = tk.Text(frameTSResult,
                         wrap="none",
                         xscrollcommand=scrollbarLRH.set,
                         yscrollcommand=scrollbarLRV.set,
                         bg="#243654",
                         fg="#EEEEEE",
                         font=("Aptos", 14),
                         selectbackground="#4F6A97",
                         undo=True,
                         state=tk.DISABLED
                         )
scrollbarRV.configure(command=textBoxResultT.yview)
scrollbarRH.configure(command=textBoxResultT.xview)

# Frame para darle tamaño a btnTSCAtras sin problemas
frameBtnTSCAtras = tk.Frame(frameTSControl, width=100, height=50)

# Botón para pasar a la pantalla del método general
btnTSCAtras = tk.Button(
    frameBtnTSCAtras,
    text="Atrás",
    font=("Aptos", 12),
    bg="#334B74",
    fg="#EEEEEE",
    activebackground="#425C8A",
    activeforeground="#FAFAFA",
    command=cmdTSCAtras,
    width=250,
    height=50,
    relief="flat",
    borderwidth=0
)

# Frame para darle tamaño a btnTSCResolver sin problemas
frameBtnTSCResolver = tk.Frame(frameTSControl, width=100, height=50)

# Botón para pasar a la pantalla del método general
btnTSCResolver = tk.Button(
    frameBtnTSCResolver,
    text="Resolver",
    font=("Aptos", 12),
    bg="#334B74",
    fg="#EEEEEE",
    activebackground="#425C8A",
    activeforeground="#FAFAFA",
    command=cmdTSCResolver,
    width=250,
    height=50,
    relief="flat",
    borderwidth=0
)

# Frame para darle tamaño a btnTSCAtras sin problemas
frameBtnTSCResultados = tk.Frame(frameTSControl, width=100, height=50)

# Botón para pasar a la pantalla del método general
btnTSCResultados = tk.Button(
    frameBtnTSCResultados,
    text="Resultados",
    font=("Aptos", 12),
    bg="#334B74",
    fg="#EEEEEE",
    activebackground="#425C8A",
    activeforeground="#FAFAFA",
    command=cmdTSCResultados,
    width=250,
    height=50,
    relief="flat",
    borderwidth=0
)

frameTSOpc1 = tk.Frame(
    frameTSOpc,
    bg="#334B74",
    # bg="red",
    height=30,
    width=300
)

labelTSOpc1a = tk.Label(
    frameTSOpc1,
    text="Número de almacenes:",
    font=("Aptos", 12),
    bg="#334B74",
    fg="#EEEEEE",
    height=1,
    width=20

)

# entryTSOpc1a = tk.Text(
#     frameTSOpc1,
#     font = ("Aptos", 12),
#     wrap = "none",
#     undo = True,
#     height = 2,
#     width = 10
# )

entryTSOpc1a = tk.Entry(
    frameTSOpc1,
    font=("Aptos", 12),
    width=7
)

frameTSOpcbtn = tk.Frame(frameTSOpc, height=60, width=100)
btnTSOpc = tk.Button(
    frameTSOpcbtn,
    text="Confirmar",
    font=("Aptos", 12),
    bg="#172235",
    fg="#EEEEEE",
    activebackground="#334B74",
    activeforeground="#FAFAFA",
    # command = ,
    relief="flat",
    borderwidth=0
)

labelTSOpc1b = tk.Label(
    frameTSOpc1,
    text="Número de destinos:",
    font=("Aptos", 12),
    bg="#334B74",
    fg="#EEEEEE",
    height=1,
    width=20

)

entryTSOpc1b = tk.Entry(
    frameTSOpc1,
    font=("Aptos", 12),
    width=7
)

# -------------------- COLOCACIÓN INICIAL Y BUCLE -------------------
# Barra de herramientas
root.config(menu=barraH)

# Pantalla Menú principal
frameMenu.grid_propagate(False)
frameMenu.pack(fill="none", expand=True)
frameMenu.columnconfigure(0, weight=1)
frameMenu.rowconfigure((0, 1, 2), weight=1)
frameBtnGSolver.grid(row=0, column=0, padx=10, pady=(20, 0))
frameBtnGSolver.pack_propagate(False)
btnGSolver.pack(fill="both", expand=True)
frameBtnTSolver.grid(row=1, column=0, padx=10, pady=(60, 20))
frameBtnTSolver.pack_propagate(False)
btnTSolver.pack(fill="both", expand=True)

# Pantalla General Solver
frameGSolver.columnconfigure(1, weight=1)
frameGSolver.rowconfigure(0, weight=1)
frameGSOpc.grid_propagate(False)
frameGSOpc.grid(row=0, column=0, padx=10, pady=(10, 0), sticky=tk.S + tk.N + tk.W)
frameGSControl.grid_propagate(False)
frameGSControl.grid(row=1, column=0, padx=10, pady=10, sticky=tk.S + tk.W)
frameGSControl.columnconfigure((0, 1, 2), weight=1)
frameGSControl.rowconfigure(0, weight=1)
frameGSText.grid_propagate(False)
frameGSText.grid(row=0, column=1, padx=(0, 10), pady=10, sticky=tk.N + tk.S + tk.W + tk.E, rowspan=2)
frameGSResult.grid_propagate(False)
frameGSResult.grid(row=0, column=2, padx=(0, 10), pady=10, sticky=tk.N + tk.S + tk.W + tk.E, rowspan=2)
frameGSResult.grid_remove()
# Frame con el textbox del GSolver
frameGSText.rowconfigure(0, weight=1)
frameGSText.columnconfigure(0, weight=1)
textBox.grid_propagate(True)
textBox.grid(row=0, column=0, padx=(10, 0), pady=(10, 0), sticky=tk.N + tk.S + tk.E + tk.W)
scrollbarTBV.grid(row=0, column=1, padx=(0, 10), pady=(10, 0), sticky="ns")
scrollbarTBH.grid(row=1, column=0, padx=(10, 0), pady=(0, 10), sticky="we")
# Frame con los resultados del GSolver
frameGSResult.rowconfigure(0, weight=1)
frameGSResult.columnconfigure(0, weight=1)
textBoxResult.grid_propagate(True)
textBoxResult.grid(row=0, column=0, padx=(10, 0), pady=(10, 0), sticky=tk.N + tk.S + tk.E + tk.W)
scrollbarRV.grid(row=0, column=1, padx=(0, 10), pady=(10, 0), sticky="ns")
scrollbarRH.grid(row=1, column=0, padx=(10, 0), pady=(0, 10), sticky="we")
# Frame de control del GSolver
frameBtnGSCAtras.pack_propagate(False)
frameBtnGSCAtras.grid(row=0, column=0, padx=(10, 0), pady=10)
btnGSCAtras.pack(expand=True)
frameBtnGSCResolver.pack_propagate(False)
frameBtnGSCResolver.grid(row=0, column=1, padx=10, pady=10)
btnGSCResolver.pack(expand=True)
frameBtnGSCResultados.pack_propagate(False)
frameBtnGSCResultados.grid(row=0, column=2, padx=(0, 10), pady=10)
btnGSCResultados.pack(expand=True)

# Pantalla Problema de transportes
frameTSolver.columnconfigure(1, weight=1)
frameTSolver.rowconfigure(0, weight=1)
# frameTSOpc.grid_propagate()
frameTSOpc.grid(row=0, column=0, padx=10, pady=(10, 0), sticky=tk.S + tk.N + tk.W)
frameTSControl.grid_propagate(False)
frameTSControl.grid(row=1, column=0, padx=10, pady=10, sticky=tk.S + tk.W)
frameTSControl.columnconfigure((0, 1, 2), weight=1)
frameTSControl.rowconfigure(0, weight=1)
frameTSText.grid_propagate(False)
frameTSText.grid(row=0, column=1, padx=(0, 10), pady=10, sticky=tk.N + tk.S + tk.W + tk.E, rowspan=2)
frameTSResult.grid_propagate(False)
frameTSResult.grid(row=0, column=2, padx=(0, 10), pady=10, sticky=tk.N + tk.S + tk.W + tk.E, rowspan=2)
frameTSResult.grid_remove()
# Frame con el textbox del TSolver
frameTSText.rowconfigure(0, weight=1)
frameTSText.columnconfigure(0, weight=1)
textBoxT.grid_propagate(True)
textBoxT.grid(row=0, column=0, padx=(10, 0), pady=(10, 0), sticky=tk.N + tk.S + tk.E + tk.W)
scrollbarLBV.grid(row=0, column=1, padx=(0, 10), pady=(10, 0), sticky="ns")
scrollbarLBH.grid(row=1, column=0, padx=(10, 0), pady=(0, 10), sticky="we")
# Frame con los resultados del TSolver
frameTSResult.rowconfigure(0, weight=1)
frameTSResult.columnconfigure(0, weight=1)
textBoxResultT.grid_propagate(True)
textBoxResultT.grid(row=0, column=0, padx=(10, 0), pady=(10, 0), sticky=tk.N + tk.S + tk.E + tk.W)
scrollbarLRV.grid(row=0, column=1, padx=(0, 10), pady=(10, 0), sticky="ns")
scrollbarLRH.grid(row=1, column=0, padx=(10, 0), pady=(0, 10), sticky="we")
# Frame de control del TSolver
frameBtnTSCAtras.pack_propagate(False)
frameBtnTSCAtras.grid(row=0, column=0, padx=(10, 0), pady=10)
btnTSCAtras.pack(expand=True)
frameBtnTSCResolver.pack_propagate(False)
frameBtnTSCResolver.grid(row=0, column=1, padx=10, pady=10)
btnTSCResolver.pack(expand=True)
frameBtnTSCResultados.pack_propagate(False)
frameBtnTSCResultados.grid(row=0, column=2, padx=(0, 10), pady=10)
btnTSCResultados.pack(expand=True)
# Frame con las opciones del TSolver
frameTSOpc1.grid(row=0, column=0, padx=(10, 20), pady=10, sticky="nwe")
labelTSOpc1a.grid(row=0, column=0, padx=10, pady=10, sticky="nw")
entryTSOpc1a.grid(row=0, column=1, padx=(0, 10), pady=(10,), sticky="ne")
labelTSOpc1b.grid(row=1, column=0, padx=10, pady=10, sticky="nw")
entryTSOpc1b.grid(row=1, column=1, padx=(0, 10), pady=(10,), sticky="ne")
frameTSOpcbtn.grid(row=1, column=0, padx=(10, 20), pady=10, sticky="nwe")
frameTSOpcbtn.pack_propagate(True)
btnTSOpc.pack(expand=True, fill="both")
btnTSOpc.pack_propagate(True)

root.mainloop()  # Se encarga de actualizar los cambios sobre la ventana constantemente
