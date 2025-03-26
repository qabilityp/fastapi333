import os
from celery import Celery
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import database


REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:example@db:5432/postgres")

celery_app = Celery(
    "celery_worker",
    broker=REDIS_URL,
    backend=REDIS_URL
)

# settings Celery
celery_app.conf.update(
    result_backend=REDIS_URL,
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    timezone='UTC',
    enable_utc=True,
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@celery_app.task
def add(x, y):
    return x + y


@celery_app.task
def send_email(user_id):
    db = SessionLocal()
    try:
        user = db.query(database.SQLAlchemyUser).filter(database.SQLAlchemyUser.id == user_id).first()
        if user:
            msg = f"Sending email to the user {user.username}"
            print(msg)
        else:
            print(f"User with ID {user_id} not found")
    finally:
        db.close()
