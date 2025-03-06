from flask import Flask, make_response, jsonify, request
from database import create_tables
import hipotecas

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return "Bienvenidos al sistema de hipotecas"

@app.route('/clientes', methods=['POST'])
def crearCliente():
    compruebaJSON()
    cliente = request.json
    dni_cliente = cliente['dni_cliente']
    nombre = cliente['nombre']
    email = cliente['email']
    capital = cliente['capital']
    return make_response(jsonify(hipotecas.crearCliente(dni_cliente, nombre, email, capital)), 200)

@app.route('/clientes', methods=['GET'])
def obtenerClientes():
    return make_response(jsonify(hipotecas.obtieneClientes()), 200)

@app.route('/cliente/<dni_cliente>', methods=['GET'])
def obtieneCliente(dni_cliente):
    cliente = hipotecas.obtieneCliente(dni_cliente)
    if cliente:
        return make_response(jsonify(cliente), 200)
    else:
        return make_response(jsonify(cliente), 404)

@app.route('/cliente/<dni_cliente>', methods=['DELETE'])
def eliminaCliente(dni_cliente):
    return make_response(jsonify(hipotecas.eliminaCliente(dni_cliente)), 200)

@app.route('/cliente/<dni_cliente>', methods=['PUT'])
def modificaCliente(dni_cliente):
    compruebaJSON()
    cliente = request.json
    nombre = cliente['nombre']
    email = cliente['email']
    capital = cliente['capital']
    return make_response(jsonify(hipotecas.modificaCliente(dni_cliente, nombre, email, capital)), 200)

@app.route('/cliente/<dni_cliente>/hipoteca', methods=['POST'])
def solicitaSimulacion(dni_cliente):
    compruebaJSON()
    cliente = request.json
    tae = cliente['tae']
    plazo = cliente['plazo']
    return make_response(jsonify(hipotecas.solicitaSimulacion(dni_cliente, tae, plazo)), 200)

def compruebaJSON():
    if not request.is_json:
        return make_response(jsonify({"error": "El cuerpo de la solicitud debe ser JSON"}), 400)

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

