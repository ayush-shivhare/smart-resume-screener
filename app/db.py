from sqlalchemy import create_engine, Column, Integer, String, Text, Float
from sqlalchemy.orm import declarative_base, sessionmaker
from .config import DB_URL

engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

class Candidate(Base):
    __tablename__ = "candidates"
    id = Column(Integer, primary_key=True)
    name = Column(String(256))
    email = Column(String(256))
    raw_text = Column(Text)
    skills = Column(Text)      # comma-joined
    education = Column(Text)   # JSON-ish string
    experience = Column(Text)  # JSON-ish string
    last_score = Column(Float, default=0.0)
    last_justification = Column(Text, default="")

def init_db():
    Base.metadata.create_all(bind=engine)
