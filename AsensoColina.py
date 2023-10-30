import matplotlib.pyplot as plt
import numpy as np
import random

def inicializar_cuadricula(n):
    # Crea una cuadrícula NxN con todos los elementos inicializados a 0.
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

def distancia_manhattan(punto1, punto2):
    return abs(punto1[0] - punto2[0]) + abs(punto1[1] - punto2[1])

def busqueda_ascenso_colina(cuadricula, inicio, meta, max_iteraciones):
    # Inicializa las variables.
    actual = inicio  # Comenzamos desde el punto de inicio.
    visitados = set()  # Conjunto para rastrear los nodos visitados.
    lista_visitados = []  # Lista para almacenar los nodos visitados en orden.
    camino = []  # Lista para almacenar el camino seguido.
    iteraciones = 0  # Contador de iteraciones.

    # Mientras no lleguemos a la meta y no excedamos el número máximo de iteraciones:
    while actual != meta and iteraciones < max_iteraciones:
        visitados.add(actual)  # Marcamos el nodo actual como visitado.
        lista_visitados.append(actual)  # Agregamos el nodo actual a la lista de nodos visitados.
        camino.append(actual)  # Agregamos el nodo actual al camino.
        x, y = actual

        # Definimos movimientos posibles: arriba, abajo, izquierda, derecha.
        movimientos = [(x, y + 1), (x, y - 1), (x + 1, y), (x - 1, y)]
        # Ordenamos los movimientos por su distancia manhattan a la meta.
        movimientos.sort(key=lambda movimiento: distancia_manhattan(movimiento, meta))

        # Iteramos a través de los movimientos y seleccionamos el primero válido no visitado.
        for movimiento in movimientos:
            if es_valida(movimiento[0], movimiento[1], cuadricula) and movimiento not in visitados:
                actual = movimiento  # Actualizamos la posición actual.
                break

        iteraciones += 1  # Incrementamos el contador de iteraciones.

    # Si se supera el número máximo de iteraciones, mostramos un mensaje.
    if iteraciones >= max_iteraciones:
        print("El algoritmo se atascó después de", max_iteraciones, "iteraciones.")

    # Si llegamos a la meta, agregamos la posición de la meta al camino.
    if actual == meta:
        camino.append(meta)

    # Devolvemos tanto el camino como la lista de nodos visitados.
    return camino, lista_visitados


def dibujar_cuadricula(cuadricula, inicio, meta, camino, visitados):
    fig, ax = plt.subplots()

    ax.set_facecolor('white')
    tamaño_celda = 1

    for i in range(len(cuadricula)):
        for j in range(len(cuadricula[0])):
            if cuadricula[i][j] == 1:
                ax.add_patch(plt.Rectangle((j * tamaño_celda, i * tamaño_celda), tamaño_celda, tamaño_celda, color='black'))
            elif cuadricula[i][j] == 0:
                if meta:
                    distancia = distancia_manhattan((i, j), meta)
                    max_distancia = max(len(cuadricula), len(cuadricula[0]))  # Máxima distancia posible en la cuadrícula
                    valor_calor = 1 - (distancia / max_distancia)  # Ajusta el valor entre 0 (frío) y 1 (caliente)
                    color = plt.cm.viridis(valor_calor)  # Utiliza el mapa de colores viridis de Matplotlib
                else:
                    color = 'white'

                ax.add_patch(plt.Rectangle((j * tamaño_celda, i * tamaño_celda), tamaño_celda, tamaño_celda, color=color))

    plt.scatter(inicio[1] * tamaño_celda + tamaño_celda / 2, inicio[0] * tamaño_celda + tamaño_celda / 2, color='orange', marker='o', s=100)
    plt.scatter(meta[1] * tamaño_celda + tamaño_celda / 2, meta[0] * tamaño_celda + tamaño_celda / 2, color='red', marker='x', s=100)

    if camino:
        camino_x, camino_y = zip(*camino)
        camino_x = [x * tamaño_celda + tamaño_celda / 2 for x in camino_x]
        camino_y = [y * tamaño_celda + tamaño_celda / 2 for y in camino_y]
        plt.plot(camino_y, camino_x, color='blue', label='Camino')

    if visitados:
        visitados_x, visitados_y = zip(*visitados)
        visitados_x = [x * tamaño_celda + tamaño_celda / 2 for x in visitados_x]
        visitados_y = [y * tamaño_celda + tamaño_celda / 2 for y in visitados_y]
        for i, (x, y) in enumerate(zip(visitados_x, visitados_y), 1):
            plt.text(y, x, str(i), ha='center', va='center', color='white', fontsize=14)

    for i in range(len(cuadricula) + 1):
        plt.axhline(y=i * tamaño_celda, color='black', linewidth=0.1)
    for j in range(len(cuadricula[0]) + 1):
        plt.axvline(x=j * tamaño_celda, color='black', linewidth=0.1)

    plt.legend()
    plt.show()

def main():
    tamaño_cuadricula = 10
    cuadricula = inicializar_cuadricula(tamaño_cuadricula)
    num_obstaculos = (tamaño_cuadricula * tamaño_cuadricula) // 4
    generar_obstaculos(cuadricula, num_obstaculos)

    try:
        inicio, meta = generar_inicio_meta(cuadricula)
    except ValueError as e:
        print(e)
        return

    camino, visitados = busqueda_ascenso_colina(cuadricula, inicio, meta, num_obstaculos)

    if camino:
        print("Camino encontrado:", camino)
        print("Camino recorrido:", visitados)
    else:
        print("No se encontró un camino válido.")

    dibujar_cuadricula(cuadricula, inicio, meta, camino, visitados)

if __name__ == "__main__":
    main()
