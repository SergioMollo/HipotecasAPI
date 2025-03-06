from flask import Flask, request
from database import get_db
import re
import sqlite3

DNI_EXPRESION = "[0-9]{8}[A-Z]"
DIGITO_CONTROL = "TRWAGMYFPDXBNJZSQVHLCKE"
EMAIL_EXPRESION = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
NOMBRE_EXPRESION = "[A-Z][a-zA-Z]+"

app = Flask(__name__)

def crearCliente(dni_cliente, nombre, email, capital):
    if comprobarDNI(dni_cliente) and comprobarNombre(nombre) and comprobarEmail(email) and comprobarFloat(capital):
        db = get_db()
        cursor = db.cursor()
        query = "INSERT INTO clientes(dni_cliente, nombre, email, capital) VALUES (?, ?, ?, ?)"
        cursor.execute(query, [dni_cliente, nombre, email, capital])
        db.commit()
        return True
    return False

def obtieneClientes():
    db = get_db()
    cursor = db.cursor()
    query = "SELECT dni_cliente, nombre, email, capital FROM clientes"
    cursor.execute(query)
    clientes_data = cursor.fetchall()
    clientes = []

    for cliente in clientes_data:  
        clientes.append(dict(cliente))

    return clientes

def obtieneCliente(dni_cliente):
    if comprobarDNI(dni_cliente):
        db = get_db()
        cursor = db.cursor()
        query = "SELECT dni_cliente, nombre, email, capital FROM clientes WHERE dni_cliente = ?"
        cursor.execute(query, [dni_cliente])
        cliente = cursor.fetchone()

        cursor2 = db.cursor()
        query2 = "SELECT tae, plazo, cuota_mensual, importe_total FROM hipotecas WHERE dni_cliente = ?"
        cursor2.execute(query2, [dni_cliente])
        hipoteca = cursor2.fetchone()

        if not cliente:
            return None  
        hipoteca = dict(hipoteca) if hipoteca else None

        cliente = dict(cliente)
        cliente["hipoteca"] = hipoteca

        return [cliente]
    return None

def eliminaCliente(dni_cliente):
    if comprobarDNI(dni_cliente):
        db = get_db()
        cursor = db.cursor()
        query = "DELETE FROM clientes WHERE dni_cliente = ?"
        cursor.execute(query, [dni_cliente])
        db.commit()
        return True
    return False

def modificaCliente(dni_cliente, nombre, email, capital):
    if comprobarDNI(dni_cliente) and comprobarNombre(nombre) and comprobarEmail(email) and comprobarFloat(capital):
        db = get_db()
        cursor = db.cursor()
        query = "UPDATE clientes SET nombre = ?, email = ?, capital = ? WHERE dni_cliente = ?"
        cursor.execute(query, [nombre, email, capital, dni_cliente])
        db.commit()
        return True
    return False

def solicitaSimulacion(dni_cliente, tae, plazo):
    if comprobarDNI(dni_cliente) and comprobarFloat(tae) and comprobarFloat(plazo):
        db = get_db()
        cursor = db.cursor()

        query = "SELECT capital FROM clientes WHERE dni_cliente = ?"
        cursor.execute(query, [dni_cliente])
        result = cursor.fetchone()
        
        capital = result[0]
        cuota = calculaCuota(capital, tae, plazo)
        importe = cuota * plazo

        query = "INSERT INTO hipotecas(dni_cliente, tae, plazo, cuota_mensual, importe_total) VALUES (?, ?, ?, ? , ?)"
        cursor.execute(query, [dni_cliente, tae, plazo, cuota, importe])
        db.commit()
        return True
    return False

def comprobarDNI(dni):
    if not re.match(DNI_EXPRESION, dni):
        return False
    return dni[8] == DIGITO_CONTROL[int(dni[:8]) % 23]

def comprobarNombre(nombre):
    if re.match(NOMBRE_EXPRESION, nombre):
        return True
    return False

def comprobarEmail(email):
    if re.match(EMAIL_EXPRESION, email):
        return True
    return False

def comprobarEntero(valor):
    try:
        return int(valor) > 0
    except ValueError:
        return False

def comprobarFloat(valor):
    try:
        return float(valor) > 0
    except ValueError:
        return False

def calculaCuota(capital, tae, plazo):
    interes = tae / 100 / 12
    meses = plazo * 12
    cuota = (capital * interes) / (1 - (1 + interes)**(-meses))
    return cuota

