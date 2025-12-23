from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'default_bus_key')

# Database connection: Uses Internal Database URL from Render settings
# IMPORTANT: Render's URL starts with 'postgres://', SQLAlchemy needs 'postgresql://'
db_url = os.environ.get('DATABASE_URL')
if db_url and db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = db_url or 'sqlite:///local_test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the table structure (Model)
class BusTrip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.String(50))
    dia = db.Column(db.String(20))
    hora_salida = db.Column(db.String(10))
    hora_llegada = db.Column(db.String(10))
    temperatura = db.Column(db.Float)
    ocupacion = db.Column(db.Integer)
    precipitaciones = db.Column(db.Integer)
    visibilidad = db.Column(db.Integer)

@app.route('/')
def index():
    # READ: Fetch all trips to show on the page
    trips = BusTrip.query.all()
    return render_template('sitio1.html', trips=trips)

@app.route('/procesar-datos', methods=['POST'])
def procesar():
    # WRITE: Receive data from the HTML form
    nuevo_viaje = BusTrip(
        fecha=request.form.get('fecha'),
        dia=request.form.get('dia'),
        hora_salida=request.form.get('hora_salida'),
        hora_llegada=request.form.get('hora_llegada'),
        temperatura=float(request.form.get('temperatura', 0)),
        ocupacion=int(request.form.get('ocupacion', 0)),
        precipitaciones=int(request.form.get('precipitaciones', 0)),
        visibilidad=int(request.form.get('visibilidad', 0))
    )
    db.session.add(nuevo_viaje)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all() # Automatically creates the table in Postgres
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))