import os
import pg8000
import json

def process_upload(event, context):
    # Fetching environment variables for database connection
    connection_name = os.getenv("CLOUD_SQL_CONNECTION_NAME")
    db_name = os.getenv("DB_NAME")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASS")

    # Constructing the Unix socket path for the direct connection
    unix_socket_path = f"/cloudsql/{connection_name}/.s.PGSQL.5432"

    try:
        file_name = event.get('name')
        if not file_name:
            raise ValueError("No file name in the event data")

        print(f"Received event for file: {file_name}")

        # Establishing direct database connection
        print("Connecting directly to Cloud SQL using pg8000...")
        connection = pg8000.connect(
            user=db_user,
            password=db_password,
            database=db_name,
            unix_sock=unix_socket_path
        )

        # Performing database operations
        cursor = connection.cursor()
        print("Connected to the database. Ensuring 'uploads' table exists...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS uploads (
                id SERIAL PRIMARY KEY,
                file_name VARCHAR(255) NOT NULL,
                upload_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        print("'uploads' table is ready.")

        print(f"Inserting new upload entry for file: {file_name}")
        cursor.execute(
            "INSERT INTO uploads (file_name, upload_timestamp) VALUES (%s, NOW())",
            (file_name,)
        )
        connection.commit()  # Committing the transaction
        print(f"Successfully processed file: {file_name}")

        # Cleanup
        cursor.close()
        connection.close()

    except Exception as e:
        print(f"Error processing file: {e}")
        return f"Error: {e}"

    return 'ok'
