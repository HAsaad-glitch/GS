from dotenv import load_dotenv
import os
load_dotenv()


class TrinoConfig:
    HOST = os.environ.get("TRINO_HOST")
    PORT = os.environ.get("TRINO_PORT")
    USERNAME = os.environ.get("TRINO_USERNAME")
    PASSWORD = os.environ.get("TRINO_PASSWORD")
    TRINO_DB_PATH = os.environ.get("TRINO_DB_PATH")
    TRINO_CONTAINER_NAME = os.environ.get("TRINO_CONTAINER_NAME")


class GenerateCatalog:
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
    CHROMA_HOST = os.environ.get("CHROMA_HOST")
    CHROMA_PORT = os.environ.get("CHROMA_PORT")
    CHROMA_COLLECTION = os.environ.get("CHROMA_COLLECTION")


class Configs:
    # "TRINO" or "DREMIO"
    DATALAKE_ENGINE = os.environ.get("DATALAKE_ENGINE")
    DATALAKE_ENGINE_DREMIO = os.environ.get("DATALAKE_ENGINE_DREMIO")
    DATALAKE_ENGINE_TRINO = os.environ.get("DATALAKE_ENGINE_TRINO")
    TEMPORAL_URL = os.environ.get("TEMPORAL_URL")
    FLASK_ADMIN_USERNAME = os.environ.get("FLASK_ADMIN_USERNAME")
    FLASK_ADMIN_PASSWORD = os.environ.get("FLASK_ADMIN_PASSWORD")
    TEMPORAL_ACTIVITIES_MAXIMUM_RETRY_ATTEMPTS = int(os.environ.get("TEMPORAL_ACTIVITIES_MAXIMUM_RETRY_ATTEMPTS"))
    DATALAKE_CATALOG = os.environ.get("DATALAKE_CATALOG")


class Redis:
    HOST = os.environ.get("REDIS_HOST")
    PORT = int(os.environ.get("REDIS_PORT"))
    PASSWORD = os.environ.get("REDIS_PASSWORD")
    QUERY_RESULT_DB = int(os.environ.get("REDIS_DB_QUERY_RESULT"))
    LLM_DB = 2
    RESPONSE_EXPIRY_SECONDS = 1200
    OPPORTUNITIES = 3


class LLM:
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
    MODEL = os.environ.get("MODEL1")


class DuckDB:
    HOST = os.environ.get("DUCK_DB_HOST")
    PORT = os.environ.get("DUCK_DB_PORT")
    S3_BUCKET_NAME = os.environ.get("S3_BUCKET_NAME")
    QUERY_LIMIT = 100
    PROFILE_QUERY_LIMIT = 1000



