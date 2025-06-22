from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class OrganizationBalanceDTO(BaseModel):
    balance: float
    inn: str


class OrganizationDTO(OrganizationBalanceDTO):
    name: str


class PaymentBaseDTO(BaseModel):
    operation_id: UUID
    amount: float
    payer_inn: str
    create_date: datetime = Field(default_factory=datetime.today)


class PaymentDTO(PaymentBaseDTO):
    document_number: str
    document_date: datetime
    update_date: datetime = Field(default_factory=datetime.today)


class PaymentTransactionDTO(PaymentBaseDTO):
    status: str