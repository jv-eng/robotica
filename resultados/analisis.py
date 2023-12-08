import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#cargar fichero
file = input("introducir nombre fichero: ")
data = pd.read_csv("resultados_centrada" + ".csv")

#mostrar cabeceras
print("Cabecera: ")
print(data.head())
print()

#mostrar datos estadísticos
print("Estadísticos: ")
print(data.describe())
print()

#menor tiempo
filas_menor_tiempo = data.nsmallest(5, "Tiempo de Simulación")
print("Combinaciones con menor tiempo de ejecución")
print("Semilla\tNº individuos\tNº generaciones\tOperador de selección\tOperador de cruce\tOperador de mutación\tOperador de reemplazo\tTiempo de simulación")
print(filas_menor_tiempo)
print()