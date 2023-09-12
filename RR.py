import matplotlib.pyplot as plt

def round_robin(procesos, tiempo_llegada, rafaga, quantum):
    n = len(procesos)
    tiempo_espera = [0] * n
    tiempo_retorno = [0] * n
    tiempo_ejecucion = list(rafaga)  
    tiempo_actual = 0

    while True:
        completado = True

        for i in range(n):
            if tiempo_llegada[i] <= tiempo_actual:
                if tiempo_ejecucion[i] > 0:
                    completado = False

                    if tiempo_ejecucion[i] > quantum:
                        tiempo_actual += quantum
                        tiempo_ejecucion[i] -= quantum
                    else:
                        tiempo_actual += tiempo_ejecucion[i]
                        tiempo_espera[i] = tiempo_actual - rafaga[i] - tiempo_llegada[i]
                        tiempo_ejecucion[i] = 0
                        tiempo_retorno[i] = tiempo_actual - tiempo_llegada[i]

            else:
                break

        if completado:
            break

    tiempo_retorno_promedio = sum(tiempo_retorno) / n
    return tiempo_espera, tiempo_retorno, tiempo_retorno_promedio

def generar_gantt(procesos, tiempo_llegada, rafaga, tiempo_espera):
    gantt = []
    tiempo_actual = 0
    while True:
        completado = True

        for i in range(len(procesos)):
            if tiempo_llegada[i] <= tiempo_actual and rafaga[i] > 0:
                completado = False
                if rafaga[i] > quantum:
                    gantt.append((procesos[i], tiempo_actual, tiempo_actual + quantum))
                    tiempo_actual += quantum
                    rafaga[i] -= quantum
                else:
                    gantt.append((procesos[i], tiempo_actual, tiempo_actual + rafaga[i]))
                    tiempo_actual += rafaga[i]
                    rafaga[i] = 0

        if completado:
            break

    return gantt

# Obtener datos del usuario
num_procesos = int(input("Ingrese el número de procesos: "))
procesos = []
tiempo_llegada = []
rafaga = []

for i in range(num_procesos):
    procesos.append(f'P{i + 1}')
    tiempo_llegada.append(int(input(f"Tiempo de llegada para P{i + 1}: ")))
    rafaga.append(int(input(f"Ráfaga para P{i + 1}: ")))

quantum = int(input("Ingrese el quantum: "))

# Calcular tiempos
tiempo_espera, tiempo_retorno, tiempo_retorno_promedio = round_robin(procesos, tiempo_llegada, rafaga, quantum)

# Generar el diagrama de Gantt
gantt = generar_gantt(procesos, tiempo_llegada, rafaga, tiempo_espera)

# Mostrar resultados
print(f'Tiempo de espera: {tiempo_espera}')
print(f'Tiempo de retorno: {tiempo_retorno}')
print(f'Tiempo de retorno promedio: {tiempo_retorno_promedio}')

# Crear el diagrama de Gantt gráfico
fig, gnt = plt.subplots()

for i, (proceso, inicio, fin) in enumerate(gantt):
    gnt.broken_barh([(inicio, fin - inicio)], (i * 10, 9), facecolors=('blue'))

gnt.set_xlabel('Tiempo')
gnt.set_yticks([i * 10 + 5 for i in range(len(procesos))])
gnt.set_yticklabels(procesos)

plt.show()
