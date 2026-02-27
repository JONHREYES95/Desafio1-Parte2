"""
Sistema de Servicios Empresariales - Backend principal.
Arquitectura de 3 capas: presentación (templates), lógica (rutas), datos (SQLite).
Todo el backend en un solo archivo para simplicidad.
"""

import sqlite3
import os
from flask import Flask, render_template, request, redirect, url_for

# -----------------------------------------------------------------------------
# Configuración de la aplicación Flask
# -----------------------------------------------------------------------------
app = Flask(__name__)
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "empresa.db")


def get_db():
    """Obtiene una conexión a SQLite. Cada request usa su propia conexión."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Permite acceder por nombre de columna
    return conn


def init_db():
    """
    Crea las tablas si no existen y carga los 3 servicios fijos en 'servicios'.
    Se ejecuta al arrancar la aplicación.
    """
    conn = get_db()
    cur = conn.cursor()

    # Tabla clientes
    cur.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            telefono TEXT,
            correo TEXT
        )
    """)

    # Tabla servicios
    cur.execute("""
        CREATE TABLE IF NOT EXISTS servicios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL
        )
    """)

    # Comprobar si ya hay servicios (para no duplicar al reiniciar)
    cur.execute("SELECT COUNT(*) FROM servicios")
    if cur.fetchone()[0] == 0:
        cur.executemany(
            "INSERT INTO servicios (nombre) VALUES (?)",
            [
                ("Mantenimiento Preventivo",),
                ("Reparación",),
                ("Limpieza",),
            ],
        )

    # Tabla solicitudes (FK a clientes y servicios)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS solicitudes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER NOT NULL,
            servicio_id INTEGER NOT NULL,
            estado TEXT DEFAULT 'Pendiente',
            FOREIGN KEY (cliente_id) REFERENCES clientes(id),
            FOREIGN KEY (servicio_id) REFERENCES servicios(id)
        )
    """)

    conn.commit()
    conn.close()


# -----------------------------------------------------------------------------
# RUTAS - Vista de Clientes
# -----------------------------------------------------------------------------


@app.route("/clientes", methods=["GET", "POST"])
def clientes():
    """
    GET: Muestra la página de clientes con formulario y listado.
    POST: Inserta un nuevo cliente y redirige a la misma vista.
    """
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        telefono = request.form.get("telefono", "").strip()
        correo = request.form.get("correo", "").strip()
        if nombre:
            conn = get_db()
            conn.execute(
                "INSERT INTO clientes (nombre, telefono, correo) VALUES (?, ?, ?)",
                (nombre, telefono, correo),
            )
            conn.commit()
            conn.close()
        return redirect(url_for("clientes"))

    # GET: leer todos los clientes para la tabla
    conn = get_db()
    cur = conn.execute("SELECT id, nombre, telefono, correo FROM clientes ORDER BY id")
    lista_clientes = cur.fetchall()
    conn.close()

    return render_template("clientes.html", clientes=lista_clientes)


# -----------------------------------------------------------------------------
# RUTAS - Vista de Solicitudes
# -----------------------------------------------------------------------------


@app.route("/solicitudes", methods=["GET", "POST"])
def solicitudes():
    """
    GET: Muestra la página de solicitudes con formulario y listado.
    POST: Inserta una nueva solicitud y redirige a la misma vista.
    """
    conn = get_db()

    if request.method == "POST":
        cliente_id = request.form.get("cliente_id")
        servicio_id = request.form.get("servicio_id")
        if cliente_id and servicio_id:
            conn.execute(
                "INSERT INTO solicitudes (cliente_id, servicio_id, estado) VALUES (?, ?, 'Pendiente')",
                (cliente_id, servicio_id),
            )
            conn.commit()
        conn.close()
        return redirect(url_for("solicitudes"))

    # GET: cargar clientes y servicios para los selects
    cur = conn.execute("SELECT id, nombre FROM clientes ORDER BY nombre")
    lista_clientes = cur.fetchall()
    cur = conn.execute("SELECT id, nombre FROM servicios ORDER BY id")
    lista_servicios = cur.fetchall()

    # Listado de solicitudes con nombre de cliente y servicio (JOIN)
    cur = conn.execute("""
        SELECT s.id, s.estado, c.nombre AS cliente_nombre, sv.nombre AS servicio_nombre
        FROM solicitudes s
        JOIN clientes c ON s.cliente_id = c.id
        JOIN servicios sv ON s.servicio_id = sv.id
        ORDER BY s.id
    """)
    lista_solicitudes = cur.fetchall()
    conn.close()

    return render_template(
        "solicitudes.html",
        clientes=lista_clientes,
        servicios=lista_servicios,
        solicitudes=lista_solicitudes,
    )


@app.route("/solicitudes/actualizar-estado", methods=["POST"])
def actualizar_estado_solicitud():
    """
    Recibe el id de la solicitud y el nuevo estado por POST.
    Actualiza la fila y redirige a /solicitudes.
    """
    solicitud_id = request.form.get("solicitud_id")
    nuevo_estado = request.form.get("estado")
    if solicitud_id and nuevo_estado and nuevo_estado in ("Pendiente", "En Proceso", "Terminado"):
        conn = get_db()
        conn.execute("UPDATE solicitudes SET estado = ? WHERE id = ?", (nuevo_estado, solicitud_id))
        conn.commit()
        conn.close()
    return redirect(url_for("solicitudes"))


# -----------------------------------------------------------------------------
# Ruta raíz: redirigir a clientes
# -----------------------------------------------------------------------------


@app.route("/")
def index():
    """Redirige al usuario a la vista de clientes."""
    return redirect(url_for("clientes"))


# -----------------------------------------------------------------------------
# Punto de entrada
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5000)
