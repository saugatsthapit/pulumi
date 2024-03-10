from components import ServerlessApp, CloudSqlInstance, DatabaseSchemaInfo

# Instantiate the CloudSqlInstance component
sql_instance = CloudSqlInstance('my-serverless-app')

# Pass the sql_instance to DatabaseSchemaInfo for capturing details
database_schema_info = DatabaseSchemaInfo('my-database-schema-setup', sql_instance)

# Instantiate the ServerlessApp component
app = ServerlessApp('my-serverless-app')
