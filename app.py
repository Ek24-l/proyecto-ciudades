from flask import Flask, render_template, request, jsonify
from busquedas import *
import os

app = Flask(__name__)

# 🌍 TU GRAFO
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

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/buscar', methods=['POST'])
def buscar():
    data = request.json
    inicio = data['inicio']
    objetivo = data['objetivo']
    metodo = data['metodo']

    if inicio not in conexiones or objetivo not in conexiones:
        return jsonify({"error": "Ciudad no válida"})

    if metodo == "recursiva":
        camino = busqueda_recursiva(conexiones, inicio, objetivo)
        return jsonify({"camino": camino})

    elif metodo == "profundidad":
        camino = busqueda_profundidad(conexiones, inicio, objetivo)
        return jsonify({"camino": camino})

    elif metodo == "costo":
        camino, costo = busqueda_costo_uniforme(conexiones, inicio, objetivo)
        return jsonify({"camino": camino, "costo": costo})

    return jsonify({"error": "Método inválido"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))