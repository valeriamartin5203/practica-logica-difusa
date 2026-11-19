
import numpy as np
import matplotlib.pyplot as plt
import skfuzzy as fuzz

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# ==========================================
# COLORES DEL PROYECTO
# ==========================================

ROSA = "#D987AE"
ROSA_CLARO = "#E6A4C5"
MORADO = "#B77ACB"
FONDO = "#FFF5FA"
TEXTO = "#793D5C"
BLANCO = "#FFFFFF"


plt.rcParams["font.family"] = "DejaVu Sans"


# ==========================================
# GRÁFICAS DEL SISTEMA DIFUSO
# ==========================================

class GraficasDifusas:

    def __init__(self, contenedor):

        self.figura, self.ejes = plt.subplots(
            1, 3,
            figsize=(12, 4.5),
            dpi=90
        )

        self.figura.patch.set_facecolor(FONDO)

        self.canvas = FigureCanvasTkAgg(
            self.figura,
            master=contenedor
        )

        self.canvas.get_tk_widget().pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        self.dibujar_iniciales()

    # ======================================
    # GRÁFICAS INICIALES
    # ======================================

    def dibujar_iniciales(self):

        ax1, ax2, ax3 = self.ejes

        x_horas = np.arange(0, 12.1, 0.1)
        x = np.arange(0, 101, 1)

        # HORAS

        ax1.plot(
            x_horas,
            fuzz.trimf(x_horas, [0, 0, 4]),
            color=ROSA,
            linewidth=2,
            label="Pocas"
        )

        ax1.plot(
            x_horas,
            fuzz.trimf(x_horas, [2, 6, 10]),
            color=MORADO,
            linewidth=2,
            label="Moderadas"
        )

        ax1.plot(
            x_horas,
            fuzz.trimf(x_horas, [8, 12, 12]),
            color=ROSA_CLARO,
            linewidth=2,
            label="Muchas"
        )

        self.estilizar(
            ax1, "Horas de estudio", "Horas", 0, 12
        )

        # CALIFICACIÓN

        ax2.plot(
            x,
            fuzz.trimf(x, [0, 0, 50]),
            color=ROSA,
            linewidth=2,
            label="Baja"
        )

        ax2.plot(
            x,
            fuzz.trimf(x, [30, 60, 85]),
            color=MORADO,
            linewidth=2,
            label="Regular"
        )

        ax2.plot(
            x,
            fuzz.trimf(x, [70, 100, 100]),
            color=ROSA_CLARO,
            linewidth=2,
            label="Alta"
        )

        self.estilizar(
            ax2, "Calificación", "Puntos", 0, 100
        )

        # RENDIMIENTO

        ax3.plot(
            x,
            fuzz.trimf(x, [0, 0, 45]),
            color=ROSA,
            linewidth=2,
            label="Bajo"
        )

        ax3.plot(
            x,
            fuzz.trimf(x, [25, 50, 75]),
            color=MORADO,
            linewidth=2,
            label="Medio"
        )

        ax3.plot(
            x,
            fuzz.trimf(x, [55, 100, 100]),
            color=ROSA_CLARO,
            linewidth=2,
            label="Alto"
        )

        self.estilizar(
            ax3, "Salida: rendimiento", "Rendimiento", 0, 100
        )

        self.figura.subplots_adjust(
            left=0.07,
            right=0.98,
            bottom=0.16,
            top=0.86,
            wspace=0.35
        )

        self.canvas.draw()

    # ======================================
    # ESTILO GENERAL
    # ======================================

    @staticmethod
    def estilizar(ax, titulo, xlabel, xmin, xmax):

        ax.set_title(
            titulo,
            color=TEXTO,
            fontweight="bold",
            fontsize=10,
            pad=12
        )

        ax.set_xlabel(xlabel, fontsize=9)
        ax.set_ylabel("Pertenencia", fontsize=9)

        ax.set_xlim(xmin, xmax)
        ax.set_ylim(0, 1.1)

        ax.set_facecolor(BLANCO)

        ax.grid(
            alpha=0.2,
            linestyle="--"
        )

        ax.legend(
            fontsize=8,
            frameon=False,
            loc="best"
        )

        ax.tick_params(labelsize=8)

    # ======================================
    # ACTUALIZAR GRÁFICAS
    # ======================================

    def actualizar(self, datos):

        ax1, ax2, ax3 = self.ejes

        horas = datos["horas"]
        calificacion = datos["calificacion"]

        x_horas = np.arange(0, 12.1, 0.1)
        x = np.arange(0, 101, 1)

        # ----------------------------------
        # GRÁFICA DE HORAS
        # ----------------------------------

        ax1.clear()

        curvas_h = [
            ("pocas", [0, 0, 4], ROSA),
            ("moderadas", [2, 6, 10], MORADO),
            ("muchas", [8, 12, 12], ROSA_CLARO)
        ]

        for nombre, puntos, color in curvas_h:

            grado = datos["grados_horas"][nombre]

            ax1.plot(
                x_horas,
                fuzz.trimf(x_horas, puntos),
                color=color,
                linewidth=2,
                label=nombre.capitalize()
            )

            ax1.scatter(
                [horas],
                [grado],
                color=color,
                edgecolors=TEXTO,
                s=55,
                zorder=5
            )

        ax1.axvline(
            horas,
            color=TEXTO,
            linestyle="--",
            linewidth=1.5,
            label=f"Entrada: {horas:g} h"
        )

        self.estilizar(
            ax1, "Horas de estudio", "Horas", 0, 12
        )

        # ----------------------------------
        # GRÁFICA DE CALIFICACIÓN
        # ----------------------------------

        ax2.clear()

        curvas_c = [
            ("baja", [0, 0, 50], ROSA),
            ("regular", [30, 60, 85], MORADO),
            ("alta", [70, 100, 100], ROSA_CLARO)
        ]

        for nombre, puntos, color in curvas_c:

            grado = datos["grados_calificacion"][nombre]

            ax2.plot(
                x,
                fuzz.trimf(x, puntos),
                color=color,
                linewidth=2,
                label=nombre.capitalize()
            )

            ax2.scatter(
                [calificacion],
                [grado],
                color=color,
                edgecolors=TEXTO,
                s=55,
                zorder=5
            )

        ax2.axvline(
            calificacion,
            color=TEXTO,
            linestyle="--",
            linewidth=1.5,
            label=f"Entrada: {calificacion:g}"
        )

        self.estilizar(
            ax2, "Calificación", "Puntos", 0, 100
        )

        # ----------------------------------
        # GRÁFICA DE INFERENCIA
        # ----------------------------------

        ax3.clear()

        universo = datos["universo_salida"]

        ax3.plot(
            universo,
            fuzz.trimf(universo, [0, 0, 45]),
            color=ROSA,
            linewidth=2,
            label="Bajo"
        )

        ax3.plot(
            universo,
            fuzz.trimf(universo, [25, 50, 75]),
            color=MORADO,
            linewidth=2,
            label="Medio"
        )

        ax3.plot(
            universo,
            fuzz.trimf(universo, [55, 100, 100]),
            color=ROSA_CLARO,
            linewidth=2,
            label="Alto"
        )

        ax3.fill_between(
            universo,
            0,
            datos["salida_agregada"],
            color=ROSA,
            alpha=0.4,
            label="Salida agregada"
        )

        ax3.axvline(
            datos["resultado"],
            color=TEXTO,
            linestyle="--",
            linewidth=2,
            label=f"Resultado: {datos['resultado']:.2f}"
        )

        self.estilizar(
            ax3, "Inferencia y resultado", "Rendimiento", 0, 100
        )

        self.figura.subplots_adjust(
            left=0.07,
            right=0.98,
            bottom=0.16,
            top=0.86,
            wspace=0.35
        )

        self.canvas.draw_idle()


