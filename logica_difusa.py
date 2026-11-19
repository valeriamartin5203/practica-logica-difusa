import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


class EvaluadorDifuso:
    """Sistema Mamdani para evaluar rendimiento estudiantil."""

    def __init__(self):
        self.horas = ctrl.Antecedent(np.arange(0, 12.1, 0.1), "horas")
        self.calificacion = ctrl.Antecedent(np.arange(0, 101, 1), "calificacion")
        self.rendimiento = ctrl.Consequent(np.arange(0, 101, 1), "rendimiento")

        # Funciones de pertenencia de las horas
        self.horas["pocas"] = fuzz.trimf(self.horas.universe, [0, 0, 4])
        self.horas["moderadas"] = fuzz.trimf(self.horas.universe, [2, 6, 10])
        self.horas["muchas"] = fuzz.trimf(self.horas.universe, [8, 12, 12])

        # Funciones de pertenencia de la calificación
        self.calificacion["baja"] = fuzz.trimf(
            self.calificacion.universe, [0, 0, 50]
        )
        self.calificacion["regular"] = fuzz.trimf(
            self.calificacion.universe, [30, 60, 85]
        )
        self.calificacion["alta"] = fuzz.trimf(
            self.calificacion.universe, [70, 100, 100]
        )

        # Funciones de pertenencia de la salida
        self.rendimiento["bajo"] = fuzz.trimf(
            self.rendimiento.universe, [0, 0, 45]
        )
        self.rendimiento["medio"] = fuzz.trimf(
            self.rendimiento.universe, [25, 50, 75]
        )
        self.rendimiento["alto"] = fuzz.trimf(
            self.rendimiento.universe, [55, 100, 100]
        )

        # Cada tupla representa: horas, calificación, rendimiento
        self.reglas_datos = [
            ("pocas", "baja", "bajo"),
            ("pocas", "regular", "bajo"),
            ("pocas", "alta", "medio"),
            ("moderadas", "baja", "bajo"),
            ("moderadas", "regular", "medio"),
            ("moderadas", "alta", "alto"),
            ("muchas", "baja", "medio"),
            ("muchas", "regular", "alto"),
            ("muchas", "alta", "alto"),
        ]

        reglas = [
            ctrl.Rule(
                self.horas[h] & self.calificacion[c],
                self.rendimiento[r]
            )
            for h, c, r in self.reglas_datos
        ]

        self.sistema = ctrl.ControlSystem(reglas)

    def evaluar(self, horas, calificacion):
        # Se crea una simulación nueva para cada evaluación.
        simulacion = ctrl.ControlSystemSimulation(self.sistema)
        simulacion.input["horas"] = horas
        simulacion.input["calificacion"] = calificacion
        simulacion.compute()

        resultado = float(simulacion.output["rendimiento"])

        grados_horas = {
            nombre: float(fuzz.interp_membership(
                self.horas.universe, self.horas[nombre].mf, horas
            ))
            for nombre in ("pocas", "moderadas", "muchas")
        }

        grados_calificacion = {
            nombre: float(fuzz.interp_membership(
                self.calificacion.universe,
                self.calificacion[nombre].mf,
                calificacion
            ))
            for nombre in ("baja", "regular", "alta")
        }

        # Matriz: filas = calificación; columnas = horas.
        matriz = np.zeros((3, 3), dtype=float)
        indice_horas = {"pocas": 0, "moderadas": 1, "muchas": 2}
        indice_calificacion = {"baja": 0, "regular": 1, "alta": 2}

        universo = self.rendimiento.universe
        salida_agregada = np.zeros_like(universo, dtype=float)
        reglas_activadas = []

        for numero, (h, c, r) in enumerate(self.reglas_datos, start=1):
            activacion = min(grados_horas[h], grados_calificacion[c])

            matriz[indice_calificacion[c], indice_horas[h]] = activacion

            salida_recortada = np.fmin(
                activacion, self.rendimiento[r].mf
            )
            salida_agregada = np.fmax(
                salida_agregada, salida_recortada
            )

            reglas_activadas.append({
                "numero": numero,
                "horas": h,
                "calificacion": c,
                "rendimiento": r,
                "activacion": float(activacion)
            })

        centroide_manual = float(
            fuzz.defuzz(universo, salida_agregada, "centroid")
        )

        if resultado < 40:
            nivel = "BAJO"
            descripcion = (
                "Se recomienda fortalecer los hábitos de estudio "
                "y dedicar más tiempo a preparar las actividades."
            )
        elif resultado < 70:
            nivel = "MEDIO"
            descripcion = (
                "El rendimiento es intermedio. Puede mejorar "
                "manteniendo una rutina de estudio constante."
            )
        else:
            nivel = "ALTO"
            descripcion = (
                "El rendimiento es alto. Conviene mantener "
                "los buenos hábitos de estudio."
            )

        datos = {
            "horas": horas,
            "calificacion": calificacion,
            "resultado": resultado,
            "centroide": centroide_manual,
            "grados_horas": grados_horas,
            "grados_calificacion": grados_calificacion,
            "matriz": matriz,
            "salida_agregada": salida_agregada,
            "universo_salida": universo,
            "reglas_activadas": reglas_activadas,
        }

        return resultado, nivel, descripcion, datos
