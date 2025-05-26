import sqlite3

def setup_database():
    connection = sqlite3.connect('lib/db/database.db')  
    cursor = connection.cursor()

    print("Setting up database...")

    with open('lib/db/schema.sql') as f:
        schema_sql = f.read()
        cursor.executescript(schema_sql)
        print("Schema applied.")

    
    try:
        import lib.db.seed as seed
        seed.seed_data(cursor)
        print("Seed data inserted.")
    except ModuleNotFoundError:
        print("No seed data module found.")

    connection.commit()
    connection.close()
    print("Database setup complete.")

if __name__ == "__main__":
    setup_database()
