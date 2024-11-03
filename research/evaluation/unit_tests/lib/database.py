from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from contextlib import contextmanager
from datetime import datetime
import os
from dotenv import load_dotenv
import logging

logger = logging.getLogger("database")
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
    comparison_reason = Column(String)
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
        session.refresh(assistant)

    return assistant

def testcase_insert(assistant_name: str, system_prompt: str, temperature: float, max_tokens: int, model: str):

    test_case_data = {
        "system_prompt": system_prompt,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "model": model
    }

    test_case_id = None
    with db_session() as session:

        assistant = session.query(Assistant).filter_by(name=assistant_name).first()
        if assistant is None:
            raise ValueError(f"Assistant '{assistant_name}' does not exist.")

        test_case_data[ "assistant_id" ] = assistant.id,
        test_case = TestCase(**test_case_data)
        session.add(test_case)
        session.commit()
        session.refresh(test_case)
        test_case_id = test_case.id

    return test_case_id

def test_result_insert(test_case_id: int, llm_test_results: list):

    with db_session() as session:

        test_case = session.get(TestCase, test_case_id)
        session.refresh(test_case)
        if test_case is None:
            raise ValueError(f"Test case  '{test_case_id}' does not exist.")

        for result_item in llm_test_results:

            test_result_data = {
                "test_case_id": test_case_id,
                "test_name": result_item[ "name" ],
                "result": "",
                "error_message": "",
                "test_number": result_item[ "testNumber" ],
                "user_prompt": result_item[ "user_prompt" ],
                "answer": result_item[ "answer" ],
                "expected_answer": result_item[ "expected_answer" ],
                "prompt_tokens": result_item[ "prompt_tokens" ],
                "completion_tokens": result_item[ "completion_tokens" ],
                "model_name": result_item[ "model_name" ],
                "filtered_hate": result_item[ "filtered_hate" ],
                "filtered_protected_material_code": result_item[ "filtered_protected_material_code" ],
                "filtered_protected_material_text": result_item[ "filtered_protected_material_text" ],
                "filtered_self_harm": result_item[ "filtered_self_harm" ],
                "filtered_sexual": result_item[ "filtered_sexual" ],
                "filtered_violence": result_item[ "filtered_violence" ],
                "comparison_score": result_item[ "comparison_score" ],
                "comparison_best_answer": result_item[ "best_answer" ],
                "comparison_reason": result_item[ "comparison_reason" ]
            }

            test_result = TestResult(**test_result_data)
            session.add(test_result)

        session.commit()


# Init db engine
load_dotenv()

dbname = os.getenv("DATABASE_NAME")
dbserver = os.getenv("DATABASE_SERVER")
dbuser = os.getenv("DATABASE_USERNAME")
dbpassword = os.getenv("DATABASE_PASSWORD")
dbport = 5432

logger.info(f"Open database {dbname} on server {dbserver} with user {dbuser}")
print(f"Open database {dbname} on server {dbserver} with user {dbuser}")

DATABASE_URL = f"postgresql://{dbuser}:{dbpassword}@{dbserver}:{dbport}/{dbname}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Exemple d'utilisation
if __name__ == "__main__":
  setup_database()
  Base.metadata.drop_all(engine)
  sql = Base.metadata.create_all(engine)
  print(sql)