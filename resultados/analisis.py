import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#cargar fichero
file = input("introducir nombre fichero: ")
data = pd.read_csv(file + ".csv")

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

#scatter plot con tiempo vs nº generaciones & individuos
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
ax1.scatter(data['Número de Individuos'], data['Tiempo de Simulación'], alpha=0.7)
ax1.set_title("Número de individuos vs Tiempo de simulación")
ax1.set_xlabel("Número de individuos")
ax1.set_ylabel("Tiempo de simulación")
ax2.scatter(data['Número de Generaciones'], data['Tiempo de Simulación'], alpha=0.7)
ax2.set_title("Número de individuos vs Tiempo de simulación")
ax2.set_xlabel("Número de individuos")
ax2.set_ylabel("Tiempo de simulación")
plt.tight_layout()
plt.show()

#matriz de correlación
correlation_matrix = data.corr()
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
plt.title("Matriz de correlación")
plt.show()
