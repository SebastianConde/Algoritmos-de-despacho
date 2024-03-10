import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt

#Nombres: Luis Sebastian Conde Toro y Santiago Ramirez Gonzalez
#Asignatura: Sistemas Operativos

def ordenar_procesos_fifo(procesos):
    procesos.sort(key=lambda x: x[2]) #Ordenar por tiempo de llegada
    return procesos

def ordenar_procesos_sjf(procesos):
    # Crear una copia de la lista de procesos para evitar modificar la original
    procesos_copia = procesos.copy()

    # Ordenar la copia por tiempo de llegada
    procesos_copia.sort(key=lambda x: x[2])

    # Lista de procesos ordenados
    procesos_ordenados = []

    # Tiempo de ráfaga acumulado
    tiempo_rafaga_acumulado = 0

    # Iterar sobre los procesos
    while procesos_copia:
        # Buscar procesos con tiempo de llegada menor o igual al tiempo de ráfaga acumulado
        procesos_llegada_antigua = [p for p in procesos_copia if p[2] <= tiempo_rafaga_acumulado]

        # Si hay procesos con tiempo de llegada antiguo
        if procesos_llegada_antigua:
            # Ordenar estos procesos por tiempo de ejecución (ráfaga)
            procesos_llegada_antigua.sort(key=lambda x: x[1])

            # Tomar el proceso con la ráfaga más corta y agregarlo a la lista de procesos ordenados
            proceso = procesos_llegada_antigua.pop(0)
            procesos_ordenados.append(proceso)

            # Actualizar el tiempo de ráfaga acumulado
            tiempo_rafaga_acumulado += proceso[1]

            # Eliminar el proceso de la lista de procesos restantes
            procesos_copia.remove(proceso)

        else:
            # Si no hay procesos con tiempo de llegada antiguo, buscar el proceso con el tiempo de llegada más corto
            proceso = min(procesos_copia, key=lambda x: x[2])

            # Agregar este proceso a la lista de procesos ordenados
            procesos_ordenados.append(proceso)

            # Actualizar el tiempo de ráfaga acumulado
            tiempo_rafaga_acumulado += proceso[1]

            # Eliminar el proceso de la lista de procesos restantes
            procesos_copia.remove(proceso)

    return procesos_ordenados




def mostrar_diagrama_gantt_RR(procesos, quantum): #Round Robin
    nombres_procesos, tiempos_rafaga = separar_procesos(procesos)
    xlim = sum(tiempos_rafaga) + 1 #Limite del eje X dinámico

    #Tiempos de inicio de cada proceso
    tiempos_inicio = []

    #Tiempos de finalización de cada proceso
    tiempos_finalizacion = []

    # Crear la figura y los ejes
    fig, ax = plt.subplots()

    # Establecer límites de los ejes
    ax.set_xlim(0, xlim)

    # Dibujar el plano cartesiano
    ax.plot([0, xlim], [0, 0], color='black')  # Eje X
    ax.plot([0, 0], [0, len(nombres_procesos)], color='black')  # Eje Y 

    rafaga_anterior = 0 
    tiempos_rafaga_copia = tiempos_rafaga.copy() 
    
    posiciones_originales = list(range(len(tiempos_rafaga_copia))) # Lista para almacenar las posiciones originales de los elementos, con el fin de mapear cada proceso y que a la hora de graficar den las líneas en las alturas que son
    tiempo_final_proceso = []

    i = 0
    while i < len(tiempos_rafaga_copia):
        nombre_proceso = nombres_procesos[i]
        ax.text(-1, i+0.25, nombre_proceso, ha='right', va='center') # Agregar los nombres de los procesos en el eje vertical
        tiempos_rafaga_copia[i] -= quantum # Restar el quantum al tiempo de ráfaga del proceso
        if tiempos_rafaga_copia[i] == 0:
            tiempo_final_proceso.append(quantum + quantum*i + rafaga_anterior)
        ax.plot([0 + quantum*i + rafaga_anterior, quantum + quantum*i + rafaga_anterior], [0.25 + posiciones_originales[i], 0.25 + posiciones_originales[i]], color='red') # Dibujar las líneas de los procesos de un punto a punto dependiendo el quantum y el proceso en el que vayamos del bucle, se tiene en cuenta la línea en que altura debe estar por el mapeo de posiciones
        
        tiempos_inicio.append(0 + quantum*i + rafaga_anterior)
        tiempos_finalizacion.append(quantum + quantum*i + rafaga_anterior)
        
        if i == len(tiempos_rafaga_copia) - 1:
            rafaga_anterior += quantum * len(tiempos_rafaga_copia)
            j = 0
            while j < len(tiempos_rafaga_copia):
                # Verificar si el elemento en tiempos_rafaga_copia es 0
                if tiempos_rafaga_copia[j] == 0:
                    i = -1  # Reiniciar el índice para volver a comenzar nueva ronda después de eliminar los procesos terminados
                    posiciones_originales.remove(posiciones_originales[j]) # Eliminar la posición original del proceso del mapeo
                    tiempos_rafaga_copia.remove(tiempos_rafaga_copia[j]) # Eliminar el tiempo de ráfaga del proceso
                    j = -1  # Reiniciar el índice para volver a comenzar desde el principio del subblucle después de eliminar
                j += 1

        i += 1

    # Quitar los números en el eje Y
    ax.set_yticklabels([])

    # Mostrar el plano cartesiano
    plt.grid(True)
    plt.show()
    return tiempos_inicio, tiempos_finalizacion, tiempo_final_proceso

