from pydantic import BaseModel
from typing import List, Optional

class Transaction(BaseModel):
    transaction_date: str
    processing_date: str
    description: str
    town: str
    foreign_amount: Optional[float] = None
    foreign_currency: Optional[str] = None
    exchange_rate: Optional[float] = None
    amount_eur: float
    total_amount: float

class CardStatement(BaseModel):
    account: str
    account_holder: str
    account_type: str
    statement_date: str
    card_number: str
    card_holder: str
    expiry_date: str
    utilization_limit: float
    transactions: List[Transaction]
    total_amount: float
    debit_date: str

class Response(BaseModel):
    card_statement: CardStatement

CardStatement.model_rebuild()  # This is required to enable recursive types
