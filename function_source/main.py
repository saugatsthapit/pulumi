import psycopg2
import os

def process_upload(event, context):
    """Triggered by a new file upload to the bucket."""
    file_name = event['name']

    # Connect to the database
    db_connection = psycopg2.connect(
        dbname='my-serverless-app-db',
        user='postgres',
        password='Welcome#1234',
        host='35.238.105.47'
    )

    cursor = db_connection.cursor()

    # Ensure the 'uploads' table exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS uploads (
            id SERIAL PRIMARY KEY,
            file_name VARCHAR(255) NOT NULL,
            upload_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # Insert the new upload entry
    cursor.execute(
        "INSERT INTO uploads (file_name, upload_timestamp) VALUES (%s, NOW())",
        (file_name,)
    )

    # Commit the transaction and close the connection
    db_connection.commit()
    cursor.close()
    db_connection.close()

    print(f"Processed file: {file_name}")
