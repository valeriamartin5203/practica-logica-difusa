
import os
import csv
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

import customtkinter as ctk

from logica_difusa import EvaluadorDifuso
from graficas import crear_graficas, crear_grafica_estadisticas

# ==========================================
# COLORES
# ==========================================

ROSA = "#D987AE"
ROSA_OSCURO = "#C66F99"
ROSA_CLARO = "#FCE8F1"
FONDO = "#FFF5FA"
TEXTO = "#793D5C"
MORADO = "#B77ACB"
BLANCO = "#FFFFFF"

CARPETA_DATOS = "datos"
ARCHIVO_ESTUDIANTES = os.path.join(CARPETA_DATOS, "estudiantes.csv")
ARCHIVO_EVALUACIONES = os.path.join(CARPETA_DATOS, "evaluaciones.csv")

# ==========================================
# ARCHIVOS CSV
# ==========================================

def preparar_archivos():

    os.makedirs(CARPETA_DATOS, exist_ok=True)

    archivos = {
        ARCHIVO_ESTUDIANTES: [
            "matricula", "nombre", "grupo"
        ],
        ARCHIVO_EVALUACIONES: [
            "fecha", "matricula", "nombre", "grupo",
            "horas", "calificacion", "resultado", "nivel"
        ]
    }

    for ruta, columnas in archivos.items():

        if not os.path.exists(ruta):

            with open(
                ruta, "w",
                newline="",
                encoding="utf-8-sig"
            ) as archivo:

                escritor = csv.DictWriter(
                    archivo,
                    fieldnames=columnas
                )

                escritor.writeheader()

def leer_csv(ruta):

    with open(
        ruta, "r",
        newline="",
        encoding="utf-8-sig"
    ) as archivo:

        return list(csv.DictReader(archivo))

def guardar_estudiante(matricula, nombre, grupo):

    estudiantes = leer_csv(ARCHIVO_ESTUDIANTES)

    encontrado = False

    for estudiante in estudiantes:

        if estudiante["matricula"] == matricula:

            estudiante["nombre"] = nombre
            estudiante["grupo"] = grupo

            encontrado = True
            break

    if not encontrado:

        estudiantes.append({
            "matricula": matricula,
            "nombre": nombre,
            "grupo": grupo
        })

    with open(
        ARCHIVO_ESTUDIANTES, "w",
        newline="",
        encoding="utf-8-sig"
    ) as archivo:

        escritor = csv.DictWriter(
            archivo,
            fieldnames=["matricula", "nombre", "grupo"]
        )

        escritor.writeheader()
        escritor.writerows(estudiantes)

def guardar_evaluacion(registro):

    columnas = [
        "fecha", "matricula", "nombre", "grupo",
        "horas", "calificacion", "resultado", "nivel"
    ]

    with open(
        ARCHIVO_EVALUACIONES, "a",
        newline="",
        encoding="utf-8-sig"
    ) as archivo:

        escritor = csv.DictWriter(
            archivo,
            fieldnames=columnas
        )

        escritor.writerow(registro)

# ==========================================
# APLICACIÓN PRINCIPAL
# ==========================================