# ==========================================
# GRÁFICA DE ESTADÍSTICAS
# ==========================================

class GraficaEstadisticas:

    def __init__(self, contenedor):

        self.figura, self.ax = plt.subplots(
            figsize=(9, 3.5),
            dpi=90
        )

        self.figura.patch.set_facecolor(FONDO)

        self.canvas = FigureCanvasTkAgg(
            self.figura,
            master=contenedor
        )

        self.canvas.get_tk_widget().pack(
            fill="both",
            expand=True,
            padx=12,
            pady=8
        )

        self.mostrar_vacio()

    # ======================================
    # GRÁFICA SIN DATOS
    # ======================================

    def mostrar_vacio(self):

        self.ax.clear()
        self.ax.set_facecolor(FONDO)

        self.ax.text(
            0.5,
            0.5,
            "Todavía no hay evaluaciones",
            ha="center",
            va="center",
            transform=self.ax.transAxes,
            color=TEXTO,
            fontsize=12
        )

        self.ax.set_title(
            "Promedio de rendimiento por estudiante",
            color=TEXTO,
            fontsize=12,
            fontweight="bold",
            pad=15
        )

        self.ax.set_xticks([])
        self.ax.set_yticks([])

        self.figura.subplots_adjust(
            left=0.10,
            right=0.97,
            bottom=0.20,
            top=0.80
        )

        self.canvas.draw_idle()

    # ======================================
    # ACTUALIZAR COMPARACIÓN
    # ======================================

    def actualizar(self, evaluaciones):

        self.ax.clear()
        self.ax.set_facecolor(FONDO)

        if not evaluaciones:
            self.mostrar_vacio()
            return

        agrupados = {}

        for evaluacion in evaluaciones:

            matricula = evaluacion["matricula"]
            nombre = evaluacion["nombre"]

            if matricula not in agrupados:

                agrupados[matricula] = {
                    "nombre": nombre,
                    "resultados": []
                }

            agrupados[matricula]["nombre"] = nombre

            agrupados[matricula]["resultados"].append(
                float(evaluacion["resultado"])
            )

        # MOSTRAR LOS ÚLTIMOS 10 ESTUDIANTES

        elementos = list(agrupados.values())[-10:]

        nombres = [
            elemento["nombre"][:14]
            for elemento in elementos
        ]

        promedios = [
            float(np.mean(elemento["resultados"]))
            for elemento in elementos
        ]

        posiciones = np.arange(len(nombres))

        colores = [
            ROSA if p < 40
            else MORADO if p < 70
            else ROSA_CLARO
            for p in promedios
        ]

        barras = self.ax.bar(
            posiciones,
            promedios,
            width=0.48,
            color=colores,
            edgecolor=BLANCO,
            linewidth=1.5
        )

        self.ax.set_title(
            "Promedio de rendimiento por estudiante",
            color=TEXTO,
            fontsize=12,
            fontweight="bold",
            pad=15
        )

        self.ax.set_ylabel(
            "Rendimiento (%)",
            color=TEXTO,
            fontsize=9
        )

        self.ax.set_ylim(0, 110)

        self.ax.set_xticks(posiciones)

        self.ax.set_xticklabels(
            nombres,
            rotation=15,
            ha="right",
            fontsize=9
        )

        self.ax.grid(
            axis="y",
            alpha=0.2,
            linestyle="--"
        )

        self.ax.set_axisbelow(True)

        self.ax.tick_params(
            axis="y",
            labelsize=8
        )

        # PORCENTAJES ENCIMA DE LAS BARRAS

        for barra, valor in zip(barras, promedios):

            self.ax.text(
                barra.get_x() + barra.get_width() / 2,
                valor + 2,
                f"{valor:.1f}%",
                ha="center",
                va="bottom",
                fontsize=9,
                color=TEXTO,
                fontweight="bold"
            )

        # EVITAR QUE LOS TEXTOS SE CORTEN

        if len(nombres) == 1:
            self.ax.set_xlim(-0.8, 0.8)
        else:
            self.ax.set_xlim(-0.6, len(nombres) - 0.4)

        self.figura.subplots_adjust(
            left=0.10,
            right=0.97,
            bottom=0.25,
            top=0.80
        )

        self.canvas.draw_idle()


# ==========================================
# FUNCIONES PARA CREAR LAS GRÁFICAS
# ==========================================

def crear_graficas(contenedor):

    return GraficasDifusas(contenedor)


def crear_grafica_estadisticas(contenedor):

    return GraficaEstadisticas(contenedor)
