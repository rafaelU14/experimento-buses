from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'bus_experiment_quito_2025')

# FIX: Force PostgreSQL dialect for SQLAlchemy
db_url = os.environ.get('DATABASE_URL')
if db_url and db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Table Model
class BusTrip(db.Model):
    __tablename__ = 'bus_trip' # Explicitly naming the table
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.String(50))
    dia = db.Column(db.String(20))
    hora_salida = db.Column(db.String(10))
    hora_llegada = db.Column(db.String(10))
    temperatura = db.Column(db.Float)
    ocupacion = db.Column(db.Integer)
    precipitaciones = db.Column(db.Integer)
    visibilidad = db.Column(db.Integer)

# Create tables immediately upon script execution
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    try:
        trips = BusTrip.query.order_by(BusTrip.id.desc()).all()
        return render_template('sitio1.html', trips=trips)
    except Exception as e:
        return f"Database Error: {e}. Check if tables were created."

@app.route('/procesar-datos', methods=['POST'])
def procesar():
    nuevo_viaje = BusTrip(
        fecha=request.form.get('fecha'),
        dia=request.form.get('dia'),
        hora_salida=request.form.get('hora_salida'),
        hora_llegada=request.form.get('hora_llegada'),
        temperatura=float(request.form.get('temperatura', 0)),
        ocupacion=int(request.form.get('ocupacion', 1)),
        precipitaciones=int(request.form.get('precipitaciones', 1)),
        visibilidad=int(request.form.get('visibilidad', 1))
    )
    db.session.add(nuevo_viaje)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