def separar_procesos(procesos): #Separar los procesos en dos listas, una con los nombres y otra con los tiempos de ráfaga por facilidad
    nombres_procesos = []
    tiempos_rafaga = []

    for proceso in procesos:
        nombre, tiempo_rafaga, _ = proceso
        nombres_procesos.append(nombre)
        tiempos_rafaga.append(tiempo_rafaga)

    return nombres_procesos, tiempos_rafaga


def mostrar_diagrama_gantt(procesos): #FIFO y SJF
    nombres_procesos, tiempos_rafaga = separar_procesos(procesos)
    xlim = sum(tiempos_rafaga) + 1 #Limite del eje X dinámico

    #Tiempos de inicio de cada proceso
    tiempos_inicio = []

    #Tiempos de finalización de cada proceso
    tiempos_finalizacion = []

    # Crear la figura y los ejes
    fig, ax = plt.subplots()

    # Establecer límites de los ejes
    ax.set_xlim(0, xlim)

    # Dibujar el plano cartesiano
    ax.plot([0, xlim], [0, 0], color='black')  # Eje X
    ax.plot([0, 0], [0, len(nombres_procesos)], color='black')  # Eje Y

    rafaga_anterior = 0
    # Agregar los nombres de los procesos en el eje vertical
    for i, nombre_proceso in enumerate(nombres_procesos):
        ax.text(-1, i+0.25, nombre_proceso, ha='right', va='center') # Agregar los nombres de los procesos en el eje vertical
        ax.plot([0 + rafaga_anterior, tiempos_rafaga[i] + rafaga_anterior], [0.25 + i, 0.25 + i], color='red') # Dibujar las líneas de los procesos de un punto a punto dependiendo el quantum y el proceso en el que vayamos del bucle, se tiene en cuenta la línea en que altura debe estar con la posición
        tiempos_inicio.append(rafaga_anterior) # Añadir el tiempo de inicio del proceso a la lista
        rafaga_anterior += tiempos_rafaga[i] # Sumar el tiempo de ráfaga del proceso al tiempo de ráfaga anterior
        tiempos_finalizacion.append(rafaga_anterior) # Añadir el tiempo de finalización del proceso a la lista

    # Quitar los números en el eje Y
    ax.set_yticklabels([])

    # Mostrar el plano cartesiano
    plt.grid(True)
    plt.show()
    return tiempos_inicio, tiempos_finalizacion

def calcular_tiempo_espera(procesos, tiempos_inicio): #Calcular el tiempo de espera promedio
    tiempos_espera = []
    for i, proceso in enumerate(procesos):
        _, _, tiempo_llegada = proceso #Desempaquetar el tiempo de llegada
        tiempo_espera = tiempos_inicio[i] - tiempo_llegada #Calcular el tiempo de espera
        tiempos_espera.append(tiempo_espera)

    return sum(tiempos_espera) / len(tiempos_espera) #Calcular el promedio de los tiempos de espera

