from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database URL from environment variable
# Default to SQLite for development, but can be overridden for MySQL
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./rideshare.db")

# For MySQL, use this format:
# DATABASE_URL = "mysql+pymysql://username:password@localhost:3306/database_name"

print(f"🔗 Connecting to database: {DATABASE_URL.split('@')[0] if '@' in DATABASE_URL else DATABASE_URL}")

# Engine configuration
if "sqlite" in DATABASE_URL:
    # SQLite specific configuration
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
else:
    # MySQL specific configuration  
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        pool_recycle=300,
        echo=False  # Set to True for SQL query logging
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
