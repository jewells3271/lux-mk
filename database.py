from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Hostinger MySQL Connection
# Format: mysql+pymysql://username:password@host/dbname
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://u649168233_lux:Revolution2026/@sql.freedb.tech/u649168233_revolution"
# Note: Host usually needs to be specific. Assuming 'sql.freedb.tech' or similar if external, 
# but for Hostinger usually 'localhost' if running ON Hostinger, or a specific IP if remote.
# Since the user gave 'u649168233_', this looks like Hostinger Shared Hosting.
# Remote MySQL usually requires the IP. For now, I'll try the common endpoint or ask.
# Actually, for Revolution/VPS, we might need to be careful. 
# Let's stick to the URL provided in the screenshot context if available, otherwise guess generic.
# User didn't provide HOST IP. I will use a placeholder and warn/notify or try to infer.
# Wait, user said "db that is with the website".
# If the python script is LOCAL, it needs "Remote MySQL" enabled and the IP.
# If I don't have the IP, I can't connect.
# I will use a generic Hostinger IP structure or better yet, make it capable of falling back.
# Let's try to deduce or ask. But better: Just put the credentials in and assume standard 'mysql.hostinger.com' or similar?
# No, Hostinger DB hosts are usually 'mysql.hostinger.com' or 'localhost' (internal).
# I'll use a likely hostname but might need to correct it.
# Actually, the user just gave DB name, User, Pass. NO HOST.
# I will use a variable and ask or set a default.
# Lacking the host, I'll return to SQLite for *now* to avoid breakage, 
# BUT I will write the code to support it easily.
# Actually, I'll write the code with the creds but comment it out until I get the Host URI.
# RETHINK: User provided specific constraints.
# Let's set it up but use a placeholder for HOST.

import os
from dotenv import load_dotenv

load_dotenv()

# Default to SQLite for local development
# Use absolute path for SQLite to avoid confusion with --app-dir
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(os.path.dirname(BASE_DIR), "data")
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

DEFAULT_DB_URL = f"sqlite:///{os.path.join(DATA_DIR, 'lux_memory.db')}"
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", DEFAULT_DB_URL).strip()

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
