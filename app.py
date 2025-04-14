from flask import Flask, render_template, request, redirect, url_for, flash, send_file  # type: ignore
from flask_mysqldb import MySQL  # type: ignore
import datetime
import pandas as pd
import os
import io
from dotenv import load_dotenv # type: ignore

load_dotenv()

app = Flask(__name__)

app.config['MYSQL_HOST'] = os.getenv("MYSQL_HOST")
app.config['MYSQL_USER'] = os.getenv("MYSQL_USER")
app.config['MYSQL_PASSWORD'] = os.getenv("MYSQL_PASSWORD")
app.config['MYSQL_DB'] = os.getenv("MYSQL_DB")
mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/comprar', methods=['GET'])
def comprar():
    return render_template('comprar_tickets.html')

@app.route('/comprar', methods=['POST'])
def procesar_compra():
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    email = request.form['correo']
    categoria = request.form['categoria']
    cantidad = int(request.form['cant'])

    if cantidad <= 0:
        flash("La cantidad debe ser mayor a cero", "danger")
        return redirect(url_for('comprar'))

    descuentos = {
        'estudiante': 0.5,
        'profesional': 0.3,
        'orador': 0.1
    }
    descuento = descuentos.get(categoria, 0)
    precio_unitario = 10000
    total = cantidad * precio_unitario * (1 - descuento)

    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO tickets (nombre, email, categoria, cantidad, total, fecha)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (f"{nombre} {apellido}", email, categoria, cantidad, total, datetime.datetime.now()))
    mysql.connection.commit()
    cur.close()

    flash('Compra realizada con éxito', 'success')
    return render_template('confirmacion.html', nombre=nombre, email=email, cantidad=cantidad, categoria=categoria, total=total)

@app.route('/admin/tickets')
def ver_tickets():
    filtro = request.args.get('filtro_categoria')
    busqueda = request.args.get('busqueda')

    cur = mysql.connection.cursor()

    if filtro and busqueda:
        cur.execute("""
            SELECT * FROM tickets
            WHERE categoria = %s AND (nombre LIKE %s OR email LIKE %s)
            ORDER BY fecha DESC
        """, (filtro, f"%{busqueda}%", f"%{busqueda}%"))
    elif filtro:
        cur.execute("SELECT * FROM tickets WHERE categoria = %s ORDER BY fecha DESC", (filtro,))
    elif busqueda:
        cur.execute("SELECT * FROM tickets WHERE nombre LIKE %s OR email LIKE %s ORDER BY fecha DESC", (f"%{busqueda}%", f"%{busqueda}%"))
    else:
        cur.execute("SELECT * FROM tickets ORDER BY fecha DESC")

    tickets = cur.fetchall()
    cur.close()
    return render_template('admin_tickets.html', tickets=tickets)

@app.route('/admin/exportar')
def exportar_excel():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, nombre, email, categoria, cantidad, total, fecha FROM tickets ORDER BY fecha DESC")
    datos = cur.fetchall()
    columnas = ['ID', 'Nombre', 'Email', 'Categoría', 'Cantidad', 'Total', 'Fecha']
    cur.close()

    df = pd.DataFrame(datos, columns=columnas)

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Tickets')

    output.seek(0)
    return send_file(output, download_name="tickets.xlsx", as_attachment=True)
if __name__ == '__main__':
    app.run(debug=True)
