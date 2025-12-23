import pandas as pd
import os
from sqlalchemy import create_engine

def analizar_desde_db():
    db_url = os.environ.get('DATABASE_URL')
    if not db_url:
        print("Error: No se encontró DATABASE_URL")
        return

    # Fix URL for SQLAlchemy compatibility
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)

    engine = create_engine(db_url)
    
    # Read directly from the database table 'bus_trip'
    df = pd.read_sql('SELECT * FROM bus_trip', engine)
    
    if df.empty:
        print("La base de datos está vacía.")
        return

    # Your existing analysis logic (unchanged)
    concurrencia_promedio = df['ocupacion'].mean()
    print(f"Concurrencia Promedio: {concurrencia_promedio:.2f}")

if __name__ == '__main__':
    analizar_desde_db()