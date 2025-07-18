import os
from google.cloud import secretmanager

def gcs_secret_resolver():
    secret_name = os.getenv("GCS_DB_URI_SECRET_NAME")
    if not secret_name:
        raise ValueError("GCS_DB_URI_SECRET_NAME not set")

    project_id = os.getenv("GCP_PROJECT_ID")
    if not project_id:
        raise ValueError("GCP_PROJECT_ID must be set to use GCS secret loading.")

    # Default to "latest" if not set
    version = os.getenv("GCS_DB_URI_SECRET_VERSION", "latest")

    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_name}/versions/{version}"

    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")