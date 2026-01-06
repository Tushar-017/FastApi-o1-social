from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()

DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')

# to work with raw sequal
# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastApi', user='postgres', password=os.getenv('DB_PASSWORD'), cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print('Databses connection was succesfull!')
#         break
#     except Exception as error:
#         print('Connection to databse failed')
#         print('Error: ', error)
#         time.sleep(2)

if DB_USERNAME and DB_PASSWORD and DB_HOST:
    # URL encode the password to handle special characters like @
    encoded_password = quote_plus(DB_PASSWORD)
    SQLALCHEMY_DATABASE_URL = f'postgresql://{DB_USERNAME}:{encoded_password}@{DB_HOST}/{DB_NAME}'
else:
    # Fallback to SQLite if PostgreSQL credentials not configured
    print('DB_URL fail')
    SQLALCHEMY_DATABASE_URL = 'sqlite:///./test.db'

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in SQLALCHEMY_DATABASE_URL else {})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base= declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
