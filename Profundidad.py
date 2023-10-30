import matplotlib.pyplot as plt
import numpy as np
import random

def inicializar_cuadricula(n):
    # Crea una cuadrícula de tamaño NxN con todos los elementos inicializados en 0.
    return np.zeros((n, n), dtype=int)

def es_valida(x, y, cuadricula):
    # Verifica si las coordenadas (x, y) están dentro de la cuadrícula y no son un obstáculo (valor 1).
    return 0 <= x < len(cuadricula) and 0 <= y < len(cuadricula[0]) and cuadricula[x][y] == 0

def generar_obstaculos(cuadricula, n):
    for _ in range(n):
        x, y = random.randint(0, len(cuadricula) - 1), random.randint(0, len(cuadricula[0]) - 1)
        while cuadricula[x][y] == 1:
            x, y = random.randint(0, len(cuadricula) - 1), random.randint(0, len(cuadricula[0]) - 1)
        cuadricula[x][y] = 1

def generar_inicio_meta(cuadricula):
    celdas_libres = [(x, y) for x in range(len(cuadricula)) for y in range(len(cuadricula[0])) if cuadricula[x][y] == 0]
    if len(celdas_libres) < 2:
        raise ValueError("La cuadrícula no tiene suficientes celdas libres para establecer el inicio y la meta.")
    inicio, meta = random.sample(celdas_libres, 2)
    return inicio, meta

def busqueda_dfs(cuadricula, inicio, meta):
    # Inicializa una pila con el nodo de inicio.
    pila = [inicio]
    # Crea un conjunto para rastrear los nodos visitados.
    visitados = set()
    # Lista para almacenar los nodos visitados en orden.
    lista_visitados = []

    # Diccionario para rastrear el padre de cada nodo.
    padre = {}

    # Comienza la búsqueda DFS (Depth-First Search).
    while pila:
        actual = pila.pop()
        # Si se encuentra el nodo de destino, termina la búsqueda.
        if actual == meta:
            break

        x, y = actual
        # Si el nodo actual no ha sido visitado, agrégalo a la lista de visitados.
        if actual not in visitados:
            visitados.add(actual)
            lista_visitados.append(actual)

            # Define los movimientos posibles: izquierda, derecha, abajo, arriba.
            movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]

            # Explora los vecinos del nodo actual.
            for dx, dy in movimientos:
                vecino = (x + dx, y + dy)

                # Verifica si el vecino es válido y no ha sido visitado.
                if es_valida(vecino[0], vecino[1], cuadricula) and vecino not in visitados:
                    pila.append(vecino)
                    # Registra al nodo actual como el padre del vecino.
                    padre[vecino] = actual

    # Reconstruye la trayectoria desde el objetivo hasta el inicio.
    camino = []
    actual = meta
    while actual != inicio:
        camino.append(actual)
        # Recupera el padre del nodo actual para avanzar hacia atrás en la trayectoria.
        actual = padre.get(actual)  # Usamos .get() para evitar KeyError
        if actual is None:
            break

    camino.append(inicio)

    # Devuelve tanto la lista de nodos visitados como el camino en orden correcto.
    return lista_visitados, camino[::-1]


def dibujar_cuadricula(cuadricula, inicio, meta, camino, visitados):
    fig, ax = plt.subplots()

    # Configura el fondo blanco
    ax.set_facecolor('white')

    # Tamaño de las celdas y espaciado de la cuadrícula
    tamano_celda = 1
    for i in range(len(cuadricula)):
        for j in range(len(cuadricula[0])):
            if cuadricula[i][j] == 1:  # Obstáculo
                ax.add_patch(plt.Rectangle((j * tamano_celda, i * tamano_celda), tamano_celda, tamano_celda, color='black'))
            elif cuadricula[i][j] == 0:  # Celda libre
                ax.add_patch(plt.Rectangle((j * tamano_celda, i * tamano_celda), tamano_celda, tamano_celda, color='white', edgecolor='black'))

    plt.scatter(inicio[1] * tamano_celda + tamano_celda / 2, inicio[0] * tamano_celda + tamano_celda / 2, color='orange', marker='o', s=100)
    plt.scatter(meta[1] * tamano_celda + tamano_celda / 2, meta[0] * tamano_celda + tamano_celda / 2, color='red', marker='x', s=100)

    if camino:
        camino_x, camino_y = zip(*camino)
        camino_x = [x * tamano_celda + tamano_celda / 2 for x in camino_x]
        camino_y = [y * tamano_celda + tamano_celda / 2 for y in camino_y]
        plt.plot(camino_y, camino_x, color='blue', label='Camino')

    if visitados:
        visitados_x, visitados_y = zip(*visitados)
        visitados_x = [x * tamano_celda + tamano_celda / 2 for x in visitados_x]
        visitados_y = [y * tamano_celda + tamano_celda / 2 for y in visitados_y]
        for i, (x, y) in enumerate(zip(visitados_x, visitados_y), 1):
            plt.text(y, x, str(i), ha='center', va='center', color='green', fontsize=14)

    # Dibuja la cuadrícula
    for i in range(len(cuadricula) + 1):
        plt.axhline(y=i * tamano_celda, color='black', linewidth=0.1)
    for j in range(len(cuadricula[0]) + 1):
        plt.axvline(x=j * tamano_celda, color='black', linewidth=0.1)

    plt.legend()
    plt.show()

def main():
    n = 10  # Tamaño de la cuadrícula (NxN)
    cuadricula = inicializar_cuadricula(n)

    # Genera obstáculos aleatorios (N^2/4 obstáculos)
    num_obstaculos = (n * n) // 4
    generar_obstaculos(cuadricula, num_obstaculos)

    try:
        inicio, meta = generar_inicio_meta(cuadricula)
    except ValueError as e:
        print(e)
        return

    visitados, camino = busqueda_dfs(cuadricula, inicio, meta)
    if camino:
        print("Camino encontrado:", camino)
        print("Camino recorrido:", visitados)
    else:
        print("No se encontró un camino válido.")

    dibujar_cuadricula(cuadricula, inicio, meta, camino, visitados)

if __name__ == "__main__":
    main()
