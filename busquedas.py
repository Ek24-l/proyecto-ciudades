
import heapq

# 🔹 reconstruir camino
def reconstruir_camino(padres, inicio, objetivo):
    camino = []
    nodo = objetivo

    while nodo:
        camino.append(nodo)
        nodo = padres.get(nodo)

    return camino[::-1]


# 🔹 1. Recursiva
def busqueda_recursiva(grafo, actual, objetivo, visitados=None, camino=None):
    if visitados is None:
        visitados = set()
    if camino is None:
        camino = []

    visitados.add(actual)
    camino.append(actual)

    if actual == objetivo:
        return camino

    for vecino in grafo.get(actual, {}):
        if vecino not in visitados:
            resultado = busqueda_recursiva(grafo, vecino, objetivo, visitados, camino.copy())
            if resultado:
                return resultado

    return None


# 🔹 2. Profundidad (DFS)
def busqueda_profundidad(grafo, inicio, objetivo):
    pila = [(inicio, [inicio])]
    visitados = set()

    while pila:
        nodo, camino = pila.pop()

        if nodo == objetivo:
            return camino

        if nodo not in visitados:
            visitados.add(nodo)

            for vecino in grafo.get(nodo, {}):
                pila.append((vecino, camino + [vecino]))

    return None


# 🔹 3. Costo uniforme (UCS)
def busqueda_costo_uniforme(grafo, inicio, objetivo):
    cola = []
    contador = 0  # 🔥 evita error

    heapq.heappush(cola, (0, contador, inicio))
    padres = {inicio: None}
    costos = {inicio: 0}

    while cola:
        costo_actual, _, nodo = heapq.heappop(cola)

        if nodo == objetivo:
            return reconstruir_camino(padres, inicio, objetivo), costo_actual

        for vecino, peso in grafo.get(nodo, {}).items():
            nuevo_costo = costo_actual + peso

            if vecino not in costos or nuevo_costo < costos[vecino]:
                costos[vecino] = nuevo_costo
                padres[vecino] = nodo
                contador += 1
                heapq.heappush(cola, (nuevo_costo, contador, vecino))

    return None, None