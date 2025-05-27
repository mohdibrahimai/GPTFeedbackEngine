import os
import sqlalchemy as sa
from sqlalchemy import create_engine, Column, Integer, String, Text, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from typing import List, Dict, Optional

# Database setup
def get_database_url():
    """Get database URL from environment variables."""
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        # Try alternative environment variables
        host = os.getenv("PGHOST", "localhost")
        port = os.getenv("PGPORT", "5432")
        user = os.getenv("PGUSER", "postgres")
        password = os.getenv("PGPASSWORD", "")
        database = os.getenv("PGDATABASE", "postgres")
        
        if host and port and user and database:
            database_url = f"postgresql://{user}:{password}@{host}:{port}/{database}"
    
    return database_url

DATABASE_URL = get_database_url()
if not DATABASE_URL:
    raise ValueError("No database connection information available")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database Models
class Prompt(Base):
    __tablename__ = "prompts"
    
    id = Column(Integer, primary_key=True, index=True)
    prompt_text = Column(Text, nullable=False)
    response_text = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Evaluation(Base):
    __tablename__ = "evaluations"
    
    id = Column(Integer, primary_key=True, index=True)
    prompt_text = Column(Text, nullable=False)
    response_text = Column(Text, nullable=False)
    helpfulness_score = Column(Integer, nullable=False)
    truthfulness_score = Column(Integer, nullable=False)
    harmlessness_score = Column(Integer, nullable=False)
    comments = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

# Database functions
def init_database():
    """Initialize the database and create tables."""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def load_prompts_from_db() -> List[Dict]:
    """Load all prompts from the database."""
    db = SessionLocal()
    try:
        prompts = db.query(Prompt).all()
        return [
            {
                "id": prompt.id,
                "prompt": prompt.prompt_text,
                "response": prompt.response_text or ""
            }
            for prompt in prompts
        ]
    finally:
        db.close()

def load_evaluations_from_db() -> List[Dict]:
    """Load all evaluations from the database."""
    db = SessionLocal()
    try:
        evaluations = db.query(Evaluation).all()
        return [
            {
                "id": eval.id,
                "prompt": eval.prompt_text,
                "response": eval.response_text,
                "helpfulness_score": eval.helpfulness_score,
                "truthfulness_score": eval.truthfulness_score,
                "harmlessness_score": eval.harmlessness_score,
                "comments": eval.comments,
                "timestamp": eval.created_at.isoformat()
            }
            for eval in evaluations
        ]
    finally:
        db.close()

def save_evaluation_to_db(evaluation_data: Dict) -> bool:
    """Save an evaluation to the database."""
    db = SessionLocal()
    try:
        evaluation = Evaluation(
            prompt_text=evaluation_data["prompt"],
            response_text=evaluation_data["response"],
            helpfulness_score=evaluation_data["helpfulness_score"],
            truthfulness_score=evaluation_data["truthfulness_score"],
            harmlessness_score=evaluation_data["harmlessness_score"],
            comments=evaluation_data.get("comments", ""),
            created_at=datetime.fromisoformat(evaluation_data["timestamp"].replace('Z', '+00:00'))
        )
        db.add(evaluation)
        db.commit()
        return True
    except Exception as e:
        print(f"Error saving evaluation to database: {e}")
        db.rollback()
        return False
    finally:
        db.close()

def migrate_json_to_db():
    """Migrate existing JSON data to the database."""
    from utils import load_prompts, load_evaluations
    
    db = SessionLocal()
    try:
        # Check if data already exists
        existing_prompts = db.query(Prompt).count()
        if existing_prompts > 0:
            print("Database already contains data, skipping migration.")
            return
        
        # Migrate prompts
        json_prompts = load_prompts()
        for prompt_data in json_prompts:
            prompt = Prompt(
                prompt_text=prompt_data["prompt"],
                response_text=prompt_data.get("response", "")
            )
            db.add(prompt)
        
        # Migrate evaluations
        json_evaluations = load_evaluations()
        for eval_data in json_evaluations:
            evaluation = Evaluation(
                prompt_text=eval_data["prompt"],
                response_text=eval_data["response"],
                helpfulness_score=eval_data["helpfulness_score"],
                truthfulness_score=eval_data["truthfulness_score"],
                harmlessness_score=eval_data["harmlessness_score"],
                comments=eval_data.get("comments", ""),
                created_at=datetime.fromisoformat(eval_data["timestamp"].replace('Z', '+00:00'))
            )
            db.add(evaluation)
        
        db.commit()
        print(f"Successfully migrated {len(json_prompts)} prompts and {len(json_evaluations)} evaluations to database.")
        
    except Exception as e:
        print(f"Error during migration: {e}")
        db.rollback()
    finally:
        db.close()

def add_sample_prompt(prompt_text: str, response_text: str = "") -> bool:
    """Add a new prompt to the database."""
    db = SessionLocal()
    try:
        prompt = Prompt(
            prompt_text=prompt_text,
            response_text=response_text
        )
        db.add(prompt)
        db.commit()
        return True
    except Exception as e:
        print(f"Error adding prompt: {e}")
        db.rollback()
        return False
    finally:
        db.close()

def update_prompt_response(prompt_text: str, response_text: str) -> bool:
    """Update the response for a specific prompt."""
    db = SessionLocal()
    try:
        prompt = db.query(Prompt).filter(Prompt.prompt_text == prompt_text).first()
        if prompt:
            prompt.response_text = response_text
            db.commit()
            return True
        return False
    except Exception as e:
        print(f"Error updating prompt response: {e}")
        db.rollback()
        return False
    finally:
        db.close()

def get_evaluation_stats() -> Dict:
    """Get evaluation statistics from the database."""
    db = SessionLocal()
    try:
        evaluations = db.query(Evaluation).all()
        if not evaluations:
            return {}
        
        total_count = len(evaluations)
        avg_helpfulness = sum(e.helpfulness_score for e in evaluations) / total_count
        avg_truthfulness = sum(e.truthfulness_score for e in evaluations) / total_count
        avg_harmlessness = sum(e.harmlessness_score for e in evaluations) / total_count
        
        return {
            "total_evaluations": total_count,
            "avg_helpfulness": avg_helpfulness,
            "avg_truthfulness": avg_truthfulness,
            "avg_harmlessness": avg_harmlessness
        }
    finally:
        db.close()