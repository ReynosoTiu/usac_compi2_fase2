from Analizador_Sintactico import ejecutar_entrada, getTablaSimbolos, getErrores
from flask import Flask, request, jsonify
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

@app.route('/', methods = ["GET"])
def saludo():
    return {"mensaje": "Hola mundo!"}

# @app.route('/getLastExecution', methods = ["GET"])
# def Last():
#     return LastExecution

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


    # if request.method == "POST":
    #     entrada = request.data.decode("utf-8")
    #     entrada = json.loads(entrada)
    #     #print(entrada)
    #     global tmp_val
    #     tmp_val = entrada["analizar"]
    #     global editor
    #     editor = entrada["analizar"]
    #     return redirect(url_for("salida"))
    # else:
    #     return {"mensaje": "No compilado"}

# global LastExecution
# LastExecution = { "errores":"si" }
# @app.route('/salida')
# def salida():
#     global tmp_val
#     global Tabla
#     Tabla = {}

#     genAux = Generador()
#     genAux.cleanAll() # Limpia todos los archivos anteriores
#     generador = genAux.getInstance()

#     instrucciones = Analizar(tmp_val)
#     ast = Arbol(instrucciones)
#     tsg = TablaSimbolos()
#     ast.setTsglobal(tsg)
#     rep = "<table><tr><th>Nombre</th><th>Tipo</th><th>Ambito</th>"
#     for instruccion in ast.getInstr():
#         # if not (isinstance(instruccion, Function)):
#         value = instruccion.interpretar(ast, tsg)
#         if isinstance(value, Error):
#             ast.getErrores().append(value)
#             # aqui es opcional el que se muestren los errores en consola
#             # ast.updateConsola(value.toString())
#     rep += "<th>Posicion</th></tr>"
#     rep += tsg.htable
#     rep += "</table>"
#     consola = str(generador.getCode())
#     #print(generador.getCode())

#     # Imprimiendo lista de errores
#     tablaErr = "<table><tr><th>TIPO</th><th>DESCRIPCION</th>"
#     tablaErr += "<th>FILA</th><th>COLUMNA</th></tr>"
#     for err in ast.getErrores():
#         tablaErr += "<tr>"
#         temporal = err.toString().split("-")
#         for tem in temporal:
#             tablaErr += f"<th>{tem}</th>"
#         tablaErr += "</tr>"
#         # print(err.toString())
#     tablaErr += "<table>"
#     global Simbolos
#     Simbolos = ast.getTsglobal().getTablaG()
#     #consola = str(ast.getConsola())

#     print('Consola: ', consola)
#     global LastExecution
#     LastExecution = {'consola': consola, 'errores': tablaErr, 'editor': editor, 'simbolos':rep, 'ast':""}
#     return json.dumps(LastExecution)

if __name__ == '__main__':
    app.run()