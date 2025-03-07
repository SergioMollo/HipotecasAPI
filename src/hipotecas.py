from flask import Flask, request
from database import get_db
import re
import sqlite3

DNI_EXPRESION = "[0-9]{8}[A-Z]"
DIGITO_CONTROL = "TRWAGMYFPDXBNJZSQVHLCKE"
EMAIL_EXPRESION = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
NOMBRE_EXPRESION = "[A-Z][a-zA-Z]+"

app = Flask(__name__)

# Crea un cliente no registrado en el sistema mediante su dni, nombre, email y capital
def crearCliente(dni_cliente, nombre, email, capital):
    if comprobarDNI(dni_cliente) and comprobarNombre(nombre) and comprobarEmail(email) and comprobarFloat(capital):
        db = get_db()
        cursor = db.cursor()
        query = "SELECT * FROM clientes WHERE dni_cliente = ?"
        cursor.execute(query, [dni_cliente])

        if cursor.fetchone() is None:
            try:
                query = "INSERT INTO clientes(dni_cliente, nombre, email, capital) VALUES (?, ?, ?, ?)"
                cursor.execute(query, [dni_cliente, nombre, email, capital])
                db.commit()
                return f"Cliente registrado correctamente"
            except sqlite3.IntegrityError as e:
                return f"Error al insertar datos: {e}"
            except sqlite3.Error as e:
                return f"Error al insertar datos: {e}"
        else:
            return f"El dni introducido ya está registrado"
    return f"Los datos introducidos no son correctos"


# Obtiene los clientes registrados en el sistema
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

# Obtiene un cliente registrado en el sistema mediante su dni
#   Devuelve la informacion del cliente
#   Devuelve los datos asociados a la hipoteca en caso de existir
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

# Elimina un cliente registrado en el sistema mediante su dni
def eliminaCliente(dni_cliente):
    if comprobarDNI(dni_cliente):
        db = get_db()
        cursor = db.cursor()
        query = "SELECT * FROM clientes WHERE dni_cliente = ?"
        cursor.execute(query, [dni_cliente])

        if cursor.fetchone() is not None:
            try:
                query = "DELETE FROM clientes WHERE dni_cliente = ?"
                cursor.execute(query, [dni_cliente])
                query = "DELETE FROM hipotecas WHERE dni_cliente = ?"
                cursor.execute(query, [dni_cliente])
                db.commit()
                return f"Cliente eliminado correctamente"
            except sqlite3.IntegrityError as e:
                return f"Error al eliminar datos: {e}"
            except sqlite3.Error as e:
                return f"Error al eliminar datos: {e}"
        else:
            return f"El dni introducido no está registrado"
    return f"El dni introducido no es correcto"

# Actualiza la informacion un cliente registrado en el sistema mediante su dni, nombre, email y capital
def modificaCliente(dni_cliente, nombre, email, capital):
    if comprobarDNI(dni_cliente) and comprobarNombre(nombre) and comprobarEmail(email) and comprobarFloat(capital):
        db = get_db()
        cursor = db.cursor()
        query = "SELECT * FROM clientes WHERE dni_cliente = ?"
        cursor.execute(query, [dni_cliente])

        if cursor.fetchone() is not None:
            try:
                query = "UPDATE clientes SET nombre = ?, email = ?, capital = ? WHERE dni_cliente = ?"
                cursor.execute(query, [nombre, email, capital, dni_cliente])
                db.commit()
                return f"Informacion del cliente modificada correctamente"
            except sqlite3.IntegrityError as e:
                return f"Error al modificar datos: {e}"
            except sqlite3.Error as e:
                return f"Error al modificar datos: {e}"
        else:
            return f"El dni introducido no está registrado"
    return f"Los datos introducidos no son correctos"

# Simula el calculo de la hipoteca un cliente registrado en el sistema mediante su dni, tae y plazo
def solicitaSimulacion(dni_cliente, tae, plazo):
    if comprobarDNI(dni_cliente) and comprobarFloat(tae) and comprobarFloat(plazo):
        db = get_db()
        cursor = db.cursor()
        query = "SELECT capital FROM clientes WHERE dni_cliente = ?"
        cursor.execute(query, [dni_cliente])
        result = cursor.fetchone()

        if result is not None:
            capital = result[0]
            cuota = calculaCuota(capital, tae, plazo)
            importe = cuota * plazo

            try:
                query = "INSERT INTO hipotecas(dni_cliente, tae, plazo, cuota_mensual, importe_total) VALUES (?, ?, ?, ?, ?)"
                cursor.execute(query, [dni_cliente, tae, plazo, cuota, importe])
                db.commit()
                return f"Simulacion de hipoteca realizada correctamente"
            except sqlite3.IntegrityError as e:
                return f"Error al modificar datos: {e}"
            except sqlite3.Error as e:
                return f"Error al modificar datos: {e}"
        else:
            return f"El dni introducido no está registrado"
    return f"Los datos introducidos no son correctos"

# Comprueba la validez del dni segun el algoritmo oficial
def comprobarDNI(dni):
    if not re.match(DNI_EXPRESION, dni):
        return False
    return dni[8] == DIGITO_CONTROL[int(dni[:8]) % 23]

# Comprueba la validez del nombre admitiendo unicamente letras
def comprobarNombre(nombre):
    if re.match(NOMBRE_EXPRESION, nombre):
        return True
    return False

# Comrpueba la validez del email siguiendo la nomenclatura habitual
def comprobarEmail(email):
    if re.match(EMAIL_EXPRESION, email):
        return True
    return False

# Comprueba que el numero es un entero
def comprobarEntero(valor):
    try:
        return int(valor) > 0
    except ValueError:
        return False

# Comprueba que el numero es un valor en punto flotante
def comprobarFloat(valor):
    try:
        return float(valor) > 0
    except ValueError:
        return False

# Calcula la cuota para la hipoteca solicitada
#   cuota = capital * i / (1 - (1 + i) ^ (-n))
#	capital es el importe del préstamo hipotecario
#	i es el tipo de interés mensual (TAE / 100 / 12)
#	n es el número de meses del plazo de amortización (plazo * 12)
def calculaCuota(capital, tae, plazo):
    interes = tae / 100 / 12
    meses = plazo * 12
    cuota = (capital * interes) / (1 - (1 + interes)**(-meses))
    return cuota

