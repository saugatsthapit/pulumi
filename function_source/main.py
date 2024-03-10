import psycopg2
import os
from google.cloud import secretmanager

def access_secret_version(secret_id, version_id="latest"):
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/787061998366/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode('UTF-8')

def process_upload(event, context):
    """Triggered by a new file upload to the bucket."""
    file_name = event['name']

    # Connect to the database
    db_connection = psycopg2.connect(
        dbname=access_secret_version('DB_NAME'),
        user=access_secret_version('DB_USER'),
        password=access_secret_version('DB_PASSWORD'),
        host=access_secret_version('DB_HOST')
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
