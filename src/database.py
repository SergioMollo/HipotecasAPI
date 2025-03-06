import sqlite3

DATABASE_NAME = "hipotecaAPI.db"

# Inicializa la base de datos
def get_db():
    db = sqlite3.connect(DATABASE_NAME)
    db.row_factory = sqlite3.Row
    return db

# Crea las tablas de la base de datos si no existen
def create_tables():
    tables = [
        """CREATE TABLE IF NOT EXISTS clientes(
                dni_cliente TEXT PRIMARY KEY,
                nombre TEXT NOT NULL,
				email TEXT NOT NULL,
				capital REAL NOT NULL
            )
            """,
            """CREATE TABLE IF NOT EXISTS hipotecas(
                dni_cliente TEXT PRIMARY KEY,
                tae REAL NOT NULL,
				plazo INTEGER NOT NULL,
				cuota_mensual REAL NOT NULL,
                importe_total REAL NOT NULL
            )
            """
    ]
    db = get_db()
    cursor = db.cursor()
    for table in tables:
        cursor.execute(table)