class Aplicacion(ctk.CTk):

    def __init__(self):

        super().__init__()

        preparar_archivos()

        self.title("Student Performance AI")
        self.geometry("1280x900")
        self.minsize(1050, 750)

        self.configure(fg_color=FONDO)

        self.evaluador = EvaluadorDifuso()
        self.ultimo_resultado = None

        self.crear_interfaz()

        self.actualizar_estudiantes()
        self.actualizar_estadisticas()

    # ======================================
    # INTERFAZ GENERAL
    # ======================================

    def crear_interfaz(self):

        encabezado = ctk.CTkFrame(
            self,
            fg_color="#F5D5E5",
            corner_radius=18
        )

        encabezado.pack(
            fill="x",
            padx=20,
            pady=(15, 10)
        )

        ctk.CTkLabel(
            encabezado,
            text="Student Performance AI",
            font=("Arial", 28, "bold"),
            text_color=TEXTO
        ).pack(pady=(14, 3))

        ctk.CTkLabel(
            encabezado,
            text="Sistema inteligente de evaluación con lógica difusa",
            font=("Arial", 13),
            text_color="#905D78"
        ).pack(pady=(0, 14))

        self.pestanas = ctk.CTkTabview(
            self,
            fg_color=BLANCO,
            segmented_button_fg_color="#F5DCE9",
            segmented_button_selected_color=ROSA,
            segmented_button_selected_hover_color=ROSA_OSCURO,
            segmented_button_unselected_color="#F5DCE9",
            text_color=TEXTO
        )

        self.pestanas.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 18)
        )

        self.tab_evaluar = self.pestanas.add("Evaluar")
        self.tab_graficas = self.pestanas.add("Gráficas")
        self.tab_reglas = self.pestanas.add("Reglas")
        self.tab_estudiantes = self.pestanas.add("Estudiantes")
        self.tab_estadisticas = self.pestanas.add("Estadísticas")

        self.crear_tab_evaluar()
        self.crear_tab_graficas()
        self.crear_tab_reglas()
        self.crear_tab_estudiantes()
        self.crear_tab_estadisticas()

    # ======================================
    # ENTRADAS
    # ======================================

    def crear_entrada(self, contenedor, texto):

        entrada = ctk.CTkEntry(
            contenedor,
            width=340,
            height=40,
            placeholder_text=texto
        )

        entrada.pack(pady=6)

        return entrada

    # ======================================
    # PESTAÑA 1: EVALUAR
    # ======================================

    def crear_tab_evaluar(self):

        principal = ctk.CTkScrollableFrame(
            self.tab_evaluar,
            fg_color="transparent"
        )

        principal.pack(
            fill="both",
            expand=True,
            padx=12,
            pady=10
        )

        ctk.CTkLabel(
            principal,
            text="Registro y evaluación del estudiante",
            font=("Arial", 23, "bold"),
            text_color=TEXTO
        ).pack(pady=(10, 15))

        tarjeta = ctk.CTkFrame(
            principal,
            fg_color=ROSA_CLARO,
            corner_radius=16
        )

        tarjeta.pack(
            fill="x",
            padx=35,
            pady=8
        )

        ctk.CTkLabel(
            tarjeta,
            text="Datos del estudiante",
            font=("Arial", 17, "bold"),
            text_color=TEXTO
        ).pack(pady=(15, 5))

        self.entrada_nombre = self.crear_entrada(
            tarjeta, "Nombre completo"
        )

        self.entrada_matricula = self.crear_entrada(
            tarjeta, "Matrícula"
        )

        self.entrada_grupo = self.crear_entrada(
            tarjeta, "Grupo"
        )

        ctk.CTkButton(
            tarjeta,
            text="Registrar estudiante",
            fg_color=MORADO,
            hover_color="#9965AE",
            command=self.registrar_estudiante
        ).pack(pady=(8, 15))

        ctk.CTkLabel(
            principal,
            text="Datos académicos",
            font=("Arial", 18, "bold"),
            text_color=TEXTO
        ).pack(pady=(18, 5))

        self.entrada_horas = self.crear_entrada(
            principal,
            "Horas de estudio por semana (0 a 12)"
        )

        self.entrada_calificacion = self.crear_entrada(
            principal,
            "Calificación obtenida (0 a 100)"
        )

        ctk.CTkButton(
            principal,
            text="CALCULAR RENDIMIENTO",
            width=280,
            height=46,
            corner_radius=12,
            fg_color=ROSA,
            hover_color=ROSA_OSCURO,
            font=("Arial", 15, "bold"),
            command=self.evaluar_estudiante
        ).pack(pady=18)

        self.tarjeta_resultado = ctk.CTkFrame(
            principal,
            fg_color=ROSA_CLARO,
            corner_radius=16
        )

        self.tarjeta_resultado.pack(
            fill="x",
            padx=35,
            pady=8
        )

        self.texto_resultado = ctk.CTkLabel(
            self.tarjeta_resultado,
            text="Tu resultado aparecerá aquí",
            font=("Arial", 21, "bold"),
            text_color=TEXTO
        )

        self.texto_resultado.pack(pady=(17, 5))

        self.texto_descripcion = ctk.CTkLabel(
            self.tarjeta_resultado,
            text="Completa los datos para realizar una evaluación.",
            font=("Arial", 13),
            text_color="#905D78",
            wraplength=750
        )

        self.texto_descripcion.pack(pady=(5, 17))

        ctk.CTkButton(
            principal,
            text="Limpiar campos",
            fg_color="#BFA4B5",
            hover_color="#A88C9E",
            command=self.limpiar_campos
        ).pack(pady=10)

    # ======================================
    # REGISTRAR ESTUDIANTE
    # ======================================

    def registrar_estudiante(self):

        nombre = self.entrada_nombre.get().strip()
        matricula = self.entrada_matricula.get().strip()
        grupo = self.entrada_grupo.get().strip()

        if not nombre or not matricula or not grupo:

            messagebox.showwarning(
                "Datos incompletos",
                "Escribe nombre, matrícula y grupo."
            )

            return

        guardar_estudiante(
            matricula,
            nombre,
            grupo
        )

        self.actualizar_estudiantes()
        self.actualizar_estadisticas()

        messagebox.showinfo(
            "Registro exitoso",
            "El estudiante se guardó correctamente."
        )

    # ======================================
    # EVALUAR ESTUDIANTE
    # ======================================

    def evaluar_estudiante(self):

        try:

            nombre = self.entrada_nombre.get().strip()
            matricula = self.entrada_matricula.get().strip()
            grupo = self.entrada_grupo.get().strip()

            if not nombre or not matricula or not grupo:

                messagebox.showwarning(
                    "Datos incompletos",
                    "Primero completa nombre, matrícula y grupo."
                )

                return

            horas = float(self.entrada_horas.get())
            calificacion = float(
                self.entrada_calificacion.get()
            )

            if not 0 <= horas <= 12:

                messagebox.showwarning(
                    "Horas incorrectas",
                    "Las horas deben estar entre 0 y 12."
                )

                return

            if not 0 <= calificacion <= 100:

                messagebox.showwarning(
                    "Calificación incorrecta",
                    "La calificación debe estar entre 0 y 100."
                )

                return

            # EJECUTAR SISTEMA DIFUSO

            resultado, nivel, descripcion, datos = (
                self.evaluador.evaluar(
                    horas,
                    calificacion
                )
            )

            # GUARDAR ESTUDIANTE

            guardar_estudiante(
                matricula,
                nombre,
                grupo
            )

            # GUARDAR EVALUACIÓN

            registro = {
                "fecha": datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                "matricula": matricula,
                "nombre": nombre,
                "grupo": grupo,
                "horas": horas,
                "calificacion": calificacion,
                "resultado": round(resultado, 2),
                "nivel": nivel
            }

            guardar_evaluacion(registro)

            self.ultimo_resultado = datos

            # MOSTRAR RESULTADO

            self.texto_resultado.configure(
                text=f"{resultado:.2f}% — RENDIMIENTO {nivel}"
            )

            self.texto_descripcion.configure(
                text=descripcion
            )

            # ACTUALIZAR OTRAS PESTAÑAS

            self.actualizar_matriz(datos)

            self.graficas.actualizar(datos)

            self.dibujar_medidor(resultado, nivel)

            self.actualizar_estudiantes()

            self.actualizar_estadisticas()

            messagebox.showinfo(
                "Evaluación completada",
                f"Estudiante: {nombre}\n"
                f"Resultado: {resultado:.2f}%\n"
                f"Nivel: {nivel}"
            )

        except ValueError:

            messagebox.showerror(
                "Dato incorrecto",
                "Horas y calificación deben ser números válidos."
            )

        except Exception as error:

            messagebox.showerror(
                "Error de evaluación",
                f"No se pudo completar la evaluación:\n{error}"
            )

    # ======================================
    # LIMPIAR CAMPOS
    # ======================================

    def limpiar_campos(self):

        entradas = [
            self.entrada_nombre,
            self.entrada_matricula,
            self.entrada_grupo,
            self.entrada_horas,
            self.entrada_calificacion
        ]

        for entrada in entradas:
            entrada.delete(0, "end")

    # ======================================
    # PESTAÑA 2: GRÁFICAS
    # ======================================

    def crear_tab_graficas(self):

        ctk.CTkLabel(
            self.tab_graficas,
            text="Análisis visual de las funciones de pertenencia",
            font=("Arial", 20, "bold"),
            text_color=TEXTO
        ).pack(pady=(12, 0))

        contenedor = ctk.CTkFrame(
            self.tab_graficas,
            fg_color="transparent"
        )

        contenedor.pack(
            fill="both",
            expand=True
        )

        self.graficas = crear_graficas(contenedor)

    # ======================================
    # PESTAÑA 3: REGLAS
    # ======================================

    def crear_tab_reglas(self):

        principal = ctk.CTkScrollableFrame(
            self.tab_reglas,
            fg_color="transparent"
        )

        principal.pack(
            fill="both",
            expand=True,
            padx=12,
            pady=8
        )

        ctk.CTkLabel(
            principal,
            text="Centro de reglas difusas",
            font=("Arial", 24, "bold"),
            text_color=TEXTO
        ).pack(pady=(10, 3))

        ctk.CTkLabel(
            principal,
            text="Matriz de activación de las nueve reglas Mamdani",
            font=("Arial", 13),
            text_color="#986B83"
        ).pack(pady=(0, 12))

        tarjeta = ctk.CTkFrame(
            principal,
            fg_color=ROSA_CLARO,
            corner_radius=16
        )

        tarjeta.pack(
            fill="x",
            padx=20,
            pady=8
        )

        ctk.CTkLabel(
            tarjeta,
            text="Matriz de activación",
            font=("Arial", 18, "bold"),
            text_color=TEXTO
        ).pack(pady=(15, 3))

        ctk.CTkLabel(
            tarjeta,
            text="Filas: calificación  |  Columnas: horas de estudio",
            font=("Arial", 12),
            text_color="#986B83"
        ).pack(pady=(0, 8))

        tabla = ctk.CTkFrame(
            tarjeta,
            fg_color="transparent"
        )

        tabla.pack(pady=5)

        encabezados = [
            "Calificación / Horas",
            "Pocas",
            "Moderadas",
            "Muchas"
        ]

        for columna, texto in enumerate(encabezados):

            ctk.CTkLabel(
                tabla,
                text=texto,
                width=130,
                font=("Arial", 11, "bold"),
                text_color=TEXTO
            ).grid(
                row=0,
                column=columna,
                padx=4,
                pady=7
            )

        self.celdas_matriz = []

        for fila, nombre in enumerate(
            ["Baja", "Regular", "Alta"]
        ):

            ctk.CTkLabel(
                tabla,
                text=nombre,
                width=130,
                font=("Arial", 12, "bold"),
                text_color=TEXTO
            ).grid(
                row=fila + 1,
                column=0,
                padx=4,
                pady=6
            )

            fila_celdas = []

            for columna in range(3):

                celda = ctk.CTkLabel(
                    tabla,
                    text="0.000\n0%",
                    width=130,
                    height=62,
                    corner_radius=10,
                    fg_color="#F4D4E3",
                    text_color="#986B83",
                    font=("Arial", 13, "bold")
                )

                celda.grid(
                    row=fila + 1,
                    column=columna + 1,
                    padx=4,
                    pady=6
                )

                fila_celdas.append(celda)

            self.celdas_matriz.append(fila_celdas)

        self.texto_matriz = ctk.CTkLabel(
            tarjeta,
            text="Realiza una evaluación para activar las reglas.",
            font=("Arial", 13, "bold"),
            text_color=TEXTO
        )

        self.texto_matriz.pack(pady=(8, 5))

        # LEYENDA

        leyenda = ctk.CTkFrame(
            tarjeta,
            fg_color="transparent"
        )

        leyenda.pack(pady=(3, 15))

        for color, texto in [
            ("#F4D4E3", "Sin activación"),
            ("#E8A9C6", "Baja"),
            (ROSA, "Alta")
        ]:

            ctk.CTkLabel(
                leyenda,
                text=f"● {texto}",
                text_color=color,
                font=("Arial", 11, "bold")
            ).pack(side="left", padx=10)

        # DETALLE DE REGLAS

        ctk.CTkLabel(
            principal,
            text="Detalle de las nueve reglas",
            font=("Arial", 19, "bold"),
            text_color=TEXTO
        ).pack(pady=(17, 8))

        contenedor_reglas = ctk.CTkFrame(
            principal,
            fg_color="transparent"
        )

        contenedor_reglas.pack(
            fill="x",
            padx=8
        )

        for columna in range(3):
            contenedor_reglas.grid_columnconfigure(
                columna,
                weight=1
            )

        descripciones = [
            "Pocas horas + calificación baja → rendimiento bajo",
            "Pocas horas + calificación regular → rendimiento bajo",
            "Pocas horas + calificación alta → rendimiento medio",
            "Horas moderadas + calificación baja → rendimiento bajo",
            "Horas moderadas + calificación regular → rendimiento medio",
            "Horas moderadas + calificación alta → rendimiento alto",
            "Muchas horas + calificación baja → rendimiento medio",
            "Muchas horas + calificación regular → rendimiento alto",
            "Muchas horas + calificación alta → rendimiento alto"
        ]

        self.tarjetas_reglas = []

        for i, descripcion in enumerate(descripciones):

            marco = ctk.CTkFrame(
                contenedor_reglas,
                fg_color="#FFF0F6",
                corner_radius=12,
                border_width=1,
                border_color="#F0C9DC"
            )

            marco.grid(
                row=i // 3,
                column=i % 3,
                padx=5,
                pady=5,
                sticky="nsew"
            )

            ctk.CTkLabel(
                marco,
                text=f"REGLA {i + 1}",
                font=("Arial", 12, "bold"),
                text_color="#B45D88"
            ).pack(
                anchor="w",
                padx=10,
                pady=(10, 4)
            )

            ctk.CTkLabel(
                marco,
                text=descripcion,
                font=("Arial", 11),
                text_color=TEXTO,
                wraplength=220,
                justify="left"
            ).pack(
                fill="x",
                padx=10,
                pady=4
            )

            etiqueta = ctk.CTkLabel(
                marco,
                text="Activación: 0.000 (0%)",
                font=("Arial", 10, "bold"),
                text_color="#986B83"
            )

            etiqueta.pack(
                anchor="w",
                padx=10,
                pady=(4, 10)
            )

            self.tarjetas_reglas.append({
                "marco": marco,
                "activacion": etiqueta
            })

    # ======================================
    # ACTUALIZAR MATRIZ DE REGLAS
    # ======================================

    def actualizar_matriz(self, datos):

        # La matriz se construye a partir de las
        # activaciones que devuelve logica_difusa.py.

        matriz = [
            [0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0]
        ]

        filas = {
            "baja": 0,
            "regular": 1,
            "alta": 2
        }

        columnas = {
            "pocas": 0,
            "moderadas": 1,
            "muchas": 2
        }

        reglas = datos.get("reglas_activadas", [])

        for regla in reglas:

            fila = filas[regla["calificacion"]]
            columna = columnas[regla["horas"]]

            matriz[fila][columna] = float(
                regla["activacion"]
            )

        # ACTUALIZAR CELDAS

        for fila in range(3):

            for columna in range(3):

                valor = matriz[fila][columna]

                if valor <= 0:
                    color = "#F4D4E3"
                    color_texto = "#986B83"

                elif valor < 0.5:
                    color = "#E8A9C6"
                    color_texto = TEXTO

                else:
                    color = ROSA
                    color_texto = BLANCO

                self.celdas_matriz[fila][columna].configure(
                    text=f"{valor:.3f}\n{valor * 100:.1f}%",
                    fg_color=color,
                    text_color=color_texto
                )

        # ACTUALIZAR TARJETAS

        activadas = 0

        for i, regla in enumerate(reglas):

            valor = float(regla["activacion"])

            if valor > 0:

                activadas += 1

                color = "#FCE0ED"
                borde = ROSA
                color_texto = TEXTO

            else:

                color = "#FFF0F6"
                borde = "#F0C9DC"
                color_texto = "#986B83"

            self.tarjetas_reglas[i]["marco"].configure(
                fg_color=color,
                border_color=borde
            )

            self.tarjetas_reglas[i]["activacion"].configure(
                text=(
                    f"Activación: {valor:.3f} "
                    f"({valor * 100:.1f}%)"
                ),
                text_color=color_texto
            )

        self.texto_matriz.configure(
            text=f"Reglas activadas: {activadas} de 9"
        )

    # ======================================
    # PESTAÑA 4: ESTUDIANTES
    # ======================================

    def crear_tab_estudiantes(self):

        ctk.CTkLabel(
            self.tab_estudiantes,
            text="Registro de estudiantes",
            font=("Arial", 22, "bold"),
            text_color=TEXTO
        ).pack(pady=15)

        ctk.CTkLabel(
            self.tab_estudiantes,
            text="Los registros se guardan automáticamente en estudiantes.csv",
            font=("Arial", 12),
            text_color="#986B83"
        ).pack(pady=(0, 8))

        self.tabla_estudiantes = ctk.CTkTextbox(
            self.tab_estudiantes,
            fg_color=FONDO,
            text_color=TEXTO,
            font=("Consolas", 12)
        )

        self.tabla_estudiantes.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        ctk.CTkButton(
            self.tab_estudiantes,
            text="Actualizar lista",
            fg_color=ROSA,
            hover_color=ROSA_OSCURO,
            command=self.actualizar_estudiantes
        ).pack(pady=10)

    # ======================================
    # ACTUALIZAR LISTA DE ESTUDIANTES
    # ======================================

    def actualizar_estudiantes(self):

        estudiantes = leer_csv(ARCHIVO_ESTUDIANTES)

        self.tabla_estudiantes.configure(
            state="normal"
        )

        self.tabla_estudiantes.delete(
            "1.0",
            "end"
        )

        self.tabla_estudiantes.insert(
            "end",
            f"{'MATRÍCULA':<18}"
            f"{'NOMBRE':<32}"
            f"{'GRUPO':<15}\n"
        )

        self.tabla_estudiantes.insert(
            "end",
            "-" * 65 + "\n"
        )

        for estudiante in estudiantes:

            self.tabla_estudiantes.insert(
                "end",
                f"{estudiante['matricula']:<18}"
                f"{estudiante['nombre']:<32}"
                f"{estudiante['grupo']:<15}\n"
            )

        self.tabla_estudiantes.configure(
            state="disabled"
        )

    # ======================================
    # PESTAÑA 5: ESTADÍSTICAS
    # ======================================

    def crear_tab_estadisticas(self):

        # CONTENEDOR DESPLAZABLE
        # Evita que los elementos se encimen
        # cuando la ventana tiene poco espacio.

        principal = ctk.CTkScrollableFrame(
            self.tab_estadisticas,
            fg_color="transparent"
        )

        principal.pack(
            fill="both",
            expand=True,
            padx=8,
            pady=5
        )

        ctk.CTkLabel(
            principal,
            text="Estadísticas generales",
            font=("Arial", 23, "bold"),
            text_color=TEXTO
        ).pack(pady=(10, 8))

        # TARJETAS DE ESTADÍSTICAS

        tarjetas = ctk.CTkFrame(
            principal,
            fg_color="transparent"
        )

        tarjetas.pack(
            fill="x",
            padx=12,
            pady=5
        )

        for columna in range(3):

            tarjetas.grid_columnconfigure(
                columna,
                weight=1
            )

        self.total_estudiantes = self.crear_tarjeta(
            tarjetas,
            "Estudiantes registrados",
            "0",
            0
        )

        self.total_evaluaciones = self.crear_tarjeta(
            tarjetas,
            "Evaluaciones realizadas",
            "0",
            1
        )

        self.promedio_general = self.crear_tarjeta(
            tarjetas,
            "Promedio general",
            "0%",
            2
        )

        # MEDIDOR CIRCULAR

        ctk.CTkLabel(
            principal,
            text="Último rendimiento evaluado",
            font=("Arial", 17, "bold"),
            text_color=TEXTO
        ).pack(pady=(15, 3))

        contenedor_medidor = ctk.CTkFrame(
            principal,
            fg_color=BLANCO,
            corner_radius=15
        )

        contenedor_medidor.pack(
            pady=5
        )

        self.medidor = tk.Canvas(
            contenedor_medidor,
            width=270,
            height=180,
            bg=BLANCO,
            highlightthickness=0
        )

        self.medidor.pack(
            padx=10,
            pady=5
        )

        self.dibujar_medidor(
            0,
            "SIN DATOS"
        )

        # GRÁFICA COMPARATIVA

        ctk.CTkLabel(
            principal,
            text="Comparación entre estudiantes",
            font=("Arial", 17, "bold"),
            text_color=TEXTO
        ).pack(pady=(15, 5))

        ctk.CTkLabel(
            principal,
            text="Se muestra el promedio de rendimiento de cada estudiante.",
            font=("Arial", 12),
            text_color="#986B83"
        ).pack(pady=(0, 5))

        contenedor_grafica = ctk.CTkFrame(
            principal,
            fg_color=FONDO,
            corner_radius=12,
            height=360
        )

        contenedor_grafica.pack(
            fill="x",
            expand=True,
            padx=10,
            pady=(5, 15)
        )

        contenedor_grafica.pack_propagate(False)

        self.grafica_estadisticas = crear_grafica_estadisticas(
            contenedor_grafica
        )

    # ======================================
    # TARJETAS DE ESTADÍSTICAS
    # ======================================

    def crear_tarjeta(
        self,
        contenedor,
        titulo,
        valor,
        columna
    ):

        tarjeta = ctk.CTkFrame(
            contenedor,
            fg_color=ROSA_CLARO,
            corner_radius=14
        )

        tarjeta.grid(
            row=0,
            column=columna,
            padx=6,
            pady=7,
            sticky="nsew"
        )

        ctk.CTkLabel(
            tarjeta,
            text=titulo,
            font=("Arial", 11),
            text_color="#905D78"
        ).pack(pady=(12, 3))

        etiqueta = ctk.CTkLabel(
            tarjeta,
            text=valor,
            font=("Arial", 22, "bold"),
            text_color=TEXTO
        )

        etiqueta.pack(pady=(0, 12))

        return etiqueta

    # ======================================
    # MEDIDOR DE RENDIMIENTO
    # ======================================

    def dibujar_medidor(self, valor, nivel):

        self.medidor.delete("all")

        valor = max(0, min(float(valor), 100))

        colores = {
            "BAJO": "#E68AA5",
            "MEDIO": MORADO,
            "ALTO": ROSA,
            "SIN DATOS": "#D8C5D0"
        }

        color = colores.get(
            nivel,
            ROSA
        )

        # FONDO DEL MEDIDOR

        self.medidor.create_arc(
            20, 5, 250, 235,
            start=0,
            extent=180,
            style="arc",
            outline="#F2DCE7",
            width=19
        )

        # PROGRESO DEL MEDIDOR

        if valor > 0:

            self.medidor.create_arc(
                20, 5, 250, 235,
                start=0,
                extent=180 * valor / 100,
                style="arc",
                outline=color,
                width=19
            )

        # PORCENTAJE

        self.medidor.create_text(
            135,
            125,
            text=f"{valor:.1f}%",
            font=("Arial", 27, "bold"),
            fill=TEXTO
        )

        # NIVEL

        self.medidor.create_text(
            135,
            157,
            text=nivel,
            font=("Arial", 12, "bold"),
            fill=color
        )

    # ======================================
    # ACTUALIZAR ESTADÍSTICAS
    # ======================================

    def actualizar_estadisticas(self):

        estudiantes = leer_csv(
            ARCHIVO_ESTUDIANTES
        )

        evaluaciones = leer_csv(
            ARCHIVO_EVALUACIONES
        )

        total = len(evaluaciones)

        promedio = (
            sum(
                float(e["resultado"])
                for e in evaluaciones
            ) / total
            if total else 0
        )

        self.total_estudiantes.configure(
            text=str(len(estudiantes))
        )

        self.total_evaluaciones.configure(
            text=str(total)
        )

        self.promedio_general.configure(
            text=f"{promedio:.2f}%"
        )

        # ACTUALIZAR GRÁFICA

        self.grafica_estadisticas.actualizar(
            evaluaciones
        )

        # MOSTRAR ÚLTIMO RESULTADO GUARDADO

        if evaluaciones and self.ultimo_resultado is None:

            ultimo = evaluaciones[-1]

            self.dibujar_medidor(
                float(ultimo["resultado"]),
                ultimo["nivel"]
            )

# ==========================================
# INICIAR PROGRAMA
# ==========================================

if __name__ == "__main__":

    app = Aplicacion()
    app.mainloop()