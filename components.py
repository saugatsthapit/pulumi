import pulumi
from pulumi import ComponentResource, Output
import pulumi_gcp as gcp
import psycopg2
from pulumi.asset import FileArchive, AssetArchive, FileAsset
import zipfile
import os


class ServerlessApp(ComponentResource):
    def __init__(self, name: str, opts=None):
        super().__init__('pkg:index:ServerlessApp', name, {}, opts)

        # Function to zip the source directory
        def zip_directory(source_dir, output_filename):
            with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(source_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        zipf.write(file_path, os.path.relpath(file_path, os.path.join(source_dir, '..')))

        # Specify the source directory and the output zip filename
        source_dir = './function_source'
        zip_filename = 'function_source.zip'  # Adjust path if running pulumi up outside the directory

        # Zip the source directory
        zip_directory(source_dir, zip_filename)

        # Create a Google Cloud Storage bucket for triggering the Cloud Function
        self.bucket = gcp.storage.Bucket(f"{name}-bucket",
                                         location="US")

        # Create a Google Cloud Storage bucket for the function source code
        source_code_bucket = gcp.storage.Bucket(f"{name}-source-code-bucket",
                                                location="US")

        # Upload the zipped source code to the bucket
        source_code_object = gcp.storage.BucketObject(f"{name}-function-source",
            bucket=source_code_bucket.name,
            source=FileAsset(zip_filename)  # Use FileAsset to upload the zip file
        )

        # Create a Google Cloud Function to process uploads
        self.function = gcp.cloudfunctions.Function(f"{name}-function",
            entry_point="process_upload",
            runtime="python37",
            region="us-central1",  # Specify the desired region for your Cloud Function
            source_archive_bucket=source_code_bucket.name,
            source_archive_object=source_code_object.name,
            event_trigger={
                "event_type": "google.storage.object.finalize",
                "resource": self.bucket.id.apply(lambda id: f"projects/_/buckets/{id}"),
            },
        )

        self.register_outputs({
            'upload_bucket_name': self.bucket.name,
            'function_name': self.function.name,
        })



class CloudSqlInstance(ComponentResource):
    def __init__(self, name: str, opts=None):
        super().__init__('pkg:index:CloudSqlInstance', name, {}, opts)

        # Create a Cloud SQL instance with corrected IP configuration
        self.instance = gcp.sql.DatabaseInstance(f"{name}-instance",
            database_version="POSTGRES_13",
            region="us-central1",
            settings=gcp.sql.DatabaseInstanceSettingsArgs(
                tier="db-f1-micro",
                ip_configuration=gcp.sql.DatabaseInstanceSettingsIpConfigurationArgs(
                    ipv4_enabled=True,
                ),
            ),
        )

        # Create a SQL database
        self.database = gcp.sql.Database(f"{name}-db",
            instance=self.instance.name,
            charset="UTF8",
            collation="en_US.UTF8")

        self.register_outputs({
            'instance_name': self.instance.name,
            'database_name': self.database.name,
            'instance_connection_name': self.instance.connection_name,
            # You might need to manually extract the public IP address after instance creation
        })


class DatabaseSchemaInfo(ComponentResource):
    def __init__(self, name: str, cloud_sql_instance: CloudSqlInstance, opts=None):
        super().__init__('my:module:DatabaseSchemaInfo', name, {}, opts)

        # Assuming cloud_sql_instance is an instance of CloudSqlInstance
        # This just passes along the information; actual schema management is done externally
        self.instance_name = cloud_sql_instance.instance.name
        self.database_name = cloud_sql_instance.database.name
        # Example for public IP - ensure you're capturing this correctly depending on your setup
        self.instance_connection_name = cloud_sql_instance.instance.connection_name

        self.register_outputs({
            'instance_name': self.instance_name,
            'database_name': self.database_name,
            'instance_connection_name': self.instance_connection_name,
        })
