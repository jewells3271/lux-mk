# Lux Database Config v1.2 - Vercel & IP Verified
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Hostinger MySQL Connection
# Standard Hostinger Hostname: 8srv1915.hstgr.io
HOSTINGER_DB = "mysql+pymysql://u649168233_lux:Revolution_100@8srv1915.hstgr.io/u649168233_revolution"

import os
from dotenv import load_dotenv

load_dotenv()

# Absolute path for SQLite to avoid confusion with --app-dir
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IS_VERCEL = "VERCEL" in os.environ

# On Vercel, use /tmp for SQLite, otherwise use local data folder
if IS_VERCEL:
    DATA_DIR = "/tmp"
else:
    DATA_DIR = os.path.join(os.path.dirname(BASE_DIR), "data")

# Only try to create DATA_DIR if we are NOT on Vercel or if it doesn't and shouldn't exist
if not IS_VERCEL and not os.path.exists(DATA_DIR):
    try:
        os.makedirs(DATA_DIR)
    except Exception as e:
        print(f"Warning: Could not create DATA_DIR {DATA_DIR}: {e}")

DEFAULT_DB_URL = f"sqlite:///{os.path.join(DATA_DIR, 'lux_memory.db')}"

# Priority: Environment Var -> Hostinger Core -> Local SQLite
env_url = os.getenv("DATABASE_URL")
if env_url and env_url.strip():
    SQLALCHEMY_DATABASE_URL = env_url.strip()
else:
    # Use Hostinger by default
    SQLALCHEMY_DATABASE_URL = HOSTINGER_DB

# Stability check
if not SQLALCHEMY_DATABASE_URL or len(SQLALCHEMY_DATABASE_URL) < 5:
    SQLALCHEMY_DATABASE_URL = DEFAULT_DB_URL

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    # Only use check_same_thread for SQLite
    connect_args={"check_same_thread": False} if SQLALCHEMY_DATABASE_URL.startswith("sqlite") else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
