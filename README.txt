STUDENT PERFORMANCE AI
======================

ARCHIVOS
--------
main.py             Interfaz, pestañas, registro e historial CSV.
logica_difusa.py    Sistema de inferencia difusa Mamdani y nueve reglas.
graficas.py         Gráficas de pertenencia, inferencia y comparación.
requirements.txt    Librerías necesarias.
datos/              Se crea automáticamente al ejecutar el programa.

INSTALACIÓN EN WINDOWS / VS CODE
--------------------------------
1. Abre esta carpeta en Visual Studio Code.
2. Abre Terminal > New Terminal.
3. Ejecuta:
   python -m pip install -r requirements.txt
4. Ejecuta:
   python main.py

PESTAÑAS
--------
Evaluar: captura nombre, matrícula, grupo, horas de estudio y calificación.
Gráficas: muestra funciones de pertenencia y la salida agregada.
Reglas: muestra la matriz de activación y las nueve reglas SI-ENTONCES.
Estudiantes: consulta los estudiantes registrados.
Estadísticas: muestra totales, promedio, medidor circular y comparación.

DATOS
-----
Los archivos datos/estudiantes.csv y datos/evaluaciones.csv se crean
automáticamente. No borres la carpeta datos si deseas conservar el historial.

RANGOS
------
Horas de estudio: 0 a 12 por semana.
Calificación: 0 a 100.
