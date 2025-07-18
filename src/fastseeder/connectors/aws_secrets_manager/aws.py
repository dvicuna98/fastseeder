import os
import boto3

def aws_secret_resolver():
    secret_name = os.getenv("AWS_DB_URI_SECRET_NAME")
    if not secret_name:
        return None  # Resolver not used

    region_name = os.getenv("AWS_REGION")
    if not region_name:
        raise ValueError("AWS_REGION must be set to use AWS Secrets Manager.")

    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name=region_name)

    response = client.get_secret_value(SecretId=secret_name)
    secret_string = response.get("SecretString")

    if not secret_string:
        raise ValueError("Secret found but has no SecretString content.")

    return secret_string

