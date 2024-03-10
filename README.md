# Serverless Application with Google Cloud Platform (GCP)

This project exemplifies a sophisticated serverless application architecture leveraging the robust services offered by Google Cloud Platform (GCP), encompassing Cloud Functions, Cloud SQL, and Cloud Storage. The engineered solution is designed to automatically engage upon detecting file uploads to a designated Cloud Storage bucket, wherein it invokes a Cloud Function to process the files. Subsequently, it meticulously records each upload event within a Cloud SQL database, ensuring a seamless data flow and operational transparency.

## Directory Structure

The project's directory hierarchy is meticulously structured to facilitate ease of navigation and comprehension, ensuring a logical separation of components and resources:

```plaintext
/pulumi
├── components.py           # Pulumi components encapsulating the GCP resource declarations.
├── exa
│   └── function_source.zip # Archived source code for the Cloud Function, prepared for deployment.
├── function_source         # Source code repository for the Cloud Function.
│   ├── main.py             # Primary script of the Cloud Function, embodying the business logic.
│   └── requirements.txt    # Dependencies requisite for the Cloud Function's execution environment.
├── function_source.zip     # Compressed Cloud Function source code, streamlined for deployment.
├── gcp_credentials.json    # Authentication credentials for GCP, pivotal for programmatic access.
├── __init__.py
├── __main__.py             # Principal Pulumi script, orchestrating the deployment of the infrastructure.
├── Pulumi.dev.yaml         # Pulumi configuration file for the development stack, defining stack-specific settings.
├── Pulumi.yaml             # Core Pulumi project file, delineating project metadata.
├── requirements.txt        # Dependency manifest for Pulumi scripts, ensuring environmental consistency.
└── script.sh               # Ancillary script, potentially aiding in automation or setup procedures.
```

## Setup Instructions

### Install Pulumi

Initiate by installing Pulumi on your system, adhering to the [official documentation](https://www.pulumi.com/docs/get-started/install/). Pulumi serves as the foundation for deploying and managing cloud infrastructure as code, encapsulating complex provisioning logic into concise, versionable artifacts.

### Configure GCP Credentials

1. Ascertain the presence of a `gcp_credentials.json` file, which embodies the service account credentials necessary for authenticating with GCP.
2. Engrave the `GOOGLE_APPLICATION_CREDENTIALS` environment variable into your system's profile to ensure persistent authentication sessions across terminal instances:
    ```sh
    export GOOGLE_APPLICATION_CREDENTIALS="/path/to/gcp_credentials.json"
    ```

### Install Dependencies

Navigate to the project's root directory and instigate the installation of Python dependencies critical for the project's operation:
```sh
pip install -r requirements.txt
```

### Deploy the Infrastructure

Execute the following command to propel the deployment of your infrastructure, engaging Pulumi's mechanisms to translate your code into cloud resources:
```sh
pulumi up
```

## Usage

The application is architected to autonomously process files deposited into the designated Cloud Storage bucket. This process encapsulates the logging of upload events to a Cloud SQL database, thereby facilitating data persistence and event traceability.

To dispatch files to the bucket, leverage the Google Cloud Console or the `gsutil` CLI tool:
```sh
gsutil cp your-file.txt gs://your-bucket-name/
```

For operational insights and troubleshooting, consult the Cloud Function logs through the GCP Console.

## Cleanup

To dismantle the deployed resources and avert accruing charges, execute:
```sh
pulumi destroy
```

This operation methodically removes the resources provisioned by Pulumi, reverting the cloud environment to its pre-deployment state.

---

This documentation and the associated project serve as a testament to the capabilities and flexibility of serverless architectures on the Google Cloud Platform. While the information presented herein is crafted with precision and expertise, it's pertinent to acknowledge the ever-evolving landscape of cloud computing and infrastructure management. As such, I encourage continuous exploration and learning to keep abreast of the latest developments and best practices in the field.