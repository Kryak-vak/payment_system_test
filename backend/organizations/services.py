from django.db import transaction

from .dto import OrganizationBalanceDTO, OrganizationDTO, PaymentDTO
from .enums import PaymentStatus
from .exceptions import OrganizationNotFound, PaymentAlreadyProcessed
from .mappers import PaymentTransactionMapper
from .repositories import (
    OrganizationRepository,
    PaymentRepository,
    PaymentTransactionRepository,
)


class PaymentService:
    def __init__(self):
        self.payment_repository = PaymentRepository()
        self.org_repository = OrganizationRepository()
        self.payment_transaction_repository = PaymentTransactionRepository()
    
    def process_payment(self, payment_dto: PaymentDTO) -> PaymentDTO:
        status = PaymentStatus.FAILED
        payment_db_dto = payment_dto

        try:
            if self.payment_repository.get_payment_by_id(payment_dto.operation_id):
                raise PaymentAlreadyProcessed(obj_id=payment_dto.operation_id)

            with transaction.atomic():
                org_dto = self.org_repository.select_for_update_by_inn(
                    payment_dto.payer_inn
                )
                if not org_dto:
                    raise OrganizationNotFound(obj_id=payment_dto.payer_inn)

                self.change_balance(org_dto, payment_dto)
                payment_db_dto = self.payment_repository.create(payment_dto)
                self.org_repository.update(org_dto)

            status = PaymentStatus.SUCCESS

            return payment_db_dto
        
        finally:
            self.log_payment(payment_db_dto, status)
    
    def change_balance(self, org_dto: OrganizationDTO, payment_dto: PaymentDTO) -> None:
        org_dto.balance += payment_dto.amount
    
    def log_payment(self, payment_dto: PaymentDTO, status: str) -> None:
        payment_transaction_dto = PaymentTransactionMapper.from_payment_dto(
                                                               payment_dto, status
                                                           )

        self.payment_transaction_repository.create(payment_transaction_dto)


class OrganizationService:
    def __init__(self):
        self.org_repository = OrganizationRepository()

    def get_org_balance(self, inn: str) -> OrganizationBalanceDTO:
        org_dto = self.org_repository.get(inn=inn)
        if not org_dto:
            raise OrganizationNotFound(obj_id=inn)
        
        org_balance_dto = OrganizationBalanceDTO(
            **org_dto.model_dump(include=OrganizationBalanceDTO.model_fields.keys())
        )

        return org_balance_dto
