from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL")  # Берём URL из переменной среды

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Функция для получения сессии
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


from fastapi import FastAPI
import asyncpg


app = FastAPI()

# URL подключения к Supabase (замени на свою)
DATABASE_URL = os.getenv("DATABASE_URL")

@app.get("/test_db")
async def test_db_connection():
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        result = await conn.fetch("SELECT 1 AS test;")
        await conn.close()
        return {"status": "success", "result": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}
