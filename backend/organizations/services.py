from django.db import transaction

from .dto import OrganizationBalanceDTO, OrganizationDTO, PaymentDTO
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
        """
            Check if this payment has already been made;
            check if this payment has an existing inn;
            change org balance and create a log instance.
        """
        
        status = 'failed'

        try:
            with transaction.atomic():
                if self.payment_repository.get_payment_by_id(payment_dto.operation_id):
                    raise PaymentAlreadyProcessed(obj_id=payment_dto.operation_id)
                
                org_dto = self.org_repository.select_for_update_by_inn(
                    payment_dto.payer_inn
                )
                if not org_dto:
                    raise OrganizationNotFound(obj_id=payment_dto.payer_inn)

                self.change_balance(org_dto, payment_dto)
                payment_dto = self.payment_repository.create(payment_dto)
                self.org_repository.update(org_dto)
        
        except (PaymentAlreadyProcessed, OrganizationNotFound):
            raise
        except Exception as e:
            raise RuntimeError(f"Payment processing failed: {e}")
        else:
            status = 'success'
        
        self.log_payment(payment_dto, status)

        return payment_dto
    
    def change_balance(self, org_dto: OrganizationDTO, payment_dto: PaymentDTO) -> None:
        """
            Handle org balance changes
        """
        
        org_dto.balance += payment_dto.amount
    
    def log_payment(self, payment_dto: PaymentDTO, status: str) -> None:
        """
            Create a log instance
        """
        
        payment_transaction_dto = PaymentTransactionMapper.from_payment_dto(
                                                               payment_dto, status
                                                           )

        self.payment_transaction_repository.create(payment_transaction_dto)


class OrganizationService:
    def __init__(self):
        self.org_repository = OrganizationRepository()

    def get_org_balance(self, inn: str) -> OrganizationBalanceDTO:
        org_dto = self.org_repository.get()
        pass
