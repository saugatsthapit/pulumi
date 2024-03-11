import pulumi
import pulumi_gcp as gcp
from components import ServerlessApp, CloudSqlInstance, DatabaseSchemaInfo


# Enable necessary GCP services
cloud_functions_service = gcp.projects.Service("cloud-functions-service",
    service="cloudfunctions.googleapis.com")

cloud_sql_service = gcp.projects.Service("cloud-sql-service",
    service="sqladmin.googleapis.com")

storage_service = gcp.projects.Service("storage-service",
    service="storage.googleapis.com")

# Enable the IAM API
iam_service = gcp.projects.Service("iam-service",
    service="iam.googleapis.com")


# Ensure the service account exists, with explicit dependency on the IAM API enablement
service_account = gcp.serviceaccount.Account("pulumi-service-account",
    account_id="pulumi",
    display_name="Pulumi Service Account",
    project="hybrid-text-412119",
    opts=pulumi.ResourceOptions(depends_on=[iam_service]))

# List of roles to assign
roles = [
    "roles/cloudfunctions.admin",
    "roles/cloudsql.admin",
    "roles/cloudsql.client",
    "roles/compute.storageAdmin",
    "roles/owner",
    "roles/secretmanager.admin"
]

project_id = "hybrid-text-412119"

# Assign roles to the service account
for role in roles:
    iam_member = gcp.projects.IAMMember(f"pulumi-service-account-{role.split('/')[-1]}",
        role=role,
        member=pulumi.Output.concat("serviceAccount:", service_account.email),
        project=project_id,  # Specify the project ID here
        opts=pulumi.ResourceOptions(parent=service_account))

# Instantiate your infrastructure components below
# Instantiate the CloudSqlInstance component
sql_instance = CloudSqlInstance('my-serverless-app',
                                opts=pulumi.ResourceOptions(depends_on=[cloud_sql_service]))

# Pass the sql_instance to DatabaseSchemaInfo for capturing details
database_schema_info = DatabaseSchemaInfo('my-database-schema-setup', sql_instance)

# Instantiate the ServerlessApp component
app = ServerlessApp('my-serverless-app',
                    opts=pulumi.ResourceOptions(depends_on=[cloud_functions_service, storage_service, service_account]))
