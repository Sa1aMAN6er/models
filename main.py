from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Cash

app = FastAPI()

@app.get("/")
def root():
    return {"message": "API работает!"}

# Новый эндпоинт для проверки соединения с базой данных
@app.get("/test_db_connection")
def test_db_connection(db: Session = Depends(get_db)):
    try:
        # Проверяем, есть ли записи в таблице cash
        cash_record = db.query(Cash).first()
        if cash_record:
            return {"status": "success", "message": "Соединение установлено!", "cash_balance": cash_record.amount}
        else:
            return {"status": "success", "message": "Соединение установлено, но записей в таблице cash нет!"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
