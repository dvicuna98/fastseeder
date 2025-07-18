from dotenv import load_dotenv
load_dotenv()
import os

connector = os.getenv("FASTSEEDER_CONNECTOR")  # e.g. "gcs" or "aws"

if connector == "gcs":
    try:
        import fastseeder.connectors.google_cloud_secret_manager  # registers on import
    except ImportError:
        raise ImportError("GCS connector requested, but not installed. Use: pip install fastseeder[gcs]")

elif connector == "aws":
    try:
        import fastseeder.connectors.aws_secrets_manager
    except ImportError:
        raise ImportError("AWS connector requested, but not installed. Use: pip install fastseeder[aws]")

# else: no connector registered (fallback to DATABASE_URL or manual)