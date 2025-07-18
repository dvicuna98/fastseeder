try:
    from .gcs import gcs_secret_resolver
    from fastseeder.db import register_uri_resolver
    register_uri_resolver(gcs_secret_resolver)
except ImportError:
    print("gcs_secret_resolver not found, using default")
    pass  # GCS connector not installed, skip registration