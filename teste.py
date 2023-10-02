import psycopg2
from psycopg2 import OperationalError

# Database connection parameters
parametros = dict(
    host='localhost',
    port=5432,
    user='livia',
    password='livia',
    database='postgres'
)
# Create a connection to the default 'postgres' database
try:
    connection = psycopg2.connect(**parametros)

    # Create a new database (e.g., 'mynewdb')
    new_db_name = 'mynewdb'
    with connection.cursor() as cursor:
        cursor.execute(f"CREATE DATABASE {new_db_name};")

    # Commit the transaction and close the connection
    connection.commit()
    connection.close()
    print(f"Database '{new_db_name}' created successfully.")

except OperationalError as e:
    print(f"Error: {e}")