def calcular_tiempo_sistema(procesos, tiempos_finalizacion): #Calcular el tiempo de sistema promedio
    tiempos_sistema = []
    for i, proceso in enumerate(procesos):
        _, _, tiempo_llegada = proceso #Desempaquetar el tiempo de llegada
        tiempo_sistema = tiempos_finalizacion[i] - tiempo_llegada #Calcular el tiempo de sistema
        tiempos_sistema.append(tiempo_sistema)

    return sum(tiempos_sistema) / len(tiempos_sistema) #Calcular el promedio de los tiempos de sistema

def mostrar_tabla_procesos(procesos): #Mostrar la tabla de procesos en una ventana
    root = tk.Tk()
    root.title("Tabla de Procesos")

    tree = ttk.Treeview(root)
    tree["columns"] = ("proceso", "tiempo_ejecucion", "tiempo_llegada")
    tree.heading("proceso", text="Proceso")
    tree.heading("tiempo_ejecucion", text="Tiempo de ejecución")
    tree.heading("tiempo_llegada", text="Tiempo de llegada")

    for proceso in procesos:
        nombre, tiempo_rafaga, tiempo_llegada = proceso
        tree.insert("", "end", values=(nombre, tiempo_rafaga, tiempo_llegada))

    tree.pack(expand=True, fill=tk.BOTH)

    # Etiquetas para mostrar los tiempos de espera y sistema
    etiqueta_espera = ttk.Label(root, text="")
    etiqueta_espera.pack(pady=5)
    
    etiqueta_sistema = ttk.Label(root, text="")
    etiqueta_sistema.pack(pady=5)

    # Crear botones para los algoritmos de planificación
    btn_fifo = ttk.Button(root, text="FIFO", command=lambda: correr_algoritmo(procesos, "FIFO", etiqueta_espera, etiqueta_sistema, None))
    btn_fifo.pack(side=tk.LEFT, padx=5, pady=5)

    btn_sjf = ttk.Button(root, text="SJF", command=lambda: correr_algoritmo(procesos, "SJF", etiqueta_espera, etiqueta_sistema, None))
    btn_sjf.pack(side=tk.LEFT, padx=5, pady=5)

    btn_rr = ttk.Button(root, text="Round Robin", command=lambda: abrir_ventana_q(procesos, etiqueta_espera, etiqueta_sistema))
    btn_rr.pack(side=tk.LEFT, padx=5, pady=5)

    root.mainloop()

def abrir_ventana_q(procesos, etiqueta_espera, etiqueta_sistema): #Abrir ventana para ingresar el valor de Q
    ventana_q = tk.Toplevel()
    ventana_q.title("Ingrese el valor de Q")

    etiqueta_q = ttk.Label(ventana_q, text="Valor de Q:")
    etiqueta_q.pack(side=tk.LEFT, padx=5, pady=5)

    entrada_q = ttk.Entry(ventana_q)
    entrada_q.pack(side=tk.LEFT, padx=5, pady=5)

    btn_confirmar = ttk.Button(ventana_q, text="Confirmar", command=lambda: correr_algoritmo(procesos, "Round Robin", etiqueta_espera, etiqueta_sistema, entrada_q.get())) #Enviar el valor de Q
    btn_confirmar.pack(side=tk.LEFT, padx=5, pady=5)

