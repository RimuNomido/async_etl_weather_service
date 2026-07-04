from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from src.models import Base
from dotenv import load_dotenv
import os

load_dotenv()

db_user = os.getenv('DB_USER')
db_host = os.getenv('DB_HOST')
db_passwd = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')
db_port = os.getenv('DB_PORT')

DATABASE_URL = f"postgresql+asyncpg://{db_user}:{db_passwd}@{db_host}:{db_port}/{db_name}"

engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)