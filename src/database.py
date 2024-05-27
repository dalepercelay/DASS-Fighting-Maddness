import os
import dotenv
from sqlalchemy import create_engine

def database_connection_url():
    dotenv.load_dotenv()

    return os.environ.get("POSTGRES_URI")

#engine = create_engine(database_connection_url(), pool_pre_ping=True)
engine = create_engine("postgresql+psycopg2://postgres.lgggotiimtosbxfjhsby:dasspokemon123456789!@aws-0-us-west-1.pooler.supabase.com:5432/postgres", pool_pre_ping=True)