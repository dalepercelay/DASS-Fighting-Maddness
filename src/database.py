import os
import dotenv
from sqlalchemy import create_engine

def database_connection_url():
    dotenv.load_dotenv()

    return os.environ.get("POSTGRES_URI")

engine = create_engine(database_connection_url(), pool_pre_ping=True)
#engine = create_engine("postgresql://postgres:postgres@127.0.0.1:54322/postgres", pool_pre_ping=True)