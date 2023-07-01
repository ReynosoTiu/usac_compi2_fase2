from Analizador_Sintactico import ejecutar_entrada, getTablaSimbolos, getErrores
from flask import Flask, request, jsonify
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

@app.route('/', methods = ["GET"])
def saludo():
    return {"mensaje": "Hola mundo!"}

@app.route('/analizar', methods = ["POST"])
def compilar():
    data = request.json
    consola = ejecutar_entrada(data['analizar'])
    datos = {
        "consola": consola
    }
    return jsonify(datos)

@app.route('/reporte/TablaSimbolo', methods=['GET'])
def process_tabla_simbolo():
    # Devuelve una respuesta
    tabla_simbolo = getTablaSimbolos()
    datos = {
        "Tabla_Simbolo": tabla_simbolo
    }
    return jsonify(datos)

@app.route('/reporte/Errores', methods=['GET'])
def process_excepcion():
    # Devuelve una respuesta
    errores_excepciones = getErrores()
    datos = {
        "errores": errores_excepciones
    }
    return jsonify(datos)

if __name__ == '__main__':
    app.run()