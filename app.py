from flask import Flask, render_template, request, jsonify
import heapq

app = Flask(__name__)

# 🌍 GRAFO DE CIUDADES (tu base)
conexiones = {
    'Jiloyork': {'CDMX': 125, 'Queretaro': 513},
    'Morelos': {'Queretaro': 524},
    'CDMX': {'Jiloyork': 125, 'Queretaro': 423, 'Hidalgo': 491},
    'Hidalgo': {'CDMX': 491, 'Queretaro': 456, 'Mexicali': 309, 'Monterrey': 346},
    'Queretaro': {
        'San Luis Potosi': 203,
        'Morelos': 514,
        'Jiloyork': 513,
        'CDMX': 423,
        'Monterrey': 603,
        'Sonora': 437,
        'Hidalgo': 356,
        'Mexicali': 313,
        'Aguascalientes': 599
    },
    'San Luis Potosi': {'Queretaro': 203, 'Aguascalientes': 390},
    'Aguascalientes': {'San Luis Potosi': 390, 'Queretaro': 599},
    'Sonora': {'Queretaro': 437, 'Mexicali': 394},
    'Mexicali': {'Monterrey': 296, 'Hidalgo': 309, 'Queretaro': 313},
    'Monterrey': {'Hidalgo': 346, 'Queretaro': 603, 'Mexicali': 296}
}


# =========================
# 🔁 RECUPERAR CAMINO
# =========================
def reconstruir_camino(padres, inicio, objetivo):
    camino = []
    actual = objetivo

    while actual:
        camino.append(actual)
        actual = padres.get(actual)

    return camino[::-1]


# =========================
# 🔁 DFS RECURSIVO
# =========================
def dfs_recursivo(grafo, actual, objetivo, visitados=None, camino=None):
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
            res = dfs_recursivo(grafo, vecino, objetivo, visitados, camino.copy())
            if res:
                return res

    return None


# =========================
# 🔁 DFS ITERATIVO
# =========================
def dfs_iterativo(grafo, inicio, objetivo):
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


# =========================
# 💰 COSTO UNIFORME (UCS)
# =========================
def costo_uniforme(grafo, inicio, objetivo):
    cola = []
    contador = 0

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


# =========================
# 🌐 FRONT
# =========================
@app.route('/')
def index():
    return render_template('index.html')


# =========================
# 🚀 EJECUTAR TODO
# =========================
@app.route('/resolver', methods=['POST'])
def resolver():
    data = request.json
    inicio = data['inicio']
    objetivo = data['objetivo']

    if inicio not in conexiones or objetivo not in conexiones:
        return jsonify({"error": "Ciudad no válida"})

    # 🔁 Ejecutar los 3 algoritmos
    recursiva = dfs_recursivo(conexiones, inicio, objetivo)
    profundidad = dfs_iterativo(conexiones, inicio, objetivo)
    costo, valor = costo_uniforme(conexiones, inicio, objetivo)

    return jsonify({
        "recursiva": recursiva,
        "profundidad": profundidad,
        "costo": {
            "camino": costo,
            "costo": valor
        }
    })


# =========================
# ▶️ RUN
# =========================
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)