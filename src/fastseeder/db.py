from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
load_dotenv()
import os

_fastseeder_database_uri = None
_database_uri_resolvers = []

def set_database_uri(uri: str):
    global _fastseeder_database_uri
    _fastseeder_database_uri = uri

def register_uri_resolver(resolver_fn):
    """Registers a custom database URI resolver."""
    if resolver_fn not in _database_uri_resolvers:
        _database_uri_resolvers.append(resolver_fn)

def get_database(database_uri: str = None):
    """
    Returns SQLAlchemy engine, sessionmaker, and metadata.

    Priority:
    1. Explicit database_uri
    2. set_database_uri()
    3. registered resolvers (like GCS)
    4. DATABASE_URL from env
    """
    log_queries = os.getenv("LOG_QUERIES", "False").lower() in ("true", "1", "yes")

    uri = database_uri or _fastseeder_database_uri

    if not uri:
        for resolver in _database_uri_resolvers:
            try:
                uri = resolver()
                if uri:
                    break
            except Exception as e:
                print("Failed to resolver",e)
                continue  # silently ignore failed resolvers

    if not uri:
        uri = os.getenv("DATABASE_URL")

    if not uri:
        raise ValueError("No database URI found. Set DATABASE_URL, pass an explicit URI, or use a connector.")

    engine = create_engine(uri, echo=log_queries)
    sql_sessionmaker = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    metadata = MetaData()
    return engine, sql_sessionmaker, metadata