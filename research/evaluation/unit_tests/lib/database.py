from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from contextlib import contextmanager
from datetime import datetime
import os

Base = declarative_base()

class Assistant(Base):
    __tablename__ = 'assistants'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class TestCase(Base):
    __tablename__ = 'test_cases'
    id = Column(Integer, primary_key=True)
    assistant_id = Column(Integer, ForeignKey('assistants.id'))
    system_prompt = Column(String)
    temperature = Column(Float)
    max_tokens = Column(Integer)
    model = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class TestResult(Base):
    __tablename__ = 'test_results'
    id = Column(Integer, primary_key=True)
    test_case_id = Column(Integer, ForeignKey('test_cases.id'))
    test_name = Column(String)
    result = Column(String)
    error_message = Column(String, nullable=True)
    test_number = Column(Integer)
    user_prompt = Column(String)
    answer = Column(String)
    expected_answer = Column(String)
    prompt_tokens = Column(Integer)
    completion_tokens = Column(Integer)
    model_name = Column(String)
    filtered_hate = Column(Boolean)
    filtered_protected_material_code = Column(Boolean)
    filtered_protected_material_text = Column(Boolean)
    filtered_self_harm = Column(Boolean)
    filtered_sexual = Column(Boolean)
    filtered_violence = Column(Boolean)
    comparison_score = Column(Float)
    comparison_best_answer = Column(String)
    comaprison_reason = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

@contextmanager
def db_session():
    """Provide a transactional scope around a series of operations."""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

def setup_database():
    """Create database tables if they don't exist."""
    Base.metadata.create_all(bind=engine)

def assistant_upsert(assistant_name: str):
    """Initialize or update assistant data at the start of the test session."""

    assistant_data = {
        "name": assistant_name,
    }

    with db_session() as session:
        assistant = session.query(Assistant).filter_by(name=assistant_data["name"]).first()
        if not assistant:
            assistant = Assistant(**assistant_data)
            session.add(assistant)
        else:
            for key, value in assistant_data.items():
                setattr(assistant, key, value)
        session.commit()

    return assistant


# Init db engine
dbname = os.getenv("DATABASE_NAME")
dbserver = os.getenv("DATABASE_SERVER")
dbuser = os.getenv("DATABASE_USERNAME")
dbpassword = os.getenv("DATABASE_PASSWORD")
dbport = 5432

DATABASE_URL = f"postgresql://{dbuser}:{dbpassword}@{dbserver}:{dbport}/{dbname}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)