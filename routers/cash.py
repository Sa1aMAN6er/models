from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Cash, TransactionCash
from schemas import TransactionCashCreate
from decimal import Decimal

router = APIRouter(prefix="/cash", tags=["cash"])

@router.post("/add")
def add_cash(transaction: TransactionCashCreate, db: Session = Depends(get_db)):
    # Проверяем, есть ли запись о текущем балансе наличных
    cash = db.query(Cash).first()
    if not cash:
        cash = Cash(amount=Decimal("0.00"))
        db.add(cash)
        db.commit()
        db.refresh(cash)

    # Создаём новую транзакцию
    new_transaction = TransactionCash(
        type=transaction.type,
        amount=transaction.amount,
        date=transaction.date,
        comment=transaction.comment
    )
    db.add(new_transaction)

    # Обновляем баланс в таблице cash
    if transaction.type == "income":
        cash.amount += transaction.amount
    elif transaction.type == "expense":
        cash.amount -= transaction.amount

    db.commit()
    db.refresh(cash)

    return {"message": "Transaction added successfully", "balance": cash.amount}
