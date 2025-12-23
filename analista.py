import pandas as pd
import os
from sqlalchemy import create_engine

def analizar_desde_db():
    db_url = os.environ.get('DATABASE_URL')
    if not db_url:
        print("Error: DATABASE_URL not found.")
        return

    # Connection string fix
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)

    engine = create_engine(db_url)
    
    # Load data into Pandas
    try:
        df = pd.read_sql('SELECT * FROM bus_trip', engine)
        if df.empty:
            print("Database is empty.")
            return

        # Simple example calculation
        avg_temp = df['temperatura'].mean()
        print(f"Average Temp recorded: {avg_temp:.2f}°C")
    except Exception as e:
        print(f"Analysis Error: {e}")

if __name__ == '__main__':
    analizar_desde_db()