def correr_algoritmo(procesos, algoritmo, etiqueta_espera, etiqueta_sistema, q):
    if algoritmo == "FIFO":
        procesos = ordenar_procesos_fifo(procesos)
        tiempos_inicio, tiempos_finalizacion = mostrar_diagrama_gantt(procesos)
        tiempo_espera_promedio = calcular_tiempo_espera(procesos, tiempos_inicio)
        tiempo_sistema_promedio = calcular_tiempo_sistema(procesos, tiempos_finalizacion)
        etiqueta_espera.config(text=f"El tiempo de espera promedio es: {tiempo_espera_promedio} segundos")
        etiqueta_sistema.config(text=f"El tiempo de sistema promedio es: {tiempo_sistema_promedio} segundos")

    elif algoritmo == "SJF":
        procesos = ordenar_procesos_sjf(procesos)
        tiempos_inicio, tiempos_finalizacion = mostrar_diagrama_gantt(procesos)
        tiempo_espera_promedio = calcular_tiempo_espera(procesos, tiempos_inicio)
        tiempo_sistema_promedio = calcular_tiempo_sistema(procesos, tiempos_finalizacion)
        etiqueta_espera.config(text=f"El tiempo de espera promedio es: {tiempo_espera_promedio} segundos")
        etiqueta_sistema.config(text=f"El tiempo de sistema promedio es: {tiempo_sistema_promedio} segundos")

    elif algoritmo == "Round Robin":
        if q is None: #Validar que se haya ingresado un valor de Q
            print("Por favor ingrese el valor de Q.")
            return

        procesos = ordenar_procesos_fifo(procesos)
        tiempos_inicio, tiempos_finalizacion, tiempo_final_proceso = mostrar_diagrama_gantt_RR(procesos, int(q))

        #------SUMA OBSERVANDO PATRONES PARA HALLAR PROMEDIO DE TIEMPOS DE ESPERA----
        suma1 = sum(tiempos_inicio[:len(procesos)]) #sumar los tiempos de inicio de la primera ronda de procesos
        _, _, tiempos_llegada = zip(*procesos)
        suma2 = suma1 - sum(tiempos_llegada) #restar suma 1 con la suma de los tiempos de llegada
        suma3 = sum(tiempos_inicio[len(procesos):]) #sumar los tiempos de inicio de las demás rondas de procesos
        suma4 = suma2 + suma3 #sumar suma 2 con suma 3
        suma5 = sum(tiempos_finalizacion) - sum(tiempo_final_proceso) #restar los tiempos de finalización con la suma del tiempo final de todos los procesos
        suma6 = suma4 - suma5 #restar suma 4 con suma 5

        #------SUMA OBSERVANDO PATRONES PARA HALLAR PROMEDIO DE TIEMPOS DE SISTEMA----
        suma7 = sum(tiempo_final_proceso) - sum(tiempos_llegada) #restar la suma del tiempo final de todos los procesos con la suma de los tiempos de llegada


        etiqueta_espera.config(text=f"El tiempo de espera promedio es: {suma6/len(procesos)} segundos") 
        etiqueta_sistema.config(text=f"El tiempo de sistema promedio es: {suma7/len(procesos)} segundos")             

    else:
        print("Ingrese un algoritmo válido")

def matriz_procesos():  # Ventana para ingresar los procesos
    def agregar_proceso():
        nombre = "P" + str(len(procesos) + 1)
        rafaga = int(entrada_rafaga.get())
        llegada = int(entrada_llegada.get())
        procesos.append((nombre, rafaga, llegada))
        tree.insert("", "end", values=(nombre, rafaga, llegada))

    def abrir_tabla_procesos():
        root.destroy()  # Cerrar la ventana actual
        mostrar_tabla_procesos(procesos)

    procesos = []
    
    root = tk.Tk()
    root.title("Ingresar Procesos")

    frame = ttk.Frame(root)
    frame.pack(padx=10, pady=10)

    ttk.Label(frame, text="Tiempo de ejecución:").grid(row=0, column=0, padx=5, pady=5)
    entrada_rafaga = ttk.Entry(frame)
    entrada_rafaga.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(frame, text="Tiempo de llegada:").grid(row=1, column=0, padx=5, pady=5)
    entrada_llegada = ttk.Entry(frame)
    entrada_llegada.grid(row=1, column=1, padx=5, pady=5)

    btn_agregar = ttk.Button(frame, text="Agregar Proceso", command=agregar_proceso)
    btn_agregar.grid(row=2, columnspan=2, padx=5, pady=5)

    tree = ttk.Treeview(frame)
    tree["columns"] = ("proceso", "tiempo_ejecucion", "tiempo_llegada")
    tree.heading("proceso", text="Proceso")
    tree.heading("tiempo_ejecucion", text="Tiempo de ejecución")
    tree.heading("tiempo_llegada", text="Tiempo de llegada")
    tree.grid(row=3, columnspan=2, padx=5, pady=5)

    btn_continuar = ttk.Button(frame, text="Continuar", command=abrir_tabla_procesos)
    btn_continuar.grid(row=4, columnspan=2, padx=5, pady=5)

    root.mainloop()



matriz_procesos()  # Se tiene toda la tabla acá
    











