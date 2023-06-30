from flask import Flask, request, jsonify
from flask_cors import CORS
from App import ejecutar_entrada,ast_grafica,rep_errores,rep_tabla_simbolo

app = Flask(__name__)
CORS(app)


@app.route('/')
def hello():
    return "¡Hola, mundo!"


@app.route('/analizar', methods=['POST'])
def process_analizar():
    data = request.json
    # archivo = open(data['analizar'],'r')
    # contenido = archivo.read()
    # archivo.close()
    consola = ejecutar_entrada(data['analizar'])
    #consola = ejecutar_entrada(contenido)
    #print(consola)#borrar
    
    datos = {
        "consola": consola
    }
    return jsonify(datos)

@app.route('/reporte/Ast', methods=['GET'])
def process_ast():
    # Devuelve una respuesta
    ast_base64 = ast_grafica()
    datos = {
        "Ast": ast_base64
    }
    return jsonify(datos)

@app.route('/reporte/TablaSimbolo', methods=['GET'])
def process_tabla_simbolo():
    # Devuelve una respuesta
    tabla_simbolo = rep_tabla_simbolo()
    datos = {
        "Tabla_Simbolo": tabla_simbolo
    }
    return jsonify(datos)

@app.route('/reporte/Errores', methods=['GET'])
def process_excepcion():
    # Devuelve una respuesta
    errores_excepciones = rep_errores()
    datos = {
        "errores": errores_excepciones
    }
    return jsonify(datos)


if __name__ == '__main__':
    app.run()