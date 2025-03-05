from pydantic import BaseModel, condecimal
from datetime import datetime

class CashResponse(BaseModel):
    amount: float
    updated_at: datetime

class TransactionCreate(BaseModel):
    type: str
    amount: float

class TransactionCashCreate(BaseModel):
    type: str  # 'income' или 'expense'
    amount: condecimal(max_digits=10, decimal_places=2)  # Число с двумя знаками после запятой
    date: datetime  # Дата и время транзакции
    comment: str  # Комментарий к операции (поддержка кириллицы)

