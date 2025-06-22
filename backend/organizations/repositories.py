from abc import ABC
from typing import Generic, Optional, Type, TypeVar
from uuid import UUID

from .dto import OrganizationDTO, PaymentDTO, PaymentTransactionDTO
from .mappers import (
    BaseMapper,
    OrganizationMapper,
    PaymentMapper,
    PaymentTransactionMapper,
)
from .models import Organization, Payment, PaymentTransaction
from .types import DTOType, ModelType

MapperType = TypeVar('MapperType', bound=BaseMapper)


class BaseRepository(ABC, Generic[ModelType, MapperType, DTOType]):
    model: Type[ModelType]
    mapper: Type[MapperType]

    def create(self, dto: DTOType) -> DTOType:
        obj = self.model(**dto.model_dump())
        obj.save()
        return self._dto(obj)

    def _dto(self, obj: ModelType) -> DTOType:
        return self.mapper.to_dto(obj)


class PaymentRepository(BaseRepository[Payment, PaymentMapper, PaymentDTO]):
    model = Payment
    mapper = PaymentMapper

    def get_payment_by_id(self, operation_id: UUID) -> Optional[PaymentDTO]:
        payment = self.model.objects.filter(pk=operation_id).first()
        
        return self.mapper.to_dto(payment) if payment else None


class OrganizationRepository(
        BaseRepository[Organization, OrganizationMapper, OrganizationDTO]
    ):
    model = Organization
    mapper = OrganizationMapper

    def select_for_update_by_inn(self, payer_inn: str) -> Optional[OrganizationDTO]:
        org = self.model.objects.select_for_update().filter(
            inn=payer_inn
        ).first()
        
        return self._dto(org) if org else None

    def update(self, dto: OrganizationDTO) -> OrganizationDTO:
        org = self.model.objects.get(inn=dto.inn)
        for field, value in dto.model_dump().items():
            setattr(org, field, value)
        org.save()
        return self._dto(org)


class PaymentTransactionRepository(
        BaseRepository[
            PaymentTransaction, PaymentTransactionMapper, PaymentTransactionDTO
        ]
    ):
    model = PaymentTransaction
    mapper = PaymentTransactionMapper